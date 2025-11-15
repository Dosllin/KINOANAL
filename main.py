import json
from random import randint


# Определение классов Film и User
class Film:
    def __init__(self, id_film, title, genre, director, year, rating):
        self.id_film = id_film  # уникальный идентификатор фильма
        self.title = title  # название фильма
        self.genre = genre  # жанр фильма
        self.director = director  # режиссер фильма
        self.year = year  # год выпуска фильма
        self.rating = rating  # список оценок фильма

    def __str__(self):
        return f"Film(ID: {self.id_film}, Title: {self.title}, Genre: {self.genre}, Director: {self.director}, Year: {self.year}, Rating: {self.rating})"  # строковое представление фильма для удобства вывода


class User:
    def __init__(self, id_user, name, user_viewed_films, user_genre):
        self.id_user = id_user  # уникальный идентификатор пользователя
        self.name = name  # имя пользователя
        self.user_viewed_films = user_viewed_films  # список просмотренных пользователем фильмов
        self.user_genre = user_genre  # список предпочитаемых жанров пользователя

    def __str__(self):
        return f"User(ID: {self.id_user}, Name: {self.name}, Viewed Films: {[film.title for film in self.user_viewed_films]}, Preferred Genre: {self.user_genre})"  # строковое представление пользователя для удобства вывода


# Список всех жанров фильмов
list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                  "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                  "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]


# Менеджер для работы с фильмами и пользователями
class FilmManager():
    def __init__(self, user):
        self.user = user

    def add_film(self, film):
        self.user.user_viewed_films.append(film)  # Добавление фильма в просмотренные пользователем

    @staticmethod
    def add_user_review(film, review):
        film.rating.append(review)  # Добавление оценки к фильму


# Словарь для хранения пользователей
with open('user.json', 'r', encoding="UTF-8") as file:  # Открываем файл с пользователями для чтения
    users = json.load(file)  # Загружаем пользователей из файла в словарь

# Словарь для хранения фильмов
with open('films.json', 'r', encoding="UTF-8") as file:  # Открываем файл с фильмами для чтения
    films_data = json.load(file)  # Загружаем фильмы из файла в словарь

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


last_id = 0  # переменная для отслеживания последнего ID пользователя, чтобы при регистрации создавать уникальные ID

while True:
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
        else:
            print('Пользователь не найден. Пожалуйста, зарегистрируйтесь.')
    elif choice == '2':
        name = input('Введите имя: ')
        print('Доступные жанры:', ', '.join(list_all_genre))
        preferred_genre = input('Введите предпочитаемые жанры: ').replace(' ',
                                                                          '').lower()  # Убираем пробелы и приводим к нижнему регистру
        new_user = User(last_id + 1, name, [], preferred_genre.split(','))  # Создаем нового пользователя
        last_id += 1  # Обновляем последний ID
        users[new_user.name] = {
            'id_user': new_user.id_user,
            'name': new_user.name,
            'user_viewed_films': new_user.user_viewed_films,
            'user_genre': new_user.user_genre
        }  # Добавляем пользователя в словарь
        with open(f'user.json', 'w',
                  encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
            json.dump(users, file, indent=4, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print('Регистрация успешна.')
    elif choice == '3':
        print('Выход из программы')
        break
    else:
        print('Некорректный выбор, попробуйте снова.')
