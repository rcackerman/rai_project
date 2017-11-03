"""Utility functions for RAI project
"""
import pandas as pd

CLIENTS_CSV = pd.read_csv('nycds.csv',
                          index_col=0,
                          true_values=['Yes'],
                          false_values=['No'],
                          nrows=46)
CLIENTS = CLIENTS_CSV.transpose()


def ny_tools_pending(row):
    """Checks for open cases according to CJA and Supervised Release
    tools.
    """
    # If OPEN-MISD-STATUS = "Open - Pre-Plea" or
    # if OPEN-FEL-STATUS = "Open - Pre-Plea", then +1;
    # else -1
    return True if ((row['OPEN_MISD_STATUS'] == 'Open - Pre-Plea')
                    | (row['OPEN_FEL_STATUS'] == 'Open - Pre-Plea')) else 0


def psa_pending(row, count_acd=False):
    """Generalized check for pending charge at the time of offense
    """
    if not count_acd:
        return True if (pd.notnull(row['OPEN_MISD_STATUS']) |
                        pd.notnull(row['OPEN_FEL_STATUS'])) else False
    else:
        return True if (pd.notnull(row['OPEN_MISD_STATUS']) |
                        pd.notnull(row['OPEN_FEL_STATUS']) |
                        pd.notnull(row['OPEN_ACD'])) else False


def point_item(item, answer_scores={}, else_score=0):
    """Receives an item and returns the additional points
    """
    if item in list(answer_scores.keys()):
        return answer_scores[item]
    else:
        return else_score


def point_presence(row, items, true_score, false_score):
    """Receives any number of items and returns the points a client
    gets for the presence of a datapoint
    """
    return true_score if any(
            [pd.isnull(row[item]) for item in items]) else false_score
