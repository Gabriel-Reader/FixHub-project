import psycopg2

conn = psycopg2.connect(
    database = 'FixHub', #Coloque o database que vai mmanipular no postgresSQL
    user = 'postgres',
    password = 'Readers1205',
    host = 'localhost',
    port ='5432'
)
