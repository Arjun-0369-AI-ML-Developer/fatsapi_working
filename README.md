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
