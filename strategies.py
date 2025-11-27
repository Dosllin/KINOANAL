from parsers import Parsers
from abc import ABC, abstractmethod

users = Parsers.user_parser()
films_data = Parsers.films_parser()

class StrategyRecommendation(ABC):
    def __init__(self, user):
        self.user = user
    @abstractmethod
    def strategy(self):
        pass

"""
распаковка джейсона в список тапмлов типа (фильм, рейтинг)
и отсортировать по рейтингу через лямбда
"""

class RatingStrategy:
    @staticmethod
    def strategy():
        films_ratings = []
        for film_name, film_data in films_data.items():
            average_rating = sum(film_data["rating"]) / len(film_data["rating"])
            films_ratings.append((film_name, average_rating))
        sorted_list = sorted(films_ratings, key=lambda x: x[1], reverse=True)[:10]
        return list(map(lambda x: x[0], sorted_list))
    @staticmethod
    def filtered_year(min_year=0, max_year=9999):
        sorted_list = RatingStrategy.strategy()
        return list(filter(lambda x: min_year <= films_data[x]['year'] <= max_year, sorted_list))



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
class DirectorStrategy(StrategyRecommendation):
    def __init__(self, user): #Строго по БД
        super().__init__(user)
        self.picked_name = user

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
            if user_name == self.picked_name:
                new_dict_directors[user_name] = list(map(lambda x: directors_dict[x], user_films))

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
        return list(filter(lambda x: min_year <= films_data[x]['year'] <= max_year, sorted_list))
    def filtered_rating(self, min_rating=0, max_rating=10):
        strategy = DirectorStrategy(self.picked_name)
        sorted_list = strategy.strategy()
        return list(filter(lambda x: min_rating <= sum(films_data[x]["rating"]) / len(films_data[x]["rating"]) <= max_rating, sorted_list))



class StrategySimilarUsers(StrategyRecommendation):
    def __init__(self, user, other_users):
        super().__init__(user)
        self.other_users = other_users

    def similar(self,massive_similar_users):
        for not_main_user in self.other_users.keys(): #Перебираю всех остальных пользователей для того чтобы найти на кого пользователь похож больше всего

            count_genre = 0 # Количество совпавших жанров
            matching_genres = []
            matching_films = []  # в будущем те фильмы которые смотрели оба из пользователей я буду удалять, чтобы пользователю не предлагались те фильмы, которые он смотрел

            for genre in self.other_users[not_main_user]['user_genre']:  # перебираю жанры другого пользователя и если жанры другого пользователя есть в массиве жанров у главного то счётчик увеличивается на 1
                if genre in self.user.user_genre:
                    count_genre+=1
                    matching_genres.append(genre)

            count_watched_films = 0 # количество совпавших фильмов
            for film in self.other_users[not_main_user]['user_viewed_films']:  # перебираю просмотренные фильмы другого пользователя и если фильмы другого пользователя есть в массиве просмотренных фильмов у главного то счётчик увеличивается на 1
                if film in self.user.user_viewed_films:
                    count_watched_films+=1
                    print(film,films_data[film]['year'])
                    matching_films.append(film)
            massive_similar_users.append([not_main_user,count_genre+count_watched_films,count_genre,count_watched_films,matching_genres,matching_films]) # Добавляю пользователей с кем было совпадение
        return massive_similar_users

    def strategy(self, filter_years=None, filter_rating=-10):
        if filter_years is None:
            filter_years =  [-10000000,10000000]
        recommendation_films= [] #Финальный список фильмов, которые будут предложены пользователю
        little_recommendation_films =[] #Финальный список фильмов, которые будут предложены пользователю от менее похожих пользователей
        massive_similar_users = [] # Список людей с кем было совпадение

        massive_similar_users = self.similar(massive_similar_users) # Подою в функцию поиска похожих людей, возвращает все совпадения с пользователями
        massive_similar_users = sorted(massive_similar_users, key=lambda x: x[1], reverse=True) # Сортирую, чтобы сначала были пользователи с большим количеством совпадений
        print(massive_similar_users)
        max_count_similar = max([count_similar[1] for count_similar in massive_similar_users]) # Самое большое количество совпадений

        massive_similar_users = [user for user in massive_similar_users if user[1] > 0]  # Беру только пользователей с которыми
        massive_little_similar_users = [user for user in massive_similar_users if user[1] != max_count_similar and user[1] > 0]  # Беру только пользователей с большим количеством совпадений
        massive_big_similar_users = [user for user in massive_similar_users if user[1] == max_count_similar]  # Беру только пользователей с меньшим количеством совпадений

        # Тут я столкнулся с проблемой, что если максимальное и фильмы один в один, то возвращает пустой список
        # Я исправил это так

        if len(recommendation_films)>1:
            for film in self.user.user_viewed_films:  # Удаляю повторы фильмов
                if film in recommendation_films:
                    recommendation_films.remove(film)
            for film in self.user.user_viewed_films:  # удаляю повторы
                if film in little_recommendation_films:
                    little_recommendation_films.remove(film)

        while len(recommendation_films)<1: # пока у нас не будет хотя бы 1 фильм, который можно порекомендовать
            for name in massive_big_similar_users:
                recommendation_films += [film for film in self.other_users[name[0]]['user_viewed_films'] if
                                         filter_years[0] <= films_data[film]['year'] <= filter_years[1]
                                         and filter_rating <= sum(films_data[film]['rating']) / len(films_data[film]['rating'])]  # Беру фильмы пользователей с кем было совпадение и фильтрую их
                print(recommendation_films)
                for film in self.user.user_viewed_films: # Удаляю повторы фильмов
                    if film in recommendation_films:
                        recommendation_films.remove(film)
            else:
                if len(massive_little_similar_users) == 0: # Если в массиве пользователей нет ни одного совпавшего пользователя, то людей с кем сравнить человека нет
                    print("К сожалению таких пользователей нет, вы уникален, попробуйте использовать другую стратегию")
                    return [[],[],[]]

                recommendation_films += [film for film in
                                         self.other_users[massive_little_similar_users[0][0]]['user_viewed_films']
                                         if filter_years[0] <= films_data[film]['year'] <= filter_years[1]
                                         and filter_rating <= sum(films_data[film]['rating']) / len(films_data[film]['rating'])]  # Беру фильмы пользователей с кем было совпадение и фильтрую
                massive_little_similar_users = massive_little_similar_users[1:] # Убираю человека, который стал пользователем с самым большим количеством совпадений, из списка пользователей с маленьким совпадением
                print(recommendation_films)

                for film in self.user.user_viewed_films: # удаляю повторы
                    if film in recommendation_films:
                        recommendation_films.remove(film)

        for name in massive_little_similar_users: # Формирую массив фильмов с маленьким количеством совпадений
            little_recommendation_films += [film for film in self.other_users[name[0]]['user_viewed_films'] if
                                            filter_years[0] <= films_data[film]['year'] <= filter_years[1]
                                            and filter_rating <= sum(films_data[film]['rating']) / len(films_data[film]['rating'])]  # Беру фильмы пользователей с кем было совпадение и фильтрую
            print(little_recommendation_films)
            for film in self.user.user_viewed_films: # удаляю повторы
                if film in little_recommendation_films:
                    little_recommendation_films.remove(film)

        if len(recommendation_films)>0 and len(little_recommendation_films)>0: #Удаляем повторки в масивах
            for film in recommendation_films:
                while film in little_recommendation_films:
                    little_recommendation_films.remove(film)
                    print(film)
            for film in self.user.user_viewed_films:  # Удаляю повторы фильмов
                if film in recommendation_films:
                    recommendation_films.remove(film)




        return [list(set(recommendation_films)),list(set(little_recommendation_films)),massive_similar_users]
