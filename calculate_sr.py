"""Calculate NY Supervised Release Score"""

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

def ny_sr_pending(row):
    """Open Cases
    """
    #If OPEN-MISD-STATUS = "Open - Pre-Plea" or if OPEN-FEL-STATUS = "Open - Pre-Plea", then +1;
    #else -1
    return 1 if ((row['OPEN_MISD_STATUS'] == 'Open - Pre-Plea')
                 or (row['OPEN_FEL_STATUS'] == 'Open - Pre-Plea')) else 0

def ny_sr_first_arrest(x):
    """First Arrest
    """
    return -3 if x == 'Yes' else 3

def ny_sr_war(row):
    """Warrant in last 4 years
    """
    #If the date of (WAR-PREDISPO-RECENT-DT-1ST or WAR-PREDISPO-2Y-DT or WAR-POSTDISPO-DT) is within 4 years of date of arraignment, then +1; else -1
    return row

def ny_sr_misd_conv(row):
    """Misd. Conv. in last 1 years
    """
    #If the date of CONV-MISD-DT is within 1 year of arraignment;
    #or if OPEN-MISD-PLEA-CHG is a misdemeanor and OPEN-MISD-PLEA-DT is within 1 year of arraignment;
    #or if OPEN-FEL-PLEA-CHG is a misdemeanor and OPEN-FEL-PLEA-DT is within 1 year of arraignment, then +2;
    #else -2
    return row

def ny_sr_fel_conv(row):
    """Fel. Conv. in last 9 years
    """
    #If the date of CONV-FEL-DT is within 9 years of arraignment;
    #or if OPEN-MISD-PLEA-CHG is a felony and OPEN-MISD-PLEA-DT is within 9 years of arraignment;
    #or if OPEN-FEL-PLEA-CHG is a felony and OPEN-FEL-PLEA-DT is within 9 years of arraignment, then +1;
    #else -1
    return row

def ny_sr_drug_conv(row):
    """Drug Conv. in last 9 years
    """
    #If the date of CONV-DRUG-DT is within 9 years of arraignment, then +2; else -2
    return row

def ny_sr_fulltime_act(row):
    """Fulltime Activity
    """
    return -2 if row['FULLTIME'] == 'Yes' else 2

def calculate_sr_score(row):
    """Calculate the final SR score for any given client
    """
    score = 0
    score = score + ny_sr_age(row['AGE'])
    score = score + ny_sr_pending(row)
    score = score + ny_sr_first_arrest(row['FIRST_ARREST'])
    score = score + ny_sr_war(row)
    score = score + ny_sr_misd_conv(row)
    score = score + ny_sr_fel_conv(row)
    score = score + ny_sr_drug_conv(row)
    score = score + ny_sr_fulltime_act(row)
    return score
