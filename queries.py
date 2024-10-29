# queries.py
import pandas as pd
from db_connection import get_connection

# queries.py
import pandas as pd
from db_connection import get_connection

# Consultar información de usuarios
def fetch_users():
    query = """
    SELECT u.id, 
           u.name, 
           u."lastName", 
           u.rut, 
           u.email, 
           DATE(u.birthday) AS birthday, 
           u.phone, 
           u."emergencyName", 
           u."emergencyNumber", 
           u."emergencyRelationship", 
           u."role", 
           u."validEmail", 
           u."termsAccepted", 
           e.name AS establishment_name, 
           c.name AS career_name
    FROM "Users" u
    LEFT JOIN "Establishments" e ON u."EstablishmentId" = e.id
    LEFT JOIN "Careers" c ON u."CareerId" = c.id
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

# Consultar información de asistencia
def fetch_attendance():
    query = "SELECT * FROM asistencia"
    with get_connection() as conn:
        return pd.read_sql(query, conn)

# Consultar información de evaluaciones
def fetch_evaluations():
    query = "SELECT * FROM evaluaciones"
    with get_connection() as conn:
        return pd.read_sql(query, conn)

# Consultar otra información
def fetch_other_data():
    query = "SELECT * FROM otros"
    with get_connection() as conn:
        return pd.read_sql(query, conn)
