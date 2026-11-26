from Strategies.AbstractStrategy import RankedStrategy
from Data.parsers import Parsers



"""
распаковка джейсона в список тапмлов формата (фильм, рейтинг)
и отсортировать по рейтингу через лямбда
"""
class RatingStrategy(RankedStrategy):
    def __init__(self, user): #Строго по БД
        super().__init__(user)
        self.films_data = Parsers.films_parser()

    # основной метод
    def ranked_films(self):
        # создаём список формата (фильм, средний рейтинг)
        films_ratings = []
        for film_name, film_data in self.films_data.items():
            average_rating = sum(film_data["rating"]) / len(film_data["rating"])
            films_ratings.append((film_name, average_rating))
        # сортируем список по параметру: "средний рейтинг" по его убыванию
        sorted_list = sorted(films_ratings, key=lambda x: x[1], reverse=True)
        # возвращаем список фильмов формата [фильм1, фильм2 ...]
        return list(map(lambda x: x[0], sorted_list))
