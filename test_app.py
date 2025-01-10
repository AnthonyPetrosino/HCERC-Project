from app import app

def test_home():
    response=app.test_client().get("/")

    # Successful request
    assert response.status_code==200
    assert response.data== b"Hello world"