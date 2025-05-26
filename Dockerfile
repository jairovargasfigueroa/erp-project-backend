# Usa una imagen base oficial de Python
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al contenedor
COPY . .

# Expone el puerto 8000 (Django por defecto)
EXPOSE 8000

# Comando por defecto al arrancar
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "erp_project.wsgi:application"]
