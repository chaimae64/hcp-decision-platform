from sqlalchemy import create_engine, text
import pandas as pd


class Postgres:

    def __init__(self):

        self.engine = create_engine(
            "postgresql://postgres@localhost:5433/hcp_bi"
        )

    # -------------------------
    # Sauvegarde
    # -------------------------

    def save(self, dataframe, table_name):

        dataframe.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False
        )

        return len(dataframe)

    # -------------------------
    # Nombre de lignes
    # -------------------------

    def count_rows(self, table_name):

        with self.engine.connect() as conn:

            result = conn.execute(
                text(f'SELECT COUNT(*) FROM "{table_name}"')
            )

            return result.scalar()

    # -------------------------
    # Nombre de colonnes
    # -------------------------

    def count_columns(self, table_name):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM information_schema.columns
                    WHERE table_name=:table
                """),
                {"table": table_name}
            )

            return result.scalar()

    # -------------------------
    # Aperçu
    # -------------------------

    def preview(self, table_name, limit=5):

        query = f'SELECT * FROM "{table_name}" LIMIT {limit}'

        return pd.read_sql(query, self.engine)
    
    # -------------------------
    # Statistiques
    # -------------------------

    def statistics(self, table_name):

        dataframe = pd.read_sql(
            f'SELECT * FROM "{table_name}"',
            self.engine
        )

        return {

            "missing_values": int(dataframe.isnull().sum().sum()),

            "duplicates": int(dataframe.duplicated().sum())

        }
    # -------------------------
    # Charger une table
    # -------------------------

    def load_table(self, table_name):

        query = f'SELECT * FROM "{table_name}"'

        return pd.read_sql(query, self.engine)