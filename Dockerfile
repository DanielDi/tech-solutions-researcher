# Usamos una imagen base ligera de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo en /app dentro del contenedor
WORKDIR /app

# Copiamos los archivos necesarios para crear el venv: requirements.txt y setup_venv.py
COPY requirements.txt setup_venv.py ./

# Ejecutamos el script setup_venv.py para crear el entorno virtual e instalar las dependencias
RUN python setup_venv.py

# Actualizamos pip en el entorno virtual
RUN /app/venv/bin/pip install --upgrade pip

# Copiamos el resto del código (incluyendo app.py)
# NOTA: No copiamos el archivo .env, ya que inyectaremos las variables de entorno desde Kubernetes.
COPY . .

# Exponemos el puerto 8000 (el que usará uvicorn)
EXPOSE 8000

# Comando para iniciar la aplicación en modo desarrollo (con recarga automática)
CMD ["/app/venv/bin/python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]