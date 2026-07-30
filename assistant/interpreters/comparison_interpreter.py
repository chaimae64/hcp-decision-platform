class ComparisonInterpreter:

    @staticmethod
    def interpret(comparisons):

        if not comparisons:
            return {}

        interpreted = {}

        for dimension, indicators in comparisons.items():

            interpreted[dimension] = {}

            for indicator, comparison in indicators.items():

                severity = comparison.get("severity")

                dominance = comparison.get("dominance")

                leader = comparison.get("leader", {})
                last = comparison.get("last", {})

                interpreted[dimension][indicator] = {

                    "priority":
                        ComparisonInterpreter.interpret_priority(
                            severity
                        ),

                    "business_impact":
                        ComparisonInterpreter.interpret_business_impact(
                            dimension,
                            leader.get("category")
                        ),

                    "recommendation":
                        ComparisonInterpreter.interpret_recommendation(
                            dimension,
                            leader.get("category")
                        ),

                    "summary":
                        ComparisonInterpreter.build_summary(
                            leader,
                            last,
                            comparison.get("relative_difference"),
                            severity,
                            dominance
                        )

                }

        return interpreted

    # =====================================================
    # Priorité
    # =====================================================

    @staticmethod
    def interpret_priority(severity):

        priorities = {

            "Faible": "Faible",

            "Modérée": "Moyenne",

            "Importante": "Élevée",

            "Élevée": "Très élevée",

            "Critique": "Critique"

        }

        return priorities.get(
            severity,
            "Indéterminée"
        )

    # =====================================================
    # Impact métier
    # =====================================================

    @staticmethod
    def interpret_business_impact(
        dimension,
        leader
    ):

        if leader is None:
            return None

        dimension = dimension.lower()

        if dimension == "milieu":

            return (
                f"Le phénomène est principalement "
                f"concentré en milieu {leader.lower()}."
            )

        elif dimension == "sexe":

            return (
                f"La catégorie '{leader}' apparaît "
                f"comme la plus concernée."
            )

        elif "region" in dimension or "région" in dimension:

            return (
                f"La région '{leader}' nécessite "
                f"une attention particulière."
            )

        return (
            f"La catégorie '{leader}' domine "
            f"les autres catégories."
        )

    # =====================================================
    # Recommandation
    # =====================================================

    @staticmethod
    def interpret_recommendation(
        dimension,
        leader
    ):

        if leader is None:
            return None

        dimension = dimension.lower()

        if dimension == "milieu":

            if leader.lower() == "urbain":

                return (
                    "Renforcer les politiques "
                    "d'emploi en milieu urbain."
                )

            return (
                "Développer les programmes "
                "d'insertion en milieu rural."
            )

        elif dimension == "sexe":

            return (
                "Mettre en place des actions "
                "ciblées selon le genre."
            )

        elif "region" in dimension or "région" in dimension:

            return (
                f"Prioriser les investissements "
                f"dans la région '{leader}'."
            )

        return (
            "Mettre en place une analyse "
            "complémentaire."
        )

    # =====================================================
    # Résumé
    # =====================================================

    @staticmethod
    def build_summary(
        leader,
        last,
        difference,
        severity,
        dominance
    ):

        leader_name = leader.get("category")
        leader_value = leader.get("value")

        last_name = last.get("category")
        last_value = last.get("value")

        summary = (
            f"La catégorie '{leader_name}' présente "
            f"la valeur moyenne la plus élevée "
            f"({leader_value}). "
        )

        summary += (
            f"La catégorie '{last_name}' présente "
            f"la valeur moyenne la plus faible "
            f"({last_value}). "
        )

        if difference is not None:

            summary += (
                f"L'écart relatif est de "
                f"{difference}%. "
            )

        summary += (
            f"Le niveau de gravité est "
            f"{severity.lower()} "
            f"avec une dominance "
            f"{dominance.lower()}."
        )

        return summary.strip()