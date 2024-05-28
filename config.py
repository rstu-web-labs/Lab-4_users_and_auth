from dotenv import load_dotenv
import os

load_dotenv()

DB_POSTGRES_USERNAME = os.environ.get("DB_POSTGRES_USERNAME")
DB_POSTGRES_PASSWORD = os.environ.get("DB_POSTGRES_PASSWORD")
DB_POSTGRES_HOST = os.environ.get("DB_POSTGRES_HOST")
DB_POSTGRES_PORT = os.environ.get("DB_POSTGRES_PORT")
DB_POSTGRES_NAME = os.environ.get("DB_POSTGRES_NAME")