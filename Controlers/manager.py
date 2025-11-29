# Менеджер для работы с фильмами и пользователями
class FilmManager:
    def __init__(self, user):
        self.user = user

    def add_film_in_viewed(self, film):
        self.user.user_viewed_films.append(film)  # Добавление фильма в просмотренные пользователем

    def add_film_in_wish_list(self, film):
        self.user.user_wish_list.append(film)

    @staticmethod
    def add_user_review(film, review):
        film.rating.append(review)  # Добавление оценки к фильму
