from Data.parsers import Parsers
from Strategies.AbstractStrategy import StrategyRecommendation


users = Parsers.user_parser()
films_data = Parsers.films_parser()


class SimilarUsersStrategy(StrategyRecommendation):
    def __init__(self, user, other_users):
        super().__init__(user)
        self.other_users = other_users
    @staticmethod
    def filter_for_user(film, recommendation_films, filter_years, filter_rating, country):
        print("!!!!!")
        print(film)
        print("!!!!!")
        if (filter_years[0] <= films_data[film]['year'] <= filter_years[1] and
                filter_rating <= sum(films_data[film]['rating']) / len(films_data[film]['rating'])):
            if country != '':
                if country in films_data[film]['countries']:
                    recommendation_films.append(film)
            else:
                recommendation_films.append(film)


    def deleting_repetitions(self, recommendation_films):
        for film in self.user.user_viewed_films:  # Удаляю повторы фильмов
            if film in recommendation_films:
                recommendation_films.remove(film)

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

    def strategy(self, filter_years=None, filter_rating=-10, country = ""):
        print(country)
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

        for film in users[massive_similar_users[0][0]]['user_viewed_films']:
            if type(film) is not list:
                self.filter_for_user(film, recommendation_films, filter_years, filter_rating, country)


        for film in [users[user[0]]['user_viewed_films'] for user in massive_little_similar_users]:
            if type(film) is not list:
                self.filter_for_user(film, little_recommendation_films, filter_years, filter_rating, country)


        # Тут я столкнулся с проблемой, что если максимальное и фильмы один в один, то возвращает пустой список
        # Я исправил это так

        if len(recommendation_films)>1:
            self.deleting_repetitions(recommendation_films)
            self.deleting_repetitions(little_recommendation_films)

        while len(recommendation_films)<1: # пока у нас не будет хотя бы 1 фильм, который можно порекомендовать
            for name in massive_big_similar_users:
                for film in self.other_users[name[0]]['user_viewed_films']:
                    if type(film) is not list:
                        self.filter_for_user(film,recommendation_films,filter_years,filter_rating,country)  # Беру фильмы пользователей с кем было совпадение и фильтрую их
                print(recommendation_films)
                self.deleting_repetitions(recommendation_films)

            else:
                if len(massive_little_similar_users) == 0: # Если в массиве пользователей нет ни одного совпавшего пользователя, то людей с кем сравнить человека нет
                    print("К сожалению таких пользователей нет, вы уникален, попробуйте использовать другую стратегию")
                    return [[],[],[]]

                for film in self.other_users[massive_little_similar_users[0][0]]['user_viewed_films']:
                    if type(film) is not list:
                        self.filter_for_user(film, recommendation_films, filter_years, filter_rating, country)

                massive_little_similar_users = massive_little_similar_users[1:] # Убираю человека, который стал пользователем с самым большим количеством совпадений, из списка пользователей с маленьким совпадением
                print(recommendation_films)

                self.deleting_repetitions(recommendation_films)

        for name in massive_little_similar_users: # Формирую массив фильмов с маленьким количеством совпадений
            for film in self.other_users[name[0]]['user_viewed_films']:
                if type(film) is not list:
                    self.filter_for_user(film, little_recommendation_films, filter_years, filter_rating, country)  # Беру фильмы пользователей с кем было совпадение и фильтрую их
            print(little_recommendation_films)
            self.deleting_repetitions(little_recommendation_films)

        if len(recommendation_films)>0 and len(little_recommendation_films)>0: #Удаляем повторки в масивах
            for film in recommendation_films:
                while film in little_recommendation_films:
                    little_recommendation_films.remove(film)
                    print(film)
            self.deleting_repetitions(recommendation_films)

        return [list(set(recommendation_films)),list(set(little_recommendation_films)),massive_similar_users]
