import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute("CREATE USER connect WITH PASSWORD 'connect'")
cur.execute("ALTER ROLE connect WITH SUPERUSER")
cur.execute("CREATE DATABASE connect")
cur.close()
con.close()
