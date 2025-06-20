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
        xy=(x_arrow, y_arrow + 600),
        xytext=(x_arrow + 0.3, y_arrow + 3500),
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
    plt.ylim([0, 18000])
    plt.tight_layout()
    plt.show()