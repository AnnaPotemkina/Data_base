from random import choice

def other_style_insertion(connection, number=400):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from styles"
    )
    available_style = list(cur.fetchall())
    cur.execute(
        f"SELECT id from other"
    )
    available_other = list(cur.fetchall())
    already_used_numbers = set()
    for _ in range(number-100):
        style = choice(available_style)[0]
        other = choice(available_other)[0]
        while other in already_used_numbers:
            other = choice(available_other)[0]
        already_used_numbers.add(other)
        cur.execute(
            f"INSERT INTO other_style (style_id, other_id)"
            f"VALUES (\'{style}\', \'{other}\')"
        )
    for _ in range(100):
        style = choice(available_style)[0]
        other = choice(available_other)[0]
        cur.execute(
            f"INSERT INTO other_style (style_id, other_id)"
            f"VALUES (\'{style}\', \'{other}\')"
        )
    connection.commit()
    print("other-style added successfully!")
