from abc import ABC, abstractmethod
from Data.parsers import Parsers


class StrategyRecommendation(ABC):
    def __init__(self, user):
        self.user = user
    @abstractmethod
    def strategy(self):
        pass


class StrategyGenre(StrategyRecommendation):
    def __init__(self, user):
        super().__init__(user)
        self.films_data = Parsers.films_parser()
        self.users = Parsers.user_parser()

    # метод для получения любимых жанров(сначала из пользователя, потом из его просмотренных фильмов)
    def get_user_favourite_genres(self):
        user_data = self.users[self.user.user_name]
        liked_genres = user_data["user_genre"] # любимые жанры пользователя
        viewed_films = user_data["user_viewed_films"] # просмотренные фильмы пользователя
        viewed_genres = {}
        for film in viewed_films:
            for genre in self.films_data[film]["genre"]:
                viewed_genres[genre] = viewed_genres.get(genre, 0) + 1
        sorted_viewed_genres = sorted(viewed_genres.items(), key=lambda x: x[1], reverse=True) # рассортированные по частоте просмотра жанры
        favourite_genres = []
        for genre in liked_genres:
            favourite_genres.append(genre)
        for genre, _ in sorted_viewed_genres:
            if genre not in favourite_genres:
                favourite_genres.append(genre)
        return favourite_genres

    def strategy(self):
        # user_data = self.users[self.user.user_name] мб
        favourite_genres = self.get_user_favourite_genres()
        user_viewed = set(self.users[self.user.user_name]["user_viewed_films"]) # для удаления уже просмотренных

        recommendation_films = []
        film_scores = {}

        # нумерация по id, id_num в обратку, чем первее жанр в списке, тем больше id
        for id, genre in enumerate(favourite_genres):
            id_num = len(favourite_genres) - id
            # идем по списку фильмов
            for film_name, film_data in self.films_data.items():
                # не рекомендуем то, что пользователь уже видел
                if film_name in user_viewed:
                    continue
                # если фильм содержит этот жанр, то прибавляем очки
                if genre in film_data["genre"]:
                    film_scores[film_name] = film_scores.get(film_name, 0) + id_num

        # если подходящих фильмов нет
        if not film_scores:
            return []

        # сортируем фильмы по убыванию очков и берём топ-10
        sorted_films = sorted(film_scores.items(), key=lambda x: x[1], reverse=True)[:10]

        return list(film for film, score in sorted_films)

    # сортировка по минимальному и максимальному году
    def filtered_year(self, min_year=0, max_year=9999):
        sorted_list = self.strategy()
        return list(filter(lambda x: min_year <= self.films_data[x]['year'] <= max_year, sorted_list))

    def filtered_country(self, country=''):
        sorted_list = self.strategy()
        return [film for film in sorted_list if country in self.films_data[film]["countries"]]
