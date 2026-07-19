

class DecisionRouter:

    ROUTES = {

        "trend": {
            "keywords": [
                "tendance",
                "évolution",
                "augment",
                "diminue",
                "hausse",
                "baisse",
                "croissance",
                "décroissance"
            ],
            "modules": [
                "decision",
                "trends",
                "comparison",
                "kpis"
            ],
            "response_type": "analysis"
        },

        "comparison": {
            "keywords": [
                "compar",
                "différence",
                "écart",
                "région",
                "milieu",
                "sexe"
            ],
            "modules": [
                "decision",
                "comparison",
                "ranking"
            ],
            "response_type": "comparison"
        },

        "ranking": {
            "keywords": [
                "classement",
                "top",
                "meilleur",
                "pire"
            ],
            "modules": [
                "decision",
                "ranking"
            ],
            "response_type": "ranking"
        },

        "quality": {
            "keywords": [
                "anomal",
                "erreur",
                "qualité",
                "fiable",
                "manquant"
            ],
            "modules": [
                "decision",
                "anomalies"
            ],
            "response_type": "quality"
        },

        "recommendation": {
            "keywords": [
                "recommand",
                "solution",
                "conseil",
                "proposition"
            ],
            "modules": [
                "decision",
                "summary"
            ],
            "response_type": "recommendation"
        },

        "summary": {
            "keywords": [
                "résumé",
                "synthèse",
                "resume"
            ],
            "modules": [
                "decision",
                "summary"
            ],
            "response_type": "summary"
        }

    }

    DEFAULT_ROUTE = {

        "intent": "general",

        "modules": [

            "decision",
            "summary",
            "statistics",
            "trends",
            "comparison",
            "ranking",
            "anomalies",
            "kpis"

        ],

        "response_type": "general"

    }

    @staticmethod
    def route(question):

        question = question.lower()

        for intent, config in DecisionRouter.ROUTES.items():

            for keyword in config["keywords"]:

                if keyword in question:

                    return {

                        "intent": intent,

                        "modules": config["modules"],

                        "response_type": config["response_type"]

                    }

        return DecisionRouter.DEFAULT_ROUTE