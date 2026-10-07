from fastapi.testclient import TestClient
from testing_api import app

client = TestClient(app)

def test_home():
    response = client.get("/home")
    # print("-=--=--=-=-=-= response -=-=-=-=-=-",response)

    assert response.status_code ==200
    assert response.json() == {"message":"Hello Mini"}
    

def test_add():
    response = client.get("/add?a=5&b=8")

    assert response.status_code ==200
    assert response.json() == {"result":8}