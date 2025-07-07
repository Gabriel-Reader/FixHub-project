import psycopg2

conn = psycopg2.connect(
    database = 'FixHub1', #Coloque o database que vai mmanipular no postgresSQL
    user = 'postgres',
    password = 'password',
    host = 'localhost',
    port ='5432'
)
