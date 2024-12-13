from crypt import methods

import psycopg2
from flask import Flask, jsonify, request
from werkzeug.serving import connection_dropped_errors

app = Flask(__name__)


def ejecutar_sql(sql_text):
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "postgres"

    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )
    cursor = connection.cursor()

    cursor.execute(sql_text)

    if 'INSERT' in sql_text:
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'msg': 'insertado'})

    columnas = [desc[0] for desc in cursor.description]

    resultados = cursor.fetchall()
    empleados = [dict(zip(columnas, fila)) for fila in resultados]

    cursor.close()
    connection.close()
    return jsonify(empleados)

@app.route('/Prueba',methods=['GET'])
def otraCosa():
    resultado = ejecutar_sql(
    'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100')

    return resultado

@app.route('/empleado/empleados',methods=['GET'])
def puestos():
    resultado = ejecutar_sql(
    '''SELECT e.nombre,g.id AS id_puesto, 'Gestor' AS rol FROM "Empleado" e INNER JOIN "Gestor" g ON e.id = g.empleado UNION ALL SELECT e.nombre, p.id AS id_puesto,'Programador' AS rol FROM  "Empleado" e INNER JOIN "Programador" p ON e.id = p.empleado;''')

    return resultado

@app.route('/ejemplo_post', methods=['POST'])
def gestor_ejemplo_post():
    body_request = request.json
    nombre = body_request["nombre"]
    descripcion = body_request["descripcion"]
    fecha_inicio = body_request["fecha_inicio"]
    cliente = body_request["cliente"]
    sql = f"""
        INSERT INTO public."Proyecto" (nombre, descripcion, fecha_creacion, fecha_inicio, fecha_finalizacion, cliente)
        VALUES (
            '{nombre}',
            '{descripcion}',
            NOW(),
            '{fecha_inicio}',
            null,
            {cliente},
        );
    """
    return ejecutar_sql(sql)


if __name__=='__main__':
    app.run(debug=True)