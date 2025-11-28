import json
import random
import textwrap
from term_image.image import from_url


from strategies import *
from manager import *
from parsers import Parsers


users = Parsers.user_parser()
films_data = Parsers.films_parser()


# #### Тестовые данные ####
# film1 = Film(1, "Inception", "science fiction", "Christopher Nolan", 2010, [9, 10, 8])
# film2 = Film(2, "The Dark Knight", "action", "Christopher Nolan", 2008, [10, 9, 10])
# film3 = Film(3, "Interstellar", "science fiction", "Christopher Nolan", 2014, [9, 9, 10])
# film4 = Film(4, "Pulp Fiction", "crime", "Quentin Tarantino", 1994, [10, 9, 8])
# film5 = Film(5, "The Shawshank Redemption", "drama", "Frank Darabont", 1994 , [10, 10, 10])
#
# user1 = User(1, "Alice", [film1, film2], "science fiction")
# user2 = User(2, "Bob", [film4], "crime")
#
# manager1 = FilmManager(user1)
# manager1.add_film(film3)
# manager1.add_user_review(film1, 10)
# print(user1)

# переменная для отслеживания последнего ID пользователя, чтобы при регистрации создавать уникальные ID
last_id = max([users[user_name]['id_user'] for user_name in users]) if len(users) > 0 else 0
# В максе ищу самый большой id, чтобы по нему создавать новые, если данных в датабазе нет, то значение равно 0


def film_preview(request: str): # Функция для отображения фильма. Сюда подаётся название фильма
    print(films_data[request])
    print('=========================================')
    try:
        print(from_url(films_data[request]['image']))
    except:  # Ошибка, когда не может получить изоброжение по ссылке
        print('Не смогли найти картинку 😥')
    print("Название:", films_data[request]['title'])
    print("Жанр:", films_data[request]['genre'])
    print("Режиссёр:", films_data[request]['director'])
    print("Год выпуска:", films_data[request]['year'])
    print("Описание:")
    print(textwrap.fill(films_data[request]['description'], width=70))  # перенос каждые 70 символов (по пробелам)
    print("Средний рейтинг:",round(sum(films_data[request]['rating']) / len(films_data[request]['rating']),2) if films_data[request]['rating'] else "Нет оценок")
    print('=========================================')


def add_in_viewed_films(request: str): #Добавить фильм в просмотренные и обновить это в базе данных
    users[user.user_name]['user_viewed_films'].append(request)  # Добавляем название фильма в просмотренные пользователем
    with open(f'Database/user.json', 'w', encoding="UTF-8") as file:  # Открываем файл для записи и я обязательно переписывю его целиком
        json.dump(users, file, indent=5,ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
    print("Фильм добавлен в просмотренные")

def add_in_wish_list(request: str): #Добавить фильм в отложенные и обновить это в базе данных
    users[user.user_name]['wish_list'].append(request)  # Добавляем название фильма в отложенные пользователя
    with open(f'Database/user.json', 'w', encoding="UTF-8") as file:  # Открываем файл для записи и я обязательно переписывю его целиком
        json.dump(users, file, indent=5,ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
    print("Фильм добавлен в отложенные")

def add_rating(request: str, rating: int): #Добавить фильм в отложенные и обновить это в базе данных
    films_data[request]['rating'].append(rating)  # Добавляем Оценку фильма в отложенные пользователем
    with open(f'Database/films.json', 'w',encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
        json.dump(films_data, file, indent=5,ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
    print("Фильм добавлен в отложенные")

def search_film():
    global user
    request = input("Введите название фильма: ").capitalize()
    if request in films_data.keys():
        film_preview(request)
        print("1. Добавить фильм в просмотренные",
              "2. Добавить фильм в отложенные",
              "3. Добавить оценку фильму", sep='\n')
        if len(users[user.user_name]["user_viewed_films"]) > 0: # Если у пользователя нет ни одного фильма не даёт выйти из поиска
            print("4.Выйти из поиска")
        choice = input()
        if choice == '1':
            add_in_viewed_films(request) # Записываю в БД, что пользователь смотрел фильм
        elif choice == '2':
            add_in_wish_list(request) # Записываю в БД, что пользователь хочет посмотреть фильм
        elif choice == '3':
            score = 0 # Создаю здесь, чтобы Pycharm не ругался так правильнее
            flag = 1
            while flag == 1:
                try:
                    score = int(input("Введите оценку от 1 до 10: "))
                    flag = 0
                except ValueError:
                    print("Введите Цифру от 1 до 10!!!!")
            add_rating(request,score)
        elif choice == '4' and len(users[user.user_name]["user_viewed_films"]) > 0:
            return 0
    else:
        print("Фильм не найден")


def login_sign_in():
    global last_id
    print('1. Войти',
          '2. Зарегистрироваться',
          '3. Выйти из программы', sep='\n')

    choice = input('Выберите действие: ')
    if choice == '1':  # Вход
        name = input('Введите имя: ').strip()
        if name in users.keys(): # Ищем имя в базе данных
            print('Добро пожаловать обратно,', name)
            current_user = users[name]
            print(current_user)
            return User(id_user = users[name]['id_user'], user_name = name, user_viewed_films = users[name]['user_viewed_films'], user_genre = users[name]['user_genre'], user_wish_list = users[name]['wish_list'])
        else:
            print('Пользователь не найден. Пожалуйста, зарегистрируйтесь.')
            return 1
    elif choice == '2':
        name = input('Введите Username: ')
        print('Доступные жанры:', ', '.join(list_all_genre))
        preferred_genre = input('Введите предпочитаемые жанры: ').replace(' ','').lower()  # Убираем пробелы и приводим к нижнему регистру

        new_user = User(id_user = last_id + 1, user_name = name, user_viewed_films = [], user_genre = preferred_genre.split(','), user_wish_list = [])  # Создаем нового пользователя
        last_id += 1  # Обновляем последний ID

        users[new_user.user_name] = {
            'id_user': new_user.id_user,
            'name': new_user.user_name,
            'user_viewed_films': new_user.user_viewed_films,
            'user_genre': new_user.user_genre,
            'wish_list': new_user.user_wish_list
        }  # Добавляем пользователя в словарь

        with open(f'Database/user.json', 'w', encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
            json.dump(users, file, indent=4, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print('Регистрация успешна.')
        return User(id_user = last_id + 1, user_name = name, user_viewed_films = [], user_genre = preferred_genre.split(','), user_wish_list = []) #Создаю в классе User нового пользователя по данным которыми он ввёл
    elif choice == '3':
        print('Выход из программы')
        return 0
    else:
        print('Некорректный выбор, попробуйте снова.')
        return 1

# Данные для фильтрации, если пользователь не ввёл фильтры
filter_years = [-1000000000,100000000]
filter_rating = -10

def show_a_recommended_movie(list_movies: list):
    for film in list_movies:
        film_preview(film)
        print("1. Следующий фильм"
              "2. Добавить фильм в просмотренные",
              "3. Добавить фильм в отложенные",
              "4. Выйти из подборки", sep='\n')
        choice = input("Введите команду: ")
        if choice == "1":
            continue
        elif choice == '2':
            add_in_viewed_films(film)  # Добавляем в просмотренные
        elif choice == '3':
            add_in_wish_list(film)  # Добавляем в отложенные
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
                # print("Пользователи с кем у вас были совпадения:")
                # print([name[0] for name in main_strategy.stategy()[2]])

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


def random_films():
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
            add_in_viewed_films(film)
        elif choice == '3':
            add_in_wish_list(film)
        elif choice == '4':
            break


### MAIN MENU
Flag_login = 1
user = 0 # Просто для того, чтобы pycharm не ругался
while Flag_login==1:
    user = login_sign_in()
    if user != 1:
        Flag_login = 0


users_without_main_user = users.copy()
users_without_main_user.pop(user.user_name)

manager = FilmManager(user)

if len(users[user.user_name]["user_viewed_films"]) == 0:
    print("==================================")
    print("Похоже, вы ещё не добавили просмотренные фильмы. Пожалуйста, найдите и добавьте хотя бы один фильм.")
    input("Нажмите Enter, чтобы продолжить...")
    while len(users[user.user_name]["user_viewed_films"]) == 0:
        search_film()
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
        search_film()
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
        search_film()

    elif choice_main_menu == '7':
        random_films()

    elif choice_main_menu == '8':
        print("Досвидание!")
        break
