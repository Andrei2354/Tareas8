from syslog import LOG_INFO

import psycopg2
from flask import Flask, jsonify, request

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

# Todos

# obtener programadores (hecho)
# obtener proyectos activos o todos (medio hecho)
# obtener tareas de un proyecto (sin asignar o aignada) - 1

# Asignar gestor a proyecto
# Asignar cliente a proyecto
# asignar programador a proyecto
# asignar programador a tareas

# obtener tareas de un proyecto (sin asignar o aignada) - 1

# Crear tareas a proyectos (debe estar asignado)
# Login

# obtener tareas de un proyecto (sin asignar o aignada) - 1
@app.route('/tareas/proyectos',methods=['GET'])
def proyectos_tareas():
    body_request = request.json
    proyecto_nombre = body_request["nombre"]
    resultado = ejecutar_sql(
    f'''SELECT * FROM public."Tarea" t JOIN public."Proyecto" p ON t."proyecto" = p."id" WHERE p."nombre" = "{proyecto_nombre}"''')
    return resultado

@app.route('/proyectos')
def MostrarProyectos():
    resultado = ejecutar_sql(
    'SELECT e.nombre FROM public."Empleado" e JOIN public."Programador" p ON e."id" = p."empleado"')
    return resultado

# obtener programadores
@app.route('/programador')
def MostrarProgramador():
    resultado = ejecutar_sql(
    'SELECT e.nombre FROM public."Empleado" e JOIN public."Programador" p ON e."id" = p."empleado"')
    return resultado

@app.route('/Prueba',methods=['GET'])
def MostrarEmpleado():
    resultado = ejecutar_sql(
    'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100')
    return resultado

@app.route('/empleado/empleados',methods=['GET'])
def puestos():
    resultado = ejecutar_sql(
    '''SELECT e.nombre,g.id AS id_puesto, 'Gestor' AS rol FROM "Empleado" e INNER JOIN "Gestor" g ON e.id = g.empleado UNION ALL SELECT e.nombre, p.id AS id_puesto,'Programador' AS rol FROM  "Empleado" e INNER JOIN "Programador" p ON e.id = p.empleado;''')
    return resultado
# obtener proyectos (activos o todos)
@app.route('/proyecto/proyectos',methods=['GET'])
def proyectos():
    resultado = ejecutar_sql(
    '''SELECT * FROM public."Proyecto" ORDER BY id ASC ''')
    return resultado

@app.route('/proyecto/proyectos_activos',methods=['GET'])
def proyectosActivos():
    resultado = ejecutar_sql(
    '''SELECT * FROM public."Proyecto" WHERE "fecha_inicio" BETWEEN '2024-01-01 10:00:00' AND '2024-01-01 10:00:00' ''')
    return resultado

@app.route('/proyecto/proyectos_gestor',methods=['GET'])
def proyectosGestor():
    empleado_id = request.args.get('id')
    resultado = ejecutar_sql(f'''Select * from public."Proyecto" p inner join "GestoresProyecto" g on g.proyecto = p.id where g.gestor = {empleado_id} ''')
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
    return  (sql)

@app.route('/login_user', methods=['POST'])
def login_user():
    body_request = request.json
    user = body_request["usuario"]
    passwd = body_request["passwd"]

    is_logged = ejecutar_sql(
        f"SELECT * FROM public.\"Gestor\" WHERE usuario = '{user}' AND passwd = '{passwd}';"
    )

    if len(is_logged.json) == 0:
        return jsonify({"msg": "error"})
    empleado = ejecutar_sql(
        f"SELECT * FROM public.\"Empleado\" WHERE id = '{is_logged.json[0]["empleado"]}';"
    )

    return jsonify(
        {
            "id_empleado": empleado.json[0]["id"],
            "id_gestor": is_logged.json[0]["id"],
            "nombre": empleado.json[0]["nombre"],
            "email": empleado.json[0]["email"]
        }
    )


# Crear tareas a proyectos (debe estar asignado)
@app.route('/crear_tareas', methods=['POST'])
def gestor_tarea():
    body_request = request.json
    nombre = body_request["nombre"]
    descripcion = body_request["descripcion"]
    estimacion = body_request["estimacion"]
    programador = body_request["programador"]
    proyecto = body_request["proyecto"]
    sql = f"""
        INSERT INTO public."Tarea" (nombre, descripcion, estimacion, fecha_creacion, fecha_finalizacion, programador, proyecto)
        VALUES (
            '{nombre}',
            '{descripcion}',
            '{estimacion}',
            NOW(),
            null,
            '{programador}',
            {proyecto},
        );
    """
    return ejecutar_sql(sql)

if __name__=='__main__':
    app.run(debug=True)