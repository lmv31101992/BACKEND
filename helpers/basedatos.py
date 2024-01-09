import psycopg2
from psycopg2 import sql

def insertarDatos(conexion,tabla,usr):
    query = f"INSERT INTO {tabla} (username, full_name, email, password, disabled) VALUES ('{usr[0]}', '{usr[1]}', '{usr[2]}', '{usr[3]}', '{usr[4]}') ON CONFLICT (username) DO NOTHING"
    conexion.cursor().execute(query)

def actualizarDatosPorUsername():
    return None

def actualizarDatosPorEmail():
    return None

def actualizarDatosPorFullname():
    return None

def actualizarDatoPorPassword():
    return None

def eliminarDatos(conexion,tabla,username:str|None):
    query = f"DELETE FROM {tabla} WHERE username = '{username}'"
    conexion.cursor().execute(query)

def recibirDatoPor(table_name,connection,columm_name , value):
    try:
        with connection.cursor() as cursor:
            query = sql.SQL(f"SELECT row_to_json(t) FROM ( SELECT * FROM {table_name} WHERE {columm_name} = '{value}')t").format(sql.Identifier(table_name))
            cursor.execute(query)
            user_exists = cursor.fetchone()[0]
            return user_exists
    except psycopg2.Error:
        return None
    except TypeError:
        return None

def recibirDatos(connection,table_name):
    try:
        with connection.cursor() as cursor:
            query = sql.SQL(f"SELECT row_to_json(t) FROM ( SELECT username,full_name,email FROM {table_name})t").format(sql.Identifier(table_name))
            cursor.execute(query)
            users_exists = cursor.fetchall()
            return users_exists
    except psycopg2.Error:
        return None
    except TypeError:
        return None

def existeUsername(connection,table_name, username: str):
    try:
        # Crear un cursor para ejecutar consultas
        with connection.cursor() as cursor:
            # Crear una consulta SQL parametrizada para evitar SQL injection
            query = sql.SQL(f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE username = '{username}');").format(sql.Identifier(table_name))
            cursor.execute(query)
            user_exists = cursor.fetchone()[0]
            return user_exists
    except psycopg2.Error:
        return False