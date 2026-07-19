from datetime import datetime

from services.postgres import Postgres
from services.decision_engine import DecisionEngine


class ReportService:

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

            "summary": (
                f"Le dataset '{table}' a été analysé avec succès. "
                f"Le moteur d'aide à la décision a généré les indicateurs et recommandations."
            ),

            "recommendations": analysis["summary"]["recommendations"],

            "insights": analysis["summary"]["strengths"],

            "superset_url": None,
            
            "decision": analysis["decision"],

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

        return report