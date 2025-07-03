import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from uuid import uuid4
from datetime import datetime, time

from src.restaurants.domain.entities import Restaurant, Table


@pytest.fixture
def seed_restaurant(session: Session):
    """
    Siembra un restaurante y una mesa en la base de datos de prueba.
    """
    restaurant = Restaurant(
        id=uuid4(),
        name="Integration Test Cantina",
        address="456 API Rd",
        phone="555-5678",
        cuisine_type="integration",
        opening_time=time(18, 0),
        closing_time=time(23, 59),
    )
    table = Table(id=uuid4(), restaurant_id=restaurant.id, capacity=4)
    session.add(restaurant)
    session.add(table)
    session.commit()
    return restaurant, table


def test_create_reservation_success(client: TestClient, seed_restaurant):
    """
    Prueba la creación exitosa de una reserva a través de la API.
    """
    restaurant, table = seed_restaurant
    reservation_time = datetime.now().isoformat()

    response = client.post(
        "/reservations",
        json={
            "restaurant_id": str(restaurant.id),
            "customer": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
            },
            "reservation_time": reservation_time,
            "party_size": 2,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["restaurant_id"] == str(restaurant.id)
    assert data["party_size"] == 2
    assert data["status"] == "confirmed"


def test_create_reservation_restaurant_not_found(client: TestClient):
    """
    Prueba que la creación de una reserva falla si el restaurante no existe.
    """
    non_existent_id = uuid4()
    reservation_time = datetime.now().isoformat()

    response = client.post(
        "/reservations",
        json={
            "restaurant_id": str(non_existent_id),
            "customer": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "phone": "0987654321",
            },
            "reservation_time": reservation_time,
            "party_size": 4,
        },
    )
    assert response.status_code == 404
    assert "Restaurante no encontrado" in response.json()["detail"]


def test_list_restaurants(client: TestClient, seed_restaurant):
    """
    Prueba que la API puede listar los restaurantes existentes.
    """
    restaurant, _ = seed_restaurant
    response = client.get("/restaurants")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == restaurant.name