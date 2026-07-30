from assistant.prompts.base_prompt import BasePrompt


class StatisticsPrompt(BasePrompt):

    @staticmethod
    def build(context, question):

        return f"""
{BasePrompt.system()}

MISSION

Le contexte contient déjà les interprétations statistiques calculées par le moteur Python.

Ces interprétations sont fiables et suffisantes pour répondre à la question.

Ton rôle n'est pas de refaire une analyse statistique.

Tu dois uniquement reformuler les interprétations présentes dans le contexte avec un langage clair et naturel destiné à un décideur.

Consignes spécifiques

- Utilise uniquement les informations présentes dans le contexte.
- Ne réalise aucun calcul.
- Ne modifie pas les interprétations fournies.
- N'ajoute aucune explication, cause ou conséquence.
- Ne compare pas plusieurs années sauf si la question le demande.
- Si un champ `summary` est présent, base principalement ta réponse sur ce résumé.
- Si une information n'est pas présente dans le contexte, ne la mentionne pas.
- Termine par une conclusion concise.

{BasePrompt.rules()}

{BasePrompt.template()}

CONTEXTE

{context}

QUESTION

{question}
"""