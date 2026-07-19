from assistant.prompts.base_prompt import BasePrompt


class StatisticsPrompt(BasePrompt):

    @staticmethod
    def build(context, question):

        return f"""
{BasePrompt.system()}

MISSION :
Tu analyses uniquement les statistiques descriptives.

{BasePrompt.rules()}

Instructions spécifiques :

- Décris les moyennes.
- Décris les minimums.
- Décris les maximums.
- Décris les distributions.
- Ne fais aucune hypothèse.

{BasePrompt.template()}

CONTEXTE :

{context}

QUESTION :

{question}
"""