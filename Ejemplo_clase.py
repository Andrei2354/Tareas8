from crypt import methods

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/empleados', methods = ['GET'])

def obtener_lista_empleados():

    host = "localhost" # Ejemplo: 'localhost'
    port = "5432" # Puerto por defecto de PostgreSQL
    dbname = "alexsoft" # Nombre de la base de datos
    user = "postgres" # Usuario de la base de datos
    password = "postgres" # Contraseña del usuario

    try:
        # Establecer la conexión
        connection = psycopg2.connect(
            host = host,
            port = port,
            dbname = dbname,
            user = user,
            password = password,
            options = "-c search_path=public"
        )

        cursor = connection.cursor()

        # Consulta SQL (por ejemplo, selecciona todos los registros de una tabla llamada usuarios)
        query = 'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100'
        cursor.execute(query)

        # Obtener columnas para construit claves JSON
        columnas = [desc[0] for desc in cursor.description]

        # Convertir resultados a JSON
        resultados = cursor.fetchall()
        empleados = [dict(zip(columnas, fila)) for fila in resultados]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return jsonify(empleados)

    except psycopg2.Error as e:
        print("Error: ", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)
