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
    
    # Consultar información de colegios
def fetch_schools():
    query = """
    SELECT name FROM "Schools"
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)
    
def fetch_years():
    query = """
    SELECT name FROM "Years"
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fetch_courses_of_school(school_name, year_name):
    query = f"""
    SELECT 
        c.id AS course_id,
        g.name AS grade_name,
        sub.name AS subject_name

    FROM "Courses" c
    LEFT JOIN "Schools" s ON c."SchoolId" = s.id
    LEFT JOIN "Years" y ON c."YearId" = y.id
    LEFT JOIN "Grades" g ON c."GradeId" = g.id
    LEFT JOIN "Subjects" sub ON c."SubjectId" = sub.id
    WHERE s.name = '{school_name}' AND y.name = '{year_name}'
    ORDER BY g.name, sub.name
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

# Consultar información de usuarios por curso
def fetch_users_by_course(course_id):
    query = '''
    SELECT 
        u.id, 
        u.name, 
        u."lastName", 
        u.rut, 
        u.email, 
        DATE(u.birthday) AS birthday, 
        u.phone, 
        u."emergencyName", 
        u."emergencyNumber", 
        u."emergencyRelationship", 
        u."validEmail", 
        u."termsAccepted", 
        e.name AS establishment_name, 
        c.name AS career_name, 
        uc.role AS user_course_role 
    FROM "Users" u 
    LEFT JOIN "UserCourses" uc ON u.id = uc."UserId" 
    LEFT JOIN "Establishments" e ON u."EstablishmentId" = e.id 
    LEFT JOIN "Careers" c ON u."CareerId" = c.id 
    WHERE uc."CourseId" = %s
'''
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=(int(course_id),))
