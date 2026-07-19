import os
import requests

from dotenv import load_dotenv

load_dotenv()


class SupersetAPI:

    def __init__(self):

        self.base_url = os.getenv("SUPERSET_URL").rstrip("/")

        self.username = os.getenv("SUPERSET_USERNAME")

        self.password = os.getenv("SUPERSET_PASSWORD")

        self.database_name = os.getenv(
            "SUPERSET_DATABASE_NAME",
            "PostgreSQL"
        )

        self.token = None
        self.csrf_token = None

        self.session = requests.Session()

    # -------------------------------------------------

    def login(self):

        url = f"{self.base_url}/api/v1/security/login"

        payload = {
            "username": self.username,
            "password": self.password,
            "provider": "db",
            "refresh": True
        }

        response = self.session.post(
            url,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(response.text)

        self.token = response.json()["access_token"]

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        csrf = self.session.get(
            f"{self.base_url}/api/v1/security/csrf_token/",
            headers=headers
        )

        if csrf.status_code != 200:
            raise Exception(csrf.text)

        self.csrf_token = csrf.json()["result"]

    # -------------------------------------------------

    def headers(self):

        if self.token is None:
            self.login()

        return {
            "Authorization": f"Bearer {self.token}",
            "X-CSRFToken": self.csrf_token,
            "Referer": self.base_url,
            "Content-Type": "application/json"
        }

    # -------------------------------------------------

    def get_database_id(self, database_name=None):

        if database_name is None:
            database_name = self.database_name

        url = f"{self.base_url}/api/v1/database/"

        response = self.session.get(
            url,
            headers=self.headers()
        )

        if response.status_code != 200:
            raise Exception(response.text)

        databases = response.json()["result"]

        for database in databases:

            if database["database_name"] == database_name:
                return database["id"]

        raise Exception(
            f"Base '{database_name}' introuvable."
        )

    # -------------------------------------------------

    def dataset_exists(self, table_name, database_id):

        url = f"{self.base_url}/api/v1/dataset/"

        response = self.session.get(
            url,
            headers=self.headers()
        )

        if response.status_code != 200:
            raise Exception(response.text)

        datasets = response.json()["result"]

        for dataset in datasets:

            if (
                dataset["table_name"] == table_name
                and dataset["database"]["id"] == database_id
            ):
                return True

        return False

    # -------------------------------------------------

    def create_dataset(self, table_name, schema="public"):

        database_id = self.get_database_id()

        if self.dataset_exists(table_name, database_id):

            return {
                "created": False,
                "message": "Le Dataset existe déjà."
            }

        payload = {
            "database": database_id,
            "schema": schema,
            "table_name": table_name
        }

        url = f"{self.base_url}/api/v1/dataset/"

        response = self.session.post(
            url,
            headers=self.headers(),
            json=payload
        )

        if response.status_code not in (200, 201):

            raise Exception(response.text)

        return {
            "created": True,
            "message": "Dataset créé avec succès."
        }