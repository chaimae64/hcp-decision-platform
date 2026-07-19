import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()


class LLMService:

    # =====================================================
    # Configuration
    # =====================================================

    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    MODEL = os.getenv(
        "OLLAMA_MODEL",
        "llama3.1:8b"
    )

    TIMEOUT = 300

    # =====================================================
    # Vérifier le serveur
    # =====================================================

    @staticmethod
    def server_available():

        try:

            response = requests.get(

                f"{LLMService.OLLAMA_URL}/api/tags",

                timeout=5

            )

            return response.status_code == 200

        except Exception:

            return False

    # =====================================================
    # Liste des modèles
    # =====================================================

    @staticmethod
    def installed_models():

        try:

            response = requests.get(

                f"{LLMService.OLLAMA_URL}/api/tags"

            )

            response.raise_for_status()

            data = response.json()

            return [

                model["name"]

                for model in data["models"]

            ]

        except Exception:

            return []

    # =====================================================
    # Vérifier le modèle
    # =====================================================

    @staticmethod
    def model_available():

        return (

            LLMService.MODEL

            in

            LLMService.installed_models()

        )

    # =====================================================
    # Génération
    # =====================================================

    @staticmethod
    def generate(prompt):

        if not LLMService.server_available():

            raise Exception(

                "Le serveur Ollama n'est pas démarré."

            )

        if not LLMService.model_available():

            raise Exception(

                f"Le modèle "

                f"{LLMService.MODEL}"

                f" n'est pas installé."

            )

        payload = {

            "model":

                LLMService.MODEL,

            "prompt":

                prompt,

            "stream":

                False

        }

        start = time.perf_counter()

        try:

            response = requests.post(

                f"{LLMService.OLLAMA_URL}/api/generate",

                json=payload,

                timeout=LLMService.TIMEOUT

            )

            response.raise_for_status()

            elapsed = round(

                time.perf_counter() - start,

                2

            )

            data = response.json()

            return {

                "answer":

                    data["response"],

                "execution_time":

                    elapsed,

                "model":

                    LLMService.MODEL

            }

        except Exception as error:

            raise Exception(

                f"Ollama : {error}"

            )

    # =====================================================
    # Informations
    # =====================================================

    @staticmethod
    def info():

        return {

            "provider":

                "Ollama",

            "url":

                LLMService.OLLAMA_URL,

            "model":

                LLMService.MODEL,

            "timeout":

                LLMService.TIMEOUT,

            "server":

                LLMService.server_available(),

            "installed_models":

                LLMService.installed_models()

        }