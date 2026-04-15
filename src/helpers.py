"""
Helper functions for Toronto Auto Theft project.

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""
import matplotlib.pyplot as plt

def clean_dataset(df):
    """Clean the raw dataset and return an analysis ready DataFrame.

    Parameter:
        df: The raw DataFrame loaded in the notebook.

    Returns:
        A cleaned DataFrame with no missing values, removed unnecessary columns,
        and standardized `LOCATION_TYPE`.
    """
    clean_df = df.copy()
    clean_df = clean_df.dropna()
    clean_df = clean_df.drop (columns = ["OBJECTID", "EVENT_UNIQUE_ID",
                                        "LONG_WGS84", "LAT_WGS84", "x",
                                        "y", "REPORT_DATE",
                                        "OCC_DATE", "UCR_CODE", "UCR_EXT",
                                        "OFFENCE", "CSI_CATEGORY", "REPORT_YEAR",
                                        "REPORT_MONTH", "REPORT_DAY", "REPORT_DOY",
                                        "REPORT_DOW", "REPORT_HOUR"])
    clean_df["LOCATION_TYPE"] = clean_df["LOCATION_TYPE"].str.split('(').str[0]
    clean_df["LOCATION_TYPE"] = clean_df["LOCATION_TYPE"].str.strip()
    clean_df["OCC_YEAR"] = clean_df["OCC_YEAR"].astype(int)
    clean_df["OCC_DAY"] = clean_df["OCC_DAY"].astype(int)
    clean_df["OCC_DOY"] = clean_df["OCC_DOY"].astype(int)
    clean_df = clean_df[clean_df["OCC_YEAR"] >= 2014]
    clean_df["LOCATION_TYPE"] = clean_df["LOCATION_TYPE"].astype(str)

    return clean_df

def yearly_trends_chart(df):
    """Plot yearly auto theft counts in Toronto from 2014 to 2025 with 3 highlighted periods.

    Parameters:
        df: A cleaned DataFrame.

    Returns:
        None. Creates and draws the chart.
    """
    yearly = df.groupby('OCC_YEAR').size()

    fig, ax = plt.subplots(figsize = (12, 6))

    ax.plot(yearly.index, yearly.values, color = 'black', linewidth = 2, marker = 'o')
    ax.axvspan(2017, 2021, color = 'red', alpha = 0.3, label = 'Early Increase')
    ax.axvspan(2021, 2023, color = 'darkred', alpha = 0.5, label = 'Surge Period')
    ax.axvspan(2023, 2025, color = 'green', alpha = 0.3, label = 'Slight Decline')

    ax.set_title('Auto Theft in Toronto 2014-2025', fontsize = 16)
    ax.set_xlabel('Year', fontsize = 13)
    ax.set_ylabel('Number of Thefts', fontsize = 13)
    ax.yaxis.set_major_locator(plt.MultipleLocator(2000))
    ax.set_xticks(yearly.index)
    ax.set_xticklabels(yearly.index, rotation = 45)
    ax.set_ylim(bottom = 0)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()

    plt.tight_layout()
    plt.show()

def top10_neighbourhoods_chart(df):
    """Plot the top 10 most affected neighbourhoods by auto theft count during the surge years of 2021 to 2023.

    Parameters:
        df: A cleaned DataFrame.

    Returns:
        None. Creates and draws the chart.
    """
    top10 = (df[df['OCC_YEAR'].between(2021, 2023)].groupby('NEIGHBOURHOOD_158').size()
               .sort_values(ascending = True)
               .tail(10))

    fig, ax = plt.subplots(figsize = (12, 8))
    ax.set_facecolor('whitesmoke')
    fig.patch.set_facecolor('whitesmoke')

    colors = ['red' if i == len(top10) - 1 else 'blue' for i in range(len(top10))]
    bars = ax.barh(top10.index, top10.values, color = colors, edgecolor ='black', linewidth = 0.8, height = 0.6)

    ax.bar_label(bars, padding = 10, fontweight = 'bold', fontsize = 14)  
    ax.set_title('Top 10 Most Affected Neighbourhoods by Auto Theft During 2021-2023', fontsize = 16)
    ax.set_xlabel('Number of Thefts', fontsize = 10)
    ax.set_ylabel('Neighbourhood', fontsize = 10)
    ax.set_xlim(0, max(top10.values) + 500)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()
