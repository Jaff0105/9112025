import sqlite3

DB_PATH = "helpdesk.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # --- Tabla de usuarios ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            nombre TEXT,
            apellido TEXT,
            email TEXT,
            password TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'usuario'
        )
    """)

    # --- Tabla de tickets ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            reportado_por TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'abierto',
            prioridad TEXT NOT NULL DEFAULT 'media'
        )
    """)

    conn.commit()
    conn.close()

