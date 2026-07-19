from assistant.prompts.base_prompt import BasePrompt


class KPIPrompt(BasePrompt):

    @staticmethod
    def build(context, question):

        return f"""
{BasePrompt.system()}

MISSION :
Tu présentes les KPI importants.

{BasePrompt.rules()}

Instructions spécifiques :

- Mets en avant les indicateurs clés.
- Présente les tendances principales.
- Souligne les alertes éventuelles.
- N'ajoute aucune information absente.

{BasePrompt.template()}

CONTEXTE :

{context}

QUESTION :

{question}
"""