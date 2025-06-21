import os
from dataclasses import dataclass, field
from typing import Type, Dict, List

from datetime import datetime
import pandas as pd

from factories import dict_import_path, date_month_dict
from functions import date_treatment, rolling_per_group


@dataclass
class LoadingData:
    type_data: Type[str] = field(default_factory = str)
    
    def __post_init__(self):
        if self.type_data not in os.listdir('.\data\\'):
            raise ValueError("{} not found in data folder".format(self.type_data))
        self.FILEPATH = dict_import_path.get(self.type_data)
    
    def import_parquet_file(self, FILENAME: Type[str]):
        return pd.read_parquet(os.path.join(self.FILEPATH, FILENAME))

@dataclass
class DataTreatment:
    loader: LoadingData
    FILENAME: Type[str]
    data: Type[pd.DataFrame] = field(init=False)
    
    def __post_init__(self):
        self.data = self.loader.import_parquet_file(FILENAME = self.FILENAME)
    
    def init_treatment(self, 
                       data: Type[pd.DataFrame],
                       date_min: Type[str] = '2014-09-01') -> Type[pd.DataFrame]:
        data = data.drop_duplicates(keep='first')
        data['date'] = data['date'].apply(date_treatment)
        data = data[data['date'] >= date_min]
        data.sort_values(by=['date'], ascending=True, inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data
    
    def apply_rolling_per_group(self, data: Type[pd.DataFrame]):
        data['row_id'] = data.index
        rolling_result = (
            data
            .groupby(['types_movie'], group_keys=False)
            .apply(rolling_per_group)
        )
        data['rolling_scores_30d'] = rolling_result.sort_values('row_id')['rolling_scores_30d'].values
        data.drop(columns=['row_id'], inplace=True)
        return data