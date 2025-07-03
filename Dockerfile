# Dockerfile
# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema si fueran necesarias
# RUN apt-get update && apt-get install -y...

# Copiar los archivos de dependencias
COPY ./requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copiar el código de la aplicación al contenedor
COPY ./src /app/src
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./entrypoint.sh /app/entrypoint.sh

# Dar permisos de ejecución al script de entrada
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["/app/entrypoint.sh"]