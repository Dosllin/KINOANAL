import json

class Parsers:
    @staticmethod
    def user_parser():
        with open('Data/user.json', 'r', encoding="UTF-8") as file:  # Открываем файл с пользователями для чтения
            try:
                users = json.load(file)  # Загружаем пользователей из файла в словарь
                return users
            except json.decoder.JSONDecodeError or FileNotFoundError:
                users = {}
                return users
    @staticmethod
    def films_parser():
        with open('Data/films.json', 'r', encoding="UTF-8") as file:  # Открываем файл с фильмами для чтения
            try:
                films_data = json.load(file)  # Загружаем фильмы из файла в словарь
                return films_data
            except json.decoder.JSONDecodeError or FileNotFoundError:
                films_data = {}
                return films_data
