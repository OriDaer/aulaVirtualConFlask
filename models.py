import mysql.connector
from config import Config
import hashlib

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.conn.cursor(dictionary=True)

class Usuario(Database):
    def registrar(self, nombre, email, password, rol='estudiante'):
        self.cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        if self.cursor.fetchone():
            return False

        hashed = hashlib.sha256(password.encode()).hexdigest()
        sql = "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (nombre, email, hashed, rol))
        self.conn.commit()
        return True

    def login(self, email, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        sql = "SELECT * FROM usuarios WHERE email=%s AND password=%s"
        self.cursor.execute(sql, (email, hashed))
        return self.cursor.fetchone()

class Curso(Database):
    def crear(self, nombre, descripcion, profesor):
        sql = "INSERT INTO cursos (nombre, descripcion, profesor) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (nombre, descripcion, profesor))
        self.conn.commit()
        return self.cursor.lastrowid

    def modificar(self, id_curso, nombre=None, descripcion=None, profesor=None):
        campos = []
        valores = []
        if nombre:
            campos.append("nombre=%s")
            valores.append(nombre)
        if descripcion:
            campos.append("descripcion=%s")
            valores.append(descripcion)
        if profesor:
            campos.append("profesor=%s")
            valores.append(profesor)
        if not campos:
            return False
        sql = f"UPDATE cursos SET {', '.join(campos)} WHERE id=%s"
        valores.append(id_curso)
        self.cursor.execute(sql, tuple(valores))
        self.conn.commit()
        return True

    def eliminar(self, id_curso):
        sql = "DELETE FROM cursos WHERE id=%s"
        self.cursor.execute(sql, (id_curso,))
        self.conn.commit()
        return True

    def listar(self):
        self.cursor.execute("SELECT * FROM cursos")
        return self.cursor.fetchall()

    def obtener(self, id_curso):
        sql = "SELECT * FROM cursos WHERE id=%s"
        self.cursor.execute(sql, (id_curso,))
        return self.cursor.fetchone()


class Inscripcion(Database):
    def inscribir(self, id_curso, id_usuario):
        self.cursor.execute("SELECT * FROM inscripciones WHERE id_curso=%s AND id_usuario=%s", (id_curso, id_usuario))
        if self.cursor.fetchone():
            return False
        sql = "INSERT INTO inscripciones (id_curso, id_usuario) VALUES (%s, %s)"
        self.cursor.execute(sql, (id_curso, id_usuario))
        self.conn.commit()
        return True

    def mis_cursos(self, id_usuario):
        sql = """SELECT c.* FROM cursos c
                JOIN inscripciones i ON i.id_curso=c.id
                WHERE i.id_usuario=%s"""
        self.cursor.execute(sql, (id_usuario,))
        return self.cursor.fetchall()


class Contenido(Database):
    def agregar(self, id_curso, titulo, tipo, url, descripcion=None):
        self.titulo = titulo
        self.tipo = tipo
        self.url = url
        self.descripcion = descripcion
        sql = "INSERT INTO contenidos (id_curso, titulo, tipo, url) VALUES (%s,%s,%s,%s)"
        self.cursor.execute(sql, (id_curso, titulo, tipo, url))
        self.conn.commit()
        return True

    def listar(self, id_curso):
        self.cursor.execute("SELECT * FROM contenidos WHERE id_curso=%s", (id_curso,))
        return self.cursor.fetchall()
