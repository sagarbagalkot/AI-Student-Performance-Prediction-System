from database import get_connection


conn = get_connection()

cursor = conn.cursor()


# Check current Oracle user

cursor.execute("""
SELECT USER FROM dual
""")

print("Connected User:", cursor.fetchone()[0])

# Check USERS table

cursor.execute("""
SELECT table_name
FROM user_tables
WHERE table_name='USERS'
""")

print("USERS Table:", cursor.fetchone())



# Check STUDENT_PREDICTIONS columns

cursor.execute("""
SELECT column_name 
FROM user_tab_columns
WHERE table_name='STUDENT_PREDICTIONS'
ORDER BY column_id
""")


print("\nSTUDENT_PREDICTIONS Columns:")

for row in cursor.fetchall():

    print(row)



cursor.close()

conn.close()