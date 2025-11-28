from dataclasses import dataclass, field
from typing import List

# Список всех жанров фильмов
list_all_genre = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "fantasy",
                  "historical", "horror", "musical", "mystery", "romance", "science fiction", "thriller",
                  "war", "western", "family", "film noir", "coming-of-age", "superhero", "psychological", "satire"]


# Определение классов Film и User
# Определение класса Film
@dataclass(kw_only=True)
class Film:
    id_film: int
    title: str
    genre: List[str] = field(default_factory=list)
    director: str
    year: int
    rating: List[int] = field(default_factory=list)
    description: str
    image: str

# Определение класса User
@dataclass(kw_only=True)
class User:
    id_user: int
    user_name: str
    user_viewed_films: List[str] = field(default_factory=list)
    user_genre: List[str] = field(default_factory=list)
    user_wish_list: List[str] = field(default_factory=list)


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
