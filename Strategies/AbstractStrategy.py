from abc import ABC, abstractmethod

class StrategyRecommendation(ABC):
    def __init__(self, user):
        self.user = user
    @abstractmethod
    def strategy(self):
        pass


class RankedStrategy(StrategyRecommendation):
    limit = None

    @abstractmethod
    def ranked_films(self):
        pass

    def strategy(self, years=None, rating=None, country=""):
        result = []
        for title in self.ranked_films():
            film = self.films_data[title]
            if years and not years[0] <= film["year"] <= years[1]:
                continue
            if country and country not in film["countries"]:
                continue
            if rating:
                scores = film["rating"]
                if not scores or not rating[0] <= sum(scores) / len(scores) <= rating[1]:
                    continue
            result.append(title)
            if len(result) == self.limit:
                break
        return result

    def filtered_year(self, min_year=0, max_year=9999):
        return self.strategy(years=(min_year, max_year))

    def filtered_country(self, country=""):
        return self.strategy(country=country)

    def filtered_rating(self, min_rating=0, max_rating=10):
        return self.strategy(rating=(min_rating, max_rating))
