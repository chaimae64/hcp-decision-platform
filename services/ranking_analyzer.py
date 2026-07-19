import pandas as pd


class RankingAnalyzer:

    # --------------------------------------------------
    # Colonnes numériques
    # --------------------------------------------------

    @staticmethod
    def numeric_columns(df):

        return list(
            df.select_dtypes(include="number").columns
        )

    # --------------------------------------------------
    # Colonnes textuelles
    # --------------------------------------------------

    @staticmethod
    def text_columns(df):

        return list(
            df.select_dtypes(exclude="number").columns
        )

    # --------------------------------------------------
    # Classement d'une dimension
    # --------------------------------------------------

    @staticmethod
    def rank_dimension(
        df,
        dimension,
        indicator
    ):
        """
        Classe une dimension selon la moyenne
        d'un indicateur.
        """

        ranking = (
            df
            .groupby(dimension)[indicator]
            .mean()
            .sort_values(ascending=False)
        )

        return ranking

    # --------------------------------------------------
    # Top N
    # --------------------------------------------------

    @staticmethod
    def top(
        df,
        dimension,
        indicator,
        n=5
    ):

        ranking = RankingAnalyzer.rank_dimension(
            df,
            dimension,
            indicator
        )

        return (
            ranking
            .head(n)
            .round(2)
            .to_dict()
        )

    # --------------------------------------------------
    # Bottom N
    # --------------------------------------------------

    @staticmethod
    def bottom(
        df,
        dimension,
        indicator,
        n=5
    ):

        ranking = RankingAnalyzer.rank_dimension(
            df,
            dimension,
            indicator
        )

        return (
            ranking
            .tail(n)
            .round(2)
            .to_dict()
        )

    # --------------------------------------------------
    # Leader
    # --------------------------------------------------

    @staticmethod
    def leader(
        df,
        dimension,
        indicator
    ):

        ranking = RankingAnalyzer.rank_dimension(
            df,
            dimension,
            indicator
        )

        return {

            "name": ranking.index[0],

            "value": round(
                ranking.iloc[0],
                2
            )

        }

    # --------------------------------------------------
    # Dernier
    # --------------------------------------------------

    @staticmethod
    def last(
        df,
        dimension,
        indicator
    ):

        ranking = RankingAnalyzer.rank_dimension(
            df,
            dimension,
            indicator
        )

        return {

            "name": ranking.index[-1],

            "value": round(
                ranking.iloc[-1],
                2
            )

        }

    # --------------------------------------------------
    # Analyse complète
    # --------------------------------------------------

    @staticmethod
    def analyze(df):

        results = {}

        dimensions = RankingAnalyzer.text_columns(df)

        indicators = RankingAnalyzer.numeric_columns(df)

        for dimension in dimensions:

            results[dimension] = {}

            for indicator in indicators:

                try:

                    results[dimension][indicator] = {

                        "leader":

                            RankingAnalyzer.leader(
                                df,
                                dimension,
                                indicator
                            ),

                        "last":

                            RankingAnalyzer.last(
                                df,
                                dimension,
                                indicator
                            ),

                        "top5":

                            RankingAnalyzer.top(
                                df,
                                dimension,
                                indicator
                            ),

                        "bottom5":

                            RankingAnalyzer.bottom(
                                df,
                                dimension,
                                indicator
                            )

                    }

                except Exception:

                    pass

        return results