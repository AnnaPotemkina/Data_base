from random import randint, choice
from exhibition_insrtion import FIRST_FEMALE_NAMES, FIRST_MALE_NAMES, FEMALE_SURNAMES, MALE_SURNAMES, FEMALE_PATRONYMICS, MALE_PATRONYMICS, BIRTHDAYS

def artist_insertion(connection, number=200):
    cur = connection.cursor()
    cur.execute(
        f"SELECT id from exhibition"
    )
    available_exhibition = list(cur.fetchall())
    for _ in range(number):
        sex = randint(0, 1)  # пол художника
        first_name = choice(FIRST_FEMALE_NAMES) if sex else choice(FIRST_MALE_NAMES)
        surname = choice(FEMALE_SURNAMES) if sex else choice(MALE_SURNAMES)
        second_name = choice(FEMALE_PATRONYMICS) if sex else choice(MALE_PATRONYMICS)
        birthday = BIRTHDAYS()
        deathday = BIRTHDAYS()
        exhibition = choice(available_exhibition)[0]
        cur.execute(
            f"INSERT INTO artist (names, second_name, surname, date_of_birth, date_of_death, exhibition)"
            f"VALUES (\'{first_name}\', \'{second_name}\', \'{surname}\', \'{birthday}\', \'{deathday}\', \'{exhibition}\')"
        )
    connection.commit()
    print("artists added successfully!")




