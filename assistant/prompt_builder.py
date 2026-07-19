class PromptBuilder:

    """
    Prompt Builder V2

    Construit un prompt professionnel destiné
    au modèle de langage.
    """

    # =====================================================
    # System Prompt
    # =====================================================

    @staticmethod
    def system_prompt():

        return """
Tu es un expert en analyse statistique, Business Intelligence
et aide à la décision du Haut-Commissariat au Plan (HCP).

Tu assistes les décideurs dans l'interprétation
des indicateurs statistiques.

Tu dois fournir des réponses professionnelles,
objectives et compréhensibles.
"""

    # =====================================================
    # Règles
    # =====================================================

    @staticmethod
    def rules():

        return """
RÈGLES :

- Utilise uniquement les informations présentes
  dans le contexte.

- N'invente jamais de données.

- Si une information est absente,
  indique clairement qu'elle n'est
  pas disponible.

- Justifie toujours tes conclusions.

- Sois synthétique.

- Utilise un vocabulaire professionnel.

- Les recommandations doivent être
  réalistes et exploitables.

- Réponds toujours en français.
"""

    # =====================================================
    # Structure de réponse
    # =====================================================

    @staticmethod
    def response_template():

        return """
Structure obligatoirement la réponse ainsi :

## Résumé

...

## Analyse

...

## Interprétation

...

## Recommandations

...
"""

    # =====================================================
    # Contexte
    # =====================================================

    @staticmethod
    def context(context):

        return f"""
CONTEXTE

--------------------------

{context}
"""

    # =====================================================
    # Question
    # =====================================================

    @staticmethod
    def question(question):

        return f"""
QUESTION

--------------------------

{question}
"""

    # =====================================================
    # Prompt final
    # =====================================================

    @staticmethod
    def build(context, question):

        prompt = f"""

==============================
SYSTEM
==============================

{PromptBuilder.system_prompt()}

==============================
RÈGLES
==============================

{PromptBuilder.rules()}

==============================
FORMAT DE RÉPONSE
==============================

{PromptBuilder.response_template()}

==============================
CONTEXTE
==============================

{PromptBuilder.context(context)}

==============================
QUESTION
==============================

{PromptBuilder.question(question)}

"""

        return prompt.strip()

    # =====================================================
    # Debug
    # =====================================================

    @staticmethod
    def debug_prompt(context, question):

        print(

            PromptBuilder.build(

                context,

                question

            )

        )