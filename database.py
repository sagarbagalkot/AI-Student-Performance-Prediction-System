import oracledb

from config import DB_USERNAME, DB_PASSWORD, DB_DSN

def get_connection():

    return oracledb.connect(
        user=DB_USERNAME,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


def register_user(name, email, password):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO users
        (
            name,
            email,
            password
        )

        VALUES
        (
            :1,
            :2,
            :3
        )
    """,
    (
        name,
        email,
        password
    ))


    conn.commit()


    cursor.close()

    conn.close()

def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        user_id,
        name

        FROM users

        WHERE email=:1
        AND password=:2
    """,
    (
        email,
        password
    ))


    user = cursor.fetchone()


    cursor.close()

    conn.close()


    return user

def save_prediction(
        user_id,
        student_name,
        attendance,
        study_hours,
        assignment_marks,
        internal_marks,
        practical_marks,
        previous_marks,
        result,
        confidence
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student_predictions
        (
            user_id,
            student_name,
            attendance,
            study_hours,
            assignment_marks,
            internal_marks,
            practical_marks,
            previous_marks,
            result,
            confidence
        )

        VALUES
        (
            :1,
            :2,
            :3,
            :4,
            :5,
            :6,
            :7,
            :8,
            :9,
            :10
        )

    """,
    (
        user_id,
        student_name,
        attendance,
        study_hours,
        assignment_marks,
        internal_marks,
        practical_marks,
        previous_marks,
        result,
        confidence
    ))

    conn.commit()

    cursor.close()

    conn.close()

def get_dashboard_data():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM student_predictions
    """)

    total_students = cursor.fetchone()[0]

    cursor.execute("""
        SELECT NVL(AVG(attendance),0)
        FROM student_predictions
    """)

    average_attendance = round(cursor.fetchone()[0],2)

    cursor.execute("""
        SELECT NVL(AVG(previous_marks),0)
        FROM student_predictions
    """)

    average_marks = round(cursor.fetchone()[0],2)

    cursor.execute("""
        SELECT COUNT(*)
        FROM student_predictions
        WHERE result='Pass'
    """)

    pass_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM student_predictions
        WHERE result='Fail'
    """)

    fail_count = cursor.fetchone()[0]

    if total_students == 0:

        pass_percentage = 0

        fail_percentage = 0

    else:

        pass_percentage = round(
            (pass_count / total_students) * 100,
            2
        )

        fail_percentage = round(
            (fail_count / total_students) * 100,
            2
        )

    cursor.close()

    conn.close()

    return (
        total_students,
        average_attendance,
        pass_percentage,
        fail_percentage,
        average_marks
    )

def get_all_predictions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT

        id,
        student_name,
        attendance,
        study_hours,
        assignment_marks,
        internal_marks,
        practical_marks,
        previous_marks,
        result

        FROM student_predictions

        ORDER BY id DESC

    """)

    students = cursor.fetchall()

    cursor.close()

    conn.close()

    return students

def delete_prediction(id):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute("""
        DELETE

        FROM student_predictions

        WHERE id=:1

    """,
    (id,))
    
    conn.commit()

    cursor.close()

    conn.close()