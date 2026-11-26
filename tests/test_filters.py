import unittest
from contextlib import ExitStack
from unittest.mock import patch

from GUI import activation
from Modules.user import User


class RecommendationFilterTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.user = User(id_user=1, user_name="viewer", user_genre=["drama"],
                         user_viewed_films=["seen"])
        films = {}
        for title in ["seen", *(f"old{i}" for i in range(16)), "wrong country",
                      "low rating", "target"]:
            films[title] = {
                "genre": ["drama"], "director": "Director", "franchise": "Saga",
                "year": 1990 if title.startswith("old") else 2020,
                "rating": [5] if title == "low rating" else [8, 9],
                "countries": ["US" if title == "wrong country" else "FR"],
            }
        self.others = {"peer": {"user_genre": ["drama"], "user_viewed_films":
                                [title for title in films if title != "seen"]}}
        users = {"viewer": vars(self.user), **self.others}
        stack.enter_context(patch.object(activation.Parsers, "films_parser", return_value=films))
        stack.enter_context(patch.object(activation.Parsers, "user_parser", return_value=users))
        stack.enter_context(patch("Strategies.SimilarUsersStrategy.films_data", films))
        stack.enter_context(patch("Strategies.SimilarUsersStrategy.users", users))
        stack.enter_context(patch("builtins.print"))

    def test_combined_filters_through_ranked_menus(self):
        for menu, args in [(activation.genre_algorithm, ()), (activation.franchise_algorithm, ()),
                           (activation.director_algorithm, ()), (activation.rating_algorithm, ()),
                           (activation.multi_algorithm, (self.others,))]:
            with self.subTest(menu=menu.__name__):
                inputs = ["2", "1", "2020", "2020", "2", "8,5", "8.5",
                          "3", "FR", "4", "1", "3"]
                with patch("builtins.input", side_effect=inputs), patch.object(
                        activation, "show_a_recommended_movie") as display:
                    menu(self.user, *args)
                displayed = display.call_args.args[1]
                expected = {"seen", "target"} if menu in (
                    activation.rating_algorithm, activation.multi_algorithm) else {"target"}
                self.assertEqual(set(displayed), expected)
                self.assertEqual(len(displayed), len(expected))

    def test_similar_user_filters(self):
        strategy = activation.SimilarUsersStrategy(self.user, self.others)
        self.assertEqual(strategy.strategy([2020, 2020], 8.5, "FR")[0], ["target"])

    def test_no_similar_users(self):
        self.assertEqual(activation.SimilarUsersStrategy(self.user, {}).strategy(), [[], [], []])

    def test_empty_selection(self):
        self.assertEqual(activation.StrategyGenre(self.user).filtered_year(2030, 2031), [])
