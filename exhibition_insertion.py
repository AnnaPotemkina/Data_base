from exhibition_insrtion import get_exhibition_start

def exhibition_insertion(connection, number=100):
    cursor = connection.cursor()
    for _ in range(number):
        day_of_begining, day_of_end = get_exhibition_start(), get_exhibition_start()
        cursor.execute(
            f"INSERT INTO exhibition (date_of_beginning, date_of_ending)"
            f"VALUES(\'{day_of_begining}\', \'{day_of_end}\')"
        )
    connection.commit()
    print("Addresses added successfully!")
