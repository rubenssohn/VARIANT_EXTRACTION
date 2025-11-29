import pandas as pd

#####################
### COMMUNITY AND ACTIVITY RANKING
#####################

def rank_entities(
    df: pd.DataFrame,
    group_cols,            # list of columns to group by (e.g., ["stage", "community"])
    value_col,             # which column to aggregate (e.g., NRTIMECASE_COL)
    agg_type="mean",       # "mean", "median", "min", "max"
    sort_cols=None,        # optional explicit sort order
    rank_col_name="rank",   # name for the new rank column
    rank_within_col=None        # NEW: columns to restart ranking within
):
    """Generic ranking function for any entity based on groupings and aggregates.
    """

    agg_funcs = {
        "min": "min",
        "max": "max",
        "mean": "mean",
        "median": "median",
    }

    if agg_type not in agg_funcs:
        raise ValueError(f"agg_type must be one of {list(agg_funcs.keys())}")

    agg_name = f"{agg_type}_value"
    # Default sort = group columns + aggregated value
    if sort_cols is None:
        sort_cols = group_cols + [agg_name]
    else:
        sort_cols = sort_cols + [agg_name]

     # Extract features through aggregation
    df_ranks = (
        df.groupby(group_cols)[value_col]
          .agg(agg_funcs[agg_type])
          .reset_index(name=agg_name)
          .sort_values(sort_cols)
          .reset_index(drop=True)
    )

    # Ranking all values
    if rank_within_col is None:
        # Global ranking using index
        df_ranks[rank_col_name] = df_ranks.index# + 1
    else:
        # Per-group ranking using cumcount
        df_ranks[rank_col_name] = (
            df_ranks.groupby(rank_within_col).cumcount()# + 1
        )

    return df_ranks