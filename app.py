import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import check_password_hash

from config import Config
from database import get_db, close_db


app = Flask(__name__)

app.config.from_object(Config)

app.teardown_appcontext(close_db)


# Comprobar si el usuario tiene sesión iniciada

def login_required(function):

    from functools import wraps

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "usuario_id" not in session:

            flash(
                "Debes iniciar sesión para acceder.",
                "error"
            )

            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# Pantalla de inicio

@app.route("/")
def inicio():

    if "usuario_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# HU-01: Inicio de sesión

@app.route("/login", methods=["GET", "POST"])
def login():

    if "usuario_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip()

        password = request.form.get("password", "")

        db = get_db()

        usuario = db.execute("""
            SELECT *
            FROM usuarios
            WHERE email = ?
        """, (email,)).fetchone()

        if usuario is None:

            flash(
                "Credenciales incorrectas.",
                "error"
            )

        elif usuario["activo"] != 1:

            flash(
                "El usuario está desactivado.",
                "error"
            )

        elif not check_password_hash(
            usuario["password_hash"],
            password
        ):

            flash(
                "Credenciales incorrectas.",
                "error"
            )

        else:

            session.clear()

            session["usuario_id"] = usuario["id"]

            session["usuario_nombre"] = usuario["nombre"]

            session["perfil_id"] = usuario["perfil_id"]

            return redirect(url_for("dashboard"))

    return render_template("login.html")


# Panel principal

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")


# HU-02: Cierre de sesión

@app.route("/logout")
@login_required
def logout():

    session.clear()

    flash(
        "Has cerrado sesión correctamente.",
        "success"
    )

    return redirect(url_for("login"))

@app.after_request
def prevent_cache(response):

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"

    return response

if __name__ == "__main__":

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    app.run(debug=True)