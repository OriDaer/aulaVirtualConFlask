from flask import Flask, render_template, request, redirect, url_for, session
from models import Usuario, Curso

def init_routes(app):
    app.secret_key = "supersecretkey"

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if not email or not password:
                return "Faltan datos"
            user = Usuario().login(email, password)
            if user:
                session['user'] = user['nombre']
                session['id_usuario'] = user['id'] 
                session['rol'] = user['rol']
                if user['rol'] == 'profesor':
                    return redirect(url_for('home_profesor'))
                else:
                    return redirect(url_for('home'))
            else:
                return "Usuario o contraseña incorrecta"
        return render_template('login.html')

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            email = request.form.get('email')
            password = request.form.get('password')
            rol = request.form.get('rol', 'estudiante')
            if not nombre or not email or not password:
                return "Faltan datos"
            success = Usuario().registrar(nombre, email, password, rol)
            if success:
                return redirect(url_for('login'))
            else:
                return "El correo ya está registrado"
        return render_template('register.html')

    @app.route('/home')
    def home():
        if 'user' in session and session.get('rol') == 'estudiante':
            cursos = Curso().listar()
            return render_template('home_estudiante.html', nombre=session['user'], cursos=cursos)
        return redirect(url_for('login'))

    @app.route('/home_profesor')
    def home_profesor():
        if 'user' in session and session.get('rol') == 'profesor':
            cursos = Curso().listar()
            return render_template('home_profesor.html', nombre=session['user'], cursos=cursos)
        return redirect(url_for('login'))

    @app.route('/cursos/crear', methods=['GET','POST'])
    def crear_curso():
        if 'rol' in session and session['rol'] != 'profesor':
            return "Acceso denegado"
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            profesor = request.form.get('profesor')
            if not nombre or not profesor:
                return "Faltan datos"
            Curso().crear(nombre, descripcion, profesor)
            return redirect(url_for('home_profesor'))
        profesores = ["Profesor Juan Pérez", "Profesora Carolina"]  # Lista de profesores predeterminados
        return render_template('crear_curso.html', profesores=profesores)

    @app.route('/cursos/editar/<int:id_curso>', methods=['GET','POST'])
    def editar_curso(id_curso):
        if 'rol' in session and session['rol'] != 'profesor':
            return "Acceso denegado"
        curso = Curso().obtener(id_curso)
        if not curso:
            return "Curso no encontrado"
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            profesor = request.form.get('profesor')
            Curso().modificar(id_curso, nombre, descripcion, profesor)
            return redirect(url_for('home_profesor'))
        profesores = ["Profesor Juan Pérez"]
        return render_template('editar_curso.html', curso=curso, profesores=profesores)

    @app.route('/cursos/eliminar/<int:id_curso>')
    def eliminar_curso(id_curso):
        if 'rol' in session and session['rol'] != 'profesor':
            return "Acceso denegado"
        Curso().eliminar(id_curso)
        return redirect(url_for('home_profesor'))

    from models import Usuario, Curso, Inscripcion, Contenido

    # Ver curso con contenidos
    @app.route('/curso/<int:id_curso>')
    def ver_curso(id_curso):
        if 'rol' not in session:
            return redirect(url_for('login'))

        curso = Curso().obtener(id_curso)
        if not curso:
            return "Curso no encontrado"

        contenidos = Contenido().listar(id_curso)

        # Si es profesor, siempre puede ver
        if session['rol'] == 'profesor':
            return render_template('ver_curso.html', curso=curso, contenidos=contenidos, es_profesor=True)

        # Si es estudiante, debe estar inscrito
        id_usuario = Usuario().login(session['user'], "dummy")  # ⚠ O mejor guarda id en session al logear
        # Para simplificar: asumo guardas user_id en session al logear
        id_usuario = session.get('id_usuario')

        insc = Inscripcion().mis_cursos(id_usuario)
        ids_cursos = [c['id'] for c in insc]

        if id_curso not in ids_cursos:
            return "No estás inscrito en este curso"

        return render_template('ver_curso.html', curso=curso, contenidos=contenidos, es_profesor=False)


    # --- Inscribirse a curso ---
    @app.route('/curso/<int:id_curso>/inscribirse')
    def inscribirse(id_curso):
        if session.get('rol') != 'estudiante' or 'id_usuario' not in session:
            return redirect(url_for('login'))
        Inscripcion().inscribir(id_curso, session['id_usuario'])
        return redirect(url_for('ver_curso', id_curso=id_curso))
    # Subir contenido (solo profesor)
    @app.route('/curso/<int:id_curso>/contenido', methods=['GET','POST'])
    def agregar_contenido(id_curso):
        if session.get('rol') != 'profesor':
            return "Acceso denegado"
        if 'rol' in session and session['rol'] != 'profesor':
            return "Acceso denegado"
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            tipo = request.form.get('tipo')
            url = request.form.get('url')
            Contenido().agregar(id_curso, titulo, tipo, url)
            return redirect(url_for('ver_curso', id_curso=id_curso))
        return render_template('agregar_contenido.html', id_curso=id_curso)

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('rol', None)
        return redirect(url_for('login')) 