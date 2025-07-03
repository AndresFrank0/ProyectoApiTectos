# src/shared/exceptions.py

class CustomException(Exception):
    """Clase base para excepciones personalizadas."""
    def __init__(self, detail: str):
        self.detail = detail

# --- Auth Exceptions ---
class EmailAlreadyExistsError(CustomException):
    pass

class InvalidCredentialsError(CustomException):
    pass

# --- Restaurant Exceptions ---
class InvalidRestaurantHoursError(CustomException):
    pass

class RestaurantHasTablesError(CustomException):
    pass

class TableNumberNotUniqueError(CustomException):
    pass

# --- Reservation Exceptions ---
class ReservationConflictError(CustomException):
    pass

class ClientReservationConflictError(CustomException):
    pass
    
class ReservationTimeOutOfBoundsError(CustomException):
    pass

class InvalidReservationTimeError(CustomException):
    pass

class CancellationTimeError(CustomException):
    pass

# --- Menu Exceptions ---
class DishNameNotUniqueError(CustomException):
    pass
    
class DishInUseError(CustomException):
    pass

class InvalidPreorderError(CustomException):
    pass