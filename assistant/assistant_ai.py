from assistant.decision_router import DecisionRouter
from assistant.context_builder import ContextBuilder
from assistant.prompts.prompt_builder import PromptBuilder
from assistant.llm_service import LLMService
from assistant.response_formatter import ResponseFormatter
from assistant.question_context_filter import QuestionContextFilter
from assistant.interpreters.statistics_interpreter import StatisticsInterpreter
from assistant.interpreters.trend_interpreter import TrendInterpreter
from assistant.interpreters.comparison_interpreter import ComparisonInterpreter


from services.decision_engine import DecisionEngine


class AssistantAI:

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def ask(question, dataframe):

        try:

            route = DecisionRouter.route(question)

            dimensions = list(

                dataframe.select_dtypes(
                    include=["object", "category"]
                ).columns

            )

            route["dimension"] = DecisionRouter.detect_dimension(

                question,

                dimensions

            )

            if DecisionRouter.detect_implicit_comparison(
                question,
                route["dimension"]
            ):
                route["intent"] = "comparison"
                route["modules"] = ["comparison"]
                route["response_type"] = "comparison"

            print("Route :", route)
            analysis = DecisionEngine.analyze_by_intent(
                dataframe,
                route["intent"]
            )
            if route["intent"] == "statistics":

                analysis["interpreted_statistics"] = (
                    StatisticsInterpreter.interpret(
                        analysis.get("descriptive_statistics", {})
                    )
                )
            if route["intent"] == "trend":

                analysis["interpreted_trends"] = (
                    TrendInterpreter.interpret(
                        analysis
                    )
                )

            if route["intent"] == "comparison":

                analysis["interpreted_comparison"] = (
                    ComparisonInterpreter.interpret(
                        analysis
                    )
                )


            if route["intent"] == "statistics":
                print("===== INTERPRETED =====")
                print(analysis["interpreted_statistics"])
                
            print("Avant LLM")

            # =====================================================
            # Filtrage des statistiques
            # =====================================================

            filtered_statistics = QuestionContextFilter.filter_statistics(
                analysis.get("descriptive_statistics", {}),
                question
            )

            analysis["descriptive_statistics"] = filtered_statistics

            filtered_interpreted = QuestionContextFilter.filter_statistics(
                analysis.get("interpreted_statistics", {}),
                question
            )

            analysis["interpreted_statistics"] = filtered_interpreted

            print("===== FILTERED STATISTICS =====")
            print(filtered_statistics)

            # =====================================================
            # Construction du contexte
            # =====================================================

            prepared_context = ContextBuilder.prepare(
                analysis,
                route
            )

            print("===== FILTERED STATISTICS =====")
            print(filtered_statistics)

            print("===== CONTEXTE ENVOYÉ AU LLM =====")
            print(prepared_context)


            prompt = PromptBuilder.build(
                intent=route["intent"],

                context=prepared_context,

                question=question
            )
            print("\n===== PROMPT ENVOYÉ AU LLM =====")
            print(prompt)
            print("================================\n")

            llm_response = LLMService.generate(
                prompt
            )
            print("Après LLM")

            print("===== ANALYSIS =====")
            print(analysis)

            print("===== LLM =====")
            print(llm_response["answer"])

            return ResponseFormatter.success(
                question=question,
                analysis=analysis,
                statistics=filtered_statistics,
                llm_answer=llm_response["answer"],
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
    