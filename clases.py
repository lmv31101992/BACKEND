class Conexion:

    def __init__(self,list):
        self.database = list[0]
        self.user = list[1]
        self.password = list[2]
        self.host = list[3]
        self.port = list[4]

    # @staticmethod
        
# DATABASE_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    @staticmethod
    def recibirInstancia():
        return Conexion()

    def abrirConexion(self):
        import psycopg2
        try:
            conexion = psycopg2.connect(database=self.database,
                                        user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)
            conexion.autocommit = True
        except Exception:
            return None
        return conexion

    def abrirCursor(self):
        if self.abrirConexion() is not None:
            return self.abrirConexion().cursor()
        return None
    
    def crearTabla(self,TableName=None):
        if self.abrirConexion() is not None and TableName is not None:
            query = f"CREATE TABLE IF NOT EXISTS {TableName} (id SERIAL, username varchar unique, full_name varchar, email varchar, password varchar, disabled boolean)"
            self.abrirCursor().execute(query)

    def borrarTabla(self,TableName=None):
        query = f"DROP TABLE IF EXISTS {TableName}"
        self.abrirCursor().execute(query)
    
    def cerrarCursor(self):
        self.abrirCursor().close()


class BaseDatos:
    @staticmethod
    def recibirInstancia():
        BaseDatos()

    def insertarDatos(self,tabla,cursor,usr):
        query = f"INSERT INTO {tabla} (username, full_name, email, password, disabled) VALUES ('{usr[0]}', '{usr[1]}', '{usr[2]}', '{usr[3]}', '{usr[4]}') ON CONFLICT (username) DO NOTHING"
        cursor.execute(query)

    def actualizarDatosPorUsername(self):
        return None
    
    def actualizarDatosPorEmail(self):
        return None

    def actualizarDatosPorFullname(self):
        return None
    
    def actualizarDatoPorPassword(self):
        return None

    def eliminarDatos(self,tabla,cursor,username:str):
        query = f"DELETE FROM {tabla} WHERE username = '{username}'"
        cursor.execute(query)

    def recibirDatosPorPassword(self,tabla,cursor,pwd:str):
        import psycopg2
        query = f"SELECT row_to_json(t) FROM ( SELECT * FROM {tabla} WHERE password = '{pwd}')t"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return None
            return result[0]
        except psycopg2.IntegrityError:
            return None

    def recibirDatosPorUsername(self,tabla,cursor,username:str):
        import psycopg2
        query = f"SELECT row_to_json(t) FROM ( SELECT * FROM {tabla} WHERE username = '{username}')t"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return None
            return result[0]
        except psycopg2.errors.UndefinedTable:
            return None
        
    def recibirDatosPorEmail(self,tabla,cursor,email:str):
        import psycopg2
        query = f"SELECT row_to_json(t) FROM ( SELECT * FROM {tabla} WHERE email = '{email}')t"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return None
            return result[0]
        except psycopg2.errors.UndefinedTable:
            return None

    def recibirDatosPorFullname(self,tabla,cursor,fullname:str):
        import psycopg2
        query = f"SELECT row_to_json(t) FROM ( SELECT * FROM {tabla} WHERE full_name = '{fullname}')t"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return None
            return result[0]
        except psycopg2.errors.UndefinedTable:
            return None

    def existeUsername(self,tabla,cursor,username:str):
        import psycopg2
        query = f"SELECT EXISTS (SELECT 1 FROM {tabla} WHERE username = '{username}')"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return None
            return result[0]
        except psycopg2.errors.UndefinedTable:
            return None


class Usuario:
    from pydantic import BaseModel
    @staticmethod
    def recibirInstancia():
        return Usuario()

    class User(BaseModel):
        username : str
        email : str
        full_name: str
        disabled: bool = False
    
    class FullUser(User):
        password : str

    def HashedPassword(self,password:str):
        # Funcion HashedPassword la cual genera el hash de la contraseña que se recibe como texto plano (argumento de entrada)
        import sys
        import bcrypt
        #ciframos la contraseña plana:
        cifraded_text = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        #     realizamos esta operacion para cambiar el has de la pwd de tipo byte a tipo str
        encoding = sys.getdefaultencoding()
        return cifraded_text.decode(encoding)
    
    def HashedPassword_New(self,password:str):
        # from argon2 import PasswordHasher
        from passlib.hash import argon2
        # #ciframos la contraseña plana:
        # cifraded_text = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        # #     realizamos esta operacion para cambiar el has de la pwd de tipo byte a tipo str
        # encoding = sys.getdefaultencoding()
        # return cifraded_text.decode(encoding)
        return argon2.hash(password)
