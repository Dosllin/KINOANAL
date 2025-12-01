import json
from Data.parsers import Parsers
from Modules.user import User

users = Parsers.user_parser()
films_data = Parsers.films_parser()

list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                    "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                    "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]

# переменная для отслеживания последнего ID пользователя, чтобы при регистрации создавать уникальные ID
last_id = max([users[user_name]['id_user'] for user_name in users]) if len(users) > 0 else 0
# В максе ищу самый большой id, чтобы по нему создавать новые, если данных в датабазе нет, то значение равно 0

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
        name = input('Введите Username: ').strip()
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

        with open(f'Data/user.json', 'w', encoding="UTF-8") as file:  # открываем файл для записи и я обязательно переписывю его целиком
            json.dump(users, file, indent=4, ensure_ascii=False)  # Сохраняем обновленный словарь пользователей в файл, indent - отступы для читаемости, ensure_ascii=False - для поддержки кириллицы
        print('Регистрация успешна.')
        return User(id_user = last_id + 1, user_name = name, user_viewed_films = [], user_genre = preferred_genre.split(','), user_wish_list = []) #Создаю в классе User нового пользователя по данным которыми он ввёл
    elif choice == '3':
        print('Выход из программы')
        return 0
    else:
        print('Некорректный выбор, попробуйте снова.')
        return 1