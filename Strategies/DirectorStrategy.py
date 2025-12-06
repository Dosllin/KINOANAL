from Data.parsers import Parsers
from abc import ABC, abstractmethod

"""
посчитать всех режиссеров которые смотрел пользователь, загнать в словарь:
пользователь:{
    режиссер1: количество фильмов от него
    режиссер2: количество фильмов от него
}
для этого нужен тапл формата: ((пользователь, [режиссеры])) или словарь такого формата
отсортировать их по количеству не трогая пользователя
на основе максимального количества просмотров у определенного режиссера выдать фильмы того же режиссера 
"""
class StrategyRecommendation(ABC):
    def __init__(self, user):
        self.user = user
    @abstractmethod
    def strategy(self):
        pass

class DirectorStrategy(StrategyRecommendation):
    def __init__(self, user:str): #Строго по БД
        super().__init__(user)
        self.picked_name = user # записываем имя пользователя
        self.users = Parsers.user_parser()
        self.films_data = Parsers.films_parser()

    # данный метод создаёт словарь формата {фильм:режиссер}

    def _director_parser(self):
        directors_dict = {}
        for film_name, film_data in self.films_data.items():
            directors_dict[film_name] = film_data["director"]
        return directors_dict

    # данный метод создаёт словарь формата {пользователь:[просмотренные фильмы]}

    def _film_parser(self):
        dict_of_films = {}
        for user_name, user_data in self.users.items():
            dict_of_films[user_name] = user_data["user_viewed_films"]
        return dict_of_films


    # данный метод преобразовывает данные для работы с ними
    def _transformation_of_data(self):
        # передаем словари созданные до этого
        directors_dict = self._director_parser()
        dict_of_films = self._film_parser()
        # создаем словарь формата {пользователь:[режиссеры которых смотрел пользователь]}
        new_dict_directors = {}
        for user_name, user_films in dict_of_films.items():
            if user_name == self.picked_name:
                new_dict_directors[user_name] = list(map(lambda x: directors_dict[x], user_films))

        ### можно ускорить
        # создаем словарь формата {пользователь: [(режиссер, количество просмотров режиссера), ...]}
        directors_counter = {}
        for user_name, list_directors in new_dict_directors.items():
            directors_counter[user_name] = []
            for director in list_directors:
                counter = list_directors.count(director)
                directors_counter[user_name].append((director, counter))

        # распаковываем прошлый словарь в формат (пользователь, [(режиссер, количество просмотров режиссера), ...])
        # а так же сортируем по параметру: "количество просмотров режиссера"
        sorted_directors_counter = None
        for user_name, list_of_directors in directors_counter.items():
            print(user_name, self.picked_name)
            if user_name == self.picked_name:
                sorted_directors_counter = (user_name, sorted(set(list_of_directors), key=lambda x: x[1], reverse=True))
                break
        return sorted_directors_counter

    def strategy(self):
        film_directors_dict = self._director_parser()
        dict_films = self._film_parser()
        sorted_directors_counter = self._transformation_of_data()
        if sorted_directors_counter[1] != []:
            fav_list = []
            maximal_value = max(sorted_directors_counter[1], key=lambda x: x[1])[1]
            while True:
                if len(sorted_directors_counter[1]) > 1 and sorted_directors_counter[1][0][1] == maximal_value:
                    fav_director = max(sorted_directors_counter[1], key=lambda x: x[1])
                    fav_list.append(fav_director)
                    sorted_directors_counter[1].remove(fav_director)
                else:
                    fav_director = max(sorted_directors_counter[1], key=lambda x: x[1])
                    fav_list.append(fav_director)
                    if len(fav_list) == 1:
                        break
                    elif fav_list[-1][1] != fav_list[-2][1]:
                        fav_list.remove(fav_list[-1])
                    break

            list_recommend = []
            for name_of_film, director in film_directors_dict.items():
                for fav_director in fav_list:
                    if (director == fav_director[0]) and (name_of_film not in dict_films[self.picked_name]):
                        list_recommend.append(name_of_film)

        else:
            return "История просмотров пуста"

        return list_recommend

    def filtered_year(self, min_year=0, max_year=9999):
        strategy = DirectorStrategy(self.picked_name)
        sorted_list = strategy.strategy()
        return list(filter(lambda x: min_year <= self.films_data[x]['year'] <= max_year, sorted_list))
    def filtered_rating(self, min_rating=0, max_rating=10):
        strategy = DirectorStrategy(self.picked_name)
        sorted_list = strategy.strategy()
        return list(filter(lambda x: min_rating <= sum(self.films_data[x]["rating"]) / len(self.films_data[x]["rating"]) <= max_rating, sorted_list))
      
