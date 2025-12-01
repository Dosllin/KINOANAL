import random
from Controlers.manager import FilmManager
from Controlers.display import film_preview
from Data.parsers import Parsers

films_data = Parsers.films_parser()

def random_films(user):
    print('Случайные фильмы!')
    list_random_films = random.sample(list(films_data), 10)
    for film in list_random_films:
        film_preview(film)
        print("1. Следующий фильм"
              "2. Добавить фильм в просмотренные",
              "3. Добавить фильм в отложенные",
              "4. Выйти из случайной подборки", sep='\n')
        choice = input("Введите команду: ")
        if choice == "1":
            continue
        elif choice == '2':
            user_manager = FilmManager(user)
            user_manager.add_in_viewed_films(film)
        elif choice == '3':
            user_manager = FilmManager(user)
            user_manager.add_in_wish_list(film)
        elif choice == '4':
            break
