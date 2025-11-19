from models.database import get_connection
from config import Config
import os

class Usuario:

    @staticmethod
    def crear(nombre, apellidos, email, rol):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Insert user without dataset path
            cur.execute(
                """
                INSERT INTO usuarios(nombre, apellidos, email, rol)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, apellidos, email, rol)
            )
            uid = cur.lastrowid
            
            # Create dataset path and update user
            ruta_dataset = os.path.join(Config.DATASET_DIR, str(uid))
            cur.execute(
                """
                UPDATE usuarios SET ruta_dataset = %s WHERE id_usuario = %s
                """,
                (ruta_dataset, uid)
            )
            
            conn.commit()
            
            # Crear directorio
            os.makedirs(ruta_dataset, exist_ok=True)
            
            return uid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE estado = 1")
        return cur.fetchall()

    @staticmethod
    def obtener_por_nombre(nombre):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
        return cur.fetchone()

    @staticmethod
    def obtener_por_id(uid):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (uid,))
        return cur.fetchone()

    @staticmethod
    def editar(id_usuario, nombre, apellidos, email):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE usuarios 
            SET nombre = %s, apellidos = %s, email = %s 
            WHERE id_usuario = %s
            """,
            (nombre, apellidos, email, id_usuario)
        )
        conn.commit()
        return cur.rowcount

    @staticmethod
    def eliminar(uid):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET estado = 0 WHERE id_usuario = %s", (uid,))
        conn.commit()
        return cur.rowcount
    
    def registrar_acceso(id_usuario, resultado):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO accesos (id_usuario, resultado)
            VALUES (%s, %s)
            """,
            (id_usuario, resultado)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def obtener_historial(id_usuario):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT a.id_acceso, u.nombre, u.apellidos, a.resultado, a.fecha
            FROM accesos a
            INNER JOIN usuarios u ON u.id_usuario = a.id_usuario
            WHERE a.id_usuario = %s
            ORDER BY a.fecha DESC
            """,
            (id_usuario,)
        )
        historial = cur.fetchall()
        cur.close()
        conn.close()
        return historial
