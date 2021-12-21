from random import randint
import json

def norm_form(time):
    return '0' + str(time) if time < 10 else time

def get_random_day():
    month = norm_form(randint(1, 12))
    day = norm_form(randint(1, 30) if month != '02' else randint(1, 28))
    return f'{randint(1000, 1950)}-{month}-{day}'

def get_exhibition_start():
    month = norm_form(randint(1, 12))
    day = norm_form(randint(1, 30) if month != '02' else randint(1, 28))
    return f'{randint(2019, 2022)}-{month}-{day}'

FIRST_FEMALE_NAMES = ['Anna', 'Olga', 'Elithabeth', 'Anastasia', 'Kris', 'Alla', 'Maria', 'Kate']
FIRST_MALE_NAMES = ['Ilia', 'Denis', 'Ivan', 'Peter', 'Vinsent', 'Pole', 'Philip', 'Serj', 'Alexander']

FEMALE_SURNAMES = ['Lubimova', 'Ivanova', 'Petrova', 'Trofimova', 'Baranova', 'Anisimova', 'Maltseva', 'Pimenova']
MALE_SURNAMES = ['Ivanov', 'Petrov', 'Surikov', 'Trofimov', 'Turner', 'Panin', 'Voronin', 'Maksimov', 'Kireev']

FEMALE_PATRONYMICS = ['Sergeevna', 'Olegovna', 'Alexandrovna', 'Ivanovna', 'Petrovna', 'Denisovna']
MALE_PATRONYMICS = ['Sergeevic', 'Olegovich', 'Alexandrovich', 'Ivanovich', 'Petrovich', 'Denisovich']

BIRTHDAYS = get_random_day

GENRES = ['Портрет', 'Пейзаж', 'Марина', 'Историческая живопись', 'Батальная живопись', 'Натюрморт',
          'Жанровая живопись', 'Архитектурная живопись', 'Религиозная живопись',
          'Анималистическая живопись', 'Декоративная живопись']

MATERIAL_PICT = ['Масло','Темпера','Гуашь','Акварель','Карандаш','Уголь','Сепия','Сиена','Пастель','Ручка','Маркеры']
MATERIAL_DIFF = ['Глина','Мрамор','Дерево','Фарфор','Медь','Серебро','Латунь','Проволока','Бронза', 'Стекло','Гранит']

OWNER = ['Третьяковская галерея','Лувр','Эрмитаж',
         'Галерея Уфицци','Лондонская национальная галерея','Пушкинский музей',
         'Национальная галерея Шотландии','Старая Пинакотека','Частная коллекция','галерея Прадо',
         'Музей метрополитен',' Галерея Святого Йиржи','Дрезденская галерея','Картинная галерея «Кэритон»','Национальная Галерея Австралии']

EXHIBITION_START = get_exhibition_start()