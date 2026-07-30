
from datetime import datetime


class ResponseFormatter:

    # =====================================================
    # Réponse réussie
    # =====================================================

    @staticmethod
    def success(

            question,
            analysis,
            statistics,
            llm_answer,
            route,
            execution_time=None,
            model=None

    ):

        return {

            "status": "success",

            "question": question,

            "intent": route["intent"],

            "response_type": route["response_type"],

            "modules_used": route["modules"],

            "data": analysis,

            "statistics": statistics,


            "analysis": llm_answer,

            "execution_time": execution_time,

            "model": model,

            "timestamp":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                )

        }

    # =====================================================
    # Réponse d'erreur
    # =====================================================

    @staticmethod
    def error(

            question,
            error

    ):

        return {

            "status": "error",

            "question": question,

            "message": str(error),

            "timestamp":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                )

        }

    # =====================================================
    # Réponse vide
    # =====================================================

    @staticmethod
    def empty(question):

        return {

            "status": "empty",

            "question": question,

            "message":

                "Aucune réponse générée.",

            "timestamp":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                )

        }

    # =====================================================
    # Informations de debug
    # =====================================================

    @staticmethod
    def debug(

            route,
            prompt_length

    ):

        return {

            "intent":

                route["intent"],

            "response_type":

                route["response_type"],

            "modules":

                route["modules"],

            "prompt_length":

                prompt_length

        }
    

    @staticmethod
    def statistics(interpreted_statistics):

        if not interpreted_statistics:
            return "Aucune interprétation statistique disponible."

        year = next(iter(interpreted_statistics))
        summary = interpreted_statistics[year].get("summary", "")

        return f"En {year}, {summary}"