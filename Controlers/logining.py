import json
from Data.parsers import Parsers
from Modules.user import User
from thefuzz import process


list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                    "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                    "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]


def login_sign_in():
    users = Parsers.user_parser()
    # переменная для отслеживания последнего ID пользователя, чтобы при регистрации создавать уникальные ID
    last_id = max([users[user_name]['id_user'] for user_name in users]) if len(users) > 0 else 0
    # В максе ищу самый большой id, чтобы по нему создавать новые, если данных в датабазе нет, то значение равно 0

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
        name = input('Введите Username: ').strip()
        print('Доступные жанры:')
        count = 0

        list_five_genre = []
        for genre in list_all_genre:
            count += 1
            list_five_genre.append(genre)
            if count%5==0:
                print(', '.join(list_five_genre))
                list_five_genre = []
        if len(list_five_genre)%5!=0:
            print(', '.join(list_five_genre[len(list_five_genre)//5:]))

        preferred_genre = []
        Flag = 1
        while len(preferred_genre) <1 or Flag == 1 :
            print('Вводите предпочитаемые жанры по одному, когда вы посчитаете, что добавили все нужные жанры напишите: stop')
            genre = input('Введите 1 предпочитаемый жанр: ')

            if genre.strip().lower() == 'stop':
                Flag = 0
                break

            if genre not in list_all_genre:
                results = process.extract(genre, list_all_genre)
                print()
                print("Жанр с таким названием не был найден")
                print(f"Возможно вы допустили ошибку в написании, вы имели в виду {results[0][0]}?")
                print()
                print('==============================')
                print("1. Да (Добавить данный жанр)",
                      "2. Нет (Продолжить вводить жанры)", sep='\n')
                print('==============================')
                print()
                choice = input("Введите команду: ")
                if choice == "1":
                    preferred_genre.append(results[0][0])
                else:
                    continue
            else:
                preferred_genre.append(genre)

        new_user = User(id_user = last_id + 1, user_name = name, user_viewed_films = [], user_genre = preferred_genre, user_wish_list = [])  # Создаем нового пользователя
        last_id += 1  # Обновляем последний ID

        users[new_user.user_name] = {
            'id_user': new_user.id_user,
            'name': new_user.user_name,
            'user_viewed_films': new_user.user_viewed_films,
            'user_genre': new_user.user_genre,
            'wish_list': new_user.user_wish_list
        }  # Добавляем пользователя в словарь

        with open(f'Data/user.json', 'w', encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписываю его целиком
            json.dump(users, file, indent=4, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print('Регистрация успешна.')
        return User(id_user = last_id + 1, user_name = name, user_viewed_films = [], user_genre = preferred_genre, user_wish_list = []) #Создаю в классе User нового пользователя по данным которыми он ввёл
    elif choice == '3':
        print('Выход из программы')
        return 0
    else:
        print('Некорректный выбор, попробуйте снова.')
        return 1
