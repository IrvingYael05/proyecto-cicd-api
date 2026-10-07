# Usamos una versión ligera de Python
FROM python:3.12-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos primero las dependencias para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY app.py .

# Exponemos el puerto 80 que usará EC2
EXPOSE 80

# Comando para iniciar la aplicación
CMD ["python", "app.py"]