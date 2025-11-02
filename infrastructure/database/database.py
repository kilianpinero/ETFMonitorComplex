from infrastructure.database.connection import get_engine

# try:
#     conn = get_connection()
#     print("✅ Conectado a la base de datos")
#
#     cursor = conn.cursor()
#     cursor.execute("SELECT version();")
#     version = cursor.fetchone()
#     print("Versión de PostgreSQL:", version)
#
#     cursor.close()
#     conn.close()
#
# except Exception as e:
#     print("❌ Error al conectar:", e)

engine = get_engine()
print("Tablas creadas o verificadas exitosamente")