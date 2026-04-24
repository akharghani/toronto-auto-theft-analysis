"""
Helper functions for Toronto Auto Theft project.

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""
import matplotlib.pyplot as plt

def strip_suffix(df, column):
    """Remove parenthetical suffixes from a string column and strip whitespace.

    Parameters:
        df: The DataFrame containing the column.
        column: The name of the column to clean.

    Returns:
        A Series with the suffix removed and whitespace stripped.
    """
    return df[column].str.split('(').str[0].str.strip()

def convert_columns_to_int(df, columns):
    """Convert a list of columns to integer type.

    Parameters:
        df: The DataFrame to modify.
        columns: A list of column names to convert.

    Returns:
        The DataFrame with the specified columns cast to int.
    """
    for column in columns:
        df[column] = df[column].astype(int)
    return df

def convert_columns_to_str(df, columns):
    """Convert a list of columns to string type.

    Parameters:
        df: The DataFrame to modify.
        columns: A list of column names to convert.

    Returns:
        The DataFrame with the specified columns cast to str.
    """
    for column in columns:
        df[column] = df[column].astype(str)
    return df

def drop_columns(df):
    """Drop columns not needed for analysis.

    Parameters:
        df: The DataFrame to modify.

    Returns:
        The DataFrame with unnecessary columns removed.
    """
    return df.drop(columns = ["OBJECTID", "EVENT_UNIQUE_ID",
                             "LONG_WGS84", "LAT_WGS84", "x",
                             "y", "REPORT_DATE",
                             "OCC_DATE", "UCR_CODE", "UCR_EXT",
                             "OFFENCE", "CSI_CATEGORY", "REPORT_YEAR",
                             "REPORT_MONTH", "REPORT_DAY", "REPORT_DOY",
                             "REPORT_DOW", "REPORT_HOUR"])

def strip_column_suffixes(df):
    """Strip parenthetical suffixes from location and neighbourhood columns.

    Parameters:
        df: The DataFrame to modify.

    Returns:
        The DataFrame with suffixes removed from LOCATION_TYPE, NEIGHBOURHOOD_158, and NEIGHBOURHOOD_140.
    """
    df["LOCATION_TYPE"] = strip_suffix(df, "LOCATION_TYPE")
    df["NEIGHBOURHOOD_158"] = strip_suffix(df, "NEIGHBOURHOOD_158")
    df["NEIGHBOURHOOD_140"] = strip_suffix(df, "NEIGHBOURHOOD_140")
    return df

def convert_column_types(df):
    """Convert columns to their correct data types.

    Parameters:
        df: The DataFrame.

    Returns:
        The DataFrame with OCC_YEAR, OCC_DAY, and OCC_DOY cast to int and LOCATION_TYPE cast to str.
    """
    df = convert_columns_to_int(df, ["OCC_YEAR", "OCC_DAY", "OCC_DOY"])
    df = convert_columns_to_str(df, ["LOCATION_TYPE"])
    return df

def clean_dataset(df):
    """Clean the raw dataset and return an analysis ready DataFrame.

    Parameter:
        df: The raw DataFrame.

    Returns:
        A cleaned DataFrame with no missing values, removed unnecessary columns,
        standardized LOCATION_TYPE, stripped neighbourhood names, and corrected column types.
    """
    clean_df = df.copy()
    clean_df = clean_df.dropna()
    clean_df = drop_columns(clean_df)
    clean_df = strip_column_suffixes(clean_df)
    clean_df = convert_column_types(clean_df)
    clean_df = clean_df[clean_df["OCC_YEAR"] >= 2014]
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

    ax.set_title('2014-2025: Auto Theft Trends in Toronto', fontsize = 16)
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
    ax.set_title('2021-2023 Surge: Top 10 Most Affected Neighbourhoods', fontsize = 16)
    ax.set_xlabel('Number of Thefts', fontsize = 10)
    ax.set_ylabel('Neighbourhood', fontsize = 10)
    ax.set_xlim(0, max(top10.values) + 500)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()

def premises_proportions_table(df):
    """Return a table showing the proportion of thefts by premise type in West Humber-Clairville year by year from 2021 to 2025.
    
    Parameters:
        df: The cleaned DataFrame.
    
    Returns:
        A DataFrame showing the percentage of thefts per premise type for each year.
    """
    filter_df = df[
        (df['NEIGHBOURHOOD_158'] == 'West Humber-Clairville') &
        (df['OCC_YEAR'].between(2021, 2025))
    ]

    premises_grouped = (filter_df.groupby(['OCC_YEAR', 'PREMISES_TYPE']).size()
                              .unstack(fill_value = 0)
                              .drop(columns = ['Educational']))

    premises_proportions = (premises_grouped.div(premises_grouped.sum(axis = 1), axis = 0 ) * 100).round().astype(str) + '%'
    
    return premises_proportions

def premises_by_years_chart(df):
    """Plot the number of thefts by premise type in West Humber-Clairville from 2021 to 2025.
    
    Parameters:
        df: A clean DataFrame.
    
    Returns:
        None. Created and draws the chart.
    """
    filter_df = df[
        (df['NEIGHBOURHOOD_158'] == 'West Humber-Clairville') &
        (df['OCC_YEAR'].between(2021, 2025))
    ]

    grouped = (filter_df.groupby(['OCC_YEAR', 'PREMISES_TYPE']).size()
                     .unstack(fill_value = 0)
                     .drop(columns = ['Educational']))

    premises = grouped.columns.tolist()
    years = grouped.index.tolist()
    width = 0.16
    colors = ['firebrick', 'steelblue', 'orange', 'darkgreen', 'purple', 'gray']

    fig, ax = plt.subplots(figsize = (14, 7))
    ax.set_facecolor('whitesmoke')
    fig.patch.set_facecolor('whitesmoke')

    for i, (premise, color) in enumerate(zip(premises, colors)):
        offsets = [_ + i * width for _ in range(len(years))]
        bars = ax.bar(offsets, grouped[premise], width = width, label = premise, color = color)
        ax.bar_label(bars, fontweight = 'bold', fontsize = 12)

    ax.set_title('2021-2025: Premise Types Targeted in West Humber-Clairville', fontsize = 16)
    ax.set_xlabel('Year', fontsize = 14)
    ax.set_ylabel('Number of Thefts', fontsize = 14)
    ax.set_xticks([_ + width * 3 for _ in range(len(years))])
    ax.set_xticklabels(years)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)    
    ax.legend(title = 'Premise Type')

    plt.tight_layout()
    plt.show()