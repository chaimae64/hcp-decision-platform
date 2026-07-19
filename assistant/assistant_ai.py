from assistant.decision_router import DecisionRouter
from assistant.context_builder import ContextBuilder
from assistant.prompts.prompt_builder import PromptBuilder
from assistant.llm_service import LLMService
from assistant.response_formatter import ResponseFormatter

from services.decision_engine import DecisionEngine


class AssistantAI:

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def ask(question, dataframe):

        try:

            route = DecisionRouter.route(question)

            analysis = DecisionEngine.analyze(dataframe)

            prepared_context = ContextBuilder.prepare(
                analysis,
                route
            )

            prompt = PromptBuilder.build(
                intent=route["intent"],

                context=prepared_context,

                question=question
            )

            llm_response = LLMService.generate(
                prompt
            )

            return ResponseFormatter.success(
                question=question,
                answer=llm_response["answer"],
                route=route,
                execution_time=llm_response["execution_time"],
                model=llm_response["model"]
            )

        except Exception as error:

            return ResponseFormatter.error(
                question,
                error
            )

    # =====================================================
    # Informations
    # =====================================================

    @staticmethod
    def info():

        return {

            "assistant":

                "Decision AI Assistant",

            "version":

                "1.0",

            "provider":

                LLMService.info()

        }
    