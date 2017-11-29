# pylint: disable=W0108

"""Look at the effect the supervised release algorithm would have for our clients
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from scoring import * # only when scoring.py hasn't already been run

SR = SCORES[['top_chg', 'dv', 'age', 'client_race', 'client_ethnicity', 'client_gender',
             'outcome_bail', 'outcome_bond', 'outcome_custody',
             'sr_score', 'sr_risk', 'sr_chg_ineligible']].copy()
SR['ineligible'] = SR.apply(lambda r: True if r.sr_risk == 'High' or r.sr_chg_ineligible else False,
                            axis=1)

# Looking at only the risk assessment levels
SR.loc[(SR.sr_risk == 'High')
       & SR.outcome_custody.isin(['REMAND', 'BAIL SET']),
       'sr_rai_vs_real'] = 'Same'
SR.loc[(SR.sr_risk == 'High')
       & SR.outcome_custody.isin(['SUP REL', 'ROR']),
       'sr_rai_vs_real'] = 'Worse'
SR.loc[(SR.sr_risk != 'High')
       & SR.outcome_custody.isin(['REMAND', 'BAIL SET']),
       'sr_rai_vs_real'] = 'Better'
SR.loc[(SR.sr_risk != 'High')
       & SR.outcome_custody.isin(['SUP REL', 'ROR']),
       'sr_rai_vs_real'] = 'Same'

# Looking at supervised release as it is today
SR.loc[(SR.ineligible)
       & SR.outcome_custody.isin(['REMAND', 'BAIL SET']),
       'sr_vs_real'] = 'Same'
SR.loc[(SR.ineligible)
       & SR.outcome_custody.isin(['SUP REL', 'ROR']),
       'sr_vs_real'] = 'Worse'
SR.loc[(~SR.ineligible)
       & SR.outcome_custody.isin(['REMAND', 'BAIL SET']),
       'sr_vs_real'] = 'Better'
SR.loc[(~SR.ineligible)
       & SR.outcome_custody.isin(['SUP REL', 'ROR']),
       'sr_vs_real'] = 'Same'

counts_table = pd.DataFrame({'sr_vs_real': SR.sr_vs_real.value_counts(),
                             'sr_rai_vs_real': SR.sr_rai_vs_real.value_counts()})
counts_table['rai_pct'] = counts_table['sr_rai_vs_real'].apply(
    lambda x: (x/counts_table['sr_rai_vs_real'].sum())*100)
counts_table['sr_pct'] = counts_table['sr_vs_real'].apply(
    lambda x: (x/counts_table['sr_rai_vs_real'].sum())*100)

# Plotting
fig, ax = plt.subplots(1, 1)
ax.get_xaxis().set_visible(False)
SR.groupby(['client_race', 'sr_vs_real']) \
  .size() \
  .unstack(1) \
  .fillna(0) \
  .rename_axis(None, axis='columns') \
  .plot.bar(table=True,
            title="How would our clients do under SR?",
            label=None,
            ax=ax)


fig, ax = plt.subplots(1, 1)
ax.get_xaxis().set_visible(False)
SR.groupby(['dv', 'sr_vs_real']) \
  .size() \
  .unstack(1) \
  .fillna(0) \
  .rename_axis(None, axis='columns') \
  .plot.bar(table=True,
            title="How would our clients do under SR?",
            label=None,
            ax=ax)

fig, ax = plt.subplots(1, 1)
ax.get_xaxis().set_visible(False)
SR.groupby(['sr_risk', 'sr_vs_real']) \
  .size() \
  .unstack(1) \
  .fillna(0) \
  .rename_axis(None, axis='columns') \
  .reindex(['Low', 'Low Medium', 'Medium', 'Medium High', 'High']) \
  .plot.bar(table=True,
            title="How would our clients do under SR?",
            label=None,
            ax=ax)

SR.groupby([SR.top_chg.str.endswith('VF'), 'sr_vs_real']) \
  .size() \
  .unstack(1) \
  .fillna(0) \
  .rename_axis(None, axis='columns')
 
