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
    return -5 if (pd.notnull(row['WAR_PREDISPO_RECENT_DT_1ST'])
                  | pd.notnull(row['WAR_PREDISPO_RECENT_DT_2ND'])
                  | pd.notnull(row['WAR_PREDISPO_2Y_DT'])
                  | pd.notnull(row['WAR_POSTDISPO_DT'])) else 5


def calculate_cja_score(client):
    """Calculate the CJA score for a given client
    """
    score = 0

    # 1 for working telephone, -2 for none
    score = score + utils.point_item(client['PHONE'],
                                     answer_scores={'Yes': 1, 'No': -2})
    # Check for NYC address
    score = score + utils.point_item(client['NYC_ADDRESS'],
                                     answer_scores={'Yes': 0, 'No': -2})
    # +1 for fulltime activity, -1 for no, and -2 for anything else
    score = score + utils.point_item(client['FULLTIME_ACTIVITY'],
                                     answer_scores={'Yes': 1, 'No': -1},
                                     else_score=-2)
    # 1 for expecting someone at arraignments, -1 if no
    score = score + (1 if client['EXPECT_AT_ARR'] == 'Yes' else -1)
    # Check warrants
    score = score + cja_prior_warrant(client)
    # Check for open cases
    score = score + utils.ny_tools_pending(client)
    return score


def calculate_cja_score_alternate(client):
    """Calculate the CJA score for a given client
    """
    score = 0

    # 1 for working telephone, -2 for none
    score = score + utils.point_item(client['PHONE'],
                                     answer_scores={'Yes': 1, 'No': -2})
    # Check for NYC address
    score = score + utils.point_item(client['NYC_ADDRESS'],
                                     answer_scores={'Yes': 3,
                                                    'No': -2})
    # +1 for fulltime activity, -1 for no, and -2 for anything else
    score = score + utils.point_item(client['FULLTIME_ACTIVITY'],
                                     answer_scores={'Yes': 1, 'No': -1},
                                     else_score=-2)
    # 1 for expecting someone at arraignments, -1 if no
    score = score + (1 if client['EXPECT_AT_ARR'] == 'Yes' else -1)
    # Check warrants
    score = score + cja_prior_warrant(client)
    # Check for open cases
    score = score + utils.ny_tools_pending(client)
    return score


CJA_CLIENTS_CSV = pd.read_csv('nycds.csv',
                              index_col=0,
                              true_values=['Yes'],
                              false_values=['No'],
                              nrows=46)
CJA_CLIENTS = CJA_CLIENTS_CSV.transpose()

# Data munging
CJA_CLIENTS['AGE'] = pd.to_numeric(CJA_CLIENTS['AGE'])


CJA_CLIENTS['cja_score'] = CJA_CLIENTS.apply(
                            lambda row: calculate_cja_score(row), axis=1)
CJA_CLIENTS['alt_cja_score'] = CJA_CLIENTS.apply(
                                lambda row: calculate_cja_score_alternate(row),
                                axis=1)

CJA_SCORES = CJA_CLIENTS[['cja_score', 'alt_cja_score']]

# -13 through 2	Not Recommended for ROR
# 3 through 6	Moderate Risk for ROR
# 7 through 12	Recommended for ROR
