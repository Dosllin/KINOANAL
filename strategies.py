from parsers import Parsers

users = Parsers.user_parser()
films_data = Parsers.films_parser()

"""
распаковка джейсона в список тапмлов типа (фильм, рейтинг)
и отсортировать по рейтингу через лямбда
"""

class RatingStrategy:
    @staticmethod
    def strategy():
        films_and_ratings = []
        for film_name, film_data in films_data.items():
            film_rating = film_data["rating"]
            average_film_rating = sum(film_rating) / len(film_rating)
            films_and_ratings.append((film_name, average_film_rating))
        sorted_list = sorted(films_and_ratings, key=lambda x: x[1], reverse=True)
        return sorted_list[:3]
"""
посчитать всех режиссеров которые смотрел пользователь, загнать в словарь:
пользователь:{
    режиссер1: количество фильмов от него
    режиссер2: количество фильмов от него
}
для этого нужен тапл типа: ((пользователь, [режиссеры])) или словарь такого типа
отсортировать их по количеству не трогая пользователя
на основе максимального количества просмотров у определенного режиссера выдать фильмы того же режиссера 
"""
class DirectorStrategy:
    def __init__(self, picked_name:str): #Строго по БД
        self.picked_name = picked_name
    @staticmethod
    def _director_parser():
        directors_dict = {}
        for film_name, film_data in films_data.items():
            directors_dict[film_name] = film_data["director"]
        return directors_dict
    @staticmethod
    def _film_parser():
        dict_of_films = {}
        for user_name, user_data in users.items():
            dict_of_films[user_name] = user_data["user_viewed_films"]
        return dict_of_films

    def _transformation_of_data(self):
        directors_dict = self._director_parser()
        dict_of_films = self._film_parser()

        new_dict_directors = {}
        for user_name, user_films in dict_of_films.items():
            new_dict_directors[user_name] = []
            for user_film in user_films:
                for key, value in directors_dict.items():
                    if user_film == key:
                        new_dict_directors[user_name].append(value)

        directors_counter = {}
        for user_name, list_directors in new_dict_directors.items():
            directors_counter[user_name] = []
            for director in list_directors:
                counter = list_directors.count(director)
                directors_counter[user_name].append((director, counter))

        sorted_directors_counter = None
        for user_name, list_of_directors in directors_counter.items():
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
                    if fav_list[-1][1] != fav_list[-2][1]:
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


