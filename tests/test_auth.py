def test_register(client):
    response = client.post("/api/auth/register", json={
        "email": "new@test.com",
        "password": "123456"
    })

    assert response.status_code == 201

def test_login(client, test_user):

    response = client.post("/api/auth/login", json={
        "email": "admin3@admin.com",
        "password": "123456"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data