from random import choice

def painting_style_insertion(connection, number=800):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from styles"
    )
    available_style = list(cur.fetchall())
    cur.execute(
        f"SELECT id from painting"
    )
    available_painting = list(cur.fetchall())
    already_used_numbers = set()
    for _ in range(number-200):
        style = choice(available_style)[0]
        painting = choice(available_painting)[0]
        while painting in already_used_numbers:
            painting = choice(available_painting)[0]
        already_used_numbers.add(painting)
        cur.execute(
            f"INSERT INTO painting_style (style_id, painting_id)"
            f"VALUES (\'{style}\', \'{painting}\')"
        )
    for _ in range(200):
        style = choice(available_style)[0]
        painting = choice(available_painting)[0]
        cur.execute(
            f"INSERT INTO painting_style (style_id, painting_id)"
            f"VALUES (\'{style}\', \'{painting}\')"
        )
    connection.commit()
    print("painting-style added successfully!")
