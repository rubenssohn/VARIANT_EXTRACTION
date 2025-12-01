'''
VARIANT_EXTRACTION — A Python package and CLI tool to extract and visualize process behaviors from complex event data.
Copyright (C) 2023  Christoffer Rubensson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Website: https://hu-berlin.de/rubensson
E-Mail: {firstname.lastname}@hu-berlin.de
'''

import pandas as pd
from ...utils.data_processing import get_activity_statistics

#####################
### COALESCING and FILTERING
#####################
def classify_activity_behavior(activity, 
                               FREQ_COL='freq_percase_mean', 
                               POS_COL='pos_percase_std', 
                               THRESH_FREQ_PERCASE_MEAN=1.1, 
                               THRESH_POS_PERCASE_STD=0.15):
    '''Classify activity behavior based on frequency and position standard deviation.
    '''
    frequency_class = activity[FREQ_COL] <= THRESH_FREQ_PERCASE_MEAN
    position_class = activity[POS_COL] <= THRESH_POS_PERCASE_STD
    if frequency_class and position_class:
        return 'O1'  # Occurency low / Position std low
    elif frequency_class and not position_class:
        return 'O2'  # Occurency low / Position std high
    elif not frequency_class and position_class:
        return 'M1'  # Occurency high / Position std low
    elif not frequency_class and not position_class:
        return 'M2'  # Occurency high / Position std high
    
def classify_coalescing_method(
        activity,
        BEHAVIOR_CLASS="activity:behavior:class",
        SKEW_COL="pos_percase_std"):
    """Checks which coalescing method to be used. 
    """
    skew_class = activity[SKEW_COL]
    behavior_class = activity[BEHAVIOR_CLASS] 

    if behavior_class == 'M2':
        if skew_class > 0:
            return 'first'
        else:
            return 'last'


def coalesce_repeating_events(
        df, 
        activity_list:list, 
        coalesc_type=str, 
        ACT_COL="concept:name", 
        CASE_COL="case:concept:name", 
        ORDER_COL="order:position", 
        MAXORDER_COL="order:position:max", 
        IGNORE_COL="events:ignore", 
        reset_ignore_col = False,
        drop_events = False):
    '''
    Coalesce a list of activities.

    Parameters
    ----------
    IGNORE_COL (str): 
        The column name, which marks events to be filtered.
    coalesc_type (str): 
        Options are ['first', 'last'], where 'first' keeps first event and 'last' the last
    '''
    if IGNORE_COL not in df.columns or reset_ignore_col:
        df[IGNORE_COL] = 0
    # create condition for marking events to coalesce
    condition = pd.Series(False, index=df.index)
    activity_mask = df[ACT_COL].isin(activity_list)
    # Choose condition
    if coalesc_type == "first":
        condition = activity_mask & (df[ORDER_COL] > 0)
    elif coalesc_type == "last":
        condition = activity_mask & (df[ORDER_COL] < df[MAXORDER_COL])
    else:
        raise ValueError("coalesc_type must be 'first' or 'last'") 
    # Mark the IGNORE column only (do not overwrite entire rows)
    df.loc[condition, IGNORE_COL] = 1
    if drop_events:
        indices_to_drop = df.loc[df[IGNORE_COL].isin([1])].index
        df.drop(indices_to_drop)

    return df

# Coalescing orchestrator
def apply_coalescing_to_dataframe(
        df, 
        ACT_COL="concept:name", 
        CASE_COL="case:concept:name", 
        ORDER_COL="order:position", 
        MAXORDER_COL="order:position:max", 
        IGNORE_COL="events:ignore",
        reset_ignore_col=False,
        drop_events = False):
    '''Coalescs events in a dataframe.
    '''
    
    # Extract activity statistics as a matrix
    df_act_statistics = df.groupby(ACT_COL, sort=False).apply(get_activity_statistics)
    # define coalescing classes
    df_act_statistics['activity:behavior:class'] = df_act_statistics.apply(classify_activity_behavior, axis=1)
    df_act_statistics['coalescing:class'] = df_act_statistics.apply(classify_coalescing_method, axis=1)
    #print(df_act_statistics['coalescing:class'].unique())
    #test = df_act_statistics.copy()
    # create a new column with coalescing class in dataframe
    for coalesc_type in df_act_statistics['coalescing:class'].dropna().unique():
        activity_list = df_act_statistics.loc[
            df_act_statistics['coalescing:class'] == coalesc_type
        ].index.tolist()
        df = coalesce_repeating_events(
            df, 
            activity_list=activity_list, 
            coalesc_type=coalesc_type, 
            ACT_COL=ACT_COL,
            CASE_COL=CASE_COL,
            ORDER_COL=ORDER_COL,
            MAXORDER_COL=MAXORDER_COL,
            IGNORE_COL=IGNORE_COL,
            reset_ignore_col=reset_ignore_col,
            drop_events=drop_events)
    return df