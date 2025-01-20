from app import app

def test_home():
    response=app.test_client().get("/")

    # Tests if it recieves a successful request containing html
    assert response.status_code==200
    assert b"<!doctype html>".lower() in response.data