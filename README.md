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

   
      
