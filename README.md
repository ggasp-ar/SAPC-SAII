# SAPC (Sistemas Administrativos Programa Contable)
Programa creado para *aprobar* SISTEMAS ADMINISTRATIVOS II \
Diseñado para administrar asientos contables

# Archivo .env
Necesita tener los siguientes parametros \
SECRET_KEY  \
MYSQL_USER  \
MYSQL_PASSWORD \
MYSQL_HOST \
MYSQL_DB 
# Preparando para ejecutar el server
Primero hay que inicializar la Base de Datos utilizando los archivos hallados en *app\db* \
1 - schema (Modelo de la DB) \
2 - initialize (Carga de datos de testeo de DB)\
user = Admin password = 123

Hace falta crear el entorno virtual para correr el servidor e instalar los requisitos
```
virtualenv -p python3 env 
.\env\Scripts\activate
pip install -r requirements.txt
```

Luego, por un problema en flask hay que modificar el archivo 
> ***env\Lib\site-packages\flask_script\__init__.py***

Cambiando la linea 

> from flask._compat import text_type

Por
> from flask_script._compat import text_type

Luego estara listo para iniciarse ejecutando
```
.\env\Scripts\activate
python .\manage.py runserver
```
