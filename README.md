# fatsapi_working

# FastAPI + Pydantic CRUD API

A small, production-style example of a REST API built with **FastAPI**, **Pydantic v2** and **SQLAlchemy**. It implements full **CRUD** (Create, Read, Update, Delete) for a `Ticket` resource.

![FastAPI Pydantic CRUD flow](docs/fastapi-pydantic-crud.svg)

---

## How it works

| Layer | Tool | Responsibility |
|---|---|---|
| Routes | FastAPI | Receives HTTP requests, wires dependencies, generates Swagger docs |
| Validation | Pydantic | Validates request bodies, converts types, shapes responses |
| CRUD | SQLAlchemy | Reads and writes rows in the database |
| Storage | SQLite (default) | Can be swapped for PostgreSQL by changing one URL |

**Request lifecycle**

1. The client sends an HTTP request.
2. FastAPI matches the route and Pydantic validates the body. Invalid data returns `422` automatically.
3. The route calls a function in the CRUD layer, which uses a DB session.
4. The result is returned through `response_model`, so only the declared fields are sent back.

---

## Project structure

```
fastapi-crud/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app and routes
│   ├── database.py    # engine, session, Base
│   ├── models.py      # SQLAlchemy table
│   ├── schemas.py     # Pydantic models
│   └── crud.py        # database operations
├── docs/
│   └── fastapi-pydantic-crud.svg
├── requirements.txt
└── README.md
```

---

## Installation

```bash
python -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt`

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic>=2
```

## Run

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Code

### `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./tickets.db"   # PostgreSQL: postgresql+psycopg://user:pass@host/db

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `app/models.py`

```python
from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, default="")
    status = Column(String(20), default="new")
```

### `app/schemas.py` (Pydantic)

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["new", "open", "resolved", "closed"]


class TicketBase(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(default="", max_length=5000)


class TicketCreate(TicketBase):
    """Body for POST."""


class TicketUpdate(BaseModel):
    """Body for PATCH: every field is optional."""
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=5000)
    status: Status | None = None


class TicketRead(TicketBase):
    """Response model: what the API returns."""
    model_config = ConfigDict(from_attributes=True)   # read data from ORM objects

    id: int
    status: Status
```

### `app/crud.py`

```python
from sqlalchemy.orm import Session

from . import models, schemas


def create_ticket(db: Session, data: schemas.TicketCreate) -> models.Ticket:
    ticket = models.Ticket(**data.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_ticket(db: Session, ticket_id: int) -> models.Ticket | None:
    return db.get(models.Ticket, ticket_id)


def list_tickets(db: Session, skip: int = 0, limit: int = 50) -> list[models.Ticket]:
    return db.query(models.Ticket).order_by(models.Ticket.id.desc()).offset(skip).limit(limit).all()


def update_ticket(db: Session, ticket: models.Ticket, data: schemas.TicketUpdate) -> models.Ticket:
    for field, value in data.model_dump(exclude_unset=True).items():   # only fields the client sent
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket: models.Ticket) -> None:
    db.delete(ticket)
    db.commit()
```

### `app/main.py`

```python
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ticket CRUD API", version="1.0.0")


def get_or_404(db: Session, ticket_id: int) -> models.Ticket:
    ticket = crud.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket not found")
    return ticket


@app.post("/tickets", response_model=schemas.TicketRead, status_code=status.HTTP_201_CREATED)
def create(data: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db, data)


@app.get("/tickets", response_model=list[schemas.TicketRead])
def read_all(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    return crud.list_tickets(db, skip, limit)


@app.get("/tickets/{ticket_id}", response_model=schemas.TicketRead)
def read_one(ticket_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, ticket_id)


@app.patch("/tickets/{ticket_id}", response_model=schemas.TicketRead)
def update(ticket_id: int, data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    return crud.update_ticket(db, get_or_404(db, ticket_id), data)


@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(ticket_id: int, db: Session = Depends(get_db)):
    crud.delete_ticket(db, get_or_404(db, ticket_id))
```

---

## API endpoints

| Operation | Method | Endpoint | Success | Errors |
|---|---|---|---|---|
| Create | `POST` | `/tickets` | `201` | `422` invalid body |
| Read all | `GET` | `/tickets?skip=0&limit=50` | `200` | `422` bad query |
| Read one | `GET` | `/tickets/{id}` | `200` | `404` |
| Update | `PATCH` | `/tickets/{id}` | `200` | `404`, `422` |
| Delete | `DELETE` | `/tickets/{id}` | `204` | `404` |

## Try it with curl

```bash
# Create
curl -X POST http://127.0.0.1:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Wi-Fi is not working", "description": "Office floor 2"}'

# Read all / one
curl http://127.0.0.1:8000/tickets
curl http://127.0.0.1:8000/tickets/1

# Update (only the fields you send change)
curl -X PATCH http://127.0.0.1:8000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'

# Delete
curl -X DELETE http://127.0.0.1:8000/tickets/1
```

Example response:

```json
{
  "id": 1,
  "title": "Wi-Fi is not working",
  "description": "Office floor 2",
  "status": "new"
}
```

Invalid input, for example a title that is too short:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 3 characters",
      "input": "ab"
    }
  ]
}
```

---

## Key Pydantic ideas used

| Feature | Where | Why |
|---|---|---|
| `Field(min_length=..., max_length=...)` | `TicketBase` | Reject bad input before it reaches the database |
| Separate Create / Update / Read models | `schemas.py` | Different rules for input and output |
| `Literal[...]` | `Status` | Only allowed status values are accepted |
| `model_dump(exclude_unset=True)` | `crud.update_ticket` | Real PATCH: only changed fields are updated |
| `from_attributes=True` | `TicketRead` | Converts SQLAlchemy objects to JSON |
| `response_model` | routes | Hides internal fields and documents the response in Swagger |

## Next steps

- Add Alembic migrations instead of `create_all`
- Add authentication (OAuth2 / JWT) with a FastAPI dependency
- Add tests with `pytest` and `TestClient`
- Switch `DATABASE_URL` to PostgreSQL for production
