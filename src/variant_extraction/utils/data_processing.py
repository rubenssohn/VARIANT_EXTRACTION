import math
import numpy as np
import pandas as pd
import pm4py

def simplifyLog(df: pd.DataFrame, 
                lifecycle_activities=False, 
                filter_cases = 0, 
                filter_variants_k = 0, 
                filter_variants_per = 0):
    '''simplifies a log by keeping only necessary attributes.
    '''
    #keep following columns
    CASE_COL = 'case:concept:name'
    ACT_COL = 'concept:name'
    TIME_COL = 'time:timestamp'
    lifecycle = 'lifecycle:transition'
    # create new activities with transitions
    if (lifecycle_activities == True and 
        lifecycle in df.columns):
        if len(df[lifecycle].unique()) > 1:
            df[ACT_COL] = df[ACT_COL] + '-' + df[lifecycle]
        else:
            print('Message: No transition-activity were be created. Only one type of lifecycle transition in log.')
    else:
        print('Message: No transition-activity were be created. No transition column.')
    # keep only k amount cases in the log
    total_num_variants = len(pm4py.get_variants(df))
    if filter_cases > 0:
        case_list = df[CASE_COL].unique()[0:filter_cases]
        df = pm4py.filter_event_attribute_values(df, CASE_COL, case_list, level="case", retain=True).copy()
    elif filter_variants_k > 0:
        df = pm4py.filter_variants_top_k(df, filter_variants_k).copy()
    elif filter_variants_per > 0:
        filter_variants_k = math.ceil(filter_variants_per*total_num_variants)
        df = pm4py.filter_variants_top_k(df, filter_variants_k).copy()

    #filter log
    keep_columns = [CASE_COL, ACT_COL, TIME_COL]
    df = df.filter(keep_columns)
    return df

# Create relative timestamps
def relativeTimestamps(
        df: pd.DataFrame,
        CASE_COL="case:concept:name",
        TIME_COL="time:timestamp",
        RTIME_COL="time:timestamp:relative",
        RTIME_SEC_COL="time:relative:seconds"):
    '''adds relative timestamps to dataframe (log).
    '''
    starttimes_dict = df.groupby(CASE_COL)[TIME_COL].min().to_dict()
    df["time:timestamp:casestart"] = df[CASE_COL].map(starttimes_dict)
    df[RTIME_COL] = df[TIME_COL] - df["time:timestamp:casestart"]
    df[RTIME_SEC_COL] = df[RTIME_COL].apply(lambda t: t.total_seconds()).astype(int)
    df['time:relative:seconds:log'] = np.log(df[RTIME_SEC_COL] + 1)

    return df

# Filtering
def normalize_reltimes_log(
        df: pd.DataFrame, 
        RTIME_SEC_COL="time:relative:seconds", 
        CASE_COL="case:concept:name",
        NRTIMECASE_COL = "time:relative:normalized:case", 
        NRTIMELOG_COL = "time:relative:normalized:log"):
    """Normalize relative timestamps by log and by case."""
    # define relative timestamps
    df = relativeTimestamps(df)

    # --- log-level normalization of relative timestamps
    mins_l = df[RTIME_SEC_COL].min()
    maxs_l = df[RTIME_SEC_COL].max()
    denom_l = (maxs_l - mins_l)
    df[NRTIMELOG_COL] = (df[RTIME_SEC_COL] - mins_l) / denom_l

    # --- case-level normalization of relative timestamps
    eventgroups = df.groupby(CASE_COL)[RTIME_SEC_COL]
    mins_c = eventgroups.transform("min")
    maxs_c = eventgroups.transform("max")
    denom_c = (maxs_c - mins_c)
    # avoid division-by-zero
    df[NRTIMECASE_COL] = (df[RTIME_SEC_COL] - mins_c) / denom_c.replace(0, pd.NA)
    df[NRTIMECASE_COL] = df[NRTIMECASE_COL].fillna(0)
    return df

# Activity statistics
def get_activity_statistics(activity, 
                            CASE_COL="case:concept:name", 
                            RTIME_COL="time:relative:seconds", 
                            NRTIMELOG_COL="time:relative:normalized:log", 
                            NRTIMECASE_COL="time:relative:normalized:case"):
    """Calculate statistics for a given activity in an event log."""
    
    qs = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]  # quantiles
    
    # --- Frequencies per case ---
    freq_percase_list = activity.groupby(CASE_COL)[RTIME_COL].count()
    freq_percase_quantiles = freq_percase_list.quantile(qs)
    freq_percase_mean = freq_percase_list.mean()
    #freq_percase_mode = freq_percase_list.mode()
    freq_percase_median = freq_percase_list.median()
    freq_percase_var = freq_percase_list.var(ddof=0)
    freq_percase_std = freq_percase_list.std(ddof=0)
    freq_percase_skew = freq_percase_list.skew()
    
    # --- Positions based on relative normalized times by log and by case ---
    pos_log_list = activity[NRTIMELOG_COL]
    #print(pos_log_list)
    pos_log_quantiles = pos_log_list.quantile(qs)
    pos_log_mean, pos_log_median, pos_log_var, pos_log_std, pos_log_skew =\
    pos_log_list.mean(), pos_log_list.median(), pos_log_list.var(ddof=0), pos_log_list.std(ddof=0), pos_log_list.skew()
    
    pos_percase_list = activity[NRTIMECASE_COL]
    #print(pos_percase_list)
    pos_percase_quantiles = pos_percase_list.quantile(qs)
    pos_percase_mean, pos_percase_median, pos_percase_var, pos_percase_std, pos_percase_skew =\
    pos_percase_list.mean(), pos_percase_list.median(), pos_percase_list.var(ddof=0), pos_percase_list.std(ddof=0), pos_percase_list.skew()
    
    # --- Data ---
    data = {
        'freq_log_absolute': len(activity[RTIME_COL]),
        'freq_percase_mean': freq_percase_mean,
        #'freq_percase_mode': freq_percase_mode,
        'freq_percase_median': freq_percase_median,
        'freq_percase_var': freq_percase_var,
        'freq_percase_std': freq_percase_std,
        'freq_percase_skew': freq_percase_skew,
        'pos_log_mean': pos_log_mean,
        #'pos_log_mode': pos_log_mode,
        'pos_log_median': pos_log_median,
        'pos_log_var': pos_log_var,
        'pos_log_std': pos_log_std,
        'pos_log_skew': pos_log_skew,
        'pos_percase_mean': pos_percase_mean,
        #'pos_percase_mode': pos_percase_mode,
        'pos_percase_median': pos_percase_median,
        'pos_percase_var': pos_percase_var,
        'pos_percase_std': pos_percase_std,
        'pos_percase_skew': pos_percase_skew
    }
    
    # add quantiles to data
    for q, val in zip(qs, freq_percase_quantiles):
        data[f'freq_percase_q{int(q*100):02d}'] = val
    for q, val in zip(qs, pos_log_quantiles):
        data[f'pos_log_q{int(q*100):02d}'] = val
    for q, val in zip(qs, pos_percase_quantiles):
        data[f'pos_percase_q{int(q*100):02d}'] = val
    
    return pd.Series(data)

def map_values_to_col(df, df_ranks, key_cols, rank_col_name):
    '''Maps values from df_ranks into df using the key_cols.
    Assumes key_cols form a unique key in df_ranks.
    '''
    # Build a MultiIndex dictionary
    rank_dict = (
        df_ranks
            .set_index(key_cols)[rank_col_name]
            .to_dict()
    )
    return df[key_cols].apply(tuple, axis=1).map(rank_dict)

def add_activity_position_percase(
        df: pd.DataFrame,
        CASE_COL="case:concept:name", 
        ACT_COL="concept:name", 
        TIME_COL="time:timestamp", 
        ORDER_COL="order:position", 
        MAXORDER_COL="order:position:max"):
    # df columns: case, time, activity
    df = df.sort_values([CASE_COL, TIME_COL]).copy()
    df[ORDER_COL] = df.groupby([CASE_COL, ACT_COL]).cumcount()
    df[MAXORDER_COL] = df.groupby([CASE_COL, ACT_COL])[ORDER_COL].transform("max")
    return df

def group_unique_values_to_dict(
    df: pd.DataFrame, 
    key_col: str, 
    item_col: str,
    order_by: str | None = None,
    ascending: bool = True,
):
    '''
    Group the dataframe by `key_col` and return a dictionary where each key is a 
    unique value from `key_col` and each value is a list of unique `item_col` 
    entries for that group. Optionally sort each group's values by `order_by`.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    key_col : str
        The column to group by.
    item_col : str
        The column whose unique values will be collected for each group.
    order_by : str, optional
        Column used to sort values within each group before collecting them.
        If None, values are returned in their original appearance order.
    ascending : bool, optional
        Whether sorting by `order_by` is ascending.

    Returns
    -------
    dict
        Mapping each unique `key_col` value to a list of unique `item_col` values.
    '''
    
    grouped = df.groupby(key_col)

    result = {}

    for key, group in grouped:
        if order_by:
            group = group.sort_values(order_by, ascending=ascending)

        # ensure uniqueness in sorted order
        unique_vals = group[item_col].drop_duplicates().tolist()

        result[key] = unique_vals

    return result