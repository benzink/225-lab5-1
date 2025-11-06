import requests

def test_home_page():
    response = requests.get("http://localhost:5000")
    assert response.status_code == 200
    assert "Hello from Flask CI/CD!" in response.text
