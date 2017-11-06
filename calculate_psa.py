"""Calculate the Arnold Foundation PSA score
"""

# import os
import pandas as pd
import utils

with open('crime_of_violence.txt') as f:
    VIOLENT_CRIMES = f.read().splitlines()


def prior_convictions(row):
    """Check if client has any prior convictions.
    """
    return True if (pd.notnull(row['conv_misd_dt']) |
                    pd.notnull(row['conv_fel_dt'])) else False


def number_warrants(row):
    """Find the number of recent warrants.
    """
    if pd.notnull(row['war_predispo_recent_dt_2nd']):
        return 2
    if pd.notnull(row['war_predispo_recent_dt_1st']):
        return 1
    else:
        return 0


def psa_fta_pending(row):
    """Pending charge at the time of offense
    """
    return 1 if utils.psa_pending(row) else 0


def psa_fta_prior_conv(row):
    """Prior conviction
    If CONV-MISD-DT or CONV-FEL-DT contain data, then +1, else 0
    """
    return 1 if prior_convictions(row) else 0


def psa_fta_new_war(row):
    """Prior failure to appear pretrial in past 2 years.
    2 prior warrants = 4 points, 1 warrant = 2 points, 0 = 0 points
    """
    return number_warrants(row) * 2


def psa_fta_old_war(row):
    """Prior failure to appear pretrial older than 2 years
    If WAR-PREDISPO-2Y-DT contains data, then +1; else 0
    """
    return 1 if pd.notnull(row['war_predispo_2y_dt']) else 0


def psa_nca_age(age):
    """Age at current arrest
    If AGE is less than or equal to 22, then +2; else 0
    """
    return 2 if age <= 22 else 0


def psa_nca_pending(row):
    """Pending charge at the time of offense
    If OPEN-MISD-STATUS or OPEN-FEL-STATUS contain data, then +3; else 0
    """
    return 3 if utils.psa_pending(row) else 0


def psa_nca_misd_conv(conv):
    """Prior misdemeanor conviction
    If CONV-MISD-DT contains data, then +1, else 0
    """
    return 1 if pd.notnull(conv) else 0


def psa_nca_fel_conv(conv):
    """Prior felony conviction
    If CONV-FEL-DT contains data, then +1, else 0
    """
    return 1 if pd.notnull(conv) else 0


def psa_vio_conv(row):
    """Prior violent conviction
    If CONV-VIO-DT-3RD contains data, then +2;
    if CONV-VIO-DT-1ST contains data, but CONV-VIO-DT-3RD is empty, then +1;
    else 0
    """
    if pd.notnull(row['conv_vio_dt_3rd']):
        return 2
    if pd.notnull(row['conv_vio_dt_1st']):
        return 1
    else:
        return 0


def psa_nca_prior_sentence(sent):
    """Prior setence to incarceration
    If PRIOR-SENTENCE = "Yes", then +2; else 0
    """
    return 2 if sent == 'Yes' else 0


def psa_nvca_vio_chg(row):
    """Current violent offense
    If TOP-CHG = crime of violence, then +2; else 0
    """
    return 2 if (row['top_chg'] in VIOLENT_CRIMES) else 0


def psa_nvca_viochg_age(row):
    """Current violent offense & 20 years or younger
    If TOP-CHG = crime of violence
    and AGE is less than or equal to 20, then +1; else 0
    """
    return 1 if ((row['top_chg'] in VIOLENT_CRIMES)
                 & (row['age'] <= 20)) else 0


def psa_nvca_pending(row):
    """Pending charge at the time of offense
    If OPEN-MISD-STATUS or OPEN-FEL-STATUS contain data, then +1; else 0
    """
    return 1 if utils.psa_pending(row) else 0


def psa_nvca_prior_conv(row):
    """Prior conviction
    If CONV-MISD-DT or CONV-FEL-DT contain data, then +1, else 0
    """
    return 1 if prior_convictions(row) else 0


def calculate_fta_raw_score(client_row):
    """Starting with a score of 0, calculate the points for a given client.
    Each row is 1 client.
    """
    score = 0
    score = score + psa_fta_pending(client_row)
    score = score + psa_fta_prior_conv(client_row)
    score = score + psa_fta_new_war(client_row)
    score = score + psa_fta_old_war(client_row)
    return score


def calculate_nca_raw_score(client_row):
    """Calculate New Criminal Activity Risk score for any given client.
    """
    score = 0
    score = score + psa_nca_age(client_row['age'])
    score = score + psa_nca_pending(client_row)
    score = score + psa_nca_misd_conv(client_row['conv_misd_dt'])
    score = score + psa_nca_fel_conv(client_row['conv_fel_dt'])
    score = score + psa_vio_conv(client_row)
    score = score + number_warrants(client_row)
    score = score + psa_nca_prior_sentence(client_row['prior_sentence'])
    return score


def calculate_nvca_raw_score(client_row):
    """Calculate New Violent Criminal Activity Risk score for any given client.
    """
    score = 0
    score = score + psa_nvca_vio_chg(client_row)
    score = score + psa_nvca_viochg_age(client_row)
    score = score + psa_nvca_pending(client_row)
    score = score + psa_nvca_prior_conv(client_row)
    score = score + psa_vio_conv(client_row)
    return score


PSA_CLIENTS_CSV = pd.read_csv('nycds.csv',
                              index_col=0,
                              true_values=['Yes'],
                              false_values=['No'],
                              nrows=46)
PSA_CLIENTS = PSA_CLIENTS_CSV.transpose()

# Data munging
PSA_CLIENTS['age'] = pd.to_numeric(PSA_CLIENTS['age'])


PSA_CLIENTS['fta_raw_score'] = PSA_CLIENTS.apply(
                            lambda row: calculate_fta_raw_score(row), axis=1)
PSA_CLIENTS['nca_raw_score'] = PSA_CLIENTS.apply(
                            lambda row: calculate_nca_raw_score(row), axis=1)
PSA_CLIENTS['nvca_raw_score'] = PSA_CLIENTS.apply(
                            lambda row: calculate_nvca_raw_score(row), axis=1)

PSA_SCORES = PSA_CLIENTS[
        ['fta_raw_score', 'nca_raw_score', 'nvca_raw_score']].copy()
