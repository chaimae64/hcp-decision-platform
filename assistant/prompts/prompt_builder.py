from assistant.prompts.trend_prompt import TrendPrompt
from assistant.prompts.comparison_prompt import ComparisonPrompt
from assistant.prompts.ranking_prompt import RankingPrompt
from assistant.prompts.statistics_prompt import StatisticsPrompt
from assistant.prompts.kpi_prompt import KPIPrompt
from assistant.prompts.anomaly_prompt import AnomalyPrompt


class PromptBuilder:

    PROMPTS = {
        "trend": TrendPrompt,
        "comparison": ComparisonPrompt,
        "ranking": RankingPrompt,
        "statistics": StatisticsPrompt,
        "kpi": KPIPrompt,
        "anomaly": AnomalyPrompt,
    }

    @staticmethod
    def build(intent, context, question):

        prompt_class = PromptBuilder.PROMPTS.get(intent, TrendPrompt)

        return prompt_class.build(
            context=context,
            question=question
        )