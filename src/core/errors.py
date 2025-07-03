# src/core/errors.py

class ApplicationError(Exception):
    """Clase base para excepciones de la aplicación."""
    pass

class NotFoundError(ApplicationError):
    """Se lanza cuando no se encuentra un recurso."""
    pass

class AlreadyExistsError(ApplicationError):
    """Se lanza cuando un recurso que se intenta crear ya existe."""
    pass

class InvalidCredentialsError(ApplicationError):
    """Se lanza por credenciales de login incorrectas."""
    pass

class ValidationError(ApplicationError):
    """Se lanza por fallos en la validación de reglas de negocio."""
    pass