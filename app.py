from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
import os
from services.auth_service import AuthService
from services.importer import Importer
from services.report_service import ReportService
from assistant.assistant_ai import AssistantAI
from assistant.dataset_loader import DatasetLoader
from services.user_service import UserService

app = Flask(__name__)

app.secret_key = "hcp_secret"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role


logged_users = {}

@login_manager.user_loader
def load_user(user_id):
    return logged_users.get(int(user_id))

# Dossier des fichiers importés
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Création du dossier uploads si nécessaire
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = AuthService.login(username, password)

        if user:

            user_obj = User(
                user[0],
                user[1],
                user[2]
            )

            logged_users[user_obj.id] = user_obj

            login_user(user_obj)

            return redirect(url_for("dashboard"))

        flash("Nom d'utilisateur ou mot de passe incorrect.")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "index.html",
        username=current_user.username,
        role=current_user.role
    )




@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# =====================================================
# Accueil
# =====================================================

@app.route("/")
def home():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# =====================================================
# Import
# =====================================================

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_data():

    if current_user.role != "admin":
        flash("Seul l'administrateur peut importer un dataset.")
        return redirect(url_for("dashboard"))

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
            print("1 - Début import")

            result = Importer.run(
                filepath,
                table_name
            )

            print("2 - Fin Importer.run")

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

    import_info = session.get("import_info")

    return render_template(
        "import.html",
        import_info=import_info
    )


# =====================================================
# Assistant
# =====================================================

@app.route("/assistant", methods=["GET", "POST"])
@login_required
def assistant():

    response = None

    if request.method == "POST":

        import_info = session.get("import_info")

        if import_info is None:

            flash("Veuillez d'abord importer un dataset.")

            return redirect(url_for("import_data"))

        question = request.form.get("question")

        dataframe = DatasetLoader.load_latest(import_info)

        response = AssistantAI.ask(
            question,
            dataframe
        )

    return render_template(
        "assistant.html",
        response=response
    )


# =====================================================
# Gestion des rapports
# =====================================================

@app.route("/rapport")
@login_required
def report():

    import_info = session.get("import_info")

    return render_template(
        "report.html",
        import_info=import_info,
        reports=[]
    )


@app.route("/rapport/generate")
@login_required
def generate_report():

    import_info = session.get("import_info")

    if import_info is None:

        flash("Veuillez d'abord importer un dataset.")

        return redirect(url_for("import_data"))

    report = ReportService.generate(import_info)

    session["report_generated"] = True

    return render_template(
        "report_view.html",
        report=report,
        reports=[]
    )


@app.route("/rapport/view")
@login_required
def view_report():

    import_info = session.get("import_info")

    if import_info is None:

        flash("Veuillez d'abord importer un dataset.")

        return redirect(url_for("import_data"))

    if not session.get("report_generated"):

        flash("Aucun rapport n'a encore été généré.")

        return redirect(url_for("report"))

    report = ReportService.generate(import_info)

    return render_template(
        "report_view.html",
        report=report,
        reports=[]
    )

# =====================================================
# Gestion des utilisateurs
# =====================================================

@app.route("/users", methods=["GET", "POST"])
@login_required
def users():

    if current_user.role != "admin":
        flash("Accès refusé.")
        return redirect(url_for("dashboard"))
    edit_user = None

    edit_id = request.args.get("edit")

    if edit_id:
        edit_user = UserService.get_by_id(edit_id)
    if request.method == "POST":

        user_id = request.form.get("user_id")
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "analyst")

        # ===========================
        # Modification
        # ===========================

        if user_id:

            if not username or not email:

                flash("Le nom d'utilisateur et l'email sont obligatoires.")

            else:

                UserService.update(
                    user_id,
                    username,
                    email,
                    role
                )

                flash("Utilisateur modifié avec succès.")

                return redirect(url_for("users"))

        # ===========================
        # Création
        # ===========================

        else:

            if not username or not email or not password:

                flash("Tous les champs sont obligatoires.")

            elif password != confirm_password:

                flash("Les mots de passe ne correspondent pas.")

            else:

                result = UserService.create(
                    username,
                    email,
                    password,
                    role
                )

                if result == "username_exists":

                    flash("Ce nom d'utilisateur existe déjà.")

                elif result == "email_exists":

                    flash("Cette adresse email existe déjà.")

                else:

                    flash("Utilisateur créé avec succès.")

                    return redirect(url_for("users"))

    users_list = UserService.get_all()

    return render_template(
        "users.html",
        users=users_list,
        edit_user=edit_user
    )

@app.route("/users/password/<int:user_id>", methods=["GET", "POST"])
@login_required
def change_password(user_id):

    if current_user.role != "admin":
        flash("Accès refusé.")
        return redirect(url_for("users"))
    
    user = UserService.get_by_id(user_id)
    if not user:
        flash("Utilisateur introuvable.")
        return redirect(url_for("users"))

    if request.method == "POST":

        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not password:

            flash("Le mot de passe est obligatoire.")

        elif password != confirm_password:

            flash("Les mots de passe ne correspondent pas.")

        else:

            result = UserService.change_password(
                user_id,
                password
            )

            if result:

                flash("Mot de passe modifié avec succès.")

            else:

                flash("Utilisateur introuvable.")

            return redirect(url_for("users"))

    return render_template(
        "change_password.html",
        user_id=user_id,
        username=user[1]
    )

@app.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):

    if current_user.role != "admin":
        flash("Accès refusé.")
        return redirect(url_for("users"))

    UserService.delete(user_id)

    flash("Utilisateur supprimé avec succès.")

    return redirect(url_for("users"))
# =====================================================
# Lancement
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)