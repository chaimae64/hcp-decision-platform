import pandas as pd
import numpy as np


class DatasetProfiler:
    """
    Moteur de profilage du dataset.

    Cette classe réalise une analyse complète du DataFrame
    et fournit un profil unique utilisé par l'ensemble
    des modules de la plateforme :

    - Statistics
    - TrendAnalyzer
    - ComparisonAnalyzer
    - RankingAnalyzer
    - KPIGenerator
    - AnomalyDetector
    - Assistant IA

    Toutes les informations sont calculées une seule fois
    afin d'éviter les traitements redondants.
    """

    # =====================================================
    # Constructeur
    # =====================================================

    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()

        self.numeric_columns = list(
            self.df.select_dtypes(include="number").columns
        )

        self.categorical_columns = list(
            self.df.select_dtypes(exclude="number").columns
        )

        self.datetime_columns = list(
            self.df.select_dtypes(
                include=["datetime64", "datetime64[ns]"]
            ).columns
        )

    # =====================================================
    # Informations générales
    # =====================================================

    def general_information(self):

        memory = self.df.memory_usage(
            deep=True
        ).sum() / (1024 ** 2)

        return {

            "rows": len(self.df),

            "columns": len(self.df.columns),

            "memory_mb": round(memory, 2),

            "numeric_columns": len(
                self.numeric_columns
            ),

            "categorical_columns": len(
                self.categorical_columns
            ),

            "datetime_columns": len(
                self.datetime_columns
            )

        }

    # =====================================================
    # Informations sur les colonnes
    # =====================================================

    def column_information(self):

        profile = {}

        for column in self.df.columns:

            missing = int(
                self.df[column].isna().sum()
            )

            missing_percent = round(
                missing / len(self.df) * 100,
                2
            )

            profile[column] = {

                "dtype": str(
                    self.df[column].dtype
                ),

                "missing_values": missing,

                "missing_percent": missing_percent,

                "unique_values": int(
                    self.df[column].nunique(
                        dropna=True
                    )
                ),

                "most_frequent": (
                    None
                    if self.df[column].mode().empty
                    else self.df[column].mode().iloc[0]
                )

            }

        return profile

    # =====================================================
    # Liste des colonnes
    # =====================================================

    def column_groups(self):

        return {

            "numeric": self.numeric_columns,

            "categorical": self.categorical_columns,

            "datetime": self.datetime_columns

        }

    # =====================================================
    # Analyse principale
    # =====================================================

    def profile(self):

        return {

            "general":
                self.general_information(),

            "columns":
                self.column_information(),

            "groups":
                self.column_groups(),

            "numeric_statistics":
                self.numeric_statistics(),

            "categorical_statistics":
                self.categorical_statistics(),

            "missing_values":
                self.missing_values(),

            "duplicates":
                self.duplicates(),

            "constant_columns":
                self.constant_columns(),

            "high_missing_columns":
                self.high_missing_columns(),

            "high_cardinality_columns":
                self.high_cardinality_columns(),

            "correlations":
                self.correlations(),

            "strong_correlations":
                self.strong_correlations(),

            "data_quality":
                self.data_quality(),
            
            "profile":
                self.business_profile(),

            "recommendations":
                self.recommendations()

        }
    # =====================================================
    # Statistiques numériques avancées
    # =====================================================

    def numeric_statistics(self):

        stats = {}

        for column in self.numeric_columns:

            series = self.df[column].dropna()

            if series.empty:
                continue

            mean = series.mean()

            std = series.std()

            stats[column] = {

                "count": int(series.count()),

                "sum": round(series.sum(), 4),

                "mean": round(mean, 4),

                "median": round(series.median(), 4),

                "min": round(series.min(), 4),

                "max": round(series.max(), 4),

                "variance": round(series.var(), 4),

                "std": round(std, 4),

                "q1": round(series.quantile(0.25), 4),

                "q3": round(series.quantile(0.75), 4),

                "iqr": round(
                    series.quantile(0.75) -
                    series.quantile(0.25),
                    4
                ),

                "range": round(
                    series.max() -
                    series.min(),
                    4
                ),

                "coefficient_variation":

                    None

                    if mean == 0

                    else round(

                        (std / mean) * 100,

                        2

                    ),

                "skewness":

                    round(

                        series.skew(),

                        4

                    ),

                "kurtosis":

                    round(

                        series.kurt(),

                        4

                    )

            }

        return stats


    # =====================================================
    # Distribution des variables catégorielles
    # =====================================================

    def categorical_statistics(self):

        statistics = {}

        for column in self.categorical_columns:

            vc = self.df[column].value_counts(
                dropna=False
            )

            statistics[column] = {

                "unique_values":

                    int(

                        self.df[column].nunique()

                    ),

                "top_values":

                    vc.head(10).to_dict(),

                "most_frequent":

                    None

                    if vc.empty

                    else vc.index[0],

                "frequency":

                    None

                    if vc.empty

                    else int(vc.iloc[0])

            }

        return statistics
    
    # =====================================================
    # Valeurs manquantes
    # =====================================================

    def missing_values(self):

        result = {}

        for column in self.df.columns:

            missing = int(self.df[column].isna().sum())

            percent = round(
                (missing / len(self.df)) * 100,
                2
            )

            result[column] = {

                "count": missing,

                "percent": percent

            }

        return result


    # =====================================================
    # Doublons
    # =====================================================

    def duplicates(self):

        duplicates = int(
            self.df.duplicated().sum()
        )

        percent = round(

            duplicates / len(self.df) * 100,

            2

        )

        return {

            "count": duplicates,

            "percent": percent

        }


    # =====================================================
    # Colonnes constantes
    # =====================================================

    def constant_columns(self):

        columns = []

        for column in self.df.columns:

            if self.df[column].nunique(dropna=False) <= 1:

                columns.append(column)

        return columns


    # =====================================================
    # Colonnes avec beaucoup de valeurs manquantes
    # =====================================================

    def high_missing_columns(self, threshold=30):

        columns = []

        for column in self.df.columns:

            percent = (

                self.df[column].isna().sum()

                / len(self.df)

            ) * 100

            if percent >= threshold:

                columns.append(column)

        return columns


    # =====================================================
    # Colonnes à forte cardinalité
    # =====================================================

    def high_cardinality_columns(self, threshold=50):

        columns = []

        for column in self.categorical_columns:

            if self.df[column].nunique() >= threshold:

                columns.append(column)

        return columns


    # =====================================================
    # Corrélations
    # =====================================================

    def correlations(self):

        if len(self.numeric_columns) < 2:

            return {}

        corr = self.df[self.numeric_columns].corr()

        result = {}

        for col1 in corr.columns:

            for col2 in corr.columns:

                if col1 >= col2:

                    continue

                value = round(
                    corr.loc[col1, col2],
                    4
                )

                result[f"{col1} <-> {col2}"] = value

        return result


    # =====================================================
    # Corrélations fortes
    # =====================================================

    def strong_correlations(self, threshold=0.7):

        strong = {}

        for pair, value in self.correlations().items():

            if abs(value) >= threshold:

                strong[pair] = value

        return strong


    # =====================================================
    # Qualité globale des données
    # =====================================================

    def data_quality(self):

        score = 100

        score -= len(

            self.high_missing_columns()

        ) * 5

        score -= len(

            self.constant_columns()

        ) * 5

        score -= min(

            self.duplicates()["percent"] / 2,

            20

        )

        score = max(0, round(score, 2))

        return {

            "score": score,

            "constant_columns":
                self.constant_columns(),

            "high_missing_columns":
                self.high_missing_columns(),

            "duplicates":
                self.duplicates()

        }
    
    # =====================================================
    # Profil métier
    # =====================================================

    def business_profile(self):

        profile = {

            "contains_year": False,

            "contains_region": False,

            "contains_gender": False,

            "contains_environment": False,

            "contains_date": False,

            "contains_numeric": len(self.numeric_columns) > 0

        }

        columns = [c.lower() for c in self.df.columns]

        for col in columns:

            if "année" in col or "annee" in col or "year" in col:
                profile["contains_year"] = True

            if "région" in col or "region" in col:
                profile["contains_region"] = True

            if "sexe" in col or "gender" in col:
                profile["contains_gender"] = True

            if "milieu" in col or "environment" in col:
                profile["contains_environment"] = True

            if "date" in col:
                profile["contains_date"] = True

        return profile


    # =====================================================
    # Recommandations automatiques
    # =====================================================

    def recommendations(self):

        recommendations = []

        if self.high_missing_columns():
            recommendations.append(
                "Nettoyer les colonnes contenant de nombreuses valeurs manquantes."
            )

        if self.constant_columns():
            recommendations.append(
                "Supprimer les colonnes constantes."
            )

        if self.duplicates()["count"] > 0:
            recommendations.append(
                "Supprimer les lignes dupliquées."
            )

        if len(self.strong_correlations()) > 0:
            recommendations.append(
                "Examiner les fortes corrélations entre variables."
            )

        if not recommendations:
            recommendations.append(
                "Aucune recommandation particulière."
            )

        return recommendations