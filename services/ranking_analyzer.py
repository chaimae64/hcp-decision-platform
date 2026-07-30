import pandas as pd

from services.dataset_profiler import DatasetProfiler


class RankingAnalyzer:

    # =====================================================
    # Classement
    # =====================================================

    @staticmethod
    def rank_dimension(df, dimension, indicator):

        return (

            df

            .groupby(dimension)[indicator]

            .mean()

            .sort_values(ascending=False)

        )

    # =====================================================
    # Leader
    # =====================================================

    @staticmethod
    def leader(ranking):

        return {

            "name": ranking.index[0],

            "value": round(ranking.iloc[0], 2)

        }

    # =====================================================
    # Dernier
    # =====================================================

    @staticmethod
    def last(ranking):

        return {

            "name": ranking.index[-1],

            "value": round(ranking.iloc[-1], 2)

        }

    # =====================================================
    # Top N
    # =====================================================

    @staticmethod
    def top(ranking, n=5):

        return (

            ranking

            .head(n)

            .round(2)

            .to_dict()

        )

    # =====================================================
    # Bottom N
    # =====================================================

    @staticmethod
    def bottom(ranking, n=5):

        return (

            ranking

            .tail(n)

            .round(2)

            .to_dict()

        )

    # =====================================================
    # Analyse complète
    # =====================================================

    @staticmethod
    def analyze(df: pd.DataFrame):

        profiler = DatasetProfiler(df)

        results = {}

        for dimension in profiler.categorical_columns:

            results[dimension] = {}

            for indicator in profiler.numeric_columns:

                try:

                    ranking = RankingAnalyzer.rank_dimension(

                        df,

                        dimension,

                        indicator

                    )

                    results[dimension][indicator] = {

                        "leader":

                            RankingAnalyzer.leader(

                                ranking

                            ),

                        "last":

                            RankingAnalyzer.last(

                                ranking

                            ),

                        "top5":

                            RankingAnalyzer.top(

                                ranking

                            ),

                        "bottom5":

                            RankingAnalyzer.bottom(

                                ranking

                            ),

                        "categories_count":

                            len(ranking),

                        "ranking":

                            ranking.round(2).to_dict()

                    }

                except Exception:

                    continue

        return results
    