import json


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
    # Contexte Statistics
    # =====================================================

    @staticmethod
    def statistics_context(analysis):

        return {

            "general_information": {

                "rows": analysis["general_information"]["rows"],

                "columns": analysis["general_information"]["columns"]

            },

            "statistics": ContextBuilder.limit_dict(

                analysis.get(
                    "interpreted_statistics",
                    {}
                )

            )

        }

    # =====================================================
    # Contexte Trends
    # =====================================================

    @staticmethod
    def trend_context(analysis):

        return ContextBuilder.limit_dict(

            analysis.get(
                "interpreted_trends",
                {}
            )

        )

    # =====================================================
    # Contexte Ranking
    # =====================================================

    @staticmethod
    def ranking_context(analysis):

        result = {}

        for indicator, values in list(analysis.items())[:ContextBuilder.MAX_ITEMS]:

            result[indicator] = {

                "top5": values["top5"],

                "bottom5": values["bottom5"]

            }

        return result

    # =====================================================
    # Contexte Comparison
    # =====================================================

    @staticmethod
    def comparison_context(analysis, dimension):

        comparison = analysis.get(
            "interpreted_comparison",
            {}
        )

        if dimension and dimension in comparison:

            return {
                dimension: comparison[dimension]
            }

        # aucune dimension trouvée
        # on renvoie tout

        return ContextBuilder.limit_dict(comparison)

    # =====================================================
    # Contexte KPI
    # =====================================================

    @staticmethod
    def kpi_context(analysis):

        kpis = analysis

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

        anomalies = analysis

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
    # Contexte Summary
    # =====================================================

    @staticmethod
    def summary_context(analysis):

        return {

            "decision": analysis["decision"],

            "summary": analysis["summary"],

            "kpis": {

                "dataset": analysis["kpis"]["dataset"],

                "business": {

                    "overall_average":
                        analysis["kpis"]["business"]["overall_average"],

                    "best_indicator":
                        analysis["kpis"]["business"]["best_indicator"],

                    "worst_indicator":
                        analysis["kpis"]["business"]["worst_indicator"]

                }

            }

        }

    # =====================================================
    # Construction intelligente
    # =====================================================

    @staticmethod
    def prepare(analysis, route):

        intent = route["intent"]

        context = {}

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

        elif intent == "comparison":

            context["comparison"] = (

                ContextBuilder.comparison_context(
                    analysis,
                    route["dimension"]
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
        
        elif intent == "summary":

            context["summary"] = (

                ContextBuilder.summary_context(
                    analysis
                )

            )

        else:

            context["result"] = analysis

        return json.dumps(

            context,

            indent=4,

            ensure_ascii=False

        )