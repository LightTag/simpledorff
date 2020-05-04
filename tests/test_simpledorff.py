from unittest import TestCase
import pandas as pd
import simpledorff
import data_transforms
import metrics
from collections import Counter


class TestWikiediaExample(TestCase):
    def setUp(self) -> None:
        # Setup test data based on https://en.wikipedia.org/wiki/Krippendorff%27s_alpha#A_computational_example
        columns = list(range(1, 16))
        values = {
            "A": {6: 3, 7: 4, 8: 1, 9: 2, 10: 1, 11: 1, 12: 3, 13: 3, 15: 3},
            "B": {1: 1, 3: 2, 4: 1, 5: 3, 6: 3, 7: 4, 8: 3},
            "C": {
                3: 2,
                4: 1,
                5: 3,
                6: 4,
                7: 4,
                9: 2,
                10: 1,
                11: 1,
                12: 3,
                13: 3,
                15: 4,
            },
        }
        self.ea_table_df = pd.DataFrame.from_dict(
            values, columns=columns, orient="index"
        )

    def test_calculate_krippendorffs_alpha_wikipedia_example_nominal(self):

        alpha = simpledorff.calculate_krippendorffs_alpha(
            self.ea_table_df, metric_fn=metrics.nominal_metric
        )
        self.assertAlmostEqual(0.691, alpha, 3)

    def test_calculate_krippendorffs_alpha_wikipedia_example_interval(self):

        alpha = simpledorff.calculate_krippendorffs_alpha(
            self.ea_table_df, metric_fn=metrics.interval_metric
        )
        self.assertAlmostEqual(0.811, alpha, 3)

    def test_make_vbu_table(self):
        vbu_table = data_transforms.make_value_by_unit_table_dict(self.ea_table_df)
        expected = {
            1: Counter({1.0: 1}),
            2: Counter(),
            3: Counter({2.0: 2}),
            4: Counter({1.0: 2}),
            5: Counter({3.0: 2}),
            6: Counter({3: 2, 4: 1}),
            7: Counter({4: 3}),
            8: Counter({1.0: 1, 3.0: 1}),
            9: Counter({2.0: 2}),
            10: Counter({1.0: 2}),
            11: Counter({1.0: 2}),
            12: Counter({3.0: 2}),
            13: Counter({3.0: 2}),
            14: Counter(),
            15: Counter({3.0: 1, 4.0: 1}),
        }
        self.assertEqual(vbu_table, expected)

    def test_make_value_by_unit_table_dict(self):
        vbu_table = data_transforms.make_value_by_unit_table_dict(self.ea_table_df)
        result = data_transforms.calculate_frequency_dicts(vbu_table)
        expected = {
            "unit_freqs": {
                1: 0.0,
                3: 2.0,
                4: 2.0,
                5: 2.0,
                6: 3.0,
                7: 3.0,
                8: 2.0,
                9: 2.0,
                10: 2.0,
                11: 2.0,
                12: 2.0,
                13: 2.0,
                15: 2.0,
            },
            "class_freqs": {1.0: 7.0, 2.0: 4.0, 3.0: 10.0, 4.0: 5.0},
            "total": 26.0,
        }
        for key in expected:
            self.assertEqual(expected[key], result[key], key)


class TestPaperExample(TestCase):
    def setUp(self) -> None:
        # Setup test data based on section 3 https://a8h2w5y7.rocketcdn.me/wp-content/uploads/2016/07/fulltext.pdf
        columns = list(range(1, 13))
        values = {
            "A": {1: 1, 2: 2, 3: 3, 4: 3, 5: 2, 6: 1, 7: 4, 8: 1, 9: 2},
            "B": {1: 1, 2: 2, 3: 3, 4: 3, 5: 2, 6: 2, 7: 4, 8: 1, 9: 2, 10: 5, 12: 3},
            "C": {2: 3, 3: 3, 4: 3, 5: 3, 5: 2, 6: 3, 7: 4, 8: 2, 9: 2, 10: 5, 11: 1},
            "D": {1: 1, 2: 2, 3: 3, 4: 3, 5: 2, 6: 4, 7: 4, 8: 1, 9: 2, 10: 5, 11: 1},
        }
        self.ea_table_df = pd.DataFrame.from_dict(
            values, columns=columns, orient="index"
        )

    def test_calculate_krippendorffs_alpha_wikipedia_example_nominal(self):

        alpha = simpledorff.calculate_krippendorffs_alpha(
            self.ea_table_df, metric_fn=metrics.nominal_metric
        )
        self.assertAlmostEqual(0.743, alpha, 3)

    def test_make_vbu_table(self):
        vbu_table = data_transforms.make_value_by_unit_table_dict(self.ea_table_df)
        expected = {
            1: Counter({1.0: 3}),
            2: Counter({2.0: 3, 3.0: 1}),
            3: Counter({3.0: 4}),
            4: Counter({3.0: 4}),
            5: Counter({2.0: 4}),
            6: Counter({1.0: 1, 2.0: 1, 3.0: 1, 4.0: 1}),
            7: Counter({4.0: 4}),
            8: Counter({1.0: 3, 2.0: 1}),
            9: Counter({2.0: 4}),
            10: Counter({5.0: 3}),
            11: Counter({1.0: 2}),
            12: Counter({3.0: 1}),
        }
        self.assertEqual(vbu_table, expected)

    def test_make_value_by_unit_table_dict(self):
        vbu_table = data_transforms.make_value_by_unit_table_dict(self.ea_table_df)
        result = data_transforms.calculate_frequency_dicts(vbu_table)
        expected = {
            "unit_freqs": {
                1: 3.0,
                2: 4.0,
                3: 4.0,
                4: 4.0,
                5: 4.0,
                6: 4.0,
                7: 4.0,
                8: 4.0,
                9: 4.0,
                10: 3.0,
                11: 2.0,
                12: 0.0,
            },
            "class_freqs": {1.0: 9.0, 2.0: 13.0, 3.0: 10.0, 4.0: 5.0, 5.0: 3.0},
            "total": 40.0,
        }
        for key in expected:
            self.assertEqual(expected[key], result[key], key)
