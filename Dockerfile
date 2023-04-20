# Utilizamos la imagen oficial de Python
FROM python:3.11.2

# Set the working directory
WORKDIR /code

# Copiar los archivos de requerimientos a la imagen y ejecutar pip install
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copiamos el código fuente de la aplicación al contenedor
COPY . /code/

# Establecemos las variables de entorno para la base de datos
ENV DATABASE_URL postgres://au_video_ext:y.&hl5.R5E1fX!ld5g7Lm2dM@legal-ext-video.ccwsv3fmimn3.us-east-1.rds.amazonaws.com/legal-ext-video

# Exponemos el puerto 8080
EXPOSE 80

# Ejecutamos la aplicación
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:80
