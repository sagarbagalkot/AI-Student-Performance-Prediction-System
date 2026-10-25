import oracledb

conn = oracledb.connect(
    user="system",
    password="sagar123",
    dsn="localhost:1521/XE"
)

print("Connected Successfully")

conn.close()