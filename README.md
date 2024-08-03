# Sistema de Información para Registro de Votantes

## Descripción

Este proyecto es un sistema de información para registrar los datos de los votantes de los distintos municipios de Colombia. 
Utiliza Flask como framework principal  y SQL Server como base de datos. Además, 
utiliza el servicio de Georreferenciación de Google para obtener las coordenadas de las ubicaciones.
El sistema permite registrar los datos básicos del votante y asignarle un puesto de votación. Los roles en el sistema son:

Administrador: Puede ver toda la información ingresada por los usuarios líderes.
Líder: Solo puede ver la información que él mismo ha registrado. No puede acceder a la información de otros líderes.
Cada vez que se registra un votante, se registra también la información del usuario que lo registra (log).
Para crear un usuario líder, se requieren datos básicos de identificación y una foto de perfil. Al registrar un usuario (líderes y mesas de votación),
se obtienen las coordenadas mediante el servicio de Georreferenciación de Google.

## Características

-Registro y autenticación de usuarios
-Creación de puesto de votacion
-Edición de puesto de votacion
-Eliminación de puesto de votacion
-Visualización de todos votantes

## Requisitos Previos

Antes de comenzar, asegúrate de tener los siguientes requisitos instalados:

- Python 3.8+
- pip install -r .\requirements.txt

## Instalación

Sigue estos pasos para configurar el proyecto en tu máquina local:

1. Clona este repositorio:

   ```bash
   git clone https://github.com/jonatanmedina12/Python-Flask-Blogs.git
   cd Python-Flask-Blogs
2. Crear el Archivo .env
    ```bash
   SECRET_KEY=dev
   JWT_SECRET_KEY=dev
   DB_SERVER=localhost,1433
   DB_PORT=
   DB_NAME=Sistema_votacion
   DB_USER=sa
   DB_PASSWORD=123456**
   FLASK_RUN_HOST=0.0.0.0
   FLASK_RUN_PORT=5001
   GOOGLE_MAPS_API_KEY=tu_api_key_de_google
   
   3. Construir y Levantar los Contenedores Docker instalar docker para el funcionamiento completo
       ```bash
      docker-compose up --build

   4. Api's
         ```bash
         {
     "info": {
       "name": "Sistema de Información de Votantes",
       "description": "Documentación de la API para el sistema de registro de votantes.",
       "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
     },
     "item": [
       {
         "name": "Login",
         "request": {
           "method": "POST",
           "header": [
             {
               "key": "Content-Type",
               "value": "application/x-www-form-urlencoded"
             }
           ],
           "body": {
             "mode": "urlencoded",
             "urlencoded": [
               {
                 "key": "email",
                 "value": "[user@example.com]"
               },
               {
                 "key": "password",
                 "value": "[your_password]"
               }
             ]
           },
           "url": {
             "raw": "http://localhost:5001/auth/login",
             "protocol": "http",
             "host": [
               "localhost"
             ],
             "port": "5001",
             "path": [
               "auth",
               "login"
             ]
           }
         },
         "response": []
       },
       {
         "name": "Logout",
         "request": {
           "method": "GET",
           "url": {
             "raw": "http://localhost:5001/auth/logout",
             "protocol": "http",
             "host": [
               "localhost"
             ],
             "port": "5001",
             "path": [
               "auth",
               "logout"
             ]
           }
         },
         "response": []
       },
       {
         "name": "Home",
         "request": {
           "method": "GET",
           "url": {
             "raw": "http://localhost:5001/",
             "protocol": "http",
             "host": [
               "localhost"
             ],
             "port": "5001",
             "path": []
           }
         },
         "response": []
       },
       {
         "name": "Registrar Votantes",
         "request": {
           "method": "GET",
           "header": [
             {
               "key": "Authorization",
               "value": "Bearer [your_jwt_token]"
             }
           ],
           "url": {
             "raw": "http://localhost:5001/informacion/informacionVotantes",
             "protocol": "http",
             "host": [
               "localhost"
             ],
             "port": "5001",
             "path": [
               "informacion",
               "informacionVotantes"
             ]
           }
         },
         "response": []
       },
       {
         "name": "Eliminar Votante",
         "request": {
           "method": "POST",
           "header": [
             {
               "key": "Authorization",
               "value": "Bearer [your_jwt_token]"
             }
           ],
           "url": {
             "raw": "http://localhost:5001/informacion/eliminar_votante/{{id}}",
             "protocol": "http",
             "host": [
               "localhost"
             ],
             "port": "5001",
             "path": [
               "informacion",
               "eliminar_votante",
               "{{id}}"
             ]
           }
         },
         "response": []
       },
       {
         "name": "Editar Votante",
         "item": [
           {
             "name": "GET",
             "request": {
               "method": "GET",
               "header": [
                 {
                   "key": "Authorization",
                   "value": "Bearer [your_jwt_token]"
                 }
               ],
               "url": {
                 "raw": "http://localhost:5001/informacion/editar_votante/{{id}}",
                 "protocol": "http",
                 "host": [
                   "localhost"
                 ],
                 "port": "5001",
                 "path": [
                   "informacion",
                   "editar_votante",
                   "{{id}}"
                 ]
               }
             },
             "response": []
           },
           {
             "name": "POST",
             "request": {
               "method": "POST",
               "header": [
                 {
                   "key": "Authorization",
                   "value": "Bearer [your_jwt_token]"
                 },
                 {
                   "key": "Content-Type",
                   "value": "application/x-www-form-urlencoded"
                 }
               ],
               "body": {
                 "mode": "urlencoded",
                 "urlencoded": [
                   {
                     "key": "nombres",
                     "value": "[updated_name]"
                   },
                   {
                     "key": "apellidos",
                     "value": "[updated_surname]"
                   },
                   {
                     "key": "direccion",
                     "value": "[updated_address]"
                   },
                   {
                     "key": "telefono",
                     "value": "[updated_phone]"
                   },
                   {
                     "key": "cedula",
                     "value": "[updated_id]"
                   },
                   {
                     "key": "mesa",
                     "value": "[updated_table]"
                   }
                 ]
               },
               "url": {
                 "raw": "http://localhost:5001/informacion/editar_votante/{{id}}",
                 "protocol": "http",
                 "host": [
                   "localhost"
                 ],
                 "port": "5001",
                 "path": [
                   "informacion",
                   "editar_votante",
                   "{{id}}"
                 ]
               }
             },
             "response": []
           }
         ]
       }
     ]
   }
      
