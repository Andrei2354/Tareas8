from crypt import methods

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def ejecutar_sql(sql_text):
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "postgres"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()

        # Consulta SQL (por ejemplo, selecciona todos los registros de una tabla llamada usuarios)
        cursor.execute(sql_text)

        # Obtener columnas para contruir claves del JSON
        columnas = [desc[0] for desc in cursor.description]

        # Convertir resultados a JSON
        resultados = cursor.fetchall()
        empleados = [dict(zip(columnas, fila)) for fila in resultados]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return jsonify(empleados)

    except psycopg2.Error as e:
        print("Error", e)



@app.route('/empleados', methods=['GET'])
def obtener_lista_empleados():
    return ejecutar_sql(
        'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100'
    )



if __name__=='__main__':
    app.run(debug=True)