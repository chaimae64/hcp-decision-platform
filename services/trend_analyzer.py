import pandas as pd
import numpy as np

from services.dataset_profiler import DatasetProfiler


class TrendAnalyzer:

    # =====================================================
    # Sens de la tendance
    # =====================================================

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

    # =====================================================
    # Evolution globale
    # =====================================================

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

        return round(((last - first) / first) * 100, 2)

    # =====================================================
    # Variation absolue
    # =====================================================

    @staticmethod
    def absolute_variation(values):

        values = np.array(values, dtype=float)
        values = values[~np.isnan(values)]

        if len(values) < 2:
            return None

        return round(values[-1] - values[0], 4)

    # =====================================================
    # Variations successives
    # =====================================================

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

                variations.append(
                    round(
                        ((current - previous) / previous) * 100,
                        2
                    )
                )

        return variations

    # =====================================================
    # Volatilité
    # =====================================================

    @staticmethod
    def volatility(values):

        values = np.array(values, dtype=float)
        values = values[~np.isnan(values)]

        if len(values) < 2:
            return 0

        return round(np.std(values), 4)

    # =====================================================
    # Pente
    # =====================================================

    @staticmethod
    def slope(values):

        values = np.array(values, dtype=float)
        values = values[~np.isnan(values)]

        if len(values) < 2:
            return 0

        x = np.arange(len(values))

        slope, _ = np.polyfit(x, values, 1)

        return round(slope, 4)

    # =====================================================
    # Rupture
    # =====================================================

    @staticmethod
    def detect_break(values):

        values = np.array(values, dtype=float)

        if len(values) < 4:
            return False

        diff = np.diff(values)

        std = np.std(diff)

        if std == 0:
            return False

        return np.any(np.abs(diff) > (2 * std))

    # =====================================================
    # Interprétation
    # =====================================================

    @staticmethod
    def interpretation(direction,
                       evolution,
                       volatility,
                       rupture):

        text = ""

        if direction == "Croissante":

            text += "Une tendance à la hausse est observée. "

        elif direction == "Décroissante":

            text += "Une tendance à la baisse est observée. "

        elif direction == "Stable":

            text += "Les valeurs sont globalement stables. "

        else:

            text += "Les valeurs fluctuent de manière importante. "

        if evolution is not None:

            text += f"Evolution globale : {evolution}%. "

        if volatility > 0:

            text += f"Volatilité : {volatility}. "

        if rupture:

            text += "Une rupture de tendance a été détectée."

        return text

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df: pd.DataFrame):

        profiler = DatasetProfiler(df)

        results = {}

        for column in profiler.numeric_columns:

            values = (
                df[column]
                .dropna()
                .tolist()
            )

            direction = TrendAnalyzer.trend_direction(values)

            evolution = TrendAnalyzer.evolution_rate(values)

            yearly = TrendAnalyzer.yearly_variation(values)

            absolute = TrendAnalyzer.absolute_variation(values)

            volatility = TrendAnalyzer.volatility(values)

            slope = TrendAnalyzer.slope(values)

            rupture = TrendAnalyzer.detect_break(values)

            interpretation = TrendAnalyzer.interpretation(
                direction,
                evolution,
                volatility,
                rupture
            )

            results[column] = {

                "trend": direction,

                "global_evolution": evolution,

                "absolute_variation": absolute,

                "yearly_variation": yearly,

                "volatility": volatility,

                "slope": slope,

                "trend_break": rupture,

                "interpretation": interpretation

            }

        return results