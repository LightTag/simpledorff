import pandas as pd
from collections import Counter


def df_to_experiment_annotator_table(df, experiment_col, annotator_col, class_col):
    """

    :param df: A Dataframe we wish to transform with that contains the response of an annotator to an experiment
            |    |   document_id | annotator_id   |   annotation |
            |---:|--------------:|:---------------|-------------:|
            |  0 |             1 | A              |            1 |
            |  1 |             1 | B              |            1 |
            |  2 |             1 | D              |            1 |
            |  4 |             2 | A              |            2 |
            |  5 |             2 | B              |            2 |

    :param experiment_col: The column name that contains the experiment (unit)
    :param annotator_col: The column name that identifies an annotator
    :param class_col: The column name that identifies the annotators response (class)
    :return: A dataframe indexed by annotators, with experiments as columns and the responses in the cells
            | annotator_id   |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |   9 |   10 |   11 |   12 |
            |:---------------|----:|----:|----:|----:|----:|----:|----:|----:|----:|-----:|-----:|-----:|
            | A              |   1 |   2 |   3 |   3 |   2 |   1 |   4 |   1 |   2 |  nan |  nan |  nan |
            | B              |   1 |   2 |   3 |   3 |   2 |   2 |   4 |   1 |   2 |    5 |  nan |    3 |
            | C              | nan |   3 |   3 |   3 |   2 |   3 |   4 |   2 |   2 |    5 |    1 |  nan |
            | D              |   1 |   2 |   3 |   3 |   2 |   4 |   4 |   1 |   2 |    5 |    1 |  nan |

    """
    return df.pivot_table(
        index=annotator_col, columns=experiment_col, values=class_col, aggfunc="first"
    )


def make_value_by_unit_table_dict(experiment_annotator_df):
    """

    :param experiment_annotator_df: A dataframe that came out of  df_to_experiment_annotator_table
    :return: A dictionary of dictionaries (e.g. a table) whose rows (first level) are experiments and columns are responses
            {1: Counter({1.0: 1}),
             2: Counter(),
             3: Counter({2.0: 2}),
             4: Counter({1.0: 2}),
             5: Counter({3.0: 2}),
            """
    data_by_exp = experiment_annotator_df.T.sort_index(axis=1).sort_index()
    table_dict = {}
    for exp, row in data_by_exp.iterrows():
        vals = row.dropna().values
        table_dict[exp] = Counter()
        for val in vals:
            table_dict[exp][val] += 1
    return table_dict


def calculate_frequency_dicts(vbu_table_dict):
    """

    :param vbu_table_dict: A value by unit table dictionary, the output of  make_value_by_unit_table_dict
    :return: A dictionary of dictonaries
        {
            unit_freqs:{ 1:2..},
            class_freqs:{ 3:4..},
            total:7
        }
    """
    vbu_df = (
        pd.DataFrame.from_dict(vbu_table_dict, orient="index")
        .T.sort_index(axis=0)
        .sort_index(axis=1)
        .fillna(0)
    )
    ubv_df = vbu_df.T
    vbu_df_masked = ubv_df.mask(ubv_df.sum(1) == 1, other=0).T
    return dict(
        unit_freqs=vbu_df_masked.sum().to_dict(),
        class_freqs=vbu_df_masked.sum(1).to_dict(),
        total=vbu_df_masked.sum().sum(),
    )
