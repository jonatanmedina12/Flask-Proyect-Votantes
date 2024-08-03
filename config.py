import os
from dotenv import load_dotenv

# Especificar la ruta al archivo .env
dotenv_path = 'app/.env'
load_dotenv(dotenv_path)


class Config:
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DRIVER = 'ODBC+Driver+17+for+SQL+Server'
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
        f"?driver={DRIVER}&Encrypt=yes&TrustServerCertificate=yes"
    )
    HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    PORT = os.getenv('FLASK_RUN_PORT', 5000)

    SQLALCHEMY_SERVER_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}"
        f"?driver={DRIVER}&Encrypt=yes&TrustServerCertificate=yes"
    )
