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
