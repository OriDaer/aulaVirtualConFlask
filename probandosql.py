import mysql.connector

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",        # <-- cambialo si usás otro usuario
    password="root",    # <-- tu contraseña
    database="aula_virtual"  # <-- tu base de datos
)

cursor = conexion.cursor()

# Leer datos de la tabla
cursor.execute("SELECT * FROM usuarios")

print("Contenido de la tabla 'usuarios':")
for fila in cursor.fetchall():
    print(fila)

# Cerrar
cursor.close()
conexion.close()
