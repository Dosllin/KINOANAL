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
    def get_user_franchises(self):
        user_data = self.users[self.user.user_name]
        viewed_films = user_data["user_viewed_films"] # просмотренные фильмы пользователя

        viewed_franchises = []

        for film in viewed_films:
            viewed_franchises.append(self.films_data[film]["franchise"])

        return viewed_franchises


    def strategy(self):
        user_franchises = self.get_user_franchises()
        user_viewed = set(self.users[self.user.user_name]["user_viewed_films"])  # для удаления уже просмотренных

        recommended_films = []

        for franchise in user_franchises:

            for film_name, film_data in self.films_data.items():
                # не рекомендуем то, что пользователь уже видел
                if film_name in user_viewed:
                    continue
                # если фильм есть во франшизе, добавляем
                if franchise in film_data["franchises"]:
                    recommended_films.append(film_name)

        return recommended_films