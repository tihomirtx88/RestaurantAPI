from app.models.category import Category
from app.extensions import db

def test_get_menu(client):
    response = client.get("/api/menu/")
    print(response.status_code)
    print(response.json)
    assert response.status_code == 200

def test_create_menu(client, auth_token, app):
    # 1.Creating category
    with app.app_context():
        category = Category(name="Breakfast")
        db.session.add(category)
        db.session.commit()
        category_id = category.id

    # 2. Post request
    response = client.post(
        "/api/menu/",
        json={
            "name": "Burger",
            "description": "Test burger",
            "price": 10,
            "category_id": category_id
        },
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    # 3. Checks
    assert response.status_code in [200, 201]

    # 4. Check in database
    response2 = client.get("/api/menu/")
    data = response2.get_json()

    assert len(data) == 1
    assert data[0]["name"] == "Burger"