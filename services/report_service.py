from datetime import datetime
import os
import json
import numpy as np

from services.postgres import Postgres
from services.decision_engine import DecisionEngine
from utils.summary_generator import generate_executive_summary


class ReportService:

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
    def generate_trend_interpretation(summary):

        total = summary["total"]

        fluctuating = summary["fluctuating"]

        increasing = summary["increasing"]

        decreasing = summary["decreasing"]

        stable = summary["stable"]

        text = ""

        # ==========================================
        # Tendance dominante
        # ==========================================

        if fluctuating >= total / 2:

            text += (
                "Les analyses de tendance mettent en évidence "
                "une prédominance de tendances fluctuantes "
                "sur l'ensemble des indicateurs étudiés. "
            )

        elif increasing >= total / 2:

            text += (
                "Les indicateurs présentent une évolution "
                "majoritairement croissante. "
            )

        elif decreasing >= total / 2:

            text += (
                "Les indicateurs présentent une évolution "
                "majoritairement décroissante. "
            )

        else:

            text += (
                "Les indicateurs étudiés présentent des "
                "comportements relativement stables. "
            )

        # ==========================================
        # Ruptures
        # ==========================================

        if "Aucune" in summary["break_text"]:

            text += (
                "Aucune rupture significative de tendance "
                "n'a été détectée."
            )

        else:

            text += (
                "Plusieurs ruptures de tendance ont été "
                "détectées, traduisant une évolution "
                "hétérogène des indicateurs au cours de la "
                "période étudiée."
            )

        return text



    @staticmethod
    def generate_insights(report, analysis):
        """
        Génère automatiquement les principaux
        enseignements issus de l'analyse.
        """

        insights = []

        # =====================================================
        # 1. Tendance générale
        # =====================================================

        trends = analysis["trends"]

        counts = {
            "Croissante": 0,
            "Décroissante": 0,
            "Stable": 0,
            "Fluctuante": 0
        }

        for trend in trends.values():

            if trend["trend"] in counts:

                counts[trend["trend"]] += 1

        dominant = max(counts, key=counts.get)

        texts = {

            "Croissante":
                "Les analyses de tendance mettent en évidence une évolution globalement croissante des indicateurs étudiés.",

            "Décroissante":
                "Les analyses de tendance mettent en évidence une évolution globalement décroissante des indicateurs étudiés.",

            "Stable":
                "Les analyses de tendance montrent une évolution globalement stable des indicateurs étudiés.",

            "Fluctuante":
                "Les analyses de tendance révèlent des évolutions fluctuantes sur la période étudiée."

        }

        insights.append(texts[dominant])

        # =====================================================
        # 2. Choisir automatiquement
        #    le dernier indicateur numérique
        # =====================================================

        indicators = list(analysis["trends"].keys())

        indicator = indicators[-1]

        # =====================================================
        # 3. Analyse des comparaisons
        # =====================================================

        comparisons = analysis["comparison"]

        severity_text = {

            "Faible": "une disparité faible",

            "Modérée": "une disparité modérée",

            "Importante": "une disparité importante",

            "Élevée": "une disparité élevée",

            "Critique": "une disparité très importante"

        }

        for dimension, values in comparisons.items():

            if indicator not in values:

                continue

            comparison = values[indicator]

            leader = comparison["leader"]

            last = comparison["last"]

            difference = comparison["relative_difference"]

            severity = comparison["severity"]

            sentence = (

                f"L'analyse comparative selon la dimension "

                f"« {dimension} » montre que la catégorie "

                f"« {leader['category']} » présente la valeur "

                f"moyenne la plus élevée ({leader['value']}), "

                f"contre {last['value']} pour "

                f"« {last['category']} »"

            )

            if difference is not None:

                sentence += (

                    f", soit un écart relatif de "

                    f"{difference} %, traduisant "

                    f"{severity_text.get(severity, 'une disparité significative')} "

                    f"entre les catégories comparées."

                )

            else:

                sentence += "."

            insights.append(sentence)

        # =====================================================
        # 4. Conclusion
        # =====================================================

        insights.append(
            "L'ensemble de ces analyses met en évidence les principaux écarts observés et fournit des éléments d'interprétation utiles pour l'analyse statistique et l'aide à la décision."
        )

        return insights


    @staticmethod
    def generate_recommendations(report, analysis):
        """
        Génère automatiquement des recommandations
        à partir des résultats de l'analyse.
        """

        recommendations = []

        # =====================================================
        # Analyse des comparaisons
        # =====================================================

        indicators = list(analysis["trends"].keys())
        indicator = indicators[-1]

        comparisons = analysis["comparison"]

        critical_dimensions = []
        important_dimensions = []

        for dimension, values in comparisons.items():

            if indicator not in values:
                continue

            severity = values[indicator]["severity"]

            if severity in ["Critique", "Élevée"]:

                critical_dimensions.append(dimension)

            elif severity == "Importante":

                important_dimensions.append(dimension)

        # =====================================================
        # Recommandation liée aux comparaisons
        # =====================================================

        dimensions = critical_dimensions + important_dimensions

        if dimensions:

            if len(dimensions) == 1:

                text = dimensions[0]

            elif len(dimensions) == 2:

                text = f"{dimensions[0]} et {dimensions[1]}"

            else:

                text = (
                    ", ".join(dimensions[:-1])
                    + " et "
                    + dimensions[-1]
                )

            recommendations.append(

                f"Les analyses comparatives mettent en évidence des disparités significatives selon les dimensions « {text} ». Une étude approfondie des facteurs susceptibles d'expliquer ces écarts est recommandée afin d'améliorer leur interprétation."

            )

        # =====================================================
        # Analyse des tendances
        # =====================================================

        fluctuating = 0

        for trend in analysis["trends"].values():

            if trend["trend"] == "Fluctuante":

                fluctuating += 1

        if fluctuating >= len(analysis["trends"]) / 2:

            recommendations.append(

                "Les évolutions fluctuantes observées sur plusieurs indicateurs suggèrent de poursuivre le suivi des données afin d'évaluer leur stabilité et leur évolution dans le temps."

            )

        # =====================================================
        # Analyse des classements
        # =====================================================

        recommendations.append(

            "Les catégories présentant les valeurs les plus élevées peuvent faire l'objet d'analyses ciblées afin d'identifier les facteurs explicatifs et de définir les priorités d'action."

        )

        # =====================================================
        # Conclusion
        # =====================================================

        recommendations.append(

            "Les résultats obtenus constituent une base d'aide à la décision et peuvent être complétés par des analyses statistiques ou décisionnelles supplémentaires selon les objectifs de l'étude."

        )

        return recommendations

    @staticmethod
    def generate_conclusion(report, analysis):
        """
        Génère automatiquement la conclusion
        du rapport d'aide à la décision.
        """

        trends = report["trend_summary"]

        comparisons = report["comparison"]

        # ==========================================
        # Tendance dominante
        # ==========================================

        if trends["fluctuating"] >= trends["total"] / 2:

            trend_text = (
                "une prédominance de tendances fluctuantes "
                "sur les variables numériques analysées"
            )

        elif trends["increasing"] >= trends["total"] / 2:

            trend_text = (
                "une évolution globalement croissante "
                "des variables étudiées"
            )

        elif trends["decreasing"] >= trends["total"] / 2:

            trend_text = (
                "une évolution majoritairement décroissante "
                "des variables étudiées"
            )

        else:

            trend_text = (
                "des évolutions globalement stables "
                "sur les variables analysées"
            )

        # ==========================================
        # Dimensions analysées
        # ==========================================

        dimension_names = []

        for dimension in comparisons.keys():

            name = dimension.replace("_", " ").lower()

            dimension_names.append(name)

        if len(dimension_names) == 0:

            dimension_text = "les catégories étudiées"

        elif len(dimension_names) == 1:

            dimension_text = dimension_names[0]

        elif len(dimension_names) == 2:

            dimension_text = (

                dimension_names[0]

                + " et "

                + dimension_names[1]

            )

        else:

            dimension_text = (

                ", ".join(dimension_names[:-1])

                + " et "

                + dimension_names[-1]

            )
        # ==========================================
        # Conclusion
        # ==========================================

        conclusion = (

            f"Cette analyse met en évidence {trend_text} "

            f"ainsi que des disparités significatives selon "

            f"{dimension_text}. "

            "Les résultats obtenus offrent une vision synthétique "

            "des principales caractéristiques du jeu de données "

            "et constituent un support pertinent pour "

            "l'interprétation des données statistiques. "

            "Ils peuvent être exploités afin d'orienter "

            "les analyses complémentaires et d'accompagner "

            "les processus d'aide à la décision."

        )

        return conclusion


    @staticmethod
    def json_converter(obj):
        """
        Convertit les types NumPy en types Python
        afin de permettre la sérialisation JSON.
        """

        if isinstance(obj, np.integer):
            return int(obj)

        if isinstance(obj, np.floating):
            return float(obj)

        if isinstance(obj, np.bool_):
            return bool(obj)

        raise TypeError(
            f"Type non sérialisable : {type(obj)}"
        )



    @staticmethod
    def save_report(report):
        """
        Sauvegarde le rapport au format JSON
        dans le dossier reports.
        """

        filename = datetime.now().strftime(
            "rapport_%Y%m%d_%H%M%S.json"
        )

        filepath = os.path.join(
            "reports",
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                ensure_ascii=False,
                indent=4,
                default=ReportService.json_converter
            )

        return filename

    @staticmethod
    def load_reports():
        """
        Charge tous les rapports sauvegardés
        dans le dossier reports.
        """

        import os
        import json

        reports = []

        folder = "reports"

        if not os.path.exists(folder):
            return reports

        files = sorted(
            os.listdir(folder),
            reverse=True
        )

        for filename in files:

            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(folder, filename)

            try:

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as file:

                    report = json.load(file)

                reports.append({

                    "file": filename,

                    "date": report.get("date", "--"),

                    "dataset": report.get("filename", "--"),

                    "user": report.get("user", "Administrateur")

                })

            except Exception:

                continue

        return reports

    @staticmethod
    def open_report(filename):
        """
        Ouvre un rapport JSON sauvegardé.
        """

        filepath = os.path.join(
            "reports",
            filename
        )

        if not os.path.exists(filepath):

            return None

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)

        return report


    @staticmethod
    def delete_report(filename):
        """
        Supprime un rapport sauvegardé.
        """

        filepath = os.path.join(
            "reports",
            filename
        )

        if os.path.exists(filepath):

            os.remove(filepath)

            return True

        return False

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

            
            "recommendations": [],

            "insights": [],

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
        report["summary"] = generate_executive_summary(report)

        report["insights"] = ReportService.generate_insights(
            report,
            analysis
        )

        report["recommendations"] = ReportService.generate_recommendations(
            report,
            analysis
        )

        report["trend_summary"] = ReportService.generate_trend_summary(
            report["trends"]
        )

        report["trend_interpretation"] = (
            ReportService.generate_trend_interpretation(
                report["trend_summary"]
            )
        )

        report["conclusion"] = ReportService.generate_conclusion(
            report,
            analysis
        )
        ReportService.save_report(report)

        return report