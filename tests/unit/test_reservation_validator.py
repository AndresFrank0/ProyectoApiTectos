import pytest
from datetime import datetime, time
from uuid import uuid4

from src.core.errors import ValidationError
from src.restaurants.domain.entities import Restaurant
from src.restaurants.domain.validators import ReservationValidator


@pytest.fixture
def restaurant_fixture() -> Restaurant:
    """Crea una instancia de restaurante para las pruebas."""
    return Restaurant(
        id=uuid4(),
        name="Test Restaurant",
        address="123 Test St",
        phone="555-1234",
        cuisine_type="testing",
        opening_time=time(17, 0),  # 5:00 PM
        closing_time=time(23, 0),  # 11:00 PM
    )


def test_reservation_within_opening_hours(restaurant_fixture):
    """Prueba que una reserva dentro del horario de apertura sea válida."""
    validator = ReservationValidator()
    valid_time = datetime(2023, 1, 1, 20, 0)  # 8:00 PM
    try:
        validator.validate(restaurant_fixture, valid_time, 4)
    except ValidationError:
        pytest.fail("La validación falló inesperadamente para una hora válida.")


def test_reservation_outside_opening_hours(restaurant_fixture):
    """Prueba que una reserva fuera del horario de apertura falle."""
    validator = ReservationValidator()
    invalid_time = datetime(2023, 1, 1, 15, 0)  # 3:00 PM
    with pytest.raises(ValidationError, match="La reserva está fuera del horario de apertura"):
        validator.validate(restaurant_fixture, invalid_time, 4)


def test_reservation_too_close_to_closing_time(restaurant_fixture):
    """Prueba que una reserva demasiado cerca de la hora de cierre falle."""
    validator = ReservationValidator()
    invalid_time = datetime(2023, 1, 1, 22, 30)  # 10:30 PM
    with pytest.raises(ValidationError, match="La reserva debe ser al menos 1 hora antes del cierre"):
        validator.validate(restaurant_fixture, invalid_time, 4)


def test_invalid_party_size(restaurant_fixture):
    """Prueba que un tamaño de grupo no válido (cero o negativo) falle."""
    validator = ReservationValidator()
    with pytest.raises(ValidationError, match="El tamaño del grupo debe ser positivo"):
        validator.validate(restaurant_fixture, datetime(2023, 1, 1, 20, 0), 0)

    with pytest.raises(ValidationError, match="El tamaño del grupo debe ser positivo"):
        validator.validate(restaurant_fixture, datetime(2023, 1, 1, 20, 0), -2)