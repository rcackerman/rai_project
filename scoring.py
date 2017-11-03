"""Determine final scores for each client,
using the different risk tools
"""

# Get tables with raw scores for each client
from . import PSA_SCORES
from . import SR_SCORES
from . import CJA_SCORES

FTA_SCORES = [(0,1), (1,2), (2,3), (3,4),
              (4,4), (5,5), (6,5), (7,6)]
NCA_SCORES = [(0,1), (1,2), (2,2), (3,3),
              (4,3), (5,4), (6,4), (7,5),
              (8,5), (9,6), (10,6), (11,6),
              (12,6), (13,6)]
NVCA_FLAG = [(0, False), (1, False), (2, False),
             (3, False), (4, True), (5, True),
             (6, True), (7, True)]
