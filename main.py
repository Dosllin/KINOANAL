# проверяя код на маке обнаружил, что код выдает бесполезное
# предупреждение о библиотеке term.image(вывод картинки),решили просто заигнорить его
import warnings
warnings.filterwarnings(
    "ignore",
    message="It seems this process is not running within a terminal",
    category=UserWarning,
)
from Controlers.logining import login_sign_in
from Controlers.searcher import search_film
from Data.parsers import Parsers
from GUI.activation import similar_algorithm
from GUI.activation import director_algorithm
from GUI.activation import rating_algorithm
from GUI.activation import multi_algorithm
from GUI.activation import random_activation
from GUI.activation import franchise_algorithm
from GUI.activation import genre_algorithm
from Controlers.account import menu_account
from art import text2art


def main():
    print(text2art("KinoAnal", font="big"))
    print('Рекомендательная система фильмов: когда твой ИИ лучше знает, что ты хочешь посмотреть, чем ты сам')
    print()
    users = Parsers.user_parser()


    ### MAIN MENU
    flag_login = 1
    user = 0 # Просто для того, чтобы pycharm не ругался
    while flag_login:
        user = login_sign_in()
        if user == 0:
            print("До свидание!")
            return 0
        if user != 1:
            flag_login = 0
            users = Parsers.user_parser()



    users_without_main_user = users.copy()
    users_without_main_user.pop(user.user_name)


    if len(users[user.user_name]["user_viewed_films"]) == 0:
        print("==================================")
        print("Похоже, вы ещё не добавили просмотренные фильмы. Пожалуйста, найдите и добавьте хотя бы один фильм.")
        input("Нажмите Enter, чтобы продолжить...")
        while len(users[user.user_name]["user_viewed_films"]) == 0:
            search_film(user)
            users = Parsers.user_parser()


    while True:
        print('------------MAIN MENU------------')
        print("1. Рекомендации от похожих пользователей",
              "2. Рекомендация на основе любимых режиссеров",
              "3. Рекомендация по топу рейтинга",
              "4. Рекомендации на основе жанров",
              "5. Рекомендация на основе франшиз",
              "6. Рекомендация на основе всех стратегий",
              "7. 10 Случайных фильмов (Долой алгоритмы доверимся богу рандома)",
              "8. Поиск фильма (Добавить просмотренные фильмы)",
              "9. Посмотреть/изменить данные об аккаунте",
              "10. Выйти",sep='\n')

        choice_main_menu = input("Выберите действие: ")

        if choice_main_menu == '8':
            search_film(user)
        elif choice_main_menu  == '1':
            similar_algorithm(user, users_without_main_user)
        elif choice_main_menu == '2':
            director_algorithm(user)
        elif choice_main_menu == '3':
            rating_algorithm(user)
        elif choice_main_menu == '4':
            genre_algorithm(user)
        elif choice_main_menu == '5':
            franchise_algorithm(user)
        elif choice_main_menu == '6':
            multi_algorithm(user, users_without_main_user)
        elif choice_main_menu == '7':
            random_activation(user)
        elif choice_main_menu == '9':
            menu_account()
        elif choice_main_menu == '10':
            print("До свидание!")
            break

if __name__ == '__main__':
    main()
