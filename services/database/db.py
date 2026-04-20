import dotenv
import os
import pymysql
from pymysql import Error

dotenv.load_dotenv()

# Obtener las variables de entorno para la conexión a la base de datos
DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


def database_connection():
    try:
        # Establecer la conexión con los parámetros requeridos
        conexion = pymysql.connect(
            host=DB_ENDPOINT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if conexion.open:
            print('Conexión exitosa a la base de datos.')
            return conexion

    except Error as error:
        print(f'Error al conectar a MySQL: {error}')


def create_table():
    try:
        conexion = database_connection()
        cursor = conexion.cursor()

        # Crear la tabla boletines si no existe
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS boletines (
            boletin_id VARCHAR(36) PRIMARY KEY,
            message VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            link_s3 TEXT NOT NULL,
            flag BOOLEAN NOT NULL DEFAULT FALSE
        )
        '''
        cursor.execute(create_table_query)
        conexion.commit()
        print('Tabla "boletines" creada o ya existe.')
        return "Successfully created the table 'boletines'."
    except Error as error:
        print(f'Error al crear la tabla: {error}')
    finally:
        if 'conexion' in locals() and conexion.open:
            cursor.close()
            conexion.close()
            print('Conexión a la base de datos cerrada.')
    return "Successfully closed the database connection."


def insert_boletin(id, message, email, link_s3):
    try:
        conexion = database_connection()
        cursor = conexion.cursor()

        # Insertar un nuevo boletín
        insert_query = '''
        INSERT INTO boletines (boletin_id, message, email, link_s3) VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (id, message, email, link_s3))
        conexion.commit()
        print('Boletín insertado correctamente.')
        return "Successfully inserted the boletin."
    except Error as error:
        print(f'Error al insertar el boletín: {error}')
    finally:
        if 'conexion' in locals() and conexion.open:
            cursor.close()
            conexion.close()
            print('Conexión a la base de datos cerrada.')
    return "Failed to insert the boletin."
