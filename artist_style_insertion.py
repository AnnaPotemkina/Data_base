from random import choice

def artist_style_insertion(connection, number=300):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from styles"
    )
    available_style = list(cur.fetchall())
    cur.execute(
        f"SELECT id from artist"
    )
    available_artist = list(cur.fetchall())
    already_used_numbers = set()
    for _ in range(number-100):
        style = choice(available_style)[0]
        artist = choice(available_artist)[0]
        while artist in already_used_numbers:
            artist = choice(available_artist)[0]
        cur.execute(
            f"INSERT INTO artist (style_id, artist_id)"
            f"VALUES (\'{style}\', \'{artist}\')"
        )
    for _ in range(100):
        style = choice(available_style)
        artist = choice(available_artist)
        cur.execute(
            f"INSERT INTO artist (style_id, artist_id)"
            f"VALUES (\'{style}\', \'{artist}\')"
        )
    connection.commit()
    print("artists-style added successfully!")
