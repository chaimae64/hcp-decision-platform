from assistant.prompts.base_prompt import BasePrompt


class AnomalyPrompt(BasePrompt):

    @staticmethod
    def build(context, question):

        return f"""
{BasePrompt.system()}

MISSION :
Tu détectes uniquement les anomalies présentes dans les données.

{BasePrompt.rules()}

Instructions spécifiques :

- Signale les valeurs aberrantes.
- Signale les données manquantes.
- Signale les incohérences.
- Ne cherche pas à expliquer les causes.

{BasePrompt.template()}

CONTEXTE :

{context}

QUESTION :

{question}
"""