# Список всех жанров фильмов
list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                  "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                  "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]


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


# Менеджер для работы с фильмами и пользователями
class FilmManager:
    def __init__(self, user):
        self.user = user

    def add_film(self, film):
        self.user.user_viewed_films.append(film)  # Добавление фильма в просмотренные пользователем

    @staticmethod
    def add_user_review(film, review):
        film.rating.append(review)  # Добавление оценки к фильму