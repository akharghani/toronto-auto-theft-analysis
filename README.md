# Toronto Auto Theft Analysis

An analysis of about 76,700 auto thefts reported to the Toronto Police Service from 2014 to 2025. It looks at how thefts changed over time, which neighbourhoods were hit hardest during the 2021–2023 surge, and where in that neighbourhood vehicles were being stolen from.

This was my final project for a Python data analysis course taken in Winter 2026.

**Tools:** Python, pandas, matplotlib, scikit-learn, Jupyter

## Questions

1. Did auto theft rise gradually from 2014 to 2025, or suddenly between specific years?
2. Which neighbourhood was hit hardest during the 2021–2023 surge, and by how much?
3. In that neighbourhood, did the types of places targeted change between the peak years and afterwards?

## Key findings

- **A sudden surge, not a gradual rise.** Thefts went from about 3,500 a year in the mid-2010s to 6,701 in 2021, then nearly doubled to 12,562 in 2023 before falling to 7,221 in 2025.
- **One neighbourhood stood out.** West Humber-Clairville, next to Pearson Airport, had 2,116 thefts in 2021–2023, more than three times the next neighbourhood (York University Heights, 670).
- **Most of its thefts happened outdoors.** Outdoor locations such as parking lots and streets made up 53% to 68% of West Humber-Clairville's thefts each year from 2021 to 2025, and the share was highest in 2025.
- **A straight-line model couldn't follow the surge.** A linear regression trained on 2014–2022 underestimated 2023 and overestimated 2024 and 2025, missing by 166 thefts a year on average.

The data can't show *why* thefts surged. The notebook treats explanations such as relay attacks on keyless-entry cars as possibilities, not conclusions.

## Project structure

```
├── data/dataset.csv          # raw Toronto Police Service data
├── notebooks/analysis.ipynb  # the analysis, from data overview to conclusions
└── src/helpers.py            # cleaning and chart functions used by the notebook
```

## How to run

```bash
pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/analysis.ipynb` and run all cells.

## Data

[Auto Theft Open Data](https://data.tps.ca/datasets/TorontoPS::auto-theft-open-data/about) from the Toronto Police Service Public Safety Data Portal.

Contains information licensed under the Open Government Licence – Ontario.
