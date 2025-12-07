from abc import abstractmethod, ABC
from Data.parsers import Parsers
from collections import Counter


class StrategyRecommendation(ABC):
    def __init__(self, user):
        self.user = user
    @abstractmethod
    def strategy(self):
        pass

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
            print(strat)
        counts = list(Counter(films_list).items())
        sorted_counts = sorted(counts, key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], sorted_counts))[:15]

    def filtered_year(self, min_year=0, max_year=9999):
        sorted_list = self.strategy()
        return list(filter(lambda x: min_year <= self.films_data[x]['year'] <= max_year, sorted_list))

    def filtered_rating(self, min_rating=0, max_rating=10):
        sorted_list = self.strategy()
        return list(filter(lambda x: min_rating <= sum(self.films_data[x]["rating"]) / len(self.films_data[x]["rating"]) <= max_rating, sorted_list))