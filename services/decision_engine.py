
from services.statistics import Statistics
from services.trend_analyzer import TrendAnalyzer
from services.ranking_analyzer import RankingAnalyzer
from services.comparison_analyzer import ComparisonAnalyzer
from services.anomaly_detector import AnomalyDetector
from services.kpi_generator import KPIGenerator


class DecisionEngine:

    # =====================================================
    # Chargement des analyses
    # =====================================================

    @staticmethod
    def load_analysis(df):

        analysis = {

            "statistics":

                Statistics.analyze(df),

            "trends":

                TrendAnalyzer.analyze(df),

            "ranking":

                RankingAnalyzer.analyze(df),

            "comparison":

                ComparisonAnalyzer.analyze(df),

            "anomalies":

                AnomalyDetector.analyze(df),

            "kpis":

                KPIGenerator.analyze(df)

        }

        return analysis
    
    # =====================================================
    # Score Statistics
    # =====================================================

    @staticmethod
    def compute_statistics_score(analysis):

        statistics = analysis["statistics"]

        score = 100

        if len(statistics) == 0:

            return 0

        return score
    

    # =====================================================
    # Score Trends
    # =====================================================

    @staticmethod
    def compute_trend_score(analysis):

        trends = analysis["trends"]

        score = 100

        decreasing = 0

        stable = 0

        fluctuating = 0

        increasing = 0

        for indicator in trends.values():

            trend = indicator["trend"]

            if trend == "Croissante":

                increasing += 1

            elif trend == "Décroissante":

                decreasing += 1

            elif trend == "Stable":

                stable += 1

            else:

                fluctuating += 1

        score -= fluctuating * 10

        score -= increasing * 5

        return max(score, 0)
    

    # =====================================================
    # Score Ranking
    # =====================================================

    @staticmethod
    def compute_ranking_score(analysis):

        ranking = analysis["ranking"]

        if len(ranking) == 0:

            return 100

        return 90
    
    # =====================================================
    # Score KPI
    # =====================================================

    @staticmethod
    def compute_kpi_score(analysis):

        kpis = analysis["kpis"]

        if len(kpis) == 0:

            return 0

        return 90
    
    # =====================================================
    # Score Comparisons
    # =====================================================

    @staticmethod
    def compute_comparison_score(analysis):

        comparison = analysis["comparison"]

        score = 100

        critical = 0

        for dimension in comparison.values():

            for indicator in dimension.values():

                if indicator["severity"] == "Critique":

                    critical += 1

        score -= critical * 10

        return max(score, 0)
    
    # =====================================================
    # Score Qualité des données
    # =====================================================

    @staticmethod
    def compute_anomaly_score(analysis):

        return (

            analysis

            ["anomalies"]

            ["dataset_quality"]

            ["score"]

        )
    

    # =====================================================
    # Score décisionnel global
    # =====================================================

    @staticmethod
    def compute_decision_score(analysis):
        """
        Calcule un score global d'aide à la décision.

        Pondérations :

        Statistics      : 10 %
        Trends          : 20 %
        Comparison      : 20 %
        Ranking         : 10 %
        Anomalies       : 20 %
        KPI             : 20 %
        """

        statistics_score = DecisionEngine.compute_statistics_score(
            analysis
        )

        trend_score = DecisionEngine.compute_trend_score(
            analysis
        )

        comparison_score = DecisionEngine.compute_comparison_score(
            analysis
        )

        ranking_score = DecisionEngine.compute_ranking_score(
            analysis
        )

        anomaly_score = DecisionEngine.compute_anomaly_score(
            analysis
        )

        kpi_score = DecisionEngine.compute_kpi_score(
            analysis
        )

        decision_score = (

            statistics_score * 0.10 +

            trend_score * 0.20 +

            comparison_score * 0.20 +

            ranking_score * 0.10 +

            anomaly_score * 0.20 +

            kpi_score * 0.20

        )

        return round(decision_score, 2)

    # =====================================================
    # Niveau décisionnel
    # =====================================================

    @staticmethod
    def decision_level(score):

        if score >= 90:

            return "Excellent"

        elif score >= 80:

            return "Très bon"

        elif score >= 70:

            return "Bon"

        elif score >= 60:

            return "Acceptable"

        elif score >= 40:

            return "Faible"

        return "Critique"

    # =====================================================
    # Priorité d'intervention
    # =====================================================

    @staticmethod
    def compute_priority(score):

        if score >= 90:

            return "Surveillance"

        elif score >= 80:

            return "Faible"

        elif score >= 70:

            return "Normale"

        elif score >= 60:

            return "Importante"

        elif score >= 40:

            return "Élevée"

        return "Critique"

    # =====================================================
    # Résumé du score
    # =====================================================

    @staticmethod
    def decision_summary(analysis):

        score = DecisionEngine.compute_decision_score(
            analysis
        )

        return {

            "decision_score": score,

            "decision_level":
                DecisionEngine.decision_level(score),

            "priority":
                DecisionEngine.compute_priority(score),

            "statistics_score":
                DecisionEngine.compute_statistics_score(
                    analysis
                ),

            "trend_score":
                DecisionEngine.compute_trend_score(
                    analysis
                ),

            "comparison_score":
                DecisionEngine.compute_comparison_score(
                    analysis
                ),

            "ranking_score":
                DecisionEngine.compute_ranking_score(
                    analysis
                ),

            "anomaly_score":
                DecisionEngine.compute_anomaly_score(
                    analysis
                ),

            "kpi_score":
                DecisionEngine.compute_kpi_score(
                    analysis
                )

        }
    
    # =====================================================
    # Points forts
    # =====================================================

    @staticmethod
    def strengths(analysis):

        strengths = []

        if analysis["anomalies"]["dataset_quality"]["score"] >= 90:

            strengths.append(
                "Les données présentent une excellente qualité."
            )

        if len(

            analysis["anomalies"]["alerts"]

        ) == 0:

            strengths.append(
                "Aucune anomalie critique détectée."
            )

        trend_score = DecisionEngine.compute_trend_score(
            analysis
        )

        if trend_score >= 90:

            strengths.append(
                "Les indicateurs présentent une évolution stable."
            )

        if len(strengths) == 0:

            strengths.append(
                "Aucun point fort particulier identifié."
            )

        return strengths

    # =====================================================
    # Points faibles
    # =====================================================

    @staticmethod
    def weaknesses(analysis):

        weaknesses = []

        anomalies = analysis["anomalies"]

        if len(anomalies["critical_missing_columns"]) > 0:

            weaknesses.append(
                "Certaines colonnes présentent un taux élevé de valeurs manquantes."
            )

        if anomalies["greater_than_100"]["count"] > 0:

            weaknesses.append(
                "Des valeurs supérieures à 100 ont été détectées."
            )

        if anomalies["negative_values"]["count"] > 0:

            weaknesses.append(
                "Des valeurs négatives ont été détectées."
            )

        if DecisionEngine.compute_comparison_score(analysis) < 70:

            weaknesses.append(
                "Des disparités importantes existent entre les catégories."
            )

        if len(weaknesses) == 0:

            weaknesses.append(
                "Aucun point faible majeur détecté."
            )

        return weaknesses

    # =====================================================
    # Alertes
    # =====================================================

    @staticmethod
    def generate_alerts(analysis):

        return analysis["anomalies"]["alerts"]

    # =====================================================
    # Recommandations
    # =====================================================

    @staticmethod
    def generate_recommendations(analysis):

        recommendations = []

        recommendations.extend(

            analysis["anomalies"]["recommendations"]

        )

        if DecisionEngine.compute_trend_score(analysis) < 80:

            recommendations.append(

                "Surveiller l'évolution des indicateurs."

            )

        if DecisionEngine.compute_comparison_score(analysis) < 80:

            recommendations.append(

                "Analyser les disparités entre les catégories."

            )

        if len(recommendations) == 0:

            recommendations.append(

                "Aucune recommandation particulière."

            )

        return list(dict.fromkeys(recommendations))

    # =====================================================
    # Plan d'action
    # =====================================================

    @staticmethod
    def generate_action_plan(analysis):

        actions = []

        priority = DecisionEngine.compute_priority(

            DecisionEngine.compute_decision_score(

                analysis

            )

        )

        actions.append(

            f"Niveau de priorité : {priority}"

        )

        actions.extend(

            DecisionEngine.generate_recommendations(

                analysis

            )

        )

        return actions

    # =====================================================
    # Résumé exécutif
    # =====================================================

    @staticmethod
    def generate_summary(analysis):



        return {

            "strengths":

                DecisionEngine.strengths(
                    analysis
                ),

            "weaknesses":

                DecisionEngine.weaknesses(
                    analysis
                ),

            "alerts":

                DecisionEngine.generate_alerts(
                    analysis
                ),

            "recommendations":

                DecisionEngine.generate_recommendations(
                    analysis
                ),

            "action_plan":

                DecisionEngine.generate_action_plan(
                    analysis
                )

}


    # =====================================================
    # Analyse décisionnelle complète
    # =====================================================

    @staticmethod
    def analyze(df):
        """
        Lance l'ensemble du moteur d'aide à la décision.

        Cette méthode constitue le point d'entrée principal
        du DecisionEngine.

        Parameters
        ----------
        df : pandas.DataFrame

        Returns
        -------
        dict
        """

        # -----------------------------------------
        # Chargement des analyses
        # -----------------------------------------

        analysis = DecisionEngine.load_analysis(df)

        # -----------------------------------------
        # Résumé du score
        # -----------------------------------------

        decision = DecisionEngine.decision_summary(
            analysis
        )

        # -----------------------------------------
        # Synthèse
        # -----------------------------------------

        summary = DecisionEngine.generate_summary(
            analysis
        )

        # -----------------------------------------
        # Résultat final
        # -----------------------------------------

        return {

            "decision": decision,

            "summary": summary,

            "statistics":
                analysis["statistics"],

            "trends":
                analysis["trends"],

            "ranking":
                analysis["ranking"],

            "comparison":
                analysis["comparison"],

            "anomalies":
                analysis["anomalies"],

            "kpis":
                analysis["kpis"]

        }



