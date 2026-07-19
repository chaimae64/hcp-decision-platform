from assistant.prompts.base_prompt import BasePrompt


class RankingPrompt(BasePrompt):

    @staticmethod
    def build(context, question):

        return f"""
{BasePrompt.system()}

MISSION :
Tu identifies les meilleurs et les moins bons résultats selon les données disponibles.

{BasePrompt.rules()}

Instructions spécifiques :

- Classe les résultats.
- Affiche le Top et le Bottom.
- Mentionne les valeurs importantes.
- N'interprète pas les causes.

{BasePrompt.template()}

CONTEXTE :

{context}

QUESTION :

{question}
"""