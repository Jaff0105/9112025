from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from db import get_connection
import hashlib

# --- Blueprint para autenticación ---
auth_bp = Blueprint("auth", __name__)

def hash_password(password):
    """Encripta la contraseña con SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


# --- LOGIN ---
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        password = request.form["password"].strip()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        u = cur.fetchone()
        conn.close()

        if u and u["password"] == hash_password(password):
            session["usuario"] = usuario
            session["rol"] = u["rol"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


# --- REGISTRO ---
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        email = request.form["email"].strip()
        password = hash_password(request.form["password"].strip())
        rol = request.form["rol"].strip()

        conn = get_connection()
        cur = conn.cursor()

        # Verificar si el usuario ya existe
        cur.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        if cur.fetchone():
            conn.close()
            return render_template("register.html", error="El usuario ya existe")

        # Insertar nuevo usuario
        cur.execute("""
            INSERT INTO usuarios (usuario, nombre, apellido, email, password, rol)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (usuario, nombre, apellido, email, password, rol))

        conn.commit()
        conn.close()

        flash("Usuario registrado con éxito.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# --- LOGOUT ---
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
