from Strategies.AbstractStrategy import RankedStrategy
from Data.parsers import Parsers
from collections import Counter


class MultiStrategy(RankedStrategy):
    limit = 15

    def __init__(self, user: str, *strats):
        super().__init__(user)
        self.films_data = Parsers.films_parser()
        self.user = user
        self.strats = strats

    def ranked_films(self):
        films_list = []
        for strat in self.strats:
            films_list += strat
        counts = list(Counter(films_list).items())
        sorted_counts = sorted(counts, key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], sorted_counts))
