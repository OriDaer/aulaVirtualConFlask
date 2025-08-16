from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuración de la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ----------------- MODELO -----------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# ----------------- DECORADOR LOGIN -----------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero")
            return redirect(url_for("login_view"))
        return f(*args, **kwargs)
    return decorated

# ----------------- RUTAS HTML -----------------
@app.route("/")
def inicio():
    if "user_id" in session:
        return redirect(url_for("usuarios_view"))
    return redirect(url_for("login_view"))

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and check_password_hash(usuario.password, password):
            session["user_id"] = usuario.id
            session["username"] = usuario.username
            flash(f"Bienvenido {usuario.username}")
            return redirect(url_for("usuarios_view"))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("login_view"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register_view():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        try:
            nuevo_usuario = Usuario(nombre=nombre, email=email, username=username, password=password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Usuario registrado con éxito. Por favor inicia sesión")
            return redirect(url_for("login_view"))
        except:
            flash("Usuario o email ya existe")
            return redirect(url_for("register_view"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Sesión cerrada")
    return redirect(url_for("login_view"))

# ----------------- RUTAS CRUD -----------------
@app.route("/usuarios")
@login_required
def usuarios_view():
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/add", methods=["POST"])
@login_required
def agregar_usuario():
    nombre = request.form["nombre"]
    email = request.form["email"]
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])
    nuevo = Usuario(nombre=nombre, email=email, username=username, password=password)
    db.session.add(nuevo)
    db.session.commit()
    flash("Usuario agregado con éxito")
    return redirect(url_for("usuarios_view"))

@app.route("/usuarios/delete/<int:id>")
@login_required
def borrar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f"Usuario {usuario.username} eliminado")
    return redirect(url_for("usuarios_view"))

# ----------------- MAIN -----------------
if __name__ == "__main__":
    app.run(debug=True)
