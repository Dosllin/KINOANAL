from Strategies.AbstractStrategy import StrategyRecommendation
from Data.parsers import Parsers
from collections import Counter


class MultiStrategy(StrategyRecommendation):
    def __init__(self, user: str, *strats):
        super().__init__(user)
        self.films_data = Parsers.films_parser()
        self.user = user
        self.strats = strats

    def strategy(self):
        films_list = []
        for strat in self.strats:
            films_list += strat
        counts = list(Counter(films_list).items())
        sorted_counts = sorted(counts, key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], sorted_counts))[:15]

    def filtered_year(self, min_year=0, max_year=9999):
        return list(filter(lambda x: min_year <= self.films_data[x]['year'] <= max_year, self.strategy()))

    def filtered_rating(self, min_rating=0, max_rating=10):
        return list(filter(lambda x: min_rating <= sum(self.films_data[x]["rating"]) / len(self.films_data[x]["rating"]) <= max_rating, self.strategy()))

    def filtered_country(self, country):
        return list(filter(lambda x: country in self.films_data[x]["countries"], self.strategy()))
