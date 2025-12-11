from Strategies.AbstractStrategy import StrategyRecommendation
from Data.parsers import Parsers


class StrategyFranchise(StrategyRecommendation):
    def __init__(self, user):
        super().__init__(user)
        self.films_data = Parsers.films_parser()
        self.users = Parsers.user_parser()

    # метод для получения любимых жанров(сначала из пользователя, потом из его просмотренных фильмов)
    def get_user_franchises(self):
        user_data = self.users[self.user.user_name]
        viewed_films = user_data["user_viewed_films"] # просмотренные фильмы пользователя

        viewed_franchises = set()  # удаляем дубли
        for film in viewed_films:
            # если фильма нет в базе — пропускаем
            if film not in self.films_data:
                continue
            film_data = self.films_data[film]
            # если нет ключа franchise или он пустой — пропускаем
            if "franchise" not in film_data:
                continue
            if not film_data["franchise"]:
                continue
            viewed_franchises.add(film_data["franchise"])
        return list(viewed_franchises)


    def strategy(self):
        user_franchises = self.get_user_franchises()
        print("Франшизы пользователя:", user_franchises)
        user_viewed = set(self.users[self.user.user_name]["user_viewed_films"])
        recommended_films = []
        # проходим по всем фильмам в базе
        for film_name, film_data in self.films_data.items():
            film_franchise = film_data["franchise"]
            # уже просмотренные - пропускаем или если у фильма нет поля franchise — пропускаем или franchise = ""
            if film_name in user_viewed or "franchise" not in film_data or not film_franchise:
                continue
            # проверяем строгое совпадение франшизы
            if film_franchise in user_franchises:
                recommended_films.append(film_name)
        return recommended_films
