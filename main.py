from random import randint
# Определение классов Film и User
class Film:
    def __init__(self, id_film, title, genre, director, year, rating):
        self.id_film = id_film
        self.title = title
        self.genre = genre
        self.director = director
        self.year = year
        self.rating = rating
        self.__observers = []

    def __str__(self):
        return f"Film(ID: {self.id_film}, Title: {self.title}, Genre: {self.genre}, Director: {self.director}, Year: {self.year}, Rating: {self.rating})"


class User:
    def __init__(self, id_user, name, user_viewed_films, user_genre):
        self.id_user = id_user
        self.name = name
        self.user_viewed_films = user_viewed_films
        self.user_genre = user_genre

    def __str__(self):
        return f"User(ID: {self.id_user}, Name: {self.name}, Viewed Films: {[film.title for film in self.user_viewed_films]}, Preferred Genre: {self.user_genre})"

# Список всех жанров фильмов
list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                  "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                  "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]
# Менеджер для работы с фильмами и пользователями
class FilmManager():
    def __init__(self,user):
        self.user = user

    def add_film(self, film):
        self.user.user_viewed_films.append(film)

    @staticmethod
    def add_user_review(film, review):
        film.rating.append(review)


users = {

}#Сюда добавлять пользователей при регистрации



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
last_id = 0 # переменная для отслеживания последнего ID пользователя, чтобы при регистрации создавать уникальные ID
while True:
    print('1. Войти',
          '2. Зарегистрироваться',
          '3. Выйти из программы', sep='\n')

    choice = input('Выберите действие: ')
    if choice == '1':
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
        preferred_genre = input('Введите предпочитаемые жанры: ').replace(' ','').lower()
        new_user = User(last_id+1, name, [], preferred_genre.split(','))
        print(new_user)
        users[new_user.name] = new_user


    elif choice == '3':
        print('Выход из программы')
        break
    else:
        print('Некорректный выбор, попробуйте снова.')
