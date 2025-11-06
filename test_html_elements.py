from main import app

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask CI/CD Demo" in response.data
