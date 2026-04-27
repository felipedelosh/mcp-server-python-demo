"""
FelipedelosH
2026

"""
# main.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres_mcp_demo"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123")
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

mcp = FastMCP("RappiDemo")

@mcp.tool()
def saludar(nombre: str = "mundo") -> str:
    """Saluda a una persona."""
    return f"¡Hola, {nombre}!"

@mcp.tool()
def test_db_connection() -> dict:
    """Prueba la conexión a la base de datos y devuelve el listado de tablas en el esquema 'public'."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Obtener todas las tablas del esquema public (excluyendo las del sistema)
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row['table_name'] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return {
            "success": True,
            "database": DB_CONFIG["database"],
            "host": DB_CONFIG["host"],
            "tables": tables
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "database": DB_CONFIG["database"],
            "host": DB_CONFIG["host"]
        }

@mcp.tool()
def crear_usuario(nombre: str, email: str, phone: str = None, rappi_id: str = None) -> dict:
    """Crea un usuario en la base de datos."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, email, phone, rappi_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, email
        """, (nombre, email, phone, rappi_id))
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"exito": True, "usuario": dict(new_user)}
    except psycopg2.IntegrityError as e:
        return {"exito": False, "error": f"Email o dato duplicado: {email}"}
    except Exception as e:
        return {"exito": False, "error": str(e)}

@mcp.tool()
def listar_usuarios(limite: int = 10) -> list:
    """Lista los últimos usuarios registrados."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone, rappi_id FROM users ORDER BY id DESC LIMIT %s", (limite,))
    users = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(u) for u in users]

@mcp.tool()
def acumular_puntos(user_id: int, points: int) -> dict:
    """
    Acumula puntos a un usuario. Crea un registro en event_accumulations.
    Si la operación es exitosa, registra un evento con estado 'OK'.
    En caso contrario (usuario no existe, puntos inválidos, error DB), registra 'FAIL'.
    """
    if points <= 0:
        return {"exito": False, "error": "Los puntos deben ser mayores a cero."}

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar que el usuario existe
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cur.fetchone():
            conn.rollback()
            return {"exito": False, "error": f"Usuario con id {user_id} no existe."}

        # Insertar acumulación
        cur.execute("""
            INSERT INTO event_accumulations (user_id, points)
            VALUES (%s, %s)
            RETURNING id
        """, (user_id, points))
        accum_id = cur.fetchone()['id']

        # Registrar evento exitoso
        event_id_str = f"ACC_{user_id}_{accum_id}_{int(datetime.now().timestamp())}"
        cur.execute("""
            INSERT INTO events (event_id, status, points)
            VALUES (%s, 'OK', %s)
        """, (event_id_str, points))

        conn.commit()
        cur.close()
        return {
            "exito": True,
            "acumulacion_id": accum_id,
            "mensaje": f"Se acumularon {points} puntos al usuario {user_id}."
        }
    except Exception as e:
        if conn:
            conn.rollback()
        return {"exito": False, "error": f"Error en la base de datos: {str(e)}"}
    finally:
        if conn:
            conn.close()


@mcp.tool()
def redimir_puntos(user_id: int, points: int) -> dict:
    """
    Redime puntos de un usuario. Crea un registro en event_redeems.
    Si la operación es exitosa, registra un evento con estado 'OK'.
    En caso contrario (usuario no existe, puntos inválidos, error DB), registra 'FAIL'.
    """
    if points <= 0:
        return {"exito": False, "error": "Los puntos deben ser mayores a cero."}

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar existencia del usuario
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cur.fetchone():
            conn.rollback()
            return {"exito": False, "error": f"Usuario con id {user_id} no existe."}

        # Insertar redención
        cur.execute("""
            INSERT INTO event_redeems (user_id, points)
            VALUES (%s, %s)
            RETURNING id
        """, (user_id, points))
        redeem_id = cur.fetchone()['id']

        # Registrar evento exitoso
        event_id_str = f"RED_{user_id}_{redeem_id}_{int(datetime.now().timestamp())}"
        cur.execute("""
            INSERT INTO events (event_id, status, points)
            VALUES (%s, 'OK', %s)
        """, (event_id_str, points))

        conn.commit()
        cur.close()
        return {
            "exito": True,
            "redencion_id": redeem_id,
            "mensaje": f"Se redimieron {points} puntos del usuario {user_id}."
        }
    except Exception as e:
        if conn:
            conn.rollback()
        return {"exito": False, "error": f"Error en la base de datos: {str(e)}"}
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Transporte STDIO: permite a Claude Desktop hablar con este proceso
    mcp.run(transport="stdio")
