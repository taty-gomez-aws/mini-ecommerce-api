import pytest


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/register", json={"email": "products@example.com", "password": "secret123"}
    )
    response = client.post(
        "/login",
        data={"username": "products@example.com", "password": "secret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_products_requires_auth(client):
    response = client.get("/products/")
    assert response.status_code == 401


def test_create_and_list_product(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "Keyboard",
            "description": "Mechanical",
            "price": 49.99,
            "in_stock": True,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Keyboard"

    response = client.get("/products/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_nonexistent_product(client, auth_headers):
    response = client.get("/products/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_product(client, auth_headers):
    create = client.post(
        "/products/", json={"name": "Mouse", "price": 19.99}, headers=auth_headers
    )
    product_id = create.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"name": "Mouse Pro", "price": 29.99},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Mouse Pro"


def test_delete_product(client, auth_headers):
    create = client.post(
        "/products/", json={"name": "Monitor", "price": 199.99}, headers=auth_headers
    )
    product_id = create.json()["id"]

    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204
    assert (
        client.get(f"/products/{product_id}", headers=auth_headers).status_code == 404
    )
