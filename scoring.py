# pylint: disable=W0108

"""Determine final scores for each client,
using the different risk tools
"""

# get tables with raw scores for each client
import pandas as pd
import calculate_psa
import calculate_sr
import calculate_cja

FTA_ADJUSTED_SCORES = {0: 1, 1: 2, 2: 3, 3: 4,
                       4: 4, 5: 5, 6: 5, 7: 6}
NCA_ADJUSTED_SCORES = {0: 1, 1: 2, 2: 2, 3: 3,
                       4: 3, 5: 4, 6: 4, 7: 5,
                       8: 5, 9: 6, 10: 6, 11: 6,
                       12: 6, 13: 6}

def sr_risk_level(x):
    """Get risk level for supervised release,
    based on raw score
    """
    if x in list(range(-16, -9)):
        return 'Low'
    elif x in list(range(-9, -4)):
        return 'Low Medium'
    elif x in list(range(-4, 1)):
        return 'Medium'
    elif x in list(range(1, 5)):
        return 'Medium High'
    elif x in list(range(5, 19)):
        return 'High'


def sr_eligibility(row):
    """Check basic charge eligibility for SR,
    which is any non-violent felony or non-DV misdemeanor
    """
    return True if (row['top_chg'][-2:] == 'VF'
                    or row['dv'] == 'TRUE') else False


def cja_risk_level(x):
    """Get risk level for CJA,
    based on raw score
    """
    if x in list(range(-13, 3)):
        return 'Not recommended for ROR'
    elif x in list(range(3, 7)):
        return 'Moderate risk for ROR'
    elif x in list(range(7, 13)):
        return 'Recommended for ROR'

CLIENTS = pd.read_csv('nycds.csv',
                      index_col=0,
                      true_values=['Yes', 'TRUE'],
                      false_values=['No', 'FALSE'],
                      nrows=48).transpose()

# Data munging

# Ages get changed to numeric
CLIENTS['age'] = pd.to_numeric(CLIENTS['age'])

# All dates get changed to a pandas datetime object, for easier comparisons
CLIENTS['arraign_date'] = pd.to_datetime(CLIENTS['arraign_date'])
CLIENTS['war_predispo_recent_dt_1st'] = pd.to_datetime(CLIENTS['war_predispo_recent_dt_1st'])
CLIENTS['war_predispo_recent_dt_2nd'] = pd.to_datetime(CLIENTS['war_predispo_recent_dt_2nd'])
CLIENTS['war_predispo_2y_dt'] = pd.to_datetime(CLIENTS['war_predispo_2y_dt'])
CLIENTS['war_postdispo_dt'] = pd.to_datetime(CLIENTS['war_postdispo_dt'])
CLIENTS['open_misd_plea_dt'] = pd.to_datetime(CLIENTS['open_misd_plea_dt'])
CLIENTS['open_fel_plea_dt'] = pd.to_datetime(CLIENTS['open_fel_plea_dt'])
CLIENTS['open_drug_plea_dt'] = pd.to_datetime(CLIENTS['open_drug_plea_dt'])
CLIENTS['conv_misd_dt'] = pd.to_datetime(CLIENTS['conv_misd_dt'])
CLIENTS['conv_fel_dt'] = pd.to_datetime(CLIENTS['conv_fel_dt'])
CLIENTS['conv_drug_dt'] = pd.to_datetime(CLIENTS['conv_drug_dt'])
CLIENTS['conv_vio_dt_1st'] = pd.to_datetime(CLIENTS['conv_vio_dt_1st'])
CLIENTS['conv_vio_dt_2nd'] = pd.to_datetime(CLIENTS['conv_vio_dt_2nd'])
CLIENTS['conv_vio_dt_3rd'] = pd.to_datetime(CLIENTS['conv_vio_dt_3rd'])

# All strings to strings, I guess?
CLIENTS['open_misd_plea_chg'] = CLIENTS['open_misd_plea_chg'].astype('str')
CLIENTS['open_fel_plea_chg'] = CLIENTS['open_fel_plea_chg'].astype('str')
CLIENTS['open_drug_plea_chg'] = CLIENTS['open_drug_plea_chg'].astype('str')


##
# Create raw scores for each docket

CLIENTS['sr_score'] = CLIENTS.apply(
    lambda row: calculate_sr.calculate_sr_score(row), axis=1)

CLIENTS['fta_raw_score'] = CLIENTS.apply(
    lambda row: calculate_psa.calculate_fta_raw_score(row), axis=1)
CLIENTS['nca_raw_score'] = CLIENTS.apply(
    lambda row: calculate_psa.calculate_nca_raw_score(row), axis=1)
CLIENTS['nvca_raw_score'] = CLIENTS.apply(
    lambda row: calculate_psa.calculate_nvca_raw_score(row), axis=1)

CLIENTS['cja_score'] = CLIENTS.apply(
    lambda row: calculate_cja.calculate_cja_score(row), axis=1)
CLIENTS['alt_cja_score'] = CLIENTS.apply(
    lambda row: calculate_cja.calculate_cja_score_alternate(row), axis=1)

SCORES = CLIENTS[['top_chg', 'dv', 'age', 'client_race', 'client_ethnicity',
                  'client_gender', 'sr_score', 'cja_score',
                  'fta_raw_score', 'nca_raw_score', 'nvca_raw_score',
                  'outcome_bail', 'outcome_bond', 'outcome_custody'
                 ]].copy()

##
# Calculate Supervised Release
# Check if clients are even eligible for supervised release
# Any violent felony or DV charge are not eligible
SCORES['sr_chg_ineligible'] = SCORES.apply(lambda row: sr_eligibility(row), axis=1)
# Calculate supervised release
SCORES['sr_risk'] = SCORES['sr_score'].apply(lambda x: sr_risk_level(x))

##
# Calculate CJA score
SCORES['cja_risk'] = SCORES['cja_score'].apply(lambda x: cja_risk_level(x))

##
# Calculate PSA scores
SCORES['fta_score'] = SCORES['fta_raw_score'].apply(lambda x: FTA_ADJUSTED_SCORES[x])
SCORES['nca_score'] = SCORES['nca_raw_score'].apply(lambda x: NCA_ADJUSTED_SCORES[x])
SCORES['nvca_flag'] = SCORES['nvca_raw_score'].apply(lambda x: True if x > 3 else False)
