from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

from services.importer import Importer
from services.report_service import ReportService

app = Flask(__name__)

app.secret_key = "hcp_secret"

# Dossier des fichiers importés
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Création du dossier uploads si nécessaire
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =====================================================
# Accueil
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================================
# Import
# =====================================================

@app.route("/import", methods=["GET", "POST"])
def import_data():

    if request.method == "POST":

        file = request.files.get("file")
        table_name = request.form.get("table_name", "").strip()

        if not file or file.filename == "":
            flash("Veuillez sélectionner un fichier.")
            return redirect(url_for("import_data"))

        if table_name == "":
            flash("Veuillez saisir un nom de table.")
            return redirect(url_for("import_data"))

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        try:

            result = Importer.run(
                filepath,
                table_name
            )

            session["import_info"] = {

                "filename": file.filename,

                "rows": result["rows"],

                "columns": result["columns"],

                "database": "hcp_bi",

                "table": result["table"],

                "header": result["header"],

                "numeric_columns": result["numeric_columns"],

                "text_columns": result["text_columns"],

                "superset": result["superset"]["message"]

            }

            flash("Import terminé avec succès !")

        except Exception as e:

            import traceback
            traceback.print_exc()

            flash(f"Erreur : {e}")

        return redirect(url_for("import_data"))

    import_info = session.pop("import_info", None)

    return render_template(
        "import.html",
        import_info=import_info
    )


# =====================================================
# Assistant
# =====================================================

@app.route("/assistant")
def assistant():
    return render_template("assistant.html")


# =====================================================
# Rapport
# =====================================================

@app.route("/rapport")
def report():

    import_info = session.get("import_info")

    if import_info is None:

        flash("Veuillez d'abord importer un fichier.")

        return redirect(url_for("import_data"))

    report = ReportService.generate(import_info)

    return render_template(
        "report.html",
        report=report,
        reports=[]
    )


# =====================================================
# Lancement
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)