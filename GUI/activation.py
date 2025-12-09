from GUI.display import show_a_recommended_movie
from Strategies.SimilarUsersStrategy import SimilarUsersStrategy
from Strategies.DirectorStrategy import DirectorStrategy
from Strategies.RatingStrategy import RatingStrategy
from Strategies.StrategyGenre import StrategyGenre
from Strategies.Random import random_films
from Data.parsers import Parsers
from thefuzz import process

# Данные для фильтрации, если пользователь не ввёл фильтры
filter_years = [-1000000000,100000000]
filter_rating = -10
country = ''

def input_country_filter():
    print('----------------------')
    print("Введите название только одной страны")
    print("Пример ввода: США")
    print("Пример ввода: Россия")
    films_data = Parsers.films_parser()
    list_country = []
    for name_film in films_data.keys():
        list_country += films_data[name_film]['countries']
    # print("Список стран:")
    list_country = list(set(list_country))
    country = input("Введите страну: ").strip()
    results = process.extract(country, list_country, limit=5)
    if country not in list_country:
        print("Такой страны не найденно")
        print(f"Возможно вы допустили ошибку в написании, вы имели в виду {results[0][0]}?")
        print()
        print('==============================')
        print("1. Да (Сохранить выбранное значение)",
              "2. Показать список стран",
              "3. Нет (Выйти в главное меню)", sep='\n')
        print('==============================')
        print()
        choice = input("Введите команду: ")
        if choice == "1":
            country = results[0][0]
            return country
        elif choice == "2":
            for number, country in enumerate(list_country, start=1):
                print(f"{number}. {country}")
            return ""
        else:
            return ""
    else:
        return country

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
          "3. Установить страну выпуска"
          "4. Выйти к работе алгоритма",
          "==================================", sep="\n")


# Алгоритм по похожим пользователям
def similar_algorithm(user, users_without_main_user):
    global filter_years
    global filter_rating
    global country
    while 1:
        print('----------------------------')
        print('Алгоритм на основе пользователей')
        print('----------------------------')

        algorithm_menu()

        try:
            user_choice = int(input())

            if user_choice == 1:
                main_strategy = SimilarUsersStrategy(user, users_without_main_user)
                films_list, films_list_little_similar = main_strategy.strategy(filter_years, filter_rating, country)[0], \
                main_strategy.strategy(filter_years, filter_rating, country)[1]
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
                        country = input_country_filter()
                    elif user_choice == 4:
                        break
                    else:
                        print("Некорректный ввод")
            elif user_choice == 3:
                break
            else:
                print("Некорректный ввод")

        except ValueError:
            print("Некорректный ввод")


def director_algorithm(user):
    while True:
        print('----------------------------')
        print('Алгоритм на основе режиссеров')
        print('----------------------------')

        algorithm_menu()

        try:
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
                        print('----------------------')
                        print("Введите название только одной страны")
                        print("Пример ввода: США")
                        print("Пример ввода: Россия")
                        print('Введите страну: ')
                    elif user_choice == 4:
                        break
                    else:
                        print("Некорректный ввод")
            elif user_choice == 3:
                break
            else:
                print("Некорректный ввод")

        except ValueError:
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

def genre_algorithm(user):
    while True:
        print('----------------------')
        print('Алгоритм на основе жанров')
        print('----------------------------')

        algorithm_menu()

        user_choice = int(input())

        if user_choice == 1:
            main_strategy = StrategyGenre(user)
            show_a_recommended_movie(user, main_strategy.strategy())

        elif user_choice == 2:
            while 1:
                print("==================================",
                      "1. Установить года поиска",
                      "2. Установить страну поиска",
                      "3. Выйти к работе алгоритма",
                      "==================================", sep="\n")
                user_choice = int(input("Введите команду: "))
                if user_choice == 1:
                    print('----------------------')
                    min_year = int(input("Введите минимальный год: "))
                    max_year = int(input("Введите максимальный год: "))
                    main_strategy = StrategyGenre(user)
                    show_a_recommended_movie(user, main_strategy.filtered_year(min_year, max_year))
                    print('----------------------')

                elif user_choice == 2:
                    print('----------------------')
                    country = input("Введите страну: ")
                    all_countries = ['Австралия', 'Австрия', 'Алжир', 'Аргентина', 'Армения', 'Багамы', 'Бахрейн',
                    'Беларусь','Бельгия', 'Болгария', 'Бразилия', 'Бруней-Даруссалам', 'Великобритания', 'Венгрия',
                    'Вьетнам','Гамбия', 'Гваделупа', 'Гватемала', 'Германия', 'Германия (ГДР)', 'Германия (ФРГ)', 'Гонконг',
                    'Греция', 'Грузия', 'Дания', 'Джибути', 'Доминикана', 'Египет', 'Замбия', 'Израиль', 'Индия',
                    'Индонезия', 'Иордания', 'Ирак', 'Иран', 'Ирландия', 'Исландия', 'Испания', 'Италия', 'Йемен',
                    'Казахстан', 'Каймановы острова', 'Камбоджа', 'Канада', 'Катар', 'Кения', 'Кипр', 'Китай',
                    'Колумбия', 'Корея Северная', 'Корея Южная', 'Кыргызстан', 'Латвия', 'Ливан', 'Литва',
                    'Лихтенштейн', 'Люксембург', 'Малайзия', 'Мальдивы', 'Мальта', 'Марокко', 'Мексика', 'Молдова',
                    'Монако', 'Нидерланды', 'Новая Зеландия', 'Норвегия', 'ОАЭ', 'Перу', 'Польша', 'Португалия',
                    'Россия', 'Румыния', 'СССР', 'США', 'Саудовская Аравия', 'Северная Македония', 'Сенегал',
                    'Сент-Китс и Невис', 'Сербия', 'Сербия и Черногория', 'Сингапур', 'Словакия', 'Словения',
                    'Таиланд', 'Тайвань', 'Тунис', 'Турция', 'Узбекистан', 'Украина', 'Уругвай', 'Филиппины',
                    'Финляндия', 'Франция', 'Хорватия', 'Чехия', 'Чехословакия', 'Чили', 'Швейцария', 'Швеция',
                    'Эквадор', 'Эстония', 'ЮАР', 'Югославия', 'Югославия (ФР)', 'Япония']
                    if country not in all_countries:
                        print("-------страна не найдена-------")
                    main_strategy = StrategyGenre(user)
                    show_a_recommended_movie(user, main_strategy.filtered_country(country))
                    print('----------------------')

                elif user_choice == 3:
                    break
                else:
                    print("Некорректный ввод")
        elif user_choice == 3:
            break
        else:
            print("Некорректный ввод")

def franchise_algorithm(user):
    while True:
        print('----------------------')
        print('Алгоритм на основе франшиз')
        print('----------------------')
        algorithm_menu()

        try:

            user_choice = int(input())
            if user_choice == 1:
                main_strategy = franchise_algorithm(user)
                show_a_recommended_movie(user, main_strategy.franchise_algorithm())

            elif user_choice == 2:
                break

        except ValueError:
            print("Некорректный ввод")


def multi_algorithm(user, users_without_main_user):
    while True:
        print('----------------------------')
        print('Алгоритм на основе всех стратегий')
        print('----------------------------')

        algorithm_menu()

        try:
            user_choice = int(input())

            director = DirectorStrategy(user.user_name).strategy()
            similar = SimilarUsersStrategy(user, users_without_main_user).strategy()[0]
            rating = RatingStrategy(user.user_name).strategy()

            if user_choice == 1:


                main_strategy = MultiStrategy(user, director, similar, rating)
                show_a_recommended_movie(user, main_strategy.strategy())

            elif user_choice == 2:
                while 1:

                    filter_menu()

                    user_choice = int(input("Введите команду: "))

                    if user_choice == 1:
                        print('----------------------')
                        min_year = int(input("Введите минимальный год: "))
                        max_year = int(input("Введите максимальный год: "))
                        main_strategy = MultiStrategy(user, director*10, similar*12, rating*8)
                        show_a_recommended_movie(user, main_strategy.filtered_year(min_year, max_year))

                        print('----------------------')
                    elif user_choice == 2:
                        print('----------------------')
                        min_rating = int(input("Введите минимальный рейтинг: "))
                        max_rating = int(input("Введите максимальный рейтинг: "))
                        main_strategy = MultiStrategy(user, director, similar, rating)
                        show_a_recommended_movie(user, main_strategy.filtered_year(min_rating, max_rating))
                        print('----------------------')
                    elif user_choice == 3:
                        break
                    else:
                        print("Некорректный ввод")
            elif user_choice == 3:
                break
            else:
                print("Некорректный ввод")

        except ValueError:
            print("Некорректный ввод")


def random_activation(user):
    list_random_films = random_films(user)
    show_a_recommended_movie(user, list_random_films)
