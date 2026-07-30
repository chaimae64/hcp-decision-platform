class TrendInterpreter:

    @staticmethod
    def interpret(trends):

        if not trends:
            return {}

        interpreted = {}

        for indicator, trend in trends.items():

            direction = trend.get("trend")
            evolution = trend.get("global_evolution")
            volatility = trend.get("volatility")
            rupture = trend.get("trend_break")

            interpreted[indicator] = {

                "direction": direction,

                "evolution": TrendInterpreter.interpret_evolution(
                    evolution
                ),

                "volatility": TrendInterpreter.interpret_volatility(
                    volatility
                ),

                "rupture": TrendInterpreter.interpret_break(
                    rupture
                ),

                "summary": TrendInterpreter.build_summary(
                    direction,
                    evolution,
                    volatility,
                    rupture
                )

            }

        return interpreted

    # =====================================================
    # Evolution
    # =====================================================

    @staticmethod
    def interpret_evolution(value):

        if value is None:
            return "indéterminée"

        if value > 20:
            return "forte hausse"

        elif value > 5:
            return "hausse modérée"

        elif value > -5:
            return "quasi stable"

        elif value > -20:
            return "baisse modérée"

        else:
            return "forte baisse"

    # =====================================================
    # Volatilité
    # =====================================================

    @staticmethod
    def interpret_volatility(value):

        if value is None:
            return "inconnue"

        if value < 2:
            return "faible"

        elif value < 5:
            return "modérée"

        else:
            return "élevée"

    # =====================================================
    # Rupture
    # =====================================================

    @staticmethod
    def interpret_break(value):

        if value:
            return "rupture détectée"

        return "aucune rupture"

    # =====================================================
    # Résumé
    # =====================================================

    @staticmethod
    def build_summary(
        direction,
        evolution,
        volatility,
        rupture
    ):

        summary = ""

        if direction == "Croissante":
            summary = "Une tendance générale à la hausse est observée."

        elif direction == "Décroissante":
            summary = "Une tendance générale à la baisse est observée."

        elif direction == "Stable":
            summary = "Les valeurs restent globalement stables."

        else:
            summary = "Les valeurs évoluent de manière fluctuante."

        if evolution is not None:

            if evolution > 0:
                summary += (
                    f" L'évolution globale est de +{evolution}%."
                )

            elif evolution < 0:
                summary += (
                    f" L'évolution globale est de {evolution}%."
                )

        if volatility is not None:

            if volatility < 2:
                summary += " Les variations sont peu marquées."

            elif volatility < 5:
                summary += " Les variations sont modérées."

            else:
                summary += " Les variations sont importantes."

        if rupture:
            summary += " Une rupture de tendance a été détectée."

        return summary