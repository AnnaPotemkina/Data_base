
import psycopg2
from local_settings import DATABASE, USER, PASSWORD, HOST, PORT

from artist_insertion import artist_insertion
from artist_style_insertion import artist_style_insertion
from exhibition_insertion import exhibition_insertion
from other_insertion import other_insertion
from other_style_insertion import other_style_insertion
from painting_insertion import painting_insertion
from painting_style_insertion import painting_style_insertion
from sculpture_insertion import sculpture_insertion
from sculpture_style_insertion import sculpture_style_insertion
from ticket_insertion import ticke_insertion

con = psycopg2.connect(
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

print("Connection created successfully!")

exhibition_insertion(connection=con, number=100)
artist_insertion(connection=con, number=200)
other_insertion(connection=con, number=300)
painting_insertion(connection=con, number=600)
sculpture_insertion(connection=con, number=300)
ticke_insertion(connection=con, number=400)
#artist_style_insertion(connection=con, number=300)
other_style_insertion(connection=con, number=400)
painting_style_insertion(connection=con, number=800)
sculpture_style_insertion(connection=con, number=400)

print('Everything is all right!')
con.close()