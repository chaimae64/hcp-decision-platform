

import pandas as pd

from sqlalchemy import inspect

from database.connection import DatabaseConnection


class DatabaseService:

    # =====================================================
    # Charger une table
    # =====================================================

    @staticmethod
    def load_table(table_name):

        engine = DatabaseConnection.get_engine()

        query = f"SELECT * FROM {table_name}"

        return pd.read_sql(query, engine)

    # =====================================================
    # Liste des tables
    # =====================================================

    @staticmethod
    def get_tables():

        engine = DatabaseConnection.get_engine()

        inspector = inspect(engine)

        return inspector.get_table_names()

    # =====================================================
    # Vérifier l'existence d'une table
    # =====================================================

    @staticmethod
    def table_exists(table_name):

        tables = DatabaseService.get_tables()

        return table_name in tables

    # =====================================================
    # Sauvegarder un DataFrame
    # =====================================================

    @staticmethod
    def save_dataframe(

            dataframe,

            table_name,

            if_exists="replace"

    ):

        engine = DatabaseConnection.get_engine()

        dataframe.to_sql(

            table_name,

            engine,

            if_exists=if_exists,

            index=False

        )

    # =====================================================
    # Supprimer une table
    # =====================================================

    @staticmethod
    def delete_table(table_name):

        engine = DatabaseConnection.get_engine()

        with engine.begin() as connection:

            connection.exec_driver_sql(

                f"DROP TABLE IF EXISTS {table_name}"

            )