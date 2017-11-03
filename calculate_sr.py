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
    day_of_reckoning = row['ARRAIGN_DATE'] - pd.Timedelta(4, 'Y')
    return 1 if ((row['WAR_PREDISPO_RECENT_DT_1ST'] > day_of_reckoning)
                 | (row['WAR_PREDISPO_2Y_DT'] > day_of_reckoning)
                 | (row['WAR_POSTDISPO_DT'] > day_of_reckoning)) else -1


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
    day_of_reckoning = row['ARRAIGN_DATE'] - pd.Timedelta(1, 'Y')
    return 2 if ((row['CONV_MISD_DT'] > day_of_reckoning)
                 | (row['OPEN_MISD_PLEA_CHG'].endswith('M')
                    & row['OPEN_MISD_PLEA_DT'] > day_of_reckoning)
                 | (row['OPEN_FEL_PLEA_CHG'].endswith('M')
                     & row['OPEN_FEL_PLEA_DT'] > day_of_reckoning)) else -2


def ny_sr_fel_conv(row):
    """Fel. Conv. in last 9 years
    """
    # If the date of CONV-FEL-DT is within 9 years of arraignment;
    # or if OPEN-MISD-PLEA-CHG is a felony and OPEN-MISD-PLEA-DT
    # is within 9 years of arraignment;
    # or if OPEN-FEL-PLEA-CHG is a felony and OPEN-FEL-PLEA-DT
    # is within 9 years of arraignment, then +1;
    # else -1
    day_of_reckoning = row['ARRAIGN_DATE'] - pd.Timedelta(9, 'Y')
    return 2 if ((row['CONV_FEL_DT'] > day_of_reckoning)
                 | (row['OPEN_MISD_PLEA_CHG'].endswith('F')
                    & row['OPEN_MISD_PLEA_DT'] > day_of_reckoning)
                 | (row['OPEN_FEL_PLEA_CHG'].endswith('F')
                    & row['OPEN_FEL_PLEA_DT'] > day_of_reckoning)) else -2


def ny_sr_drug_conv(row):
    """Drug Conv. in last 9 years
    """
    # If the date of CONV-DRUG-DT is within 9 years of arraignment,
    # then +2; else -2
    day_of_reckoning = row['ARRAIGN_DATE'] - pd.Timedelta(9, 'Y')
    return 2 if ((row['CONV_DRUG_DT'] > day_of_reckoning)
                 | (row['OPEN_DRUG_PLEA_DT'] > day_of_reckoning)) else -2


def ny_sr_fulltime_act(row):
    """Fulltime Activity
    """
    return -2 if row['FULLTIME'] == 'Yes' else 2


def calculate_sr_score(row):
    """Calculate the final SR score for any given client
    """
    score = 0
    score = score + ny_sr_age(row['AGE'])
    score = score + utils.ny_tools_pending(row)
    score = score + ny_sr_first_arrest(row['FIRST_ARREST'])
    score = score + ny_sr_war(row)
    score = score + ny_sr_misd_conv(row)
    score = score + ny_sr_fel_conv(row)
    score = score + ny_sr_drug_conv(row)
    score = score + ny_sr_fulltime_act(row)
    return score

# -16 through -10	LOW
# -9 through -5	LOW MEDIUM
# -4 through 0	MEDIUM
# 1 through 4	MEDIUM HIGH
# 5 though 18	HIGH
