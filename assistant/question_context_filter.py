import json
import re


class QuestionContextFilter:
    """
    Filtre le contexte en fonction de la question de l'utilisateur.

    Objectif :
    - Réduire la taille du contexte envoyé au LLM.
    - Conserver uniquement les informations pertinentes.
    """

    @staticmethod
    def filter(context_json, question, intent):
        """
        context_json : contexte généré par ContextBuilder (JSON string)
        question : question de l'utilisateur
        intent : intention détectée
        """

        # Conversion du JSON en dictionnaire
        context = json.loads(context_json)

        # Cas particulier : statistiques
        if intent == "statistics":

            # Recherche d'une année dans la question
            match = re.search(r"\b(2020|2021|2022|2023|2024|2025)\b", question)

            if match:

                year = match.group(1)

                stats = context.get("statistics", {})
                descriptive = stats.get("descriptive_statistics", {})

                if year in descriptive:

                    stats["descriptive_statistics"] = {
                        year: descriptive[year]
                    }

                    context["statistics"] = stats

        # Retour au format JSON
        return json.dumps(
            context,
            indent=4,
            ensure_ascii=False
        )
    
    @staticmethod
    def filter_statistics(statistics, question):
        """
        Filtre les statistiques descriptives selon l'année demandée
        dans la question de l'utilisateur.

        Si aucune année n'est trouvée ou si l'année n'existe pas
        dans les statistiques, toutes les statistiques sont retournées.
        """

        import re

        # Recherche d'une année à 4 chiffres
        match = re.search(r"\b\d{4}\b", question)

        # Aucune année trouvée
        if not match:
            return statistics

        year = match.group(0)

        # L'année existe dans les statistiques
        if year in statistics:
            return {
                year: statistics[year]
            }

        # L'année demandée n'existe pas dans le dataset
        return statistics
