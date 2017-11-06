"""Calculate NY Supervised Release Score"""

import pandas as pd
import utils


def ny_sr_age(age):
    """Age
    """
    if (age >= 16 and age <= 19):
        return 6
    elif (age >= 20 and age <= 29):
        return 1
    elif (age >= 30 and age <= 39):
        return -3
    elif age >= 40:
        return -4


def ny_sr_first_arrest(x):
    """First Arrest
    """
    return -3 if x == 'Yes' else 3


def ny_sr_war(row):
    """Warrant in last 4 years
    If the date of any warrant is within 4 years
    of date of arraignment, then +1; else -1
    """
    day_of_reckoning = row['arraign_date'] - pd.Timedelta(4, 'Y')
    return 1 if ((row['war_predispo_recent_dt_1st'] > day_of_reckoning)
                 | (row['war_predispo_2y_dt'] > day_of_reckoning)
                 | (row['war_postdispo_dt'] > day_of_reckoning)) else -1


def ny_sr_misd_conv(row):
    """Misd. Conv. in last 1 years
    Because of how we collected data, we're looking at both
    CONV_MISD_DT and the "open" misdemeanors.

    If the date of CONV-MISD-DT is within 1 year of arraignment;
    or if OPEN-MISD-PLEA-CHG is a misdemeanor
    and OPEN-MISD-PLEA-DT is within 1 year of arraignment;
    or if OPEN-FEL-PLEA-CHG is a misdemeanor
    and OPEN-FEL-PLEA-DT is within 1 year of arraignment, then +2;
    else -2
    """
    day_of_reckoning = row['arraign_date'] - pd.Timedelta(1, 'Y')
    return 2 if ((row['conv_misd_dt'] > day_of_reckoning)
                 | (row['open_misd_plea_dt'] > day_of_reckoning)
                 | (row['open_fel_plea_dt'] > day_of_reckoning)) else -2


def ny_sr_fel_conv(row):
    """Fel. Conv. in last 9 years
    """
    # If the date of CONV-FEL-DT is within 9 years of arraignment;
    # or if OPEN-MISD-PLEA-CHG is a felony and OPEN-MISD-PLEA-DT
    # is within 9 years of arraignment;
    # or if OPEN-FEL-PLEA-CHG is a felony and OPEN-FEL-PLEA-DT
    # is within 9 years of arraignment, then +1;
    # else -1
    day_of_reckoning = row['arraign_date'] - pd.Timedelta(9, 'Y')
    return 2 if ((row['conv_fel_dt'] > day_of_reckoning)
                 | (row['open_misd_plea_dt'] > day_of_reckoning)
                 | (row['open_fel_plea_dt'] > day_of_reckoning)) else -2


def ny_sr_drug_conv(row):
    """Drug Conv. in last 9 years
    """
    # If the date of CONV-DRUG-DT is within 9 years of arraignment,
    # then +2; else -2
    day_of_reckoning = row['arraign_date'] - pd.Timedelta(9, 'Y')
    return 2 if ((row['conv_drug_dt'] > day_of_reckoning)
                 | (row['open_drug_plea_dt'] > day_of_reckoning)) else -2


def ny_sr_fulltime_act(row):
    """Fulltime Activity
    """
    return -2 if row['fulltime_activity'] == 'Yes' else 2


def calculate_sr_score(row):
    """Calculate the final SR score for any given client
    """
    score = 0
    score = score + ny_sr_age(row['age'])
    score = score + utils.ny_tools_pending(row)
    score = score + ny_sr_first_arrest(row['first_arrest'])
    score = score + ny_sr_war(row)
    score = score + ny_sr_misd_conv(row)
    score = score + ny_sr_fel_conv(row)
    score = score + ny_sr_drug_conv(row)
    score = score + ny_sr_fulltime_act(row)
    return score


SR_CLIENTS = pd.read_csv('nycds.csv',
                         index_col=0,
                         true_values=['Yes'],
                         false_values=['No'],
                         nrows=46).transpose()

# Data munging

# Ages get changed to numeric
SR_CLIENTS['age'] = pd.to_numeric(SR_CLIENTS['age'])

# All dates get changed to a pandas datetime object, for easier comparisons
SR_CLIENTS['arraign_date'] = pd.to_datetime(SR_CLIENTS['arraign_date'])
SR_CLIENTS['war_predispo_recent_dt_1st'] = pd.to_datetime(
        SR_CLIENTS['war_predispo_recent_dt_1st'])
SR_CLIENTS['war_predispo_recent_dt_2nd'] = pd.to_datetime(
        SR_CLIENTS['war_predispo_recent_dt_2nd'])
SR_CLIENTS['war_predispo_2y_dt'] = pd.to_datetime(
        SR_CLIENTS['war_predispo_2y_dt'])
SR_CLIENTS['war_postdispo_dt'] = pd.to_datetime(SR_CLIENTS['war_postdispo_dt'])
SR_CLIENTS['open_misd_plea_dt'] = pd.to_datetime(
        SR_CLIENTS['open_misd_plea_dt'])
SR_CLIENTS['open_fel_plea_dt'] = pd.to_datetime(SR_CLIENTS['open_fel_plea_dt'])
SR_CLIENTS['open_drug_plea_dt'] = pd.to_datetime(
        SR_CLIENTS['open_drug_plea_dt'])
SR_CLIENTS['conv_misd_dt'] = pd.to_datetime(SR_CLIENTS['conv_misd_dt'])
SR_CLIENTS['conv_fel_dt'] = pd.to_datetime(SR_CLIENTS['conv_fel_dt'])
SR_CLIENTS['conv_drug_dt'] = pd.to_datetime(SR_CLIENTS['conv_drug_dt'])
SR_CLIENTS['conv_vio_dt_1st'] = pd.to_datetime(SR_CLIENTS['conv_vio_dt_1st'])
SR_CLIENTS['conv_vio_dt_2nd'] = pd.to_datetime(SR_CLIENTS['conv_vio_dt_2nd'])
SR_CLIENTS['conv_vio_dt_3rd'] = pd.to_datetime(SR_CLIENTS['conv_vio_dt_3rd'])

# All strings to strings, I guess?
SR_CLIENTS['open_misd_plea_chg'] = SR_CLIENTS['open_misd_plea_chg'].astype('str')
SR_CLIENTS['open_fel_plea_chg'] = SR_CLIENTS['open_fel_plea_chg'].astype('str')


SR_CLIENTS['sr_score'] = SR_CLIENTS.apply(
        lambda row: calculate_sr_score(row), axis=1)

SR_SCORES = SR_CLIENTS[['sr_score']].copy()
