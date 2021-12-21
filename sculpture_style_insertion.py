from random import choice

def sculpture_style_insertion(connection, number=400):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from styles"
    )
    available_style = list(cur.fetchall())
    cur.execute(
        f"SELECT id from sculpture"
    )
    available_sculpture = list(cur.fetchall())
    already_used_numbers = set()
    for _ in range(number-100):
        style = choice(available_style)[0]
        sculpture = choice(available_sculpture)[0]
        while sculpture in already_used_numbers:
            sculpture = choice(available_sculpture)[0]
        already_used_numbers.add(sculpture)
        cur.execute(
            f"INSERT INTO sculpture_style (style_id, sculpture_id)"
            f"VALUES (\'{style}\', \'{sculpture}\')"
        )
    for _ in range(100):
        style = choice(available_style)[0]
        sculpture = choice(available_sculpture)[0]
        cur.execute(
            f"INSERT INTO sculpture_style (style_id, sculpture_id)"
            f"VALUES (\'{style}\', \'{sculpture}\')"
        )
    connection.commit()
    print("sculpture-style added successfully!")
