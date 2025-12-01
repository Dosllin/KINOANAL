from Data.parsers import Parsers
import json

users = Parsers.user_parser()
films_data = Parsers.films_parser()

# Менеджер для работы с фильмами и пользователями
class FilmManager:
    def __init__(self, user):
        self.user = user

    def add_in_viewed_films(self, request: str):  # Добавить фильм в просмотренные и обновить это в базе данных
        users[self.user.user_name]['user_viewed_films'].append(request)  # Добавляем название фильма в просмотренные пользователем
        with open(f'Data/user.json', 'w', encoding="UTF-8") as file:  # Открываем файл для записи и я обязательно переписывю его целиком
            json.dump(users, file, indent=5, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print("Фильм добавлен в просмотренные")

    def add_in_wish_list(self, request: str):  # Добавить фильм в отложенные и обновить это в базе данных
        users[self.user.user_name]['wish_list'].append(request)  # Добавляем название фильма в отложенные пользователя
        with open(f'Data/user.json', 'w', encoding="UTF-8") as file:  # Открываем файл для записи и я обязательно переписывю его целиком
            json.dump(users, file, indent=5, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print("Фильм добавлен в отложенные")

    @staticmethod
    def add_rating(request: str, rating: int):  # Добавить фильм в отложенные и обновить это в базе данных
        films_data[request]['rating'].append(rating)  # Добавляем Оценку фильма в отложенные пользователем
        with open(f'Data/films.json', 'w', encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
            json.dump(films_data, file, indent=5, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print("Фильм добавлен в отложенные")
