class StatisticsInterpreter:

    @staticmethod
    def interpret(statistics):

        if not statistics:
            return {}

        interpreted = {}

        for year, stats in statistics.items():

            interpreted[year] = {

                "dispersion":
                    StatisticsInterpreter.interpret_dispersion(
                        stats.get("coefficient_variation")
                    ),

                "homogeneite":
                    StatisticsInterpreter.interpret_homogeneity(
                        stats.get("coefficient_variation")
                    ),

                "distribution":
                    StatisticsInterpreter.interpret_skewness(
                        stats.get("skewness")
                    ),

                "forme_distribution":
                    StatisticsInterpreter.interpret_kurtosis(
                        stats.get("kurtosis")
                    ),

                "summary":
                    StatisticsInterpreter.build_summary(stats)

            }

        return interpreted

    # =====================================================
    # Dispersion
    # =====================================================

    @staticmethod
    def interpret_dispersion(cv):

        if cv is None:
            return None

        if cv < 15:
            return "faible"

        elif cv < 30:
            return "modérée"

        else:
            return "élevée"

    # =====================================================
    # Asymétrie
    # =====================================================

    @staticmethod
    def interpret_skewness(skewness):

        if skewness is None:
            return None

        if abs(skewness) < 0.5:
            return "quasi symétrique"

        elif skewness > 0:
            return "asymétrique à droite"

        else:
            return "asymétrique à gauche"

    # =====================================================
    # Kurtosis
    # =====================================================

    @staticmethod
    def interpret_kurtosis(kurtosis):

        if kurtosis is None:
            return None

        if kurtosis < -0.5:
            return "aplatie"

        elif kurtosis <= 0.5:
            return "proche d'une distribution normale"

        else:
            return "très concentrée"

    # =====================================================
    # Homogénéité
    # =====================================================

    @staticmethod
    def interpret_homogeneity(cv):

        if cv is None:
            return None

        if cv < 15:
            return "très homogène"

        elif cv < 30:
            return "assez homogène"

        else:
            return "hétérogène"

    # =====================================================
    # Variabilité
    # =====================================================

    @staticmethod
    def interpret_variability(std):

        if std is None:
            return None

        if std < 5:
            return "faible"

        elif std < 10:
            return "modérée"

        else:
            return "forte"
        
    @staticmethod
    def build_summary(stats):

        cv = stats.get("coefficient_variation")
        skewness = stats.get("skewness")
        kurtosis = stats.get("kurtosis")

        dispersion = StatisticsInterpreter.interpret_dispersion(cv)
        homogeneity = StatisticsInterpreter.interpret_homogeneity(cv)
        distribution = StatisticsInterpreter.interpret_skewness(skewness)
        shape = StatisticsInterpreter.interpret_kurtosis(kurtosis)

        summary = ""

        # Dispersion + homogénéité
        if dispersion == "élevée" and homogeneity == "hétérogène":
            summary = "Les données présentent une forte variabilité entre les observations."

        elif dispersion == "modérée" and homogeneity == "assez homogène":
            summary = "Les observations présentent une variabilité modérée."

        elif dispersion == "faible" and homogeneity == "très homogène":
            summary = "Les observations sont globalement homogènes."

        # Distribution
        if distribution == "quasi symétrique":
            summary += " La distribution reste globalement équilibrée."

        elif distribution == "asymétrique à droite":
            summary += " La distribution est orientée vers les valeurs les plus élevées."

        elif distribution == "asymétrique à gauche":
            summary += " La distribution est orientée vers les valeurs les plus faibles."

        # Forme
        if shape == "aplatie":
            summary += " Les valeurs sont relativement étalées."

        elif shape == "proche d'une distribution normale":
            summary += " La forme de la distribution est proche d'une distribution normale."

        elif shape == "très concentrée":
            summary += " Les valeurs sont fortement concentrées."

        return summary.strip()