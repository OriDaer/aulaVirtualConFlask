from flask import Flask
from routes import init_routes

app = Flask(__name__)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
# tiene q salirte cm q estas en la curricula y ahi t salen todos los cursos
#hay q hacer gestion de estudiantes tmb pero fijate bien q falta de gestion cursos
#de cursos solo falta relacionar los cursos con instructores y estudiantes
