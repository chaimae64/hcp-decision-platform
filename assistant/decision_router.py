import re
import unicodedata

class DecisionRouter:
    """
    Analyse la question utilisateur afin de déterminer :

    - l'intention
    - les filtres détectés
    - les entités métier
    - les modules d'analyse nécessaires
    """

    ROUTES = {

        "statistics": {
            "keywords": [
                "décris", "décrire", "description",
                "statistique", "statistiques",
                "dataset", "colonnes", "variables",
                "structure", "combien", "nombre"
            ],
            "modules": ["statistics"],
            "response_type": "statistics"
        },

        "trend": {
            "keywords": [
                "tendance",
                "évolution",
                "augment",
                "augmentation",
                "hausse",
                "baisse",
                "diminue",
                "croissance",
                "décroissance",
                "progression"
            ],
            "modules": ["trend"],
            "response_type": "analysis"
        },

        "comparison": {
            "keywords": [
                "compar",
                "compare",
                "comparaison",

                "différence",
                "différences",

                "écart",
                "écarts",

                "disparité",
                "disparités",

                "versus",
                "vs",

                "entre"
            ],
            "modules": ["comparison"],
            "response_type": "comparison"
        },

        "ranking": {
            "keywords": [
                "top",
                "classement",
                "meilleur",
                "meilleurs",
                "pire",
                "pires",
                "plus élevé",
                "plus faible"
            ],
            "modules": ["ranking"],
            "response_type": "ranking"
        },

        "anomaly": {
            "keywords": [
                "anomal",
                "erreur",
                "qualité",
                "fiable",
                "manquant",
                "doublon",
                "incohérence",
                "outlier"
            ],
            "modules": ["anomalies"],
            "response_type": "anomaly"
        },

        "kpi": {
            "keywords": [
                "kpi",
                "indicateur",
                "performance",
                "moyenne",
                "minimum",
                "maximum",
                "médiane",
                "variance",
                "écart-type"
            ],
            "modules": ["kpis"],
            "response_type": "kpi"
        },

        "summary": {
            "keywords": [
                "résumé",
                "resume",
                "synthèse",
                "conclusion"
            ],
            "modules": ["summary"],
            "response_type": "summary"
        }

    }
    DIMENSION_ALIASES = {

        "Région": [
            "région",
            "region",
            "province",
            "territoire",
            "localité"
        ],

        "Sexe": [
            "sexe",
            "genre",
            "homme",
            "hommes",
            "femme",
            "femmes",
            "masculin",
            "féminin"
        ],

        "Milieu": [
            "milieu",
            "zone",
            "urbain",
            "rural",
            "campagne",
            "ville"
        ]

    }

    DEFAULT_ROUTE = {

        "intent": "statistics",

        "modules": ["statistics"],

        "response_type": "statistics"

    }

    ####################################################################
    @staticmethod
    def normalize(text):

        text = text.lower()

        return "".join(

            c

            for c in unicodedata.normalize("NFD", text)

            if unicodedata.category(c) != "Mn"

        )

    @staticmethod
    def detect_intent(question):

        q = DecisionRouter.normalize(question)
        trend_keywords = [
            "tendance",
            "évolution",
            "evolution",
            "hausse",
            "baisse",
            "augmentation",
            "diminution",
            "croissance",
            "progression",
            "régression",
            "stable",
            "volatilité",
            "évolue",
            "evolue",
            "évoluent",
            "evoluent",
            "fluctuation",
            "fluctuations",
            "volatilité",
            "variation",
            "variations",
            "rupture"
        ]

        if any(keyword in q for keyword in trend_keywords):
            route = DecisionRouter.ROUTES["trend"]
            return {
                "intent": "trend",
                "modules": route["modules"],
                "response_type": route["response_type"]
            }

        scores = {}

        for intent, config in DecisionRouter.ROUTES.items():

            score = 0

            for keyword in config["keywords"]:

                if keyword in q:
                    score += 1

            scores[intent] = score

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            return DecisionRouter.DEFAULT_ROUTE

        route = DecisionRouter.ROUTES[best]

        return {

            "intent": best,

            "modules": route["modules"],

            "response_type": route["response_type"]

        }

    ####################################################################

    @staticmethod
    def extract_years(question):

        years = re.findall(r"\b(19\d{2}|20\d{2})\b", question)

        return list(set(years))

    ####################################################################

    @staticmethod
    def extract_gender(question):

        q = question.lower()

        genders = []

        if "homme" in q or "hommes" in q:
            genders.append("Hommes")

        if "femme" in q or "femmes" in q:
            genders.append("Femmes")

        return genders

    ####################################################################

    @staticmethod
    def extract_environment(question):

        q = question.lower()

        env = []

        if "urbain" in q:
            env.append("Urbain")

        if "rural" in q:
            env.append("Rural")

        return env

    ####################################################################

    @staticmethod
    def detect_metrics(question):

        q = question.lower()

        metrics = []

        keywords = [

            "chômage",
            "emploi",
            "population",
            "inflation",
            "salaire",
            "revenu",
            "croissance"

        ]

        for metric in keywords:

            if metric in q:
                metrics.append(metric)

        return metrics

    ####################################################################

    @staticmethod
    def detect_operations(question):

        q = question.lower()

        operations = []

        if "moyenne" in q:
            operations.append("mean")

        if "maximum" in q or "max" in q:
            operations.append("max")

        if "minimum" in q or "min" in q:
            operations.append("min")

        if "somme" in q:
            operations.append("sum")

        if "compte" in q or "nombre" in q:
            operations.append("count")

        return operations

    @staticmethod
    def detect_implicit_comparison(question, dimension):

        q = DecisionRouter.normalize(question)

        comparators = [

            "plus",

            "moins",

            "meilleur",

            "meilleurs",

            "pire",

            "pires"

        ]

        targets = [

            "touché",

            "touchée",

            "touchés",

            "touchées",

            "concerné",

            "concernée",

            "élevé",

            "élevée",

            "faible",

            "important",

            "importante"

        ]


        if dimension is None:

            return False

        has_comparator = any(
            DecisionRouter.normalize(word) in q
            for word in comparators
        )

        has_target = any(
            DecisionRouter.normalize(word) in q
            for word in targets
        )


        return (

            dimension is not None

            and

            has_comparator

            and

            has_target

        )

    ####################################################################

    @staticmethod
    def route(question):

        route = DecisionRouter.detect_intent(question)

        route["question"] = question

        route["years"] = DecisionRouter.extract_years(question)

        route["gender"] = DecisionRouter.extract_gender(question)

        route["environment"] = DecisionRouter.extract_environment(question)

        route["metrics"] = DecisionRouter.detect_metrics(question)

        route["operations"] = DecisionRouter.detect_operations(question)

        route["needs_llm"] = True

        route["needs_statistics"] = True

        return route


    @staticmethod
    def detect_dimension(question, dimensions):

        q = DecisionRouter.normalize(question)

        for dimension in dimensions:

            # recherche directe

            if DecisionRouter.normalize(dimension) in q:

                return dimension

            # recherche par alias

            aliases = DecisionRouter.DIMENSION_ALIASES.get(
                dimension,
                []
            )

            for alias in aliases:

                if DecisionRouter.normalize(alias) in q:

                    return dimension

        return None
