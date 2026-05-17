

def test_create_reservation(client, auth_token):
    response = client.post(
        "/api/reservations/",
        json={
            "reservation_date": "2026-04-15T18:00:00",
            "guests": 2
        },
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["guests"] == 2
    assert "id" in data

def test_get_my_reservations(client, auth_token):

    client.post(
        "/api/reservations/",
        json={
            "reservation_date": "2026-04-15T18:00:00",
            "guests": 2
        },
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    response = client.get(
        "/api/reservations/my",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    # Check data is it list
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(r["guests"] == 2 for r in data)