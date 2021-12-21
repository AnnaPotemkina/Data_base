from random import choice
def ticke_insertion(connection, number=400):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from exhibition"
    )
    available_exhibition = list(cur.fetchall())
    cur.execute(
        f"SELECT id from benefits"
    )
    available_benefits = list(cur.fetchall())
    for _ in range(number):
        benefit = choice(available_benefits)[0]
        exhibition = choice(available_exhibition)[0]
        cur.execute(
            f"SELECT discount from benefits WHERE id = \'{benefit}\'"
        )
        cost = int(1000-1000*(choice(cur.fetchall())[0])/100)
        cur.execute(
            f"INSERT INTO ticket (costs, benefit, exhibition)"
            f"VALUES (\'{cost}\', \'{benefit}\', \'{exhibition}\')"
        )
    connection.commit()
    print("tickets added successfully!")
