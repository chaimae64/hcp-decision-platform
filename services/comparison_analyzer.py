import pandas as pd


class ComparisonAnalyzer:

    # =====================================================
    # Colonnes numériques
    # =====================================================

    @staticmethod
    def numeric_columns(df):

        return list(
            df.select_dtypes(include="number").columns
        )

    # =====================================================
    # Colonnes textuelles
    # =====================================================

    @staticmethod
    def text_columns(df):

        return list(
            df.select_dtypes(exclude="number").columns
        )

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
    # Impact métier
    # =====================================================

    @staticmethod
    def business_impact(
        dimension,
        leader,
        severity
    ):

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
    # Niveau de priorité
    # =====================================================

    @staticmethod
    def priority(severity):

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
    # Recommandation stratégique
    # =====================================================

    @staticmethod
    def recommendation(
        dimension,
        leader,
        severity
    ):

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
    # Interprétation intelligente
    # =====================================================

    @staticmethod
    def interpretation(
        grouped,
        difference,
        severity
    ):

        leader = grouped.index[0]
        leader_value = grouped.iloc[0]

        last = grouped.index[-1]
        last_value = grouped.iloc[-1]

        text = (
            f"La catégorie '{leader}' présente "
            f"la valeur moyenne la plus élevée "
            f"({leader_value:.2f}). "
        )

        text += (
            f"La catégorie '{last}' présente "
            f"la valeur moyenne la plus faible "
            f"({last_value:.2f}). "
        )

        if difference is not None:

            text += (
                f"L'écart entre les deux catégories "
                f"est de {difference:.2f}%. "
            )

        text += (
            f"Le niveau de gravité est "
            f"considéré comme '{severity}'."
        )

        return text

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df):

        results = {}

        dimensions = (
            ComparisonAnalyzer.text_columns(df)
        )

        indicators = (
            ComparisonAnalyzer.numeric_columns(df)
        )

        for dimension in dimensions:

            results[dimension] = {}

            for indicator in indicators:

                try:

                    grouped = ComparisonAnalyzer.compare(
                        df,
                        dimension,
                        indicator
                    )

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

                        "priority":

                            ComparisonAnalyzer.priority(
                                severity
                            ),

                        "dominance":

                            ComparisonAnalyzer.dominance(
                                diff
                            ),

                        "business_impact":

                            ComparisonAnalyzer.business_impact(

                                dimension,

                                leader,

                                severity

                            ),

                        "recommendation":

                            ComparisonAnalyzer.recommendation(

                                dimension,

                                leader,

                                severity

                            ),

                        "interpretation":

                            ComparisonAnalyzer.interpretation(

                                grouped,

                                diff,

                                severity

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