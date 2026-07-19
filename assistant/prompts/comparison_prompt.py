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

- Compare uniquement les valeurs présentes.
- Mets en évidence les écarts importants.
- Identifie les régions, années ou catégories qui se distinguent.
- N'invente aucune explication.

{BasePrompt.template()}

CONTEXTE :

{context}

QUESTION :

{question}
"""