import textwrap
from term_image.image import from_url
from Controlers.manager import FilmManager
from Data.parsers import Parsers



def film_preview(request: str): # Функция для отображения фильма. Сюда подаётся название фильма
    films_data = Parsers.films_parser()
    print(films_data[request])
    print('=========================================')
    try:
        print(from_url(films_data[request]['image']))
    except:  # Ошибка, когда не может получить изоброжение по ссылке
        print('Не смогли найти картинку 😥')
    print("Название:", films_data[request]['title'])
    print("Жанры:", ", ".join(films_data[request]['genre']))
    print("Режиссёр:", films_data[request]['director'])
    print("Год выпуска:", films_data[request]['year'])
    print("Страна:", ", ".join(films_data[request]['countries']))
    print("Средний рейтинг:",round(sum(films_data[request]['rating']) / len(films_data[request]['rating']), 2) if films_data[request]['rating'] else "Нет оценок")
    print()
    print("Описание:")
    print(textwrap.fill(films_data[request]['description'], width=70))  # перенос каждые 70 символов (по пробелам)
    print()
    print('=========================================')


def show_a_recommended_movie(user, list_movies: list):
    for film in list_movies:
        film_preview(film)
        print("1. Следующий фильм",
              "2. Добавить фильм в просмотренные",
              "3. Добавить фильм в отложенные",
              "4. Выйти из подборки", sep='\n')
        choice = input("Введите команду: ")
        if choice == "1":
            continue
        elif choice == '2':
            user_manager = FilmManager(user)
            user_manager.add_in_viewed_films(film)  # Добавляем в просмотренные
        elif choice == '3':
            user_manager = FilmManager(user)
            user_manager.add_in_wish_list(film)  # Добавляем в отложенные
        elif choice == '4':
            break
