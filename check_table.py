import oracledb

conn = oracledb.connect(
    user="system",
    password="sagar123",
    dsn="localhost:1521/XEPDB1"
)

cur = conn.cursor()

cur.execute("SELECT SYS_CONTEXT('USERENV','CON_NAME') FROM dual")
print("Container:", cur.fetchone())

cur.execute("SELECT column_name FROM user_tab_columns WHERE table_name='STUDENT_PREDICTIONS' ORDER BY column_id")

print("\nColumns:")
for row in cur:
    print(row[0])

cur.close()
conn.close()