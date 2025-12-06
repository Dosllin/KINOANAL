from GUI.display import show_a_recommended_movie
from Strategies.StrategySimilarUsers import StrategySimilarUsers
from Strategies.DirectorStrategy import DirectorStrategy
from Strategies.RatingStrategy import RatingStrategy
from Strategies.Random import random_films


# Данные для фильтрации, если пользователь не ввёл фильтры
filter_years = [-1000000000,100000000]
filter_rating = -10


def algorithm_menu():
    print("============================",
          "1. Начать работу алгоритма",
          "2. Установить фильтрацию",
          "3. Вернуться обратно в меню",
          "============================", sep="\n")

def filter_menu():
    print("==================================",
          "1. Установить года поиска",
          "2. Установить минимальный рейтинг",
          "3. Выйти к работе алгоритма",
          "==================================", sep="\n")


# Алгоритм по похожим пользователям
def similar_algorithm(user, users_without_main_user):
    global filter_years
    global filter_rating
    while 1:
        print('----------------------------')
        print('Алгоритм на основе пользователей')
        print('----------------------------')

        algorithm_menu()

        user_choice = int(input())

        if user_choice == 1:
            main_strategy = StrategySimilarUsers(user, users_without_main_user)
            films_list, films_list_little_similar = main_strategy.strategy(filter_years, filter_rating)[0], \
            main_strategy.strategy(filter_years, filter_rating)[1]
            show_a_recommended_movie(user, films_list) # У меня код в 2 частях повторялся, пай чарм посоветовал в отдельный деф закинуть


            if len(films_list_little_similar) > 0:  # Если у пользователя ещё были фильмы с другими менее похожими людьми, то мы предлагаем показать такие фильмы
                print("Может быть вам интересны ещё фильмы пользователей с кем у вас было меньше совпадений?")
                user_choice = input("Введите да/нет: ").lower()
                if user_choice == 'да':
                    show_a_recommended_movie(user, films_list_little_similar)


        elif user_choice == 2:
            while 1:

                filter_menu()

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
                    print("Некорректный ввод")
        elif user_choice == 3:
            break
        else:
            print("Некорректный ввод")


def director_algorithm(user):
    while True:
        print('----------------------------')
        print('Алгоритм на основе режиссеров')
        print('----------------------------')

        algorithm_menu()

        user_choice = int(input())

        if user_choice == 1:

            main_strategy = DirectorStrategy(user.user_name)
            show_a_recommended_movie(user, main_strategy.strategy())

        elif user_choice == 2:
            while 1:

                filter_menu()

                user_choice = int(input("Введите команду: "))

                if user_choice == 1:
                    print('----------------------')
                    min_year = int(input("Введите минимальный год: "))
                    max_year = int(input("Введите максимальный год: "))
                    main_strategy = DirectorStrategy(user.user_name)
                    show_a_recommended_movie(user, main_strategy.filtered_year(min_year, max_year))

                    print('----------------------')
                elif user_choice == 2:
                    print('----------------------')
                    min_rating = int(input("Введите минимальный рейтинг: "))
                    max_rating = int(input("Введите максимальный рейтинг: "))
                    main_strategy = DirectorStrategy(user.user_name)
                    show_a_recommended_movie(user, main_strategy.filtered_rating(min_rating, max_rating))
                    print('----------------------')
                elif user_choice == 3:
                    break
                else:
                    print("Некорректный ввод")
        elif user_choice == 3:
            break
        else:
            print("Некорректный ввод")


def rating_algorithm(user):
    while True:
        print('----------------------------')
        print('Алгоритм на основе рейтинга')
        print('----------------------------')

        algorithm_menu()

        user_choice = int(input())

        if user_choice == 1:

            main_strategy = RatingStrategy(user)
            show_a_recommended_movie(user, main_strategy.strategy())

        elif user_choice == 2:
            while 1:
                print("==================================",
                      "1. Установить года поиска",
                      "2. Выйти к работе алгоритма",
                      "==================================", sep="\n")
                user_choice = int(input("Введите команду: "))

                if user_choice == 1:
                    print('----------------------')
                    min_year = int(input("Введите минимальный год: "))
                    max_year = int(input("Введите максимальный год: "))
                    main_strategy = RatingStrategy(user)
                    show_a_recommended_movie(user, main_strategy.filtered_year(min_year, max_year))

                    print('----------------------')

                elif user_choice == 2:
                    break
                else:
                    print("Некорректный ввод")
        elif user_choice == 3:
            break
        else:
            print("Некорректный ввод")


def random_activation(user):
    list_random_films = random_films(user)
    show_a_recommended_movie(user, list_random_films)
