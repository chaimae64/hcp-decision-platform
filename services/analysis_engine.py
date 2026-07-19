import pandas as pd
from sqlalchemy import create_engine


class AnalysisEngine:

    def __init__(self):

        self.engine = create_engine(
            "postgresql://postgres@localhost:5433/hcp_bi"
        )

    # -----------------------------------------------------
    # Charger une table PostgreSQL
    # -----------------------------------------------------

    def load_table(self, table_name):

        query = f'SELECT * FROM "{table_name}"'

        df = pd.read_sql(query, self.engine)

        if df.empty:
            raise Exception(
                f"La table '{table_name}' est vide."
            )

        return df

    # -----------------------------------------------------
    # Détecter les colonnes numériques
    # -----------------------------------------------------

    def get_numeric_columns(self, df):

        return list(
            df.select_dtypes(
                include="number"
            ).columns
        )

    # -----------------------------------------------------
    # Détecter les colonnes textuelles
    # -----------------------------------------------------

    def get_text_columns(self, df):

        return list(
            df.select_dtypes(
                exclude="number"
            ).columns
        )

    # -----------------------------------------------------
    # Statistiques générales
    # -----------------------------------------------------

    def general_information(self, df):

        numeric_columns = self.get_numeric_columns(df)
        text_columns = self.get_text_columns(df)

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "numeric_columns": len(numeric_columns),

            "text_columns": len(text_columns),

            "missing_values": int(
                df.isna().sum().sum()
            )

        }

    # -----------------------------------------------------
    # Détecter automatiquement les dimensions
    # -----------------------------------------------------

    def detect_dimensions(self, df):

        return self.get_text_columns(df)

    # -----------------------------------------------------
    # Détecter automatiquement les indicateurs
    # -----------------------------------------------------

    def detect_indicators(self, df):

        return self.get_numeric_columns(df)

    # -----------------------------------------------------
    # Statistiques descriptives
    # -----------------------------------------------------

    def descriptive_statistics(self, df):

        statistics = {}

        for column in self.get_numeric_columns(df):

            statistics[column] = {

                "mean": round(df[column].mean(), 2),

                "median": round(df[column].median(), 2),

                "min": round(df[column].min(), 2),

                "max": round(df[column].max(), 2),

                "std": round(df[column].std(), 2),

                "variance": round(df[column].var(), 2)

            }

        return statistics

    # -----------------------------------------------------
    # Répartition des dimensions
    # -----------------------------------------------------

    def distributions(self, df):

        result = {}

        for column in self.get_text_columns(df):

            result[column] = (
                df[column]
                .value_counts()
                .to_dict()
            )

        return result

    # -----------------------------------------------------
    # Analyse complète
    # -----------------------------------------------------

    def analyze(self, table_name):

        df = self.load_table(table_name)

        return {

            "table": table_name,

            "general_information":
                self.general_information(df),

            "dimensions":
                self.detect_dimensions(df),

            "indicators":
                self.detect_indicators(df),

            "statistics":
                self.descriptive_statistics(df),

            "distributions":
                self.distributions(df)

        }