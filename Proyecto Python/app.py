from flask import Flask, render_template
from db import init_db
from auth import auth_bp
from tickets import tickets_bp

app = Flask(__name__)
app.secret_key = "clave_segura_123"

# Inicializar base de datos
init_db()

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
