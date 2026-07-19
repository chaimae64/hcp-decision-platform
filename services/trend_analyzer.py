import pandas as pd
import numpy as np


class TrendAnalyzer:

    # --------------------------------------------------
    # Colonnes numériques
    # --------------------------------------------------

    @staticmethod
    def numeric_columns(df):

        return list(
            df.select_dtypes(include="number").columns
        )

    # --------------------------------------------------
    # Déterminer le sens de la tendance
    # --------------------------------------------------

    @staticmethod
    def trend_direction(values):

        values = np.array(values, dtype=float)

        values = values[~np.isnan(values)]

        if len(values) < 2:
            return "Indéterminée"

        differences = np.diff(values)

        positive = np.sum(differences > 0)
        negative = np.sum(differences < 0)

        if positive == len(differences):

            return "Croissante"

        if negative == len(differences):

            return "Décroissante"

        if np.all(np.abs(differences) < 0.001):

            return "Stable"

        return "Fluctuante"

    # --------------------------------------------------
    # Evolution globale (%)
    # --------------------------------------------------

    @staticmethod
    def evolution_rate(values):

        values = np.array(values, dtype=float)

        values = values[~np.isnan(values)]

        if len(values) < 2:
            return None

        first = values[0]
        last = values[-1]

        if first == 0:
            return None

        rate = ((last - first) / first) * 100

        return round(rate, 2)

    # --------------------------------------------------
    # Evolution annuelle
    # --------------------------------------------------

    @staticmethod
    def yearly_variation(values):

        values = np.array(values, dtype=float)

        variations = []

        for i in range(1, len(values)):

            previous = values[i - 1]
            current = values[i]

            if previous == 0:

                variations.append(None)

            else:

                percentage = (
                    (current - previous)
                    / previous
                ) * 100

                variations.append(
                    round(
                        percentage,
                        2
                    )
                )

        return variations

    # --------------------------------------------------
    # Détecter une rupture de tendance
    # --------------------------------------------------

    @staticmethod
    def detect_break(values):

        values = np.array(values, dtype=float)

        if len(values) < 4:
            return False

        differences = np.diff(values)

        std = np.std(differences)

        if std == 0:
            return False

        for d in differences:

            if abs(d) > (2 * std):

                return True

        return False

    # --------------------------------------------------
    # Générer une interprétation
    # --------------------------------------------------

    @staticmethod
    def interpretation(direction,
                       evolution,
                       rupture):

        text = ""

        if direction == "Croissante":

            text += (
                "Une tendance globale à la hausse "
                "est observée. "
            )

        elif direction == "Décroissante":

            text += (
                "Une diminution progressive "
                "est observée. "
            )

        elif direction == "Stable":

            text += (
                "Les valeurs restent globalement "
                "stables. "
            )

        else:

            text += (
                "Les valeurs présentent "
                "des fluctuations importantes. "
            )

        if evolution is not None:

            text += (
                f"L'évolution globale est de "
                f"{evolution}%."
            )

        if rupture:

            text += (
                " Une rupture importante "
                "de tendance a été détectée."
            )

        return text

    # --------------------------------------------------
    # Analyse complète
    # --------------------------------------------------

    @staticmethod
    def analyze(df):

        results = {}

        columns = TrendAnalyzer.numeric_columns(df)

        for column in columns:

            values = (
                df[column]
                .dropna()
                .tolist()
            )

            direction = (
                TrendAnalyzer.trend_direction(
                    values
                )
            )

            evolution = (
                TrendAnalyzer.evolution_rate(
                    values
                )
            )

            yearly = (
                TrendAnalyzer.yearly_variation(
                    values
                )
            )

            rupture = (
                TrendAnalyzer.detect_break(
                    values
                )
            )

            interpretation = (
                TrendAnalyzer.interpretation(
                    direction,
                    evolution,
                    rupture
                )
            )

            results[column] = {

                "trend": direction,

                "global_evolution": evolution,

                "yearly_variation": yearly,

                "trend_break": rupture,

                "interpretation": interpretation

            }

        return results
    
