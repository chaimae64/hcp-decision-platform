import pandas as pd

from services.dataset_profiler import DatasetProfiler


class Statistics:

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:
        """
        Analyse statistique basée sur DatasetProfiler.
        """

        profiler = DatasetProfiler(df)

        profile = profiler.profile()

        return {

            "general_information":

                profile["general"],

            "descriptive_statistics":

                profile["numeric_statistics"],

            "distributions":

                profile["categorical_statistics"],

            "dimensions":

                profile["groups"]["categorical"],

            "indicators":

                profile["groups"]["numeric"],

            "column_information":

                profile["columns"],

            "missing_values":

                profile["missing_values"],

            "duplicates":

                profile["duplicates"],

            "constant_columns":

                profile["constant_columns"],

            "high_missing_columns":

                profile["high_missing_columns"],

            "high_cardinality_columns":

                profile["high_cardinality_columns"],

            "correlations":

                profile["correlations"],

            "strong_correlations":

                profile["strong_correlations"],

            "data_quality":

                profile["data_quality"],

            "business_profile":

                profile["profile"],

            "recommendations":

                profile["recommendations"]

        }