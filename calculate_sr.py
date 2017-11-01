def ny_sr_age(row):
    """Age
    """
    #If AGE = 16-19, then +6;
    #if AGE = 20-29, then +1;
    #if AGE = 30-39, then -3;
    #if AGE is greater than or equal to 40, then -4.

def ny_sr_pending(row):
    """Open Cases
    """
    #If OPEN-MISD-STATUS = "Open - Pre-Plea" or if OPEN-FEL-STATUS = "Open - Pre-Plea", then +1;
    #else -1
    return row

def ny_sr_first_arrest(row):
    """First Arrest
    """
    #If FIRST-ARREST = "Yes", then -3; else +3
    return row

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
    #If FULLTIME-ACTIVITY = "Yes", then -2; else +2
    return row
