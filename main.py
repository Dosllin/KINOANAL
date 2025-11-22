from strategies import *
import json
import textwrap
from abc import ABC, abstractmethod
from term_image.image import from_url
from parsers import Parsers


users = Parsers.user_parser()
films_data = Parsers.films_parser()


# Определение классов Film и User
class Film:
    def __init__(self, id_film, title, genre, director, year, rating, description, image):
        self.id_film = id_film  # уникальный идентификатор фильма
        self.title = title  # название фильма
        self.genre = genre  # жанр фильма
        self.director = director  # режиссер фильма
        self.year = year  # год выпуска фильма
        self.rating = rating  # список оценок фильма
        self.description = description
        self.image = image

    def __str__(self):
        return f"Film(ID: {self.id_film}, Title: {self.title}, Genre: {self.genre}, Director: {self.director}, Year: {self.year}, Rating: {self.rating})"  # строковое представление фильма для удобства вывода


class User:
    def __init__(self, id_user, user_name, user_viewed_films, user_genre):
        self.id_user = id_user  # уникальный идентификатор пользователя
        self.user_name = user_name  # имя пользователя
        self.user_viewed_films = user_viewed_films  # список просмотренных пользователем фильмов
        self.user_genre = user_genre  # список предпочитаемых жанров пользователя

    def __str__(self):
        return f"User(ID: {self.id_user}, Name: {self.user_name}, Viewed Films: {[film.title for film in self.user_viewed_films]}, Preferred Genre: {self.user_genre})"  # строковое представление пользователя для удобства вывода


# Список всех жанров фильмов
list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                  "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                  "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]


# Менеджер для работы с фильмами и пользователями
class FilmManager:
    def __init__(self, user):
        self.user = user

    def add_film(self, film):
        self.user.user_viewed_films.append(film)  # Добавление фильма в просмотренные пользователем

    @staticmethod
    def add_user_review(film, review):
        film.rating.append(review)  # Добавление оценки к фильму


DirectorStrategy1 = DirectorStrategy("Илья")
print(DirectorStrategy1.strategy())

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


class Strategy_recomendation(ABC):
    def __init__(self, user,other_users):
        self.user = user
        self.other_users = other_users
    @abstractmethod
    def stategy(self):
        pass
class Strategy_similar_users(Strategy_recomendation):
    def __init__(self, user, other_users):
        super().__init__(user,other_users)
    def stategy(self):
        recomendation_films= [] #Финальный список фильмов, которые будут предложены пользователю
        litle_recomendation_films =[] #Финальный список фильмов, которые будут предложены пользователю от менее похожих пользователей
        massive_similar_users = [] # Список людей с кем было совпадение
        for not_main_user in self.other_users.keys(): #Перебираю всех остальных пользователей для того чтобы найти на кого пользватель похож больше всего

            count_genre = 0 #количество совпавших жанров
            matching_genres = []
            matching_films = []  # в будущем те фильмы которые смотрели оба из пользователей я буду удалять, чтобы пользователю не предлагались те фильмы, которые он смотрел

            for genre in self.other_users[not_main_user]['user_genre']: # перебираю жанры другого пользователя и если жанры другого пользователя есть в массиве жанров у главного то счётчик увеличивается на 1
                if genre in user.user_genre:
                    count_genre+=1
                    matching_genres.append(genre)

            count_wached_films = 0 # количество совпавших фильмов
            for film in self.other_users[not_main_user]['user_viewed_films']:  # перебираю просмотренные фильмы другого пользователя и если фильмы другого пользователя есть в массиве просмотренных фильмов у главного то счётчик увеличивается на 1
                if film in user.user_viewed_films:
                    count_wached_films+=1
                    matching_films.append(film)
            massive_similar_users.append([not_main_user,count_genre+count_wached_films,count_genre,count_wached_films,matching_genres,matching_films]) # Добавляю пользователей с кем было совпадение
        massive_similar_users = sorted(massive_similar_users, key=lambda x: x[1], reverse=True) # Сортирую, чтобы сначала были пользователи с большим количеством совпадений
        max_count_similar = max([count_similar[1] for count_similar in massive_similar_users]) # Самое большое количество совпадений

        massive_similar_users = [users for users in massive_similar_users if users[1]>0]  # Беру только пользователей с которыми
        massive_litle_similar_users = [users for users in massive_similar_users if users[1] != max_count_similar and users[1]>0]  # Беру только пользователей с большиим количеством совпадений
        massive_big_similar_users = [users for users in massive_similar_users if users[1] == max_count_similar]  # Беру только пользователей с меньшим количеством совпадений

        # Тут я столкнулся с проблемой, что если максимальное и фильмы один в один, то возвращает пустой список
        # Я исправил это так

        while len(recomendation_films)<1: # пока у нас не будет хотя бы 1 фильм, который можно порекомендовать
            for name in massive_big_similar_users:
                recomendation_films+=users_without_main_user[name[0]]['user_viewed_films'] #Беру фильмы пользователей с кем было совпадение
                for film in user.user_viewed_films: # Удаляю повторы фильмов
                    if film in recomendation_films:
                        recomendation_films.remove(film)
            else:
                if len(massive_litle_similar_users) == 0: # Если в массиве пользователей нет ни одного совпавшего пользователя, то людей с кем сравнить человека нет
                    print("К сожелению таких пользователей нет, вы уникален, попробуйте использовать другую стратегию")
                    return [[],[],[]]

                recomendation_films += users_without_main_user[massive_litle_similar_users[0][0]]['user_viewed_films']  # Беру фильмы пользователей с кем было совпадение
                massive_litle_similar_users = massive_litle_similar_users[1:] # Убираю человека, который стал пользователем с самым большим количеством совпадений, из списка пользователей с маленьким совпадением

                for film in user.user_viewed_films: # удаляю повторы
                    if film in recomendation_films:
                        recomendation_films.remove(film)

        for name in massive_litle_similar_users: # Формирую массив фильмов с маленьким количеством совпадений
            litle_recomendation_films += users_without_main_user[name[0]]['user_viewed_films']  # Беру фильмы пользователей с кем было совпадение
            for film in user.user_viewed_films: # удаляю повторы
                if film in litle_recomendation_films:
                    litle_recomendation_films.remove(film)
        return [recomendation_films,litle_recomendation_films,massive_similar_users]

def film_preview(request): # Функция для отображения фильма. Сюда подаётся название фильма
    global films_data
    print(films_data[request])
    print('=========================================')
    try:
        print(from_url(films_data[request]['image']))
    except request.exceptions.ConnectionError:  # Ошибка, когда не может получить изоброжение по ссылке
        print('Не смогли найти картинку 😥')
    print("Название:", films_data[request]['title'])
    print("Жанр:", films_data[request]['genre'])
    print("Режиссёр:", films_data[request]['director'])
    print("Год выпуска:", films_data[request]['year'])
    print("Описание:")
    print(textwrap.fill(films_data[request]['description'], width=70))  # перенос каждые 70 символов (по пробелам)
    print("Средний рейтинг:",sum(films_data[request]['rating']) / len(films_data[request]['rating']) if films_data[request]['rating'] else "Нет оценок")
    print('=========================================')

def add_in_viewed_films(request): #Добавить фильм в просмотренные и обновить это в базе данных
    global user
    users[user.user_name]['user_viewed_films'].append(request)  # Добавляем название фильма в просмотренные пользователем
    with open(f'user.json', 'w',encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
        json.dump(users, file, indent=4,ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
    print("Фильм добавлен в просмотренные.")



def search_film():
    request = input("Введите название фильма: ").capitalize()
    if request in films_data.keys():
        film_preview(request)
        choice = input().lower()
        if choice == 'да':
            add_in_viewed_films(request)
        input("Введите что-нибудь, чтобы продолжить...")
        return 0
    else:
        print("Фильм не найден")



def login_sign_in():
    global last_id
    global users
    global films_data
    print('1. Войти',
          '2. Зарегистрироваться',
          '3. Выйти из программы', sep='\n')

    choice = input('Выберите действие: ')
    if choice == '1':  # Вход
        name = input('Введите имя: ')
        if name in users.keys():
            print('Добро пожаловать обратно,', name)
            current_user = users[name]
            print(current_user)
            return User(users[name]['id_user'], name, users[name]['user_viewed_films'], users[name]['user_genre'])
        else:
            print('Пользователь не найден. Пожалуйста, зарегистрируйтесь.')
            return 1
    elif choice == '2':
        name = input('Введите Username: ')
        print('Доступные жанры:', ', '.join(list_all_genre))
        preferred_genre = input('Введите предпочитаемые жанры: ').replace(' ','').lower()  # Убираем пробелы и приводим к нижнему регистру

        new_user = User(last_id + 1, name, [], preferred_genre.split(','))  # Создаем нового пользователя
        last_id += 1  # Обновляем последний ID

        users[new_user.user_name] = {
            'id_user': new_user.id_user,
            'name': new_user.user_name,
            'user_viewed_films': new_user.user_viewed_films,
            'user_genre': new_user.user_genre
        }  # Добавляем пользователя в словарь

        with open(f'user.json', 'w', encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
            json.dump(users, file, indent=4, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print('Регистрация успешна.')
        return User(last_id + 1, name, [], preferred_genre.split(',')) #Создаю в классе User нового пользователя по данным которыми он ввёл
    elif choice == '3':
        print('Выход из программы')
        return 0
    else:
        print('Некорректный выбор, попробуйте снова.')
        return 1


Flag_login = 1
while Flag_login==1:
    user = login_sign_in()
    if user != 1:
        Flag_login = 0

users_without_main_user = users.copy()
users_without_main_user.pop(user.user_name)




if len(user.user_viewed_films) == 0:
    print("==================================")
    print("Похоже, вы ещё не добавили просмотренные фильмы. Пожалуйста, найдите и добавьте хотя бы один фильм.")
    input("Нажмите Enter, чтобы продолжить...")
    while len(user.user_viewed_films) == 0:
        search_film()
while True:
    print('------------MAIN MENU------------')
    print("1. Рекомендации от похожих пользователей",
          "5. Добавить просмотренные фильмы"
          "6. Случайные фильмы (Вам будут предложены случайные фильмы и если вы их смотрели то их можно добавить в список просмотренного)",
          "7. Выйти",sep='\n')

    choice_main_menu = input("Выберите действие: ")
    if choice_main_menu == '5':
        search_film()
    elif choice_main_menu  == '1':
        print('----------------------------')
        print('Алгоритм на основе пользователей')
        print('----------------------------')
        main_strategy = Strategy_similar_users(user,users_without_main_user)
        films_list, films_list_litle_similar = main_strategy.stategy()[0],main_strategy.stategy()[1]

        for film in films_list: # перебираю фильмы из списка и показываю их превью
            film_preview(film) # показываю превью фильма
            print("Если вы уже смотрели этот фильм, можете добавить его в список просмотренных")
            user_choice = input("Добавить ? да/нет: ").lower()
            if user_choice == "да":
                add_in_viewed_films(film) # Записываем в бвзу данных, что пользователь уже смотрел этот фильм


        if len(films_list_litle_similar) > 0: # Если у пользователя ещё были фильмы с другими менее похожими людьми, то мы предлогаем показать такие фильмы
            print("Может быть вам интересны ещё фильмы пользователей с кем у вас было меньше совпадений?")
            user_choice = input("Введите да/нет: ").lower()
            if user_choice == 'да':
                for film in films_list_litle_similar:
                    film_preview(film)# показываю превью фильма
                    print("Если вы уже смотрели этот фильм, можете добавить его в список просмотренных")
                    user_choice = input("Добавить ? да/нет: ").lower()
                    if user_choice == "да":
                        add_in_viewed_films(film) # Записываем в бвзу данных, что пользователь уже смотрел этот фильм
            # print("Пользователи с кем у вас были совпадения:")
            # print([name[0] for name in main_strategy.stategy()[2]])


    elif choice_main_menu == '2':
        print('----------------------------')
        print('Алгоритм на основе ваших любимых режиссеров')
        print('----------------------------')
        print()
        User_dir_strategy = DirectorStrategy(user)
        print(User_dir_strategy.strategy())





    elif choice_main_menu == '6':
        pass

    elif choice_main_menu == '7':
        print("Досвидание")
        break
