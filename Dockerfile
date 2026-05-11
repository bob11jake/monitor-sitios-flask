# 1. Usamos una imagen base de Python (ligera)
FROM python:3.9-slim

# 2. Definimos dónde vivirá el código dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de librerías
COPY requirements.txt .

# 4. Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el contenido de tu carpeta al contenedor
COPY . .

# 6. Exponemos el puerto que usa Flask
EXPOSE 5000

# 7. El comando para iniciar la app
CMD ["python", "app.py"]
