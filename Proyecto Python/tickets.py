from flask import Blueprint, render_template, request, redirect, session
from db import get_connection

tickets_bp = Blueprint("tickets", __name__)

@tickets_bp.route("/")
def index():
    if "usuario" not in session:
        return redirect("/login")
    conn = get_connection()
    cur = conn.cursor()

    # Si es técnico, ve todos; si no, solo los suyos
    if session["rol"] == "tecnico":
        cur.execute("SELECT * FROM tickets ORDER BY id DESC")
    else:
        cur.execute("SELECT * FROM tickets WHERE reportado_por=? ORDER BY id DESC", (session["usuario"],))
    tickets = cur.fetchall()
    conn.close()
    return render_template("index.html", tickets=tickets, usuario=session["usuario"], rol=session["rol"])

@tickets_bp.route("/nuevo", methods=["POST"])
def nuevo():
    if "usuario" not in session:
        return redirect("/login")
    titulo = request.form["titulo"]
    descripcion = request.form["descripcion"]
    prioridad = request.form["prioridad"]
    reportado_por = session["usuario"]
    conn = get_connection()
    conn.execute(
        "INSERT INTO tickets (titulo, descripcion, reportado_por, prioridad) VALUES (?, ?, ?, ?)",
        (titulo, descripcion, reportado_por, prioridad),
    )
    conn.commit()
    conn.close()
    return redirect("/")

@tickets_bp.route("/cambiar_estado/<int:id>", methods=["POST"])
def cambiar_estado(id):
    if "usuario" not in session or session["rol"] != "tecnico":
        return redirect("/")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT estado FROM tickets WHERE id=?", (id,))
    ticket = cur.fetchone()
    if ticket:
        nuevo = "cerrado" if ticket["estado"] == "abierto" else "abierto"
        cur.execute("UPDATE tickets SET estado=? WHERE id=?", (nuevo, id))
        conn.commit()
    conn.close()
    return redirect("/")

@tickets_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    if "usuario" not in session or session["rol"] != "tecnico":
        return redirect("/")
    conn = get_connection()
    conn.execute("DELETE FROM tickets WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
