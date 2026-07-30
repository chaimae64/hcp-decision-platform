import pandas as pd
from services.dataset_profiler import DatasetProfiler


class ComparisonAnalyzer:


    
    # =====================================================
    # Comparaison
    # =====================================================

    @staticmethod
    def compare(
        df,
        dimension,
        indicator
    ):
        """
        Retourne la moyenne
        de chaque catégorie.
        """

        result = (

            df

            .groupby(dimension)[indicator]

            .mean()

            .sort_values(ascending=False)

        )

        return result.round(2)

    # =====================================================
    # Ecart absolu
    # =====================================================

    @staticmethod
    def absolute_difference(values):

        if len(values) < 2:

            return None

        return round(

            values.max()

            - values.min(),

            2

        )

    # =====================================================
    # Ecart relatif (%)
    # =====================================================

    @staticmethod
    def relative_difference(values):

        if len(values) < 2:

            return None

        minimum = values.min()

        maximum = values.max()

        if minimum == 0:

            return None

        return round(

            (

                (maximum - minimum)

                / minimum

            ) * 100,

            2

        )

    # =====================================================
    # Gravité
    # =====================================================

    @staticmethod
    def severity(percent):

        """
        Détermine le niveau
        de gravité.
        """

        if percent is None:

            return "Indéterminée"

        if percent < 10:

            return "Faible"

        elif percent < 25:

            return "Modérée"

        elif percent < 50:

            return "Importante"

        elif percent < 75:

            return "Élevée"

        return "Critique"

    # =====================================================
    # Dominance
    # =====================================================

    @staticmethod
    def dominance(percent):

        """
        Mesure la domination
        de la première catégorie.
        """

        if percent is None:

            return "Indéterminée"

        if percent < 15:

            return "Faible"

        elif percent < 35:

            return "Moyenne"

        elif percent < 60:

            return "Forte"

        return "Très forte"

    # =====================================================
    # Leader
    # =====================================================

    @staticmethod
    def leader(grouped):

        return {

            "category":

                grouped.index[0],

            "value":

                round(

                    grouped.iloc[0],

                    2

                )

        }

    # =====================================================
    # Dernier
    # =====================================================

    @staticmethod
    def last(grouped):

        return {

            "category":

                grouped.index[-1],

            "value":

                round(

                    grouped.iloc[-1],

                    2

                )

        }
     

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df):

        results = {}
        profiler = DatasetProfiler(df)

        dimensions = profiler.categorical_columns

        indicators = profiler.numeric_columns

        for dimension in dimensions:

            results[dimension] = {}

            for indicator in indicators:

                try:

                    grouped = ComparisonAnalyzer.compare(
                        df,
                        dimension,
                        indicator
                    )

                    if grouped.empty:
                        continue

                    if len(grouped) < 2:
                        continue

                    leader = grouped.index[0]

                    diff = (
                        ComparisonAnalyzer.relative_difference(
                            grouped.values
                        )
                    )

                    severity = (
                        ComparisonAnalyzer.severity(
                            diff
                        )
                    )

                    results[dimension][indicator] = {

                        "values":

                            grouped.to_dict(),
                        
                        "top5":

                            grouped.head(5).round(2).to_dict(),

                        "bottom5":
                            grouped.tail(5).round(2).to_dict(),

                        "categories_count":
                            len(grouped),
                            

                        "leader":

                            ComparisonAnalyzer.leader(
                                grouped
                            ),

                        "last":

                            ComparisonAnalyzer.last(
                                grouped
                            ),

                        "absolute_difference":

                            ComparisonAnalyzer.absolute_difference(
                                grouped.values
                            ),

                        "relative_difference":

                            diff,

                        "severity":

                            severity,


                        "dominance":

                            ComparisonAnalyzer.dominance(
                                diff
                            )


                    }

                except Exception as error:

                    print(

                        f"Erreur comparaison "

                        f"{dimension} / {indicator} :",

                        error

                    )

                    continue

        return results