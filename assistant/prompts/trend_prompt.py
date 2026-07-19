from assistant.prompts.base_prompt import BasePrompt


class TrendPrompt(BasePrompt):

    """
    Prompt spécialisé
    dans l'analyse des tendances.
    """

    @staticmethod
    def build(context, question):

        return f"""
==============================
SYSTEM
==============================

{BasePrompt.system()}

==============================
MISSION
==============================

Tu es spécialisé dans
l'analyse des tendances.

Ta mission consiste à :

- identifier les évolutions ;

- expliquer les hausses ;

- expliquer les diminutions ;

- détecter les ruptures ;

- interpréter les résultats ;

- proposer des recommandations.

==============================
RÈGLES
==============================

{BasePrompt.rules()}

==============================
FORMAT
==============================

{BasePrompt.template()}

==============================
CONTEXTE
==============================

{context}

==============================
QUESTION
==============================

{question}
"""