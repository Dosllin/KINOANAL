import json
from Data.parsers import Parsers
from Modules.user import User
from Controlers.manager import FilmManager

list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                    "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                    "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]

def menu_account(user):
    users = Parsers.user_parser()  # Загружаем JSON пользователей
    while True:

        print("НЕ РАБОТАЕТ")
        print("НЕ РАБОТАЕТ")
        print("НЕ РАБОТАЕТ")
        print("НЕ РАБОТАЕТ")
        print("НЕ РАБОТАЕТ")

        films_data = Parsers.films_parser()
        user_data = users[user.user_name]

        print("============================",
            "1. Изменить предпочитаемые жанры",
            "2. Изменить историю просмотров",
            "3. Изменить список отложенных",
            "4. Сохранить изменения и выйти в меню",
            "5. Не сохранять и выйти в меню",
            "============================",sep='\n')

        user_choice = input("Выберите действие: ")


        if user_choice == '1':

            print("============================",
                  "1. Удалить предпочитаемый жанр",
                  "2. Добавить предпочитаемый жанр",
                  "3. Выйти назад",
                  "============================", sep='\n')

            user_choice = input("Выберите действие: ")

            if user_choice == '1':

                print("Ваши жанры:", user_data["user_genre"])
                genre_delete = input("Введите жанр для удаления: ")
                if genre_delete in user_data["user_genre"]:
                    user_data["user_genre"].remove(genre_delete)
                    Parsers.user_saver(users)
                    print("Жанр удалён!")
                else:
                    print("Такого жанра нет.")

            elif user_choice == '2':

                print("Доступные жанры:", list_all_genre)
                genre_add = input("Введите жанр для добавления: ")
                if genre_add not in list_all_genre:
                    print("Такого жанра не существует!")
                elif genre_add in user_data["user_genre"]:
                    print("Этот жанр уже добавлен.")
                else:
                    user_data["user_genre"].append(genre_add)
                    Parsers.user_saver(users)
                    print("Жанр добавлен!")

            elif user_choice == '3':
                pass

            else:
                print("Некорректный ввод")


        elif user_choice == '2':
            print("============================",
                  "1. Удалить просмотренный фильм",
                  "2. Добавить просмотренный фильм",
                  "3. Выйти назад",
                  "============================", sep='\n')

            user_choice = input("Выберите действие: ")

            if user_choice == '1':

                print("Просмотренные фильмы:", user_data["user_viewed_films"])
                film = input("Введите фильм для удаления: ")
                if film in user_data["user_viewed_films"]:
                    user_data["user_viewed_films"].remove(film)
                    print("Фильм удалён.")
                else:
                    print("Фильм не найден.")

            elif user_choice == '2':

                film = input("Введите фильм для добавления: ")
                if film in films_data["user_viewed_films"]:
                    user_data["user_viewed_films"].append(film)
                    print("Фильм добавлен.")
                else:
                    print("Фильм не найден.")

            elif user_choice == '3':
                pass
            else:
                print("Некорректный ввод")


        elif user_choice == '3':

            print("============================",
                  "1. Удалить отложенный фильм",
                  "2. Добавить отложенный фильм",
                  "3. Выйти назад",
                  "============================", sep='\n')

            user_choice = input("Выберите действие: ")

            if user_choice == '1':

                print("Список отложенных:", user_data["wish_list"])
                film = input("Введите фильм для удаления: ")
                if film in user_data["wish_list"]:
                    user_data["wish_list"].remove(film)
                    print("Фильм убран из отложенных.")
                else:
                    print("Фильм не найден.")

            elif user_choice == '2':

                film = input("Введите фильм для добавления: ")
                user_data["wish_list"].append(film)
                print("Фильм добавлен в отложенные.")
                if film in films_data["user_viewed_films"]:
                    user_data["wish_list"].append(film)
                    print("Фильм добавлен в отложенные.")
                else:
                    print("Фильм не найден.")

            elif user_choice == '3':
                pass
            else:
                print("Некорректный ввод")


        elif user_choice == '4':
            # user_data
            with open('user.json', 'w', encoding='utf-8') as f:
                json.dump(user, f, ensure_ascii=False, indent=4)
            break

        elif user_choice == '5':
            break


        else:
            print("Некорректный ввод")
            break
