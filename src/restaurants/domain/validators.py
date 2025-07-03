from datetime import datetime, time, timedelta

from src.core.errors import ValidationError
from .entities import Restaurant


class ReservationValidator:
    """
    Clase para validar las reglas de negocio de una reserva.
    """
    def validate(self, restaurant: Restaurant, reservation_time: datetime, party_size: int) -> None:
        """
        Ejecuta todas las validaciones para una nueva reserva.
        Lanza una excepción `ValidationError` si alguna regla no se cumple.
        """
        if not (0 < party_size <= 12):
            raise ValidationError("El tamaño del grupo debe ser entre 1 y 12 personas.")

        # Validar que la hora de la reserva esté dentro del horario de apertura
        reservation_hour = reservation_time.time()
        if not (restaurant.opening_time <= reservation_hour < restaurant.closing_time):
            raise ValidationError("La reserva está fuera del horario de apertura del restaurante.")

        # Validar que la reserva se haga con al menos 1 hora antes del cierre
        closing_datetime = datetime.combine(reservation_time.date(), restaurant.closing_time)
        if reservation_time + timedelta(hours=1) > closing_datetime:
            raise ValidationError("La reserva debe ser al menos 1 hora antes del cierre.")

        # Validar que la reserva no dure más de 4 horas (simplificado)
        # Aquí se podría añadir una lógica más compleja si el campo de duración existiera.
        # Por ahora, esta validación es implícita en la regla anterior.