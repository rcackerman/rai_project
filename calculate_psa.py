"""Calculate the Arnold Foundation PSA score
"""

import os
import pandas as pd

def pending(row, count_acd=False):
    """Generalized check for pending charge at the time of offense
    """
    if count_acd == False:
        return True if (pd.notnull(row['OPEN_MISD_STATUS']) |
                        pd.notnull(row['OPEN_FEL_STATUS'])) else False
    else:
        return True if (pd.notnull(row['OPEN_MISD_STATUS']) |
                        pd.notnull(row['OPEN_FEL_STATUS']) |
                        pd.notnull(row['OPEN_ACD'])) else False

def prior_convictions(row):
    return True if (pd.notnull(row['CONV_MISD_DT']) |
                    pd.notnull(row['CONV_FEL_DT'])) else False

def number_warrants(row):
    if pd.notnull(row['WAR_PREDISPO_RECENT_DT_2ND']):
        return 2
    if pd.notnull(row['WAR_PREDISPO_RECENT_DT_1ST']):
        return 1
    else:
        return 0

def psa_fta_pending(row):
    """Pending charge at the time of offense
    """
    return 1 if pending(row) else 0

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
    return 1 if pd.notnull(row['WAR_PREDISPO_2Y_DT']) else 0

def psa_nca_age(row):
    """Age at current arrest
    If AGE is less than or equal to 22, then +2; else 0
    """
    return 2 if row['age'] <= 22 else 0

def psa_nca_pending(row):
    """Pending charge at the time of offense
    If OPEN-MISD-STATUS or OPEN-FEL-STATUS contain data, then +3; else 0
    """
    return 3 if pending(row) else 0

def psa_nca_misd_conv(row):
    """Prior misdemeanor conviction
    If CONV-MISD-DT contains data, then +1, else 0
    """
    return 1 if pd.notnull(row['CONV_MISD_DT']) else 0

def psa_nca_fel_conv(row):
    """Prior felony conviction
    If CONV-FEL-DT contains data, then +1, else 0
    """
    return 1 if pd.notnull(row['CONV_FEL_DT']) else 0

def psa_vio_conv(row):
    """Prior violent conviction
    If CONV-VIO-DT-3RD contains data, then +2;
    if CONV-VIO-DT-1ST contains data, but CONV-VIO-DT-3RD is empty, then +1; else 0
    """
    if pd.notnull(row['CONV_VIO_DT_3RD']):
        return 2
    if pd.notnull(row['CONV_VIO_DT_1ST']):
        return 1
    else:
        return 0

def psa_nca_new_war(row):
    """Prior failure to appear pretrial in past 2 years
    """
    return number_warrants(row)

def psa_nca_prior_sentence(row):
    """Prior setence to incarceration
    If PRIOR-SENTENCE = "Yes", then +2; else 0
    """
    return 2 if row(['PRIOR_SENTENCE']) == 'Yes' else 0

def psa_nvca_vio_chg(row):
    """Current violent offense
    If TOP-CHG = crime of violence, then +2; else 0
    """
    return 2 if (row['TOP_CHG'] in VIOLENT_CRIMES) else 0

def psa_nvca_viochg_age(row):
    """Current violent offense & 20 years or younger
    If TOP-CHG = crime of violence and AGE is less than or equal to 20, then +1; else 0
    """
    return 1 if ((row['TOP_CHG'] in VIOLENT_CRIMES) & (row['AGE'] <= 20)) else 0

def psa_nvca_pending(row):
    """Pending charge at the time of offense
    If OPEN-MISD-STATUS or OPEN-FEL-STATUS contain data, then +1; else 0
    """
    return 1 if pending(row) else 0

def psa_nvca_prior_conv(row):
    """Prior conviction
    If CONV-MISD-DT or CONV-FEL-DT contain data, then +1, else 0
    """
    return 1 if prior_convictions(row) else 0


CSV = pd.read_csv()
with open('f', 'r') as f:
    VIOLENT_CRIMES = f.readlines()

clients = CSV.pivot()
