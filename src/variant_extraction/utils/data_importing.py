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