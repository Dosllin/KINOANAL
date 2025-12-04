from Controlers.display import film_preview
from Controlers.manager import FilmManager
from Data.parsers import Parsers



def search_film(user):
    users = Parsers.user_parser()
    films_data = Parsers.films_parser()
    request = input("Введите название фильма: ").capitalize()
    if request in films_data.keys():
        film_preview(request)
        print("1. Добавить фильм в просмотренные",
              "2. Добавить фильм в отложенные",
              "3. Добавить оценку фильму", sep='\n')
        if len(users[user.user_name]["user_viewed_films"]) > 0: # Если у пользователя нет ни одного фильма не даёт выйти из поиска
            print("4. Выйти из поиска")

        choice = input()
        if choice == '1':
            user_manager = FilmManager(user)
            user_manager.add_in_viewed_films(request) # Записываю в БД, что пользователь смотрел фильм
            users = Parsers.user_parser()
            films_data = Parsers.films_parser()
        elif choice == '2':
            user_manager = FilmManager(user)
            user_manager.add_in_wish_list(request) # Записываю в БД, что пользователь хочет посмотреть фильм
            users = Parsers.user_parser()
            films_data = Parsers.films_parser()
        elif choice == '3':
            score = 0 # Создаю здесь, чтобы Pycharm не ругался так правильнее
            flag = 1
            while flag == 1:
                try:
                    score = int(input("Введите оценку от 1 до 10: "))
                    flag = 0
                except ValueError:
                    print("Введите Цифру от 1 до 10!!!!")
            user_manager = FilmManager(user)
            user_manager.add_rating(request,score)

        elif choice == '4' and len(users[user.user_name]["user_viewed_films"]) > 0:
            print(0)
            return 0
    else:
        print("Фильм не найден")
