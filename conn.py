import sqlite3
from datetime import datetime, timedelta

# 🔗 Conexión a la base de datos
conn = sqlite3.connect("validades.db")
cursor = conn.cursor()

# 🏗️ Crear tabla si no existe
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS validades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo INTEGER NOT NULL,
        validade TEXT NOT NULL,
        cantidad INTEGER NOT NULL
    )
"""
)
conn.commit()


# 🔸 Agregar validade con validación de duplicados
def agregar_validade(codigo, validade, cantidad):
    cursor.execute(
        """
        SELECT * FROM validades WHERE codigo = ? AND validade = ?
    """,
        (codigo, validade),
    )
    existe = cursor.fetchone()
    if existe:
        raise Exception("❌ Ya existe un registro con ese código y validade.")
    else:
        cursor.execute(
            """
            INSERT INTO validades (codigo, validade, cantidad) 
            VALUES (?, ?, ?)
        """,
            (codigo, validade, cantidad),
        )
        conn.commit()


# 🔸 Listar validades desde hoy en adelante
def listar_validades_desde_hoy():
    hoy = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        """
        SELECT * FROM validades WHERE validade >= ? ORDER BY validade ASC
    """,
        (hoy,),
    )
    return cursor.fetchall()


# 🔸 Buscar por código desde hoy en adelante
def buscar_validade_por_codigo(codigo):
    hoy = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        """
        SELECT * FROM validades WHERE codigo = ? AND validade >= ? ORDER BY validade ASC
    """,
        (codigo, hoy),
    )
    return cursor.fetchall()


# 🔸 Obtener top 6 productos con mayor cantidad y validade más próxima
def obtener_top_6():
    hoy = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        """
        SELECT codigo, validade, SUM(cantidad) as total_cantidad 
        FROM validades 
        WHERE validade >= ?
        GROUP BY codigo, validade
        ORDER BY total_cantidad DESC, validade ASC
        LIMIT 6
    """,
        (hoy,),
    )
    return cursor.fetchall()


# 🔸 Eliminar registros vencidos según cantidad de días
def limpiar_registros_vencidos(dias):
    if dias <= 0:
        return  # No eliminar si es 0
    fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    cursor.execute(
        """
        DELETE FROM validades WHERE validade < ?
    """,
        (fecha_limite,),
    )
    conn.commit()


# 🔸 Cerrar conexión
def cerrar_conexion():
    conn.close()
