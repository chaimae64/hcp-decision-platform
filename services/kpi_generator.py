import pandas as pd
from services.dataset_profiler import DatasetProfiler


class KPIGenerator:

    # =====================================================
    # KPI d'une colonne numérique
    # =====================================================

    @staticmethod
    def statistics(series):

        return {

            "count": int(series.count()),

            "sum": round(series.sum(), 2),

            "mean": round(series.mean(), 2),

            "median": round(series.median(), 2),

            "minimum": round(series.min(), 2),

            "maximum": round(series.max(), 2),

            "range": round(
                series.max() - series.min(),
                2
            ),

            "variance": round(series.var(), 2),

            "std": round(series.std(), 2),

            "q1": round(series.quantile(0.25), 2),

            "q3": round(series.quantile(0.75), 2)

        }

    # =====================================================
    # KPI globaux
    # =====================================================

    @staticmethod
    def global_statistics(df):

        results = {}
        profiler = DatasetProfiler(df)
        for column in profiler.numeric_columns:

            results[column] = KPIGenerator.statistics(
                df[column]
            )

        return results

    # =====================================================
    # Nombre total d'observations
    # =====================================================

    @staticmethod
    def total_observations(df):

        return len(df)

    # =====================================================
    # Nombre de variables
    # =====================================================

    @staticmethod
    def total_variables(df):

        return len(df.columns)

    # =====================================================
    # Nombre d'indicateurs
    # =====================================================

    @staticmethod
    def total_indicators(df):

        profiler = DatasetProfiler(df)

        return len(
            profiler.numeric_columns
        )

    # =====================================================
    # Nombre de dimensions
    # =====================================================

    @staticmethod
    def total_dimensions(df):

        profiler = DatasetProfiler(df)

        return len(
            profiler.categorical_columns
        )

    # =====================================================
    # Résumé statistique
    # =====================================================

    @staticmethod
    def dataset_summary(df):

        return {

            "rows":
                KPIGenerator.total_observations(df),

            "columns":
                KPIGenerator.total_variables(df),

            "dimensions":
                KPIGenerator.total_dimensions(df),

            "indicators":
                KPIGenerator.total_indicators(df)

        }
        # =====================================================
    # Meilleur indicateur
    # =====================================================

    @staticmethod
    def best_indicator(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        if not indicators:
            return None

        means = {}

        for col in indicators:
            means[col] = df[col].mean()

        best = max(means, key=means.get)

        return {

            "indicator": best,

            "value": round(means[best], 2)

        }

    # =====================================================
    # Indicateur le plus faible
    # =====================================================

    @staticmethod
    def worst_indicator(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        if not indicators:
            return None

        means = {}

        for col in indicators:
            means[col] = df[col].mean()

        worst = min(means, key=means.get)

        return {

            "indicator": worst,

            "value": round(means[worst], 2)

        }

    # =====================================================
    # Meilleure catégorie
    # =====================================================

    @staticmethod
    def best_category(df, dimension, indicator):

        ranking = (

            df

            .groupby(dimension)[indicator]

            .mean()

            .sort_values(ascending=False)

        )

        return {

            "category": ranking.index[0],

            "value": round(ranking.iloc[0], 2)

        }

    # =====================================================
    # Catégorie la plus faible
    # =====================================================

    @staticmethod
    def worst_category(df, dimension, indicator):

        ranking = (

            df

            .groupby(dimension)[indicator]

            .mean()

            .sort_values()

        )

        return {

            "category": ranking.index[0],

            "value": round(ranking.iloc[0], 2)

        }

    # =====================================================
    # Moyenne générale
    # =====================================================

    @staticmethod
    def overall_average(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        if len(indicators) == 0:
            return None

        values = []

        for col in indicators:

            values.extend(

                df[col]

                .dropna()

                .tolist()

            )

        return round(

            sum(values)

            / len(values),

            2

        )

    # =====================================================
    # Valeur maximale du dataset
    # =====================================================

    @staticmethod
    def global_maximum(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        maximum = None

        column = None

        for col in indicators:

            value = df[col].max()

            if maximum is None or value > maximum:

                maximum = value

                column = col

        return {

            "indicator": column,

            "value": round(maximum,2)

        }

    # =====================================================
    # Valeur minimale du dataset
    # =====================================================

    @staticmethod
    def global_minimum(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        minimum = None

        column = None

        for col in indicators:

            value = df[col].min()

            if minimum is None or value < minimum:

                minimum = value

                column = col

        return {

            "indicator": column,

            "value": round(minimum,2)

        }

    # =====================================================
    # KPI métier
    # =====================================================

    @staticmethod
    def business_kpis(df):

        result = {

            "overall_average":

                KPIGenerator.overall_average(df),

            "best_indicator":

                KPIGenerator.best_indicator(df),

            "worst_indicator":

                KPIGenerator.worst_indicator(df),

            "global_maximum":

                KPIGenerator.global_maximum(df),

            "global_minimum":

                KPIGenerator.global_minimum(df)

        }

        profiler = DatasetProfiler(df)

        dimensions = profiler.categorical_columns

        indicators = profiler.numeric_columns

        result["categories"] = {}

        for dimension in dimensions:

            result["categories"][dimension] = {}

            for indicator in indicators:

                try:

                    result["categories"][dimension][indicator] = {

                        "best":

                            KPIGenerator.best_category(

                                df,

                                dimension,

                                indicator

                            ),

                        "worst":

                            KPIGenerator.worst_category(

                                df,

                                dimension,

                                indicator

                            )

                    }

                except Exception:

                    continue

        return result
    
        # =====================================================
    # Evolution globale des indicateurs
    # =====================================================

    @staticmethod
    def global_evolution(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        evolution = {}

        for i in range(len(indicators) - 1):

            current = indicators[i]
            next_indicator = indicators[i + 1]

            current_mean = df[current].mean()
            next_mean = df[next_indicator].mean()

            if current_mean == 0:

                rate = None

            else:

                rate = round(

                    ((next_mean - current_mean) / current_mean) * 100,

                    2

                )

            evolution[f"{current} -> {next_indicator}"] = rate

        return evolution

    # =====================================================
    # Tendance globale
    # =====================================================

    @staticmethod
    def global_trend(df):

        profiler = DatasetProfiler(df)

        indicators = profiler.numeric_columns

        means = []

        for col in indicators:

            means.append(df[col].mean())

        if len(means) < 2:

            return "Indéterminée"

        increasing = all(

            means[i] <= means[i+1]

            for i in range(len(means)-1)

        )

        decreasing = all(

            means[i] >= means[i+1]

            for i in range(len(means)-1)

        )

        if increasing:

            return "Croissante"

        if decreasing:

            return "Décroissante"

        return "Fluctuante"

    # =====================================================
    # Priorité décisionnelle
    # =====================================================

    @staticmethod
    def priority(df):

        avg = KPIGenerator.overall_average(df)

        if avg is None:

            return "Indéterminée"

        if avg >= 70:

            return "Critique"

        elif avg >= 50:

            return "Très élevée"

        elif avg >= 30:

            return "Élevée"

        elif avg >= 15:

            return "Moyenne"

        return "Faible"

    # =====================================================
    # Score décisionnel
    # =====================================================

    @staticmethod
    def decision_score(df):

        avg = KPIGenerator.overall_average(df)

        if avg is None:

            return 0

        score = min(100, round(avg, 2))

        return score

    # =====================================================
    # Niveau décisionnel
    # =====================================================

    @staticmethod
    def decision_level(score):

        if score >= 80:

            return "Très critique"

        elif score >= 60:

            return "Critique"

        elif score >= 40:

            return "Élevé"

        elif score >= 20:

            return "Modéré"

        return "Faible"

    # =====================================================
    # Résumé exécutif
    # =====================================================

    @staticmethod
    def executive_summary(df):

        average = KPIGenerator.overall_average(df)

        best = KPIGenerator.best_indicator(df)

        worst = KPIGenerator.worst_indicator(df)

        trend = KPIGenerator.global_trend(df)

        priority = KPIGenerator.priority(df)

        return {

            "average": average,

            "trend": trend,

            "priority": priority,

            "best_indicator": best,

            "worst_indicator": worst

        }

    # =====================================================
    # KPI décisionnels
    # =====================================================

    @staticmethod
    def decision_kpis(df):

        score = KPIGenerator.decision_score(df)

        return {

            "decision_score": score,

            "decision_level":

                KPIGenerator.decision_level(score),

            "priority":

                KPIGenerator.priority(df),

            "global_trend":

                KPIGenerator.global_trend(df),

            "evolution":

                KPIGenerator.global_evolution(df),

            "executive_summary":

                KPIGenerator.executive_summary(df)

        }
    
        # =====================================================
    # Analyse complète des KPI
    # =====================================================

    @staticmethod
    def analyze(df):
        """
        Génère l'ensemble des KPI du dataset.

        Cette méthode regroupe :
        - les informations générales
        - les statistiques descriptives
        - les KPI métier
        - les KPI décisionnels

        Retour
        ------
        dict
        """
        profiler = DatasetProfiler(df)

        profile = profiler.profile()

        return {

            # ------------------------------------------
            # Informations générales
            # ------------------------------------------

            "dataset": profile["general"],

            # ------------------------------------------
            # Statistiques descriptives
            # ------------------------------------------

            "statistics": KPIGenerator.global_statistics(df),

            # ------------------------------------------
            # KPI métier
            # ------------------------------------------

            "business": KPIGenerator.business_kpis(df),

            # ------------------------------------------
            # KPI décisionnels
            # ------------------------------------------

            "decision": KPIGenerator.decision_kpis(df)

        }