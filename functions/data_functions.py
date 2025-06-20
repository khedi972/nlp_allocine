import sys
import os

project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import pandas as pd

from typing import Type
from datetime import datetime
from factories import date_month_dict

import warnings
warnings.filterwarnings('ignore')


def date_treatment(date_str: Type[str]):
    
    """
    The function reads each scrape date (in string) and does the following processing:
    
    - breakdown of each string element: day, month, year
    - each element is reformatted to an integer
    - use reformatted elements to construct a date (in datetime format)
    
    Args:
        date_str (str): Date string (FR) -> 4 Mai 2016.
        
    Returns:
        All dates are now in Python datetime format.
    """
    
    day_str, month_str, year_str = date_str.split(' ')
    
    day_dt = int(day_str)
    month_dt = date_month_dict.get(month_str)
    if month_dt is None:
        raise ValueError(f"Month '{month_str}' not recognized in date_month_dict.")
    else:
        month_dt = int(month_dt)
    year_dt = int(year_str)

    return datetime(year_dt, month_dt, day_dt )


def rolling_per_group(data: Type[pd.DataFrame], rolling_days: Type[str] = '30D'):
    """
    This function computes a centered rolling mean of the 'scores' column for a given group of data.

    Processing steps:
    - Sorts the DataFrame by 'date' in ascending order
    - Sets the 'date' column as the index (necessary for time-based rolling operations)
    - Applies a centered rolling mean over the specified time window (default: 30 days)
    - Stores the result in a new column called 'rolling_scores_30d'
    - Resets the index to bring 'date' back as a column

    Args:
        data (DataFrame): A DataFrame containing at least 'date' and 'scores' columns.
        rolling_days (str, optional): A string defining the size of the rolling window (e.g., '30D').

    Returns:
        DataFrame: The original DataFrame with an added 'rolling_scores_30d' column.
    """
    data = data.sort_values('date').set_index('date')
    data['rolling_scores_30d'] = data['scores'].rolling(rolling_days, center=True).mean()
    return data.reset_index()

