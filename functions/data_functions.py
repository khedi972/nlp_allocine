import sys
import os

project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from typing import Type
from datetime import datetime
from factories import date_month_dict

import warnings
warnings.filterwarnings('ignore')


def date_treatment(date_str: Type[str]):
    """The function transforms and put the datetime python format to our date feature"""
    
    # splitting elements that compose date feature
    day_str, month_str, year_str = date_str.split(' ')
    
    # pre format elements
    day_dt = int(day_str)
    month_dt = date_month_dict.get(month_str)
    year_dt = int(year_str)

    # returning a datetime python 
    return datetime(year_dt, month_dt, day_dt )