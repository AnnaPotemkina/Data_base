from random import choice, randint
from exhibition_insrtion import GENRES, MATERIAL_PICT, OWNER

def painting_insertion(connection, number=600):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from exhibition"
    )
    available_exhibition = list(cur.fetchall())
    cur.execute(
        f"SELECT id from artist"
    )
    available_artist = list(cur.fetchall())
    for _ in range(number):
        exhibition = choice(available_exhibition)[0]
        artist = choice(available_artist)[0]
        owner = choice(OWNER)
        material = choice(MATERIAL_PICT)
        genre = choice(GENRES)
        year_creation = randint(1000, 2000)
        cur.execute(
            f"INSERT INTO painting (owners, year_creation, material, genre, artist, exhibition)"
            f"VALUES (\'{owner}\', \'{year_creation}\', \'{material}\', \'{genre}\', \'{artist}\', \'{exhibition}\')"
        )
    connection.commit()
    print("paintings added successfully!")