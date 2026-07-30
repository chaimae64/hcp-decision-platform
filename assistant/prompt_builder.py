class PromptBuilder:

    """
    Prompt Builder V4
    Optimisé pour l'assistant décisionnel HCP.
    """

    # =====================================================
    # SYSTEM
    # =====================================================

    @staticmethod
    def system_prompt():

        return """
    Tu es un assistant intelligent d'aide à la décision du Haut-Commissariat au Plan (HCP).

    Les analyses statistiques sont déjà réalisées par le moteur Python.

    Le contexte contient uniquement des résultats fiables produits par ce moteur.

    Ton rôle n'est PAS de refaire une analyse statistique.

    Ton rôle est uniquement de reformuler les interprétations fournies afin qu'elles soient facilement compréhensibles par un décideur.

    Tu dois utiliser exclusivement les informations présentes dans le contexte.

    Tu ne dois jamais :

    - inventer une explication ;
    - inventer une cause ;
    - inventer une conséquence ;
    - inventer une comparaison ;
    - ajouter une tendance absente ;
    - compléter les informations du contexte.

    Tu reformules uniquement ce qui est fourni.

    Réponds toujours en français.

    Écris un texte naturel, professionnel et concis.

    N'utilise jamais Markdown.
    """.strip()
    # =====================================================
    # OBJECTIF
    # =====================================================

    @staticmethod
    def intent_instruction(intent):

        instructions = {

            "summary":
            """
Fais un résumé global du jeu de données.

Présente :
- les informations importantes ;
- les tendances principales ;
- les éventuels points remarquables ;
- une conclusion.
""",

           "statistics": """
            Le contexte contient déjà les interprétations statistiques.

            Ces interprétations ont été calculées automatiquement par le moteur Python.

            Ne réalise aucun calcul.

            Ne modifie pas ces interprétations.

            Ne cherche pas à en déduire d'autres informations.

            Présente simplement les principaux constats dans un langage clair destiné à un décideur.

            Ne compare jamais avec d'autres années sauf si la question le demande explicitement.

            Ne dépasse pas deux courts paragraphes.
            """

        }

        return instructions.get(

            intent,

            "Analyse les informations du contexte et réponds de manière concise."

        )

    # =====================================================
    # FORMAT
    # =====================================================

    @staticmethod
    def response_format():

        return """
    La réponse doit être :

    - claire ;
    - concise ;
    - rédigée sous forme de texte naturel ;
    - adaptée à un décideur.

    N'utilise ni titres, ni listes, ni Markdown.
    """.strip()

    # =====================================================
    # CONTEXTE
    # =====================================================

    @staticmethod
    def context(context):

        return f"""
CONTEXTE

{context}
""".strip()

    # =====================================================
    # QUESTION
    # =====================================================

    @staticmethod
    def question(question):

        return f"""
QUESTION

{question}
""".strip()

    # =====================================================
    # BUILD
    # =====================================================

    @staticmethod
    def build(intent, context, question):

        return f"""
    {PromptBuilder.system_prompt()}

    OBJECTIF

    {PromptBuilder.intent_instruction(intent)}

    FORMAT

    {PromptBuilder.response_format()}

    CONTEXTE

    {context}

    QUESTION

    {question}

    Consignes supplémentaires :

    - Utilise uniquement les informations du contexte.
    - Reformule les interprétations fournies.
    - N'ajoute aucune explication absente du contexte.
    - Si une information n'apparaît pas explicitement dans le contexte, ne la mentionne pas.
    - Ne compare jamais plusieurs années sauf si la question le demande.
    - N'invente aucune justification.
    - Termine par une conclusion concise.
    """.strip()

    # =====================================================
    # DEBUG
    # =====================================================

    @staticmethod
    def debug_prompt(intent, context, question):

        print(

            PromptBuilder.build(

                intent,
                context,
                question

            )

        )