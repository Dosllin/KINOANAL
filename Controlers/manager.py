from Data.parsers import Parsers
from Modules.user import User
from Modules.film import Film
import json



# Менеджер для работы с фильмами и пользователями
class FilmManager:

    def __init__(self, user):
        self.user = user
        self.users = Parsers.user_parser()
        self.films_data = Parsers.films_parser()

    def add_in_viewed_films(self, request: str):  # Добавить фильм в просмотренные и обновить это в базе данных
        self.users[self.user.user_name]['user_viewed_films'].append(request)  # Добавляем название фильма в просмотренные пользователем
        self.user.user_viewed_films.append(request)
        with open(f'Data/user.json', 'w', encoding="UTF-8") as file:  # Открываем файл для записи и я обязательно переписывю его целиком
            json.dump(self.users, file, indent=5, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print("Фильм добавлен в просмотренные")

    def add_in_wish_list(self, request: str):  # Добавить фильм в отложенные и обновить это в базе данных
        self.users[self.user.user_name]['wish_list'].append(request)  # Добавляем название фильма в отложенные пользователя
        self.user.user_wish_list.append(request)
        with open(f'Data/user.json', 'w', encoding="UTF-8") as file:  # Открываем файл для записи и я обязательно переписывю его целиком
            json.dump(self.users, file, indent=5, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print("Фильм добавлен в отложенные")

    def add_rating(self, request: str, rating: int):  # Добавить фильм в отложенные и обновить это в базе данных
        self.films_data[request]['rating'].append(rating)  # Добавляем Оценку фильма в отложенные пользователем
        with open(f'Data/films.json', 'w', encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
            json.dump(self.films_data, file, indent=5, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print("Фильм добавлен в отложенные")
