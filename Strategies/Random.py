import random
from Data.parsers import Parsers


def random_films(user):
    films_data = Parsers.films_parser()
    print('Случайные фильмы!')
    list_random_films = random.sample(list(films_data), 10)
    return list_random_films
