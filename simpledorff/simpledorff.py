from simpledorff import data_transforms
from simpledorff.metrics import nominal_metric


def calculate_de(frequency_dicts, metric_fn):
    """
    Calculates the expected disagreement by chance
    :param frequency_dicts: The output of data_transforms.calculate_frequency_dicts e.g.:
        {
            unit_freqs:{ 1:2..},
            class_freqs:{ 3:4..},
            total:7
        }
    :param metric_fn metric function such as nominal_metric
    :return: De a float
    """
    De = 0
    class_freqs = frequency_dicts["class_freqs"]
    class_names = list(class_freqs.keys())
    for i, c in enumerate(class_names):
        for k in class_names:
            De += class_freqs[c] * class_freqs[k] * metric_fn(c, k)
    return De


def calculate_do(vbu_table_dict, frequency_dicts, metric_fn):
    """

    :param vbu_table_dict: Output of data_transforms.make_value_by_unit_table_dict
    :param frequency_dicts: The output of data_transforms.calculate_frequency_dicts e.g.:
        {
            unit_freqs:{ 1:2..},
            class_freqs:{ 3:4..},
            total:7
        }
    :param metric_fn: metric_fn metric function such as nominal_metric
    :return:  Do a float
    """
    Do = 0
    unit_freqs = frequency_dicts["unit_freqs"]
    unit_ids = list(unit_freqs.keys())
    for unit_id in unit_ids:
        unit_classes = list(vbu_table_dict[unit_id].keys())
        if unit_freqs[unit_id] < 2:
            pass
        else:
            weight = 1 / (unit_freqs[unit_id] - 1)
            for i, c in enumerate(unit_classes):
                for k in unit_classes:
                    Do += (
                        vbu_table_dict[unit_id][c]
                        * vbu_table_dict[unit_id][k]
                        * weight
                        * metric_fn(c, k)
                    )
    return Do


def calculate_krippendorffs_alpha(ea_table_df, metric_fn=nominal_metric):
    """

    :param ea_table_df: The Experiment/Annotator table, output from data_transforms.df_to_experiment_annotator_table
    :param metric_fn: The metric function. Defaults to nominal
    :return: Alpha, a float
    """
    vbu_table_dict = data_transforms.make_value_by_unit_table_dict(ea_table_df)
    frequency_dict = data_transforms.calculate_frequency_dicts(vbu_table_dict)
    observed_disagreement = calculate_do(
        vbu_table_dict=vbu_table_dict,
        frequency_dicts=frequency_dict,
        metric_fn=metric_fn,
    )
    expected_disagreement = calculate_de(
        frequency_dicts=frequency_dict, metric_fn=metric_fn
    )
    N = frequency_dict['total']
    alpha = 1 - (observed_disagreement / expected_disagreement)*(N-1)
    return alpha


def calculate_krippendorffs_alpha_for_df(
    df, experiment_col, annotator_col, class_col, metric_fn=nominal_metric
):
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
    :return: Alpha, a float

    """
    ea_table_df = data_transforms.df_to_experiment_annotator_table(
        df,
        experiment_col=experiment_col,
        annotator_col=annotator_col,
        class_col=class_col,
    )
    return calculate_krippendorffs_alpha(ea_table_df=ea_table_df, metric_fn=metric_fn)
