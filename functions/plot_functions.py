import warnings
from typing import Type

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

warnings.filterwarnings('ignore')


def set_plot_style():
    """
    Applies a consistent and clean visual style for matplotlib and seaborn plots.

    This function configures:
    - The seaborn theme (`whitegrid`) with a muted color palette
    - Matplotlib default style and custom `rcParams` for:
        - Grid appearance and transparency
        - Axis spines removal (cleaner look)
        - Font sizes for titles, labels, and ticks
        - Figure size and resolution
        - Axis label padding
        - Tick visibility and alignment

    Recommended to call at the beginning of a script or notebook 
    to standardize all plots in your analysis.

    Note:
        You can uncomment `"figure.dpi": 300` if you want to change screen rendering resolution.
    """
    sns.set_theme(style="whitegrid", palette="muted")

    plt.style.use("default")
    plt.rcParams.update(
        {
            "axes.edgecolor": "white",
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.color": "grey",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.titlesize": 10,
            "axes.labelsize": 10,
            "axes.labelpad": 15,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            # "figure.dpi": 300,
            "savefig.dpi": 300,
            "figure.figsize": (12, 6),
            "xtick.bottom": False,
            "ytick.left": False,
        }
    )

def plot_movie_type_distribution(data: Type[pd.DataFrame], column: Type[str] = 'types_movie') -> None:
    """
    Plot the distribution of movie types as a bar chart, including percentage labels 
    and an annotation for under-represented categories.

    This function calculates the frequency and relative percentage of a specified column
    in a DataFrame (default is 'types_movie') and creates a bar chart showing the distribution.
    It also highlights two under-represented movie types with an annotation arrow.

    Args:
        data (DataFrame): The input DataFrame containing movie data.
        column (str): The name of the column containing movie type labels. 
            Defaults to 'types_movie'.

    Returns:
        None: Displays the bar chart but does not return any object.
    """
    
    # compute count and percentage
    tab_types = data[column].value_counts(sort=True)
    tab_types_pct = (tab_types / data.shape[0]) * 100

    plt.figure(figsize=(10, 6))
    bars = plt.bar(tab_types.index, tab_types.values, color="steelblue")

    # adding percentage labels above bars
    for idx, pct in enumerate(tab_types_pct):
        y_val = tab_types.values[idx]
        plt.text(idx, y_val, f"{pct:.2f}%", ha='center', va='bottom', fontsize=8)

    # annotation (arrow) between two specific under-represented bars
    target_idx_arrow1, target_idx_arrow2 = 5, 6
    x_arrow = (target_idx_arrow1 + target_idx_arrow2) / 2
    y_arrow = max(tab_types.values[[target_idx_arrow1, target_idx_arrow2]])

    plt.annotate(
        "Under-Representation",
        xy=(x_arrow, y_arrow + 200),
        xytext=(x_arrow + 0.3, y_arrow + 1000),
        arrowprops=dict(arrowstyle="->", color="firebrick", lw=1.5),
        fontsize=9,
        color="black",
        ha='center'
    )

    # plot formatting
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.xlabel('Movie Types')
    plt.ylabel('Count & Percentage (%)')
    plt.title('Movie Types Distribution', pad=15)
    plt.ylim([0, 4000])
    plt.tight_layout()
    plt.show()
    
def plot_moving_averages(dataset: Type[pd.DataFrame],
                         figsize: Type[tuple]) -> None:
    """
    Plot two subplots in a single figure:
    1) Overall moving average of 'rolling_scores_30d' by date.
    2) Moving average of 'rolling_scores_30d' by date and separated by 'types_movie'.

    Args:
        dataset (DataFrame): DataFrame with columns 'date', 'types_movie', and 'rolling_scores_30d'.
        figsize (tuple): Figure size.

    Returns:
        None: Displays the figure with two subplots.
    """
    # prepare overall series (mean per date and no movie types)
    unique_serie = dataset[['date', 'rolling_scores_30d']].groupby('date', as_index=False)['rolling_scores_30d'].mean()
    y_min1, y_max1 = unique_serie['rolling_scores_30d'].min(), unique_serie['rolling_scores_30d'].max()

    # prepare min/max for all data (with movie types)
    y_min2, y_max2 = dataset['rolling_scores_30d'].min(), dataset['rolling_scores_30d'].max()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

    # plot overall moving average
    ax1.plot(unique_serie['date'], unique_serie['rolling_scores_30d'], linewidth=0.85)
    ax1.axhspan(y_min1, y_max1, xmin=0, xmax=1, color='green', alpha=0.1)
    ax1.xaxis.set_major_locator(mdates.YearLocator(base=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.set_ylim([0, 5])
    ax1.set_title('Moving Average of scores', fontsize=10)

    # plot moving average by movie types
    for type_ in dataset['types_movie'].unique():
        type_df = dataset[dataset['types_movie'] == type_]
        ax2.plot(type_df['date'], type_df['rolling_scores_30d'], linewidth=1, alpha=0.7, label=type_)
    ax2.axhspan(y_min2, y_max2, xmin=0, xmax=1, color='green', alpha=0.1)
    ax2.xaxis.set_major_locator(mdates.YearLocator(base=1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.set_ylim([0, 5])
    ax2.legend(fontsize=8)
    ax2.set_title('Moving Average of scores by type of movies', fontsize=10)

    plt.tight_layout(pad=5)
    plt.show()