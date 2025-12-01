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
import pm4py
from pathlib import Path

def load_event_log(
        filename: str, foldername="event_data") -> pd.DataFrame:
    """Loads an event log from the specified folder and filename."""
    if filename.endswith(".xes"):
        data_path = Path(__file__).parent.parent.parent.parent / "data" / foldername / filename
        print(data_path)
        df = pm4py.read_xes(str(data_path))
    else:
        raise ValueError("'Filename' must be an .xes file and\n\
                         be in the folder 'data/processed_event_data'.")
    return df