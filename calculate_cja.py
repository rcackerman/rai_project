import pandas as pd
import utils


# def cja_point_item(item, answer_scores={}, else_score=0):
    # """Receives a CJA item and returns the score
    # """
    # if item in ['Yes', 'Yes Verified', 'No', 'No Verified']:
        # return answer_scores[item]
    # else:
        # return else_score


def cja_prior_warrant(row):
    """Does the prior bench warrant count equal zero?
    """
    # Return -5 if any warrant field contains data, else return +5
    return -5 if (pd.notnull(row['war_predispo_recent_dt_1st'])
                  | pd.notnull(row['war_predispo_recent_dt_2nd'])
                  | pd.notnull(row['war_predispo_2y_dt'])
                  | pd.notnull(row['war_postdispo_dt'])) else 5


def calculate_cja_score(client):
    """Calculate the CJA score for a given client
    """
    score = 0

    # 1 for working telephone, -2 for none
    score = score + utils.point_item(client['phone'],
                                     answer_scores={'Yes': 1, 'No': -2})
    # check for nyc address
    score = score + utils.point_item(client['nyc_address'],
                                     answer_scores={'Yes': 0, 'No': -2})
    # +1 for fulltime activity, -1 for no, and -2 for anything else
    score = score + utils.point_item(client['fulltime_activity'],
                                     answer_scores={'Yes': 1, 'No': -1},
                                     else_score=-2)
    # 1 for expecting someone at arraignments, -1 if no
    score = score + (1 if client['expect_at_arr'] == 'Yes' else -1)
    # check warrants
    score = score + cja_prior_warrant(client)
    # -1 for open cases, 1 if none
    score = score + (-1 if utils.ny_tools_pending(client) else 1)
    return score


def calculate_cja_score_alternate(client):
    """Calculate the CJA score for a given client
    """
    score = 0

    # 1 for working telephone, -2 for none
    score = score + utils.point_item(client['phone'],
                                     answer_scores={'Yes': 1, 'No': -2})
    # check for nyc address
    score = score + utils.point_item(client['nyc_address'],
                                     answer_scores={'Yes': 3,
                                                    'No': -2})
    # +1 for fulltime activity, -1 for no, and -2 for anything else
    score = score + utils.point_item(client['fulltime_activity'],
                                     answer_scores={'Yes': 1, 'No': -1},
                                     else_score=-2)
    # 1 for expecting someone at arraignments, -1 if no
    score = score + (1 if client['expect_at_arr'] == 'Yes' else -1)
    # check warrants
    score = score + cja_prior_warrant(client)
    # -1 for open cases, 1 if none
    score = score + (-1 if utils.ny_tools_pending(client) else 1)
    return score
