\#README - Proyecto Flask Usuarios
Este es el repositorio para el proyecto Flask. A continuación, se proporcionan las instrucciones para configurar y ejecutar el proyecto correctamente.

\##Instalación
Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde el sitio web oficial de Python: https://www.python.org

Instala Flask ejecutando el siguiente comando en tu terminal:

pip install flask
Instala pydal ejecutando el siguiente comando en tu terminal:


pip install pydal
Si tu proyecto requiere la instalación de psycopg2, puedes ejecutar el siguiente comando:

pip install psycopg2

\##Configuración de la Base de Datos
Crea una base de datos llamada "usuarios" en PostgreSQL. Puedes utilizar una herramienta como pgAdmin para crearla, o ejecutar el siguiente comando en la terminal de PostgreSQL:

CREATE DATABASE usuarios;
Crea un usuario con el nombre "usuario" y la contraseña "password" en PostgreSQL. Puedes ejecutar los siguientes comandos en la terminal de PostgreSQL:

CREATE USER usuario WITH PASSWORD 'password';
Asigna los privilegios adecuados al usuario "usuario" para la base de datos "usuarios". Puedes ejecutar los siguientes comandos en la terminal de PostgreSQL:

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO usuario;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usuario;
ALTER USER usuario WITH SUPERUSER;

Estos comandos otorgan todos los privilegios necesarios para que el usuario pueda acceder y manipular la base de datos.

\##Ejecución del Proyecto
Clona este repositorio en tu máquina local o descárgalo como archivo ZIP.

Navega hasta el directorio del proyecto en tu terminal.

Ejecuta el siguiente comando para iniciar el servidor Flask:

flask run
Abre tu navegador web y visita la siguiente URL: http://localhost:5000
