from typing import Type
import pandas as pd
from statsmodels.tsa.stattools import adfuller

import warnings
warnings.filterwarnings('ignore')


def interpret_pvalue(pval: Type[float]) -> Type[str]:
    """
    Interpret the p-value of an ADF statistical test according to standard significance thresholds.

    Args:
        pval (float): The p-value from the ADF test.

    Returns:
        str: Textual interpretation of the p-value.
    """
    if pval < 0.01:
        return "Reject H0 at 1% → Stationary"
    elif pval < 0.05:
        return "Reject H0 at 5% → Stationary"
    elif pval < 0.10:
        return "Reject H0 at 10% → Stationary"
    else:
        return "Fail to reject H0 → Non-stationary"

def adf_test_summary(data: Type[pd.DataFrame]) -> Type[pd.DataFrame]:
    """
    Perform the Augmented Dickey-Fuller (ADF) stationarity test on the 
    'rolling_scores_30d' variable grouped by 'types_movie', and return a 
    summary dataframe including the test statistic, p-value (formatted 
    to 5 decimals), and interpretation.

    Args:
        data (DataFrame): DataFrame containing at least the columns
            'date', 'types_movie', and 'rolling_scores_30d'.

    Returns:
        pd.DataFrame: Summary DataFrame with columns:
            - 'Movie Types Series'
            - 'Statistics' (ADF statistic rounded to 5 decimals, string format)
            - 'P-value' (string format with 5 decimals)
            - 'Test Interpretation' (textual interpretation of the result)
    """
    stat_adf = []
    pval_adf = []
    test_interpretation = []
    movie_types_list = []

    features_for_adf = ['date', 'types_movie', 'rolling_scores_30d']
    df_for_adf_test = data[features_for_adf].copy()
    df_for_adf_test.set_index('date', inplace=True)

    for type_ in df_for_adf_test['types_movie'].unique():
        movie_type_subset = df_for_adf_test[df_for_adf_test['types_movie'] == type_]
        series = movie_type_subset['rolling_scores_30d'].dropna()

        adf_result = adfuller(series)
        stat_adf.append(f"{adf_result[0]:.5f}")
        pval_adf.append(f"{adf_result[1]:.5f}")
        test_interpretation.append(interpret_pvalue(adf_result[1]))
        movie_types_list.append(type_)

    summary_adf_results = pd.DataFrame({
        'Movie Types Series': movie_types_list,
        'Statistics': stat_adf,
        'P-value': pval_adf,
        'Test Interpretation': test_interpretation
    })

    return summary_adf_results