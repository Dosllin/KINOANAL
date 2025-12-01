from Controlers.manager import FilmManager
from Controlers.logining import login_sign_in
from Controlers.display import film_preview
from Controlers.searcher import search_film
from Strategies.DirectorStrategy import DirectorStrategy
from Strategies.StrategySimilarUsers import StrategySimilarUsers
from Strategies.Random import random_films
from Data.parsers import Parsers


users = Parsers.user_parser()
films_data = Parsers.films_parser()


# Данные для фильтрации, если пользователь не ввёл фильтры
filter_years = [-1000000000,100000000]
filter_rating = -10


def show_a_recommended_movie(list_movies: list):
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


# Алгоритм по похожим пользователям
def similar_algoritm():
    global filter_years
    global filter_rating
    while 1:
        print('----------------------------')
        print('Алгоритм на основе пользователей')
        print('----------------------------')

        print("============================",
              "1. Начать работу алгоритма",
              "2. Устоновить фильтрацию",
              "3. Вернуться обратно в меню",
              "============================", sep="\n")

        user_choice = int(input())

        if user_choice == 1:
            main_strategy = StrategySimilarUsers(user, users_without_main_user)
            films_list, films_list_litle_similar = main_strategy.strategy(filter_years, filter_rating)[0], \
            main_strategy.strategy(filter_years, filter_rating)[1]
            show_a_recommended_movie(films_list) # У меня код в 2 частях повторялся, пайчарм посоветовал в отдельный деф закинуть


            if len(films_list_litle_similar) > 0:  # Если у пользователя ещё были фильмы с другими менее похожими людьми, то мы предлогаем показать такие фильмы
                print("Может быть вам интересны ещё фильмы пользователей с кем у вас было меньше совпадений?")
                user_choice = input("Введите да/нет: ").lower()
                if user_choice == 'да':
                    show_a_recommended_movie(films_list_litle_similar)


        elif user_choice == 2:
            while 1:
                print("==================================",
                      "1. Устоновить года поиска",
                      "2. Устоновить минимальный рейтинг",
                      "3. Выйти к работе алгоритма",
                      "==================================", sep="\n")
                user_choice = int(input("Введите команду: "))

                if user_choice == 1:
                    print('----------------------')
                    min_year = int(input("Введите минимальный год: "))
                    max_year = int(input("Введите максимальный год: "))
                    filter_years = [min_year, max_year]
                    print('----------------------')
                elif user_choice == 2:
                    print('----------------------')
                    filter_rating = int(input("Введите минимальный рейтинг: "))
                    print('----------------------')
                elif user_choice == 3:
                    break
                else:
                    print("Некоректный ввод")
        elif user_choice == 3:
            break
        else:
            print("Некоректный ввод")


# def random_films():
#     print('Случайные фильмы!')
#     list_random_films = random.sample(list(films_data), 10)
#     for film in list_random_films:
#         film_preview(film)
#         print("1. Следующий фильм"
#               "2. Добавить фильм в просмотренные",
#               "3. Добавить фильм в отложенные",
#               "4. Выйти из случайной подборки", sep='\n')
#         choice = input("Введите команду: ")
#         if choice == "1":
#             continue
#         elif choice == '2':
#             user_manager = FilmManager(user)
#             user_manager.add_in_viewed_films(film)
#         elif choice == '3':
#             user_manager = FilmManager(user)
#             user_manager.add_in_wish_list(film)
#         elif choice == '4':
#             break


### MAIN MENU
Flag_login = 1
user = 0 # Просто для того, чтобы pycharm не ругался
while Flag_login:
    user = login_sign_in()
    if user != 1:
        Flag_login = 0
        users = Parsers.user_parser()


users_without_main_user = users.copy()
users_without_main_user.pop(user.user_name)


if len(users[user.user_name]["user_viewed_films"]) == 0:
    print("==================================")
    print("Похоже, вы ещё не добавили просмотренные фильмы. Пожалуйста, найдите и добавьте хотя бы один фильм.")
    input("Нажмите Enter, чтобы продолжить...")
    while len(users[user.user_name]["user_viewed_films"]) == 0:
        search_film(user)
# DirectorStrategy1 = DirectorStrategy(user.user_name)
# print(DirectorStrategy1.strategy())
while True:
    print('------------MAIN MENU------------')
    print("1. Рекомендации от похожих пользователей",
          "2. Рекомендация на основе ваших любимых режиссеров",
          "6. Поиск фильма (Добавить просмотренные фильмы)",
          "7. 10 Случайных фильмов (Долой алгоритмы доверимся богу рандома)",
          "8. Выйти",sep='\n')

    choice_main_menu = input("Выберите действие: ")
    if choice_main_menu == '5':
        search_film(user)
    elif choice_main_menu  == '1':
        similar_algoritm()
    elif choice_main_menu == '2':
        print('----------------------------')
        print('Алгоритм на основе ваших любимых режиссеров')
        print('----------------------------')
        print()
        User_dir_strategy = DirectorStrategy(user.user_name)
        print(User_dir_strategy.strategy())

    elif choice_main_menu == '6':
        search_film(user)

    elif choice_main_menu == '7':
        random_films(user)

    elif choice_main_menu == '8':
        print("Досвидание!")
        break
