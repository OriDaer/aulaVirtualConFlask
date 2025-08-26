from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='app_simple',
        user='root',      # Cambia por tu usuario de MySQL
        password='root'       # Cambia por tu contraseña de MySQL
    )

# Ruta para registrar un usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    conn.close()
    return jsonify({"message": "Usuario registrado con éxito"}), 201

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# Rutas para renderizar los formularios
@app.route('/')
def index():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
