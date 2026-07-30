from assistant.prompts.base_prompt import BasePrompt


class ComparisonPrompt(BasePrompt):

    @staticmethod
    def build(context, question):

        return f"""
{BasePrompt.system()}

MISSION :
Tu compares les indicateurs statistiques présents dans les données.

{BasePrompt.rules()}

Instructions spécifiques :

- Utilise uniquement les informations présentes dans le contexte.
- Compare les catégories présentes.
- Mets en évidence les écarts importants.
- Identifie la catégorie dominante.
- Appuie-toi sur le résumé fourni si disponible.
- N'invente aucune explication qui ne figure pas dans le contexte.

{BasePrompt.template()}

CONTEXTE :

{context}

QUESTION :

{question}
"""