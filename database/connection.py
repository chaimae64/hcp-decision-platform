from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

# =====================================================
# Chargement du .env
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env", override=True)


class DatabaseConnection:

    @staticmethod
    def get_engine():

        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if password:

            url = (
                f"postgresql://"
                f"{user}:{password}"
                f"@{host}:{port}/{database}"
            )

        else:

            url = (
                f"postgresql://"
                f"{user}"
                f"@{host}:{port}/{database}"
            )

        return create_engine(url)