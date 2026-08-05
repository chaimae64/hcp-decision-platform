from collections import Counter


def detect_subject(table_name):
    """
    Détecte automatiquement le sujet à partir
    du nom de la table PostgreSQL.
    """

    table = table_name.lower()

    subjects = {

        "chomage": "le chômage",
        "emploi": "l'emploi",
        "population": "la population",
        "demographie": "la démographie",
        "naissance": "la natalité",
        "mortalite": "la mortalité",
        "inflation": "l'inflation",
        "prix": "les prix",
        "consommation": "la consommation",
        "education": "l'éducation",
        "enseignement": "l'éducation",
        "sante": "la santé",
        "revenu": "les revenus",
        "pauvrete": "la pauvreté",
        "recensement": "le recensement"

    }

    for keyword, subject in subjects.items():

        if keyword in table:

            return subject

    return "les indicateurs statistiques"


def generate_executive_summary(report):

    rows = report["rows"]
    columns = report["columns"]

    numeric = report["numeric_columns"]
    text = report["text_columns"]

    subject = detect_subject(report["table"])

    trends = report["trends"]
    recommendations = report["recommendations"]
    comparisons = report["comparison"]

    # =====================================================
    # Détermination de la tendance dominante
    # =====================================================

    trend_counter = Counter()

    for trend in trends.values():

        trend_counter[trend["trend"]] += 1

    dominant = None

    if trend_counter:

        dominant = trend_counter.most_common(1)[0][0]

    # =====================================================
    # Détection des dimensions analysées
    # =====================================================

    dimensions = [dimension.lower() for dimension in comparisons.keys()]

    detected = []

    if "région" in dimensions or "region" in dimensions:
        detected.append("les régions")

    if "sexe" in dimensions:
        detected.append("le sexe")

    if "milieu" in dimensions:
        detected.append("le milieu de résidence")

    if "âge" in dimensions or "age" in dimensions:
        detected.append("l'âge")

    if len(detected) == 0:

        dimension_text = ""

    elif len(detected) == 1:

        dimension_text = detected[0]

    elif len(detected) == 2:

        dimension_text = f"{detected[0]} et {detected[1]}"

    else:

        dimension_text = (
            ", ".join(detected[:-1])
            + " et "
            + detected[-1]
        )

    # =====================================================
    # Construction du résumé
    # =====================================================

    summary = (

        f"Le jeu de données analysé contient "
        f"{rows} observations réparties sur "
        f"{columns} variables, dont "
        f"{numeric} variables numériques et "
        f"{text} variables textuelles. "

    )

    summary += f"Cette analyse porte sur {subject}"

    if dimension_text:

        summary += f" selon {dimension_text}"

    summary += ". "

    # =====================================================
    # Interprétation des tendances
    # =====================================================

    if dominant == "Croissante":

        trend_text = (
            "une évolution globalement croissante"
        )

    elif dominant == "Décroissante":

        trend_text = (
            "une évolution majoritairement décroissante"
        )

    elif dominant == "Stable":

        trend_text = (
            "une évolution globalement stable"
        )

    else:

        trend_text = (
            "des tendances majoritairement fluctuantes"
        )

    summary += (
        f"L'analyse met principalement en évidence "
        f"{trend_text} entre les indicateurs étudiés "
        f"et a permis de générer "
        f"{len(recommendations)} recommandation"
        f"{'' if len(recommendations) == 1 else 's'} "
        f"destinée"
        f"{'' if len(recommendations) == 1 else 's'} "
        f"à accompagner la prise de décision. "
    )

    summary += (
        "Les résultats révèlent des disparités "
        "importantes entre les différentes catégories "
        "analysées, justifiant une étude approfondie "
        "afin d'éclairer la prise de décision."
    )

    return summary