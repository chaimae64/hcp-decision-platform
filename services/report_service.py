from datetime import datetime

from services.postgres import Postgres
from services.decision_engine import DecisionEngine


class ReportService:
    @staticmethod
    def generate_summary(report, analysis):

        rows = report["rows"]
        columns = report["columns"]

        score = analysis["decision"]["decision_score"]
        level = analysis["decision"]["decision_level"]

        recommendations = len(
            analysis["summary"]["recommendations"]
        )

        strengths = len(
            analysis["summary"]["strengths"]
        )

        summary = (
            f"Le jeu de données contient {rows} observations "
            f"réparties sur {columns} variables. "
            f"L'analyse décisionnelle attribue un score de "
            f"{score}/100 correspondant au niveau "
            f"« {level} ». "
            f"{strengths} point(s) fort(s) et "
            f"{recommendations} recommandation(s) "
            f"ont été identifiés."
        )

        return summary

    @staticmethod
    def generate_trend_summary(trends):

        total = len(trends)

        increasing = 0
        decreasing = 0
        stable = 0
        fluctuating = 0
        breaks = 0

        for trend in trends.values():

            if trend["trend"] == "Croissante":
                increasing += 1

            elif trend["trend"] == "Décroissante":
                decreasing += 1

            elif trend["trend"] == "Stable":
                stable += 1

            else:
                fluctuating += 1

            if trend["trend_break"]:
                breaks += 1

        if breaks == 0:
            break_text = "Aucune rupture de tendance n'a été détectée."
        else:
            break_text = (
                f"{breaks} rupture(s) de tendance ont été détectées."
            )

        return {

            "total": total,

            "increasing": increasing,

            "decreasing": decreasing,

            "stable": stable,

            "fluctuating": fluctuating,

            "break_text": break_text

        }

    @staticmethod
    def generate(import_info):

        postgres = Postgres()
        

        table = import_info["table"]
        df = postgres.load_table(table)

        preview = postgres.preview(table)
        analysis = DecisionEngine.analyze(df)
        stats = postgres.statistics(table)

        report = {

            "table": table,

            "database": import_info["database"],

            "filename": import_info["filename"],

            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),

            "dataset": table,

            "rows": postgres.count_rows(table),

            "columns": postgres.count_columns(table),

            "numeric_columns": import_info["numeric_columns"],

            "text_columns": import_info["text_columns"],

            "missing_values": stats["missing_values"],

            "duplicates": stats["duplicates"],

            
            "recommendations": analysis["summary"]["recommendations"],

            "insights": analysis["summary"]["strengths"],

            "superset_url": None,
            
            "decision": analysis["decision"],

            "kpi_cards": {

                "score": analysis["decision"]["decision_score"],

                "level": analysis["decision"]["decision_level"],

                "priority": analysis["decision"]["priority"],

                "recommendations": len(
                    analysis["summary"]["recommendations"]
                )

            },

            "statistics": analysis["statistics"],

            "trends": analysis["trends"],

            "ranking": analysis["ranking"],

            "comparison": analysis["comparison"],

            "anomalies": analysis["anomalies"],

            "kpis": analysis["kpis"],

            "preview": {

                "columns": preview.columns.tolist(),

                "rows": preview.values.tolist()

            }

        }
        report["summary"] = ReportService.generate_summary(
            report,
            analysis
        )
        report["trend_summary"] = ReportService.generate_trend_summary(
            report["trends"]
        )

        return report