from Strategies.AbstractStrategy import StrategyRecommendation
from Data.parsers import Parsers



"""
распаковка джейсона в список тапмлов формата (фильм, рейтинг)
и отсортировать по рейтингу через лямбда
"""
class RatingStrategy(StrategyRecommendation):
    def __init__(self, user): #Строго по БД
        super().__init__(user)
        self.films_data = Parsers.films_parser()

    # основной метод
    def strategy(self):
        # создаём список формата (фильм, средний рейтинг)
        films_ratings = []
        for film_name, film_data in self.films_data.items():
            average_rating = sum(film_data["rating"]) / len(film_data["rating"])
            films_ratings.append((film_name, average_rating))
        # сортируем список по параметру: "средний рейтинг" по его убыванию
        sorted_list = sorted(films_ratings, key=lambda x: x[1], reverse=True)
        # возвращаем список фильмов формата [фильм1, фильм2 ...]
        return list(map(lambda x: x[0], sorted_list))

    # метод сортировки по минимальному и максимальному году
    def filtered_year(self,min_year=0, max_year=9999):
        return list(filter(lambda x: min_year <= self.films_data[x]['year'] <= max_year, self.strategy()))

    def filtered_country(self, country):
        return list(filter(lambda x: country in self.films_data[x]["countries"], self.strategy()))

