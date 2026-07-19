import numpy as np
import pandas as pd


class AnomalyDetector:

    # =====================================================
    # Colonnes numériques
    # =====================================================

    @staticmethod
    def numeric_columns(df):

        return list(
            df.select_dtypes(
                include="number"
            ).columns
        )

    # =====================================================
    # Outliers avec IQR
    # =====================================================

    @staticmethod
    def detect_iqr(df):

        results = {}

        for column in AnomalyDetector.numeric_columns(df):

            serie = df[column].dropna()

            if len(serie) < 4:

                continue

            q1 = serie.quantile(0.25)

            q3 = serie.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr

            upper = q3 + 1.5 * iqr

            outliers = serie[
                (serie < lower) |
                (serie > upper)
            ]

            results[column] = {

                "lower_bound": round(lower,2),

                "upper_bound": round(upper,2),

                "count": len(outliers),

                "values": outliers.tolist()

            }

        return results

    # =====================================================
    # Outliers avec Z-score
    # =====================================================

    @staticmethod
    def detect_zscore(df):

        results = {}

        for column in AnomalyDetector.numeric_columns(df):

            serie = df[column].dropna()

            if len(serie) < 4:

                continue

            mean = serie.mean()

            std = serie.std()

            if std == 0:

                continue

            zscores = (

                (serie - mean)

                / std

            )

            outliers = serie[
                np.abs(zscores) > 3
            ]

            results[column] = {

                "count": len(outliers),

                "values": outliers.tolist()

            }

        return results

    # =====================================================
    # Valeurs négatives
    # =====================================================

    @staticmethod
    def negative_values(df):

        results = {}

        for column in AnomalyDetector.numeric_columns(df):

            negatives = df[
                df[column] < 0
            ][column]

            results[column] = {

                "count": len(negatives),

                "values": negatives.tolist()

            }

        return results

    # =====================================================
    # Valeurs >100
    # =====================================================

    @staticmethod
    def greater_than_100(df):

        results = {}

        for column in AnomalyDetector.numeric_columns(df):

            values = df[
                df[column] > 100
            ][column]

            results[column] = {

                "count": len(values),

                "values": values.tolist()

            }

        return results
        # =====================================================
    # Valeurs manquantes
    # =====================================================

    @staticmethod
    def missing_values(df):

        results = {}

        total_rows = len(df)

        for column in df.columns:

            missing = int(df[column].isna().sum())

            percentage = 0

            if total_rows > 0:

                percentage = round(
                    (missing / total_rows) * 100,
                    2
                )

            results[column] = {

                "count": missing,

                "percentage": percentage

            }

        return results

    # =====================================================
    # Colonnes constantes
    # =====================================================

    @staticmethod
    def constant_columns(df):

        constants = []

        for column in df.columns:

            values = df[column].dropna().unique()

            if len(values) == 1:

                constants.append(column)

        return constants

    # =====================================================
    # Colonnes entièrement vides
    # =====================================================

    @staticmethod
    def empty_columns(df):

        columns = []

        for column in df.columns:

            if df[column].isna().all():

                columns.append(column)

        return columns

    # =====================================================
    # Lignes dupliquées
    # =====================================================

    @staticmethod
    def duplicated_rows(df):

        duplicated = df[df.duplicated()]

        return {

            "count": len(duplicated),

            "rows": duplicated.index.tolist()

        }

    # =====================================================
    # Valeurs uniques
    # =====================================================

    @staticmethod
    def unique_values(df):

        results = {}

        for column in df.columns:

            results[column] = int(

                df[column]

                .nunique(

                    dropna=True

                )

            )

        return results

    # =====================================================
    # Type de chaque colonne
    # =====================================================

    @staticmethod
    def column_types(df):

        results = {}

        for column in df.columns:

            results[column] = str(

                df[column].dtype

            )

        return results

    # =====================================================
    # Colonnes fortement incomplètes
    # =====================================================

    @staticmethod
    def critical_missing_columns(
        df,
        threshold=30
    ):

        critical = []

        missing = AnomalyDetector.missing_values(df)

        for column, info in missing.items():

            if info["percentage"] >= threshold:

                critical.append({

                    "column": column,

                    "percentage": info["percentage"]

                })

        return critical

    # =====================================================
    # Résumé qualité
    # =====================================================

    @staticmethod
    def quality_summary(df):

        return {

            "missing_values":

                AnomalyDetector.missing_values(df),

            "constant_columns":

                AnomalyDetector.constant_columns(df),

            "empty_columns":

                AnomalyDetector.empty_columns(df),

            "duplicated_rows":

                AnomalyDetector.duplicated_rows(df),

            "critical_missing_columns":

                AnomalyDetector.critical_missing_columns(df),

            "column_types":

                AnomalyDetector.column_types(df),

            "unique_values":

                AnomalyDetector.unique_values(df)

        }
    
        # =====================================================
    # Score de qualité des données
    # =====================================================

    @staticmethod
    def quality_score(df):

        score = 100

        total_rows = max(len(df), 1)

        # -----------------------------
        # Valeurs manquantes
        # -----------------------------

        missing = int(df.isna().sum().sum())

        score -= missing

        # -----------------------------
        # Doublons
        # -----------------------------

        duplicates = int(df.duplicated().sum())

        score -= duplicates * 2

        # -----------------------------
        # Colonnes constantes
        # -----------------------------

        constants = len(
            AnomalyDetector.constant_columns(df)
        )

        score -= constants * 5

        # -----------------------------
        # Colonnes vides
        # -----------------------------

        empty = len(
            AnomalyDetector.empty_columns(df)
        )

        score -= empty * 8

        # -----------------------------
        # Valeurs négatives
        # -----------------------------

        negatives = 0

        for values in AnomalyDetector.negative_values(df).values():

            negatives += values["count"]

        score -= negatives * 2

        # -----------------------------
        # Valeurs >100
        # -----------------------------

        greater = 0

        for values in AnomalyDetector.greater_than_100(df).values():

            greater += values["count"]

        score -= greater * 3

        # -----------------------------
        # Outliers IQR
        # -----------------------------

        outliers = 0

        for values in AnomalyDetector.detect_iqr(df).values():

            outliers += values["count"]

        score -= outliers

        score = max(0, min(score, 100))

        return score

    # =====================================================
    # Niveau de qualité
    # =====================================================

    @staticmethod
    def quality_level(score):

        if score >= 90:

            return "Excellent"

        elif score >= 75:

            return "Bon"

        elif score >= 60:

            return "Acceptable"

        elif score >= 40:

            return "Faible"

        return "Critique"

    # =====================================================
    # Niveau de risque
    # =====================================================

    @staticmethod
    def risk_level(score):

        if score >= 90:

            return "Faible"

        elif score >= 75:

            return "Modéré"

        elif score >= 60:

            return "Élevé"

        return "Critique"

    # =====================================================
    # Alertes
    # =====================================================

    @staticmethod
    def alerts(df):

        alerts = []

        score = AnomalyDetector.quality_score(df)

        if score < 75:

            alerts.append({

                "level": "WARNING",

                "message":
                "La qualité globale des données est insuffisante."

            })

        # Colonnes critiques

        critical = AnomalyDetector.critical_missing_columns(df)

        for column in critical:

            alerts.append({

                "level": "WARNING",

                "message":
                f"La colonne '{column['column']}' contient "
                f"{column['percentage']}% de valeurs manquantes."

            })

        # Valeurs >100

        for col, values in AnomalyDetector.greater_than_100(df).items():

            if values["count"] > 0:

                alerts.append({

                    "level": "CRITICAL",

                    "message":
                    f"{values['count']} valeur(s) supérieure(s) à 100 détectée(s) dans '{col}'."

                })

        # Valeurs négatives

        for col, values in AnomalyDetector.negative_values(df).items():

            if values["count"] > 0:

                alerts.append({

                    "level": "CRITICAL",

                    "message":
                    f"{values['count']} valeur(s) négative(s) détectée(s) dans '{col}'."

                })

        # Outliers

        for col, values in AnomalyDetector.detect_iqr(df).items():

            if values["count"] > 0:

                alerts.append({

                    "level": "INFO",

                    "message":
                    f"{values['count']} valeur(s) atypique(s) détectée(s) dans '{col}'."

                })

        return alerts

    # =====================================================
    # Actions recommandées
    # =====================================================

    @staticmethod
    def recommendations(df):

        actions = []

        if len(AnomalyDetector.critical_missing_columns(df)) > 0:

            actions.append(
                "Compléter les valeurs manquantes avant toute analyse."
            )

        if len(AnomalyDetector.constant_columns(df)) > 0:

            actions.append(
                "Vérifier les colonnes constantes qui n'apportent aucune information."
            )

        if df.duplicated().sum() > 0:

            actions.append(
                "Supprimer les lignes dupliquées."
            )

        for values in AnomalyDetector.greater_than_100(df).values():

            if values["count"] > 0:

                actions.append(
                    "Contrôler les valeurs supérieures à 100 %."
                )

                break

        for values in AnomalyDetector.negative_values(df).values():

            if values["count"] > 0:

                actions.append(
                    "Contrôler les valeurs négatives."
                )

                break

        return actions

    # =====================================================
    # Résumé qualité
    # =====================================================

    @staticmethod
    def summary(df):

        score = AnomalyDetector.quality_score(df)

        return {

            "score": score,

            "quality":

                AnomalyDetector.quality_level(score),

            "risk":

                AnomalyDetector.risk_level(score),

            "alerts":

                AnomalyDetector.alerts(df),

            "recommendations":

                AnomalyDetector.recommendations(df)

        }
        # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df):
        """
        Lance l'ensemble des analyses de qualité
        et de détection d'anomalies sur le DataFrame.

        Retourne un dictionnaire complet qui sera
        utilisé par le DecisionEngine.
        """

        # -----------------------------
        # Détection des anomalies
        # -----------------------------

        iqr = AnomalyDetector.detect_iqr(df)

        zscore = AnomalyDetector.detect_zscore(df)

        negatives = AnomalyDetector.negative_values(df)

        greater100 = AnomalyDetector.greater_than_100(df)

        # -----------------------------
        # Qualité des données
        # -----------------------------

        missing = AnomalyDetector.missing_values(df)

        constants = AnomalyDetector.constant_columns(df)

        empty = AnomalyDetector.empty_columns(df)

        duplicated = AnomalyDetector.duplicated_rows(df)

        critical_missing = (
            AnomalyDetector.critical_missing_columns(df)
        )

        unique = AnomalyDetector.unique_values(df)

        types = AnomalyDetector.column_types(df)

        # -----------------------------
        # Score qualité
        # -----------------------------

        score = AnomalyDetector.quality_score(df)

        quality = AnomalyDetector.quality_level(score)

        risk = AnomalyDetector.risk_level(score)

        # -----------------------------
        # Alertes
        # -----------------------------

        alerts = AnomalyDetector.alerts(df)

        recommendations = (
            AnomalyDetector.recommendations(df)
        )

        summary = AnomalyDetector.summary(df)

        # -----------------------------
        # Nombre total d'anomalies
        # -----------------------------

        total_outliers = sum(
            item["count"]
            for item in iqr.values()
        )

        total_negative = sum(
            item["count"]
            for item in negatives.values()
        )

        total_greater100 = sum(
            item["count"]
            for item in greater100.values()
        )

        total_missing = int(
            df.isna().sum().sum()
        )

        total_duplicates = duplicated["count"]

        # -----------------------------
        # Résultat final
        # -----------------------------

        return {

            "dataset_quality": {

                "score": score,

                "quality": quality,

                "risk": risk

            },

            "statistics": {

                "rows": len(df),

                "columns": len(df.columns),

                "numeric_columns": len(
                    AnomalyDetector.numeric_columns(df)
                )

            },

            "outliers": {

                "iqr": iqr,

                "zscore": zscore,

                "count": total_outliers

            },

            "negative_values": {

                "details": negatives,

                "count": total_negative

            },

            "greater_than_100": {

                "details": greater100,

                "count": total_greater100

            },

            "missing_values": {

                "details": missing,

                "count": total_missing

            },

            "duplicated_rows": duplicated,

            "constant_columns": constants,

            "empty_columns": empty,

            "critical_missing_columns": critical_missing,

            "unique_values": unique,

            "column_types": types,

            "alerts": alerts,

            "recommendations": recommendations,

            "summary": summary

        }