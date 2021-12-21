from random import choice, randint
from exhibition_insrtion import MATERIAL_DIFF, OWNER

def sculpture_insertion(connection, number=300):
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
        material = choice(MATERIAL_DIFF)
        year_creation = randint(1000, 2000)
        cur.execute(
            f"INSERT INTO sculpture (owners, year_creation, material, artist, exhibition)"
            f"VALUES (\'{owner}\', \'{year_creation}\', \'{material}\', \'{artist}\', \'{exhibition}\')"
        )
    connection.commit()
    print("sculptures added successfully!")