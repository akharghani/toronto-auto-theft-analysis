"""
Helper functions for Toronto Auto Theft project.

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""

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
    
    return clean_df
