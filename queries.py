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

def fetch_attendance_by_course(course_id):
    query = '''
    SELECT 
        cd.date AS class_date,
        COUNT(a."UserId") AS attended_count,
        (COUNT(a."UserId")::FLOAT / NULLIF(total_students.total_count, 0)) * 100 AS attendance_percentage
    FROM "Classdays" cd
    LEFT JOIN "Attendances" a ON cd.id = a."ClassdayId" AND a."CourseId" = %s
    LEFT JOIN (
        SELECT uc."CourseId", COUNT(DISTINCT uc."UserId") AS total_count
        FROM "UserCourses" uc
        WHERE uc."role" = 'student' AND uc."CourseId" = %s
        GROUP BY uc."CourseId"
    ) AS total_students ON total_students."CourseId" = %s
    WHERE cd.state = 'finished'
    GROUP BY cd.date, total_students.total_count
    ORDER BY TO_DATE(cd.date, 'DDMMYY') ASC;
    '''
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=(int(course_id), int(course_id), int(course_id)))

def fetch_attendance_by_date(course_id, class_date):
    query = '''
    SELECT 
        u.id, 
        u.name, 
        u.phone,
        u."lastName", 
        CASE WHEN a."UserId" IS NOT NULL THEN 'present' ELSE 'absent' END AS attendance_status
    FROM "Users" u
    LEFT JOIN "UserCourses" uc ON u.id = uc."UserId" 
        AND uc."CourseId" = %s
    LEFT JOIN "Attendances" a ON u.id = a."UserId" 
        AND a."CourseId" = %s 
        AND a."ClassdayId" = (
            SELECT cd.id 
            FROM "Classdays" cd
            WHERE cd.date = %s AND cd.state = 'finished'
        )
    WHERE uc."CourseId" = %s AND uc.role = 'student'
    ORDER BY u."lastName", u.name;
    '''
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=(int(course_id), int(course_id), class_date, int(course_id)))
