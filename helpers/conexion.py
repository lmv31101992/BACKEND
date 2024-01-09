# DATABASE_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

access_list_bbdd = ['bd_pruebas',"postgres",'admin',"127.0.0.1","5432"]
docker_list = ["mypostgres","admin","admin","127.0.0.1","5400"]

def abrirConexion(list):
    import psycopg2
    try:
        conexion = psycopg2.connect(database=list[0],
                                    user=list[1],
                                    password=list[2],
                                    host=list[3],
                                    port=list[4])
        conexion.autocommit = True
    except Exception:
        return None
    return conexion

def crearTabla(conexion , TableName=None):
    if conexion is not None and TableName is not None:
        query = f"CREATE TABLE IF NOT EXISTS {TableName} (id SERIAL, username varchar unique, full_name varchar, email varchar, password varchar, disabled boolean)"
        conexion.cursor().execute(query)

def borrarTabla(conexion,TableName=None):
    query = f"DROP TABLE IF EXISTS {TableName}"
    conexion.cursor().execute(query)

def cerrarConexion(conexion):
    return conexion.close()