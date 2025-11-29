import pandas as pd
import numpy as np

#####################
### STAGE CREATION
#####################

# TODO: Add different types of time windowing
def return_timewindows_column(
        df,
        NRTIMECASE_COL="time:relative:normalized:case",
        num_stages=5,
        type="equal"
    ):
    '''Creates stages by binning the timestamps in a dataframe.
    '''
    
    col = df[NRTIMECASE_COL]
    min_val, max_val = col.min(), col.max()
    # compute equally spaced bin edges
    edges = np.linspace(min_val, max_val, num_stages + 1)

    # cut into bins
    if num_stages <= 1:
        return 0
    else:
        return pd.cut(
            col, bins=edges, labels=False, include_lowest=True)
