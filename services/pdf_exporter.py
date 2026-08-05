from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class PDFExporter:

    @staticmethod
    def export(report):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=(21*cm, 29.7*cm)
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(

            "TitleStyle",

            parent=styles["Title"],

            alignment=TA_CENTER,

            fontSize=20,

            spaceAfter=20

        )

        story = []

        # =====================================================
        # Titre
        # =====================================================

        logo = Image(

            "static/images/logo_hcp.png",

            width=2.3*cm,

            height=2.3*cm

        )

        story.append(logo)

        story.append(Spacer(1,0.3*cm))

        title = Paragraph(

            "Rapport d'aide à la décision",

            title_style

        )

        story.append(title)

        story.append(Spacer(1,0.5*cm))

        story.append(Spacer(1, 0.6*cm))

        # =====================================================
        # Informations générales
        # =====================================================

        story.append(
            Paragraph(
                "<b>Informations générales</b>",
                styles["Heading2"]
            )
        )

        info = [

            ["Nom du dataset", report["filename"]],

            ["Base de données", report["database"]],

            ["Table PostgreSQL", report["table"]],

            ["Date", report["date"]]

        ]

        table = Table(
            info,
            colWidths=[6*cm, 11*cm]
        )

        table.setStyle(TableStyle([

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#E8EEF9")),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ]))

        story.append(table)

        story.append(Spacer(1, 0.7*cm))

        # =====================================================
        # Résumé
        # =====================================================

        story.append(

            Paragraph(

                "<b>Résumé exécutif</b>",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                report["summary"],

                styles["BodyText"]

            )

        )

        story.append(Spacer(1, 0.7*cm))

        # =====================================================
        # Vue d'ensemble
        # =====================================================

        story.append(

            Paragraph(

                "<b>Vue d'ensemble du jeu de données</b>",

                styles["Heading2"]

            )

        )

        overview = [

            ["Observations", report["rows"]],

            ["Variables", report["columns"]],

            ["Variables numériques", report["numeric_columns"]],

            ["Variables textuelles", report["text_columns"]]

        ]

        table = Table(
            overview,
            colWidths=[8*cm,4*cm]
        )

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#E8EEF9"))

        ]))

        story.append(table)

        story.append(Spacer(1,0.7*cm))

        # =====================================================
        # Analyse intelligente
        # =====================================================

        story.append(

            Paragraph(

                "<b>Analyse intelligente</b>",

                styles["Heading2"]

            )

        )

        for insight in report["insights"]:

            story.append(

                Paragraph(

                    "• " + insight,

                    styles["BodyText"]

                )

            )

        story.append(Spacer(1,0.7*cm))

        # =====================================================
        # Recommandations
        # =====================================================

        story.append(

            Paragraph(

                "<b>Recommandations</b>",

                styles["Heading2"]

            )

        )

        for rec in report["recommendations"]:

            story.append(

                Paragraph(

                    "• " + rec,

                    styles["BodyText"]

                )

            )

        story.append(Spacer(1,0.7*cm))

        # =====================================================
        # Conclusion
        # =====================================================

        story.append(

            Paragraph(

                "<b>Conclusion</b>",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                report["conclusion"],

                styles["BodyText"]

            )

        )

        doc.build(

            story,

            onFirstPage=PDFExporter.add_page_number,

            onLaterPages=PDFExporter.add_page_number

        )

        pdf = buffer.getvalue()

        buffer.close()

        return pdf


    @staticmethod
    def add_page_number(canvas, doc):

        canvas.setFont(

            "Helvetica",

            9

        )

        canvas.drawRightString(

            19.5*cm,

            1*cm,

            f"Page {doc.page}"

        )