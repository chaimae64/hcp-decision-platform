import pandas as pd


class Statistics:

    @staticmethod
    def numeric_columns(df: pd.DataFrame) -> list:
        """
        Retourne les colonnes numériques.
        """

        return list(
            df.select_dtypes(include="number").columns
        )

    @staticmethod
    def text_columns(df: pd.DataFrame) -> list:
        """
        Retourne les colonnes textuelles.
        """

        return list(
            df.select_dtypes(exclude="number").columns
        )

    @staticmethod
    def global_information(df: pd.DataFrame) -> dict:
        """
        Informations générales sur le dataset.
        """

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "numeric_columns": len(
                Statistics.numeric_columns(df)
            ),

            "text_columns": len(
                Statistics.text_columns(df)
            ),

            "missing_values": int(
                df.isna().sum().sum()
            ),

            "duplicates": int(
                df.duplicated().sum()
            )

        }

    @staticmethod
    def descriptive_statistics(df: pd.DataFrame) -> dict:
        """
        Calcule les statistiques descriptives.
        """

        results = {}

        for column in Statistics.numeric_columns(df):

            results[column] = {

                "count": int(df[column].count()),

                "mean": round(df[column].mean(), 2),

                "median": round(df[column].median(), 2),

                "min": round(df[column].min(), 2),

                "max": round(df[column].max(), 2),

                "std": round(df[column].std(), 2),

                "variance": round(df[column].var(), 2),

                "sum": round(df[column].sum(), 2)

            }

        return results

    @staticmethod
    def distributions(df: pd.DataFrame) -> dict:
        """
        Distribution des colonnes textuelles.
        """

        result = {}

        for column in Statistics.text_columns(df):

            result[column] = (
                df[column]
                .value_counts(dropna=False)
                .to_dict()
            )

        return result

    @staticmethod
    def detect_dimensions(df: pd.DataFrame) -> list:
        """
        Les dimensions correspondent
        aux colonnes textuelles.
        """

        return Statistics.text_columns(df)

    @staticmethod
    def detect_indicators(df: pd.DataFrame) -> list:
        """
        Les indicateurs correspondent
        aux colonnes numériques.
        """

        return Statistics.numeric_columns(df)
    
    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:
        """
        Lance l'ensemble des analyses statistiques.
        """

        return {

            "general_information":

                Statistics.global_information(df),

            "descriptive_statistics":

                Statistics.descriptive_statistics(df),

            "distributions":

                Statistics.distributions(df),

            "dimensions":

                Statistics.detect_dimensions(df),

            "indicators":

                Statistics.detect_indicators(df)

        }
