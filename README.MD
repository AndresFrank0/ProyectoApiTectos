# El Buen Sabor - Sistema de Gestión de Reservas

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.18-48A09A?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-25.0-2496ED?style=for-the-badge&logo=docker)

Bienvenido a **El Buen Sabor**, una API RESTful para la gestión de reservas de restaurantes, construida con FastAPI y siguiendo los principios de la **Arquitectura Hexagonal**.

##  архитектура  архитектура Arquitectura

Este proyecto implementa la Arquitectura Hexagonal (también conocida como Puertos y Adaptadores) para separar claramente la lógica de negocio de las preocupaciones de la infraestructura.

* **`src/domain`**: El núcleo de la aplicación. Contiene las entidades, las reglas de negocio y las interfaces de los repositorios (puertos). No tiene dependencias externas al framework.
* **`src/application`**: Contiene los casos de uso (servicios de aplicación) que orquestan el flujo de datos desde y hacia el dominio. Depende del dominio.
* **`src/infrastructure`**: Implementaciones concretas de las interfaces definidas en el dominio (adaptadores). Aquí se encuentra la configuración de la base de datos (SQLModel), la implementación de los repositorios y la lógica de autenticación.
* **`src/api`**: La capa de presentación (API REST). Define los endpoints, gestiona las peticiones HTTP y las respuestas. Depende de los servicios de aplicación.
* **`src/core`**: Módulos compartidos como la configuración, las dependencias de FastAPI y las excepciones personalizadas.

## ✨ Características

* **Gestión de Restaurantes**: Listar y ver detalles de restaurantes.
* **Consulta de Disponibilidad**: Encontrar mesas disponibles por fecha y tamaño de grupo.
* **Creación de Reservas**: Sistema completo para realizar reservas.
* **Autenticación y Autorización**: Basado en JWT con OAuth2PasswordBearer, roles y scopes.
* **Panel de Control (Dashboard)**: Endpoints protegidos para obtener métricas de negocio.
* **Migraciones de Base de Datos**: Integración con Alembic para gestionar el esquema de la base de datos.
* **Contenerización**: Listo para desplegar con Docker y Docker Compose.
* **Testing Robusto**: Pruebas unitarias, de integración y de arquitectura.

## 🚀 Puesta en Marcha

### Prerrequisitos

* Python 3.10+
* Docker y Docker Compose
* Poetry (opcional, para gestión de dependencias local)

### 1. Configuración del Entorno

Clona el repositorio y crea un archivo `.env` a partir del ejemplo.

```bash
git clone [https://github.com/tu-usuario/el-buen-sabor.git](https://github.com/tu-usuario/el-buen-sabor.git)
cd el-buen-sabor
cp .env.example .env
```

Edita el archivo `.env` con tus propias credenciales para la base de datos y un `SECRET_KEY` seguro. Puedes generar una clave con: `openssl rand -hex 32`.

### 2. Ejecución con Docker (Recomendado)

La forma más sencilla de levantar todo el entorno (API, base de datos y pgAdmin) es con Docker Compose.

```bash
docker-compose up -d --build
```

Esto iniciará:
* El servicio de la **API** en `http://localhost:8000`.
* Una base de datos **PostgreSQL** en el puerto `5432`.
* Un servicio de **pgAdmin** en `http://localhost:5050`.

### 3. Ejecución Local (Alternativa)

Si prefieres ejecutarlo localmente sin Docker:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones de la base de datos
alembic upgrade head

# Iniciar el servidor
uvicorn src.main:app --reload
```

## 🧪 Ejecutar Pruebas

Para asegurar la calidad y el correcto funcionamiento, puedes ejecutar la suite de pruebas.

```bash
# Dentro del contenedor de Docker
docker-compose exec api pytest

# O localmente
pytest
```

## 📚 Documentación de la API

Una vez que el servidor esté en ejecución, puedes acceder a la documentación interactiva de la API generada por FastAPI:

* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)