"""Determine final scores for each client,
using the different risk tools
"""

# get tables with raw scores for each client
import calculate_psa
import calculate_sr
import calculate_cja

FTA_ADJUSTED_SCORES = [(0, 1), (1, 2), (2, 3), (3, 4),
                       (4, 4), (5, 5), (6, 5), (7, 6)]
NCA_ADJUSTED_SCORES = [(0, 1), (1, 2), (2, 2), (3, 3),
                       (4, 3), (5, 4), (6, 4), (7, 5),
                       (8, 5), (9, 6), (10, 6), (11, 6),
                       (12, 6), (13, 6)]
NVCA_FLAG = [(0, False), (1, False), (2, False),
             (3, False), (4, True), (5, True),
             (6, True), (7, True)]


def sr_risk_level(x):
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
    

def cja_risk_level(x):
    if x in list(range(-13, 3)):
        return 'Not recommended for ROR'
    elif x in list(range(3, 7)):
        return 'Moderate risk for ROR'
    elif x in list(range(7, 13)):
        return 'Recommended for ROR'


