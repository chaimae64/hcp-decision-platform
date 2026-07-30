import pandas as pd

from database.connection import DatabaseConnection


class DatasetLoader:

    # =====================================================
    # Charger une table PostgreSQL
    # =====================================================

    @staticmethod
    def load(table_name):

        engine = DatabaseConnection.get_engine()

        query = f'SELECT * FROM "{table_name}"'

        return pd.read_sql(query, engine)

    # =====================================================
    # Charger le dernier dataset importé
    # =====================================================

    @staticmethod
    def load_latest(import_info):

        return DatasetLoader.load(import_info["table"])