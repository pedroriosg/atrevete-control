# queries.py
import pandas as pd
from db_connection import get_connection

# queries.py
import pandas as pd
from db_connection import get_connection

# Consultar información de usuarios
def fetch_users():
    print("Fetching users")
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
    print("Fetching schools")
    query = """
    SELECT name FROM "Schools"
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)
    
def fetch_years():
    print("Fetching years")
    query = """
    SELECT name FROM "Years"
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fetch_courses_of_school(school_name, year_name):
    print("Fetching courses")
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
    print("Fetching user courses")
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
    print("Fetching general attendance by course for all days")
    query = '''
    SELECT 
        cd.date AS class_date,
        COUNT(DISTINCT a."UserId") AS attended_count,
        (COUNT(DISTINCT a."UserId")::FLOAT / NULLIF(total_students.total_count, 0)) * 100 AS attendance_percentage
    FROM "Classdays" cd
    INNER JOIN "ClassdayCourses" cc ON cd.id = cc."ClassdayId" AND cc."CourseId" = %s
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
        return pd.read_sql(query, conn, params=(int(course_id), int(course_id), int(course_id), int(course_id)))


def fetch_attendance_by_date(course_id, class_date):
    print("Fetching attendance by date")
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
            INNER JOIN "ClassdayCourses" cc ON cd.id = cc."ClassdayId" AND cc."CourseId" = %s
            WHERE cd.date = %s AND cd.state = 'finished'
        )
    WHERE uc."CourseId" = %s AND uc.role = 'student'
    ORDER BY u."lastName", u.name;
    '''
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=(int(course_id), int(course_id), int(course_id), class_date, int(course_id)))


def fetch_detailed_attendance_by_course(course_id):
    print("Fetching detailed attendance by course with date-specific columns")
    query = '''
    WITH ordered_classdays AS (
        SELECT cd.date,
               cd.id AS classday_id,
               ROW_NUMBER() OVER (PARTITION BY cdc."CourseId" ORDER BY TO_DATE(cd.date, 'DDMMYY') DESC) AS date_rank
        FROM "Classdays" cd
        JOIN "ClassdayCourses" cdc ON cd.id = cdc."ClassdayId"
        WHERE cdc."CourseId" = %s AND cd.state = 'finished'
    ),
    user_attendance AS (
        SELECT u.id,
               u.name,
               u."lastName",
               COUNT(a."UserId") AS attended_classes,
               MAX(CASE WHEN ocd.date_rank = 1 THEN (a."UserId" IS NOT NULL)::int ELSE 0 END) AS attended_t,
               MAX(CASE WHEN ocd.date_rank = 2 THEN (a."UserId" IS NOT NULL)::int ELSE 0 END) AS attended_t1,
               MAX(CASE WHEN ocd.date_rank = 3 THEN (a."UserId" IS NOT NULL)::int ELSE 0 END) AS attended_t2
        FROM "Users" u
        LEFT JOIN "UserCourses" uc ON u.id = uc."UserId" AND uc.role = 'student' AND uc."CourseId" = %s
        LEFT JOIN ordered_classdays ocd ON ocd.classday_id IN (
            SELECT cd.id FROM "Classdays" cd
            JOIN "ClassdayCourses" cdc ON cd.id = cdc."ClassdayId"
            WHERE cdc."CourseId" = %s AND cd.state = 'finished'
        )
        LEFT JOIN "Attendances" a ON u.id = a."UserId" AND a."ClassdayId" = ocd.classday_id AND a."CourseId" = %s
        WHERE uc."CourseId" = %s
        GROUP BY u.id, u.name, u."lastName"
    ),
    total_days AS (
        SELECT COUNT(*) AS total_count
        FROM "Classdays" cd
        JOIN "ClassdayCourses" cdc ON cd.id = cdc."ClassdayId"
        WHERE cdc."CourseId" = %s AND cd.state = 'finished'
    ),
    recent_dates AS (
        SELECT 
            MAX(CASE WHEN date_rank = 1 THEN date END) AS date_t,
            MAX(CASE WHEN date_rank = 2 THEN date END) AS date_t1,
            MAX(CASE WHEN date_rank = 3 THEN date END) AS date_t2
        FROM ordered_classdays
    )
    SELECT 
        ua.id,
        ua.name,
        ua."lastName",
        (ua.attended_classes::FLOAT / NULLIF(td.total_count, 0)) * 100 AS total_attendance_percentage,
        rd.date_t,
        rd.date_t1,
        rd.date_t2,
        ua.attended_t,
        ua.attended_t1,
        ua.attended_t2
    FROM 
        user_attendance ua,
        total_days td,
        recent_dates rd
    WHERE 
        ua.id IS NOT NULL  -- Ensure only existing users are selected
    ORDER BY 
        total_attendance_percentage ASC;
    '''
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=(int(course_id), int(course_id), int(course_id), int(course_id), int(course_id), int(course_id)))

### EVALUACIONES

def fetch_evaluations_by_course(course_id):
    print("Fetching evaluations")
    query = f"""
    SELECT 
        a.id AS assessment_id,
        a.name AS assessment_name,
        at.name AS assessment_type_name,
        at.id AS assessment_type_id
    FROM "Assessments" a
    LEFT JOIN "AssessmentCourses" ac ON ac."AssessmentId" = a.id
    LEFT JOIN "AssessmentTypes" at ON a."AssessmentTypeId" = at.id
    WHERE ac."CourseId" = {course_id}
    ORDER BY a.name
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fetch_performance_by_assessment_type(course_id, assessment_type_id):
    print("Fetching performance by assessment type")

    # Consulta para obtener todas las evaluaciones de un tipo específico para un curso
    evaluations_query = f"""
    SELECT a.id AS assessment_id, a.name AS assessment_name, a."correctAnswer"
    FROM "Assessments" a
    JOIN "AssessmentTypes" at ON a."AssessmentTypeId" = at.id
    JOIN "AssessmentCourses" ac ON a.id = ac."AssessmentId"
    WHERE ac."CourseId" = {course_id} AND a."AssessmentTypeId" = {assessment_type_id} AND ac.state = 'results'
    """

    with get_connection() as conn:
        evaluations_data = pd.read_sql(evaluations_query, conn)

    performance_results = []

    for _, row in evaluations_data.iterrows():
        assessment_id = row['assessment_id']
        correct_answer = row['correctAnswer']
        length_of_correct_answer = len(correct_answer)

        # Consulta para obtener el rendimiento de los usuarios para esta evaluación
        performance_query = f"""
        WITH course_users AS (
            SELECT uc."UserId"
            FROM "UserCourses" uc
            WHERE uc."CourseId" = {course_id} AND uc."role" = 'student'
        ),
        answered_users AS (
            SELECT ans."UserId", ans.answer
            FROM "Answers" ans
            WHERE ans."AssessmentId" = {assessment_id}
            AND ans."UserId" IN (SELECT "UserId" FROM course_users)
        ),
        performance_calculation AS (
            SELECT 
                au."UserId",
                LENGTH('{correct_answer}') AS total_chars,
                -- Count the number of correct characters
                SUM(CASE 
                    WHEN SUBSTRING(au.answer, i, 1) = SUBSTRING('{correct_answer}', i, 1) THEN 1 
                    ELSE 0 
                END) AS correct_char_count
            FROM answered_users au
            CROSS JOIN generate_series(1, LENGTH('{correct_answer}')) AS i
            GROUP BY au."UserId"
        )
        SELECT 
            ROUND((SUM(pc.correct_char_count)::numeric / SUM(pc.total_chars)) * 100, 2) AS performance_percentage,
            COUNT(DISTINCT CASE 
                WHEN LENGTH(au.answer) = {length_of_correct_answer} AND au.answer = repeat('-', {length_of_correct_answer}) 
                THEN pc."UserId" 
                END) AS absent_users
        FROM performance_calculation pc 
        JOIN course_users cu ON pc."UserId" = cu."UserId"
        JOIN answered_users au ON pc."UserId" = au."UserId"
        GROUP BY cu."UserId";
        """

        with get_connection() as conn:
            performance_data = pd.read_sql(performance_query, conn)

        absent_users_count = performance_data['absent_users'].sum()
        total_users = len(performance_data)

        present_users_data = performance_data[performance_data['absent_users'] == 0]

        # Calcular rendimiento considerando solo usuarios presentes
        performance_percentage = present_users_data['performance_percentage'].mean() if len(present_users_data) > 0 else 0
        
        # Calcular el porcentaje de asistencia
        attendance_percentage = (1 - (absent_users_count / total_users)) * 100 if total_users > 0 else 0


        performance_results.append({
            'assessment_id': assessment_id,
            'assessment_name': row['assessment_name'],
            'average_performance': performance_percentage,
            'absent_users': absent_users_count,
            'attendance_percentage': attendance_percentage,
            'total_users': total_users
        })

    return performance_results

def fetch_data_by_assessment_id(course_id, assessment_id):
    print("Fetching data by assessment ID:", assessment_id)

    # Obtener la respuesta correcta de la evaluación
    correct_answer_query = f"""
    SELECT "correctAnswer"
    FROM "Assessments"
    WHERE id = {assessment_id}
    """

    with get_connection() as conn:
        correct_answer_data = pd.read_sql(correct_answer_query, conn)

    correct_answer = correct_answer_data['correctAnswer'].values[0]
    length_of_correct_answer = len(correct_answer)

    # Consulta para obtener los detalles de los usuarios y su rendimiento, incluyendo nombre, apellido y cantidad de respuestas correctas
    query = f"""
    WITH course_users AS (
            SELECT uc."UserId"
            FROM "UserCourses" uc
            WHERE uc."CourseId" = {course_id} AND uc."role" = 'student'
        ),
        answered_users AS (
            SELECT ans."UserId", ans.answer
            FROM "Answers" ans
            WHERE ans."AssessmentId" = {assessment_id}
            AND ans."UserId" IN (SELECT "UserId" FROM course_users)
        ),
        performance_calculation AS (
            SELECT 
                au."UserId",
                LENGTH('{correct_answer}') AS total_chars,
                SUM(CASE 
                    WHEN SUBSTRING(au.answer, i, 1) = SUBSTRING('{correct_answer}', i, 1) THEN 1 
                    ELSE 0 
                END) AS correct_char_count,
                SUM(CASE 
                    WHEN SUBSTRING(au.answer, i, 1) = SUBSTRING('{correct_answer}', i, 1) THEN 1 
                    ELSE 0 
                END) AS correct_answers
            FROM answered_users au
            CROSS JOIN generate_series(1, LENGTH('{correct_answer}')) AS i
            GROUP BY au."UserId"
        )
        SELECT 
            u."name",
            u."lastName",
            SUM(pc.correct_answers) AS good_answers,
            SUM(pc.total_chars) AS total_answers,
            ROUND((SUM(pc.correct_char_count)::numeric / SUM(pc.total_chars)) * 100, 2) AS performance_percentage,
            COUNT(DISTINCT CASE 
                WHEN LENGTH(au.answer) = {length_of_correct_answer} AND au.answer = repeat('-', {length_of_correct_answer}) 
                THEN pc."UserId" 
                END) AS absent_users
        FROM performance_calculation pc 
        JOIN course_users cu ON pc."UserId" = cu."UserId"
        JOIN answered_users au ON pc."UserId" = au."UserId"
        JOIN "Users" u ON pc."UserId" = u.id
        GROUP BY u."name", u."lastName", cu."UserId"
        ORDER BY performance_percentage DESC;
    """

    with get_connection() as conn:
        performance_data = pd.read_sql(query, conn)

    return performance_data
