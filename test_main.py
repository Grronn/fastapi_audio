import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is in a file named main.py

@pytest.fixture
def client():
    return TestClient(app)

def test_process_text(client):
    # Define your test input data
    test_data = {"text": "Your test text here."}

    # Make a mock request to the /text endpoint
    response = client.post("/text", json=test_data)

    # Check if the response is successful (status code 200)
    assert response.status_code == 200
