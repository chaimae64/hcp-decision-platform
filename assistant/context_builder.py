import json

from services.decision_engine import DecisionEngine


class ContextBuilder:

    """
    Smart Context Builder

    Construit un contexte optimisé selon
    l'intention détectée par DecisionRouter.
    """

    MAX_ITEMS = 5

    # =====================================================
    # Limiter la taille d'un dictionnaire
    # =====================================================

    @staticmethod
    def limit_dict(data, limit=None):

        if limit is None:
            limit = ContextBuilder.MAX_ITEMS

        if not isinstance(data, dict):
            return data

        return dict(
            list(data.items())[:limit]
        )

    # =====================================================
    # Résumé décisionnel
    # =====================================================

    @staticmethod
    def decision_summary(analysis):

        return DecisionEngine.decision_summary(
            analysis
        )

    # =====================================================
    # Contexte Statistics
    # =====================================================

    @staticmethod
    def statistics_context(analysis):

        statistics = analysis["statistics"]

        return {

            "general_information":

                statistics["general_information"],

            "descriptive_statistics":

                ContextBuilder.limit_dict(

                    statistics["descriptive_statistics"]

                )

        }

    # =====================================================
    # Contexte Trends
    # =====================================================

    @staticmethod
    def trend_context(analysis):

        return ContextBuilder.limit_dict(

            analysis["trends"]

        )

    # =====================================================
    # Contexte Ranking
    # =====================================================

    @staticmethod
    def ranking_context(analysis):

        return ContextBuilder.limit_dict(

            analysis["ranking"]

        )

    # =====================================================
    # Contexte Comparison
    # =====================================================

    @staticmethod
    def comparison_context(analysis):

        return ContextBuilder.limit_dict(

            analysis["comparison"]

        )

    # =====================================================
    # Contexte KPI
    # =====================================================

    @staticmethod
    def kpi_context(analysis):

        kpis = analysis["kpis"]

        return {

            "dataset":

                kpis["dataset"],

            "decision":

                kpis["decision"],

            "business":

                {

                    "overall_average":

                        kpis["business"][
                            "overall_average"
                        ],

                    "best_indicator":

                        kpis["business"][
                            "best_indicator"
                        ],

                    "worst_indicator":

                        kpis["business"][
                            "worst_indicator"
                        ]

                }

        }

    # =====================================================
    # Contexte Anomalies
    # =====================================================

    @staticmethod
    def anomaly_context(analysis):

        anomalies = analysis["anomalies"]

        return {

            "dataset_quality":

                anomalies["dataset_quality"],

            "alerts":

                anomalies["alerts"][
                    :ContextBuilder.MAX_ITEMS
                ],

            "critical_missing_columns":

                anomalies[
                    "critical_missing_columns"
                ]

        }

    # =====================================================
    # Construction intelligente
    # =====================================================

    @staticmethod
    def prepare(analysis, route):

        intent = route["intent"]

        context = {

            "decision":

                ContextBuilder.decision_summary(
                    analysis
                )

        }

        if intent == "statistics":

            context["statistics"] = (

                ContextBuilder.statistics_context(
                    analysis
                )

            )

        elif intent == "trend":

            context["trends"] = (

                ContextBuilder.trend_context(
                    analysis
                )

            )

            context["comparison"] = (

                ContextBuilder.comparison_context(
                    analysis
                )

            )

            context["kpis"] = (

                ContextBuilder.kpi_context(
                    analysis
                )

            )

        elif intent == "comparison":

            context["comparison"] = (

                ContextBuilder.comparison_context(
                    analysis
                )

            )

            context["kpis"] = (

                ContextBuilder.kpi_context(
                    analysis
                )

            )

        elif intent == "ranking":

            context["ranking"] = (

                ContextBuilder.ranking_context(
                    analysis
                )

            )

        elif intent == "anomaly":

            context["anomalies"] = (

                ContextBuilder.anomaly_context(
                    analysis
                )

            )

        elif intent == "kpi":

            context["kpis"] = (

                ContextBuilder.kpi_context(
                    analysis
                )

            )

        else:

            context["statistics"] = (

                ContextBuilder.statistics_context(
                    analysis
                )

            )

            context["trends"] = (

                ContextBuilder.trend_context(
                    analysis
                )

            )

            context["comparison"] = (

                ContextBuilder.comparison_context(
                    analysis
                )

            )

            context["ranking"] = (

                ContextBuilder.ranking_context(
                    analysis
                )

            )

            context["kpis"] = (

                ContextBuilder.kpi_context(
                    analysis
                )

            )

            context["anomalies"] = (

                ContextBuilder.anomaly_context(
                    analysis
                )

            )

        return json.dumps(

            context,

            indent=4,

            ensure_ascii=False

        )