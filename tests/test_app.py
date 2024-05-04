from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_api_catbot_post():
    r = client.post("/catbot", json={
        "question": "What are the secrets of the World?"})

    assert r.json()['msg'] == "Good Question! Have no Idea!!"
