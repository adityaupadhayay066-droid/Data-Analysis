# Zomato Restaurant Data Analysis

## Overview

Zomato Restaurant Data Analysis is a Python-based data analysis project that explores restaurant categories and customer ratings using data visualization techniques.

The project uses Pandas to process the dataset and Matplotlib and Seaborn to visualize restaurant distribution and the relationship between ratings and customer votes.

## Features

* Load and inspect restaurant data using Pandas.
* Clean restaurant ratings by extracting numeric values from rating strings.
* Analyze the distribution of restaurant types.
* Visualize the relationship between restaurant ratings and customer votes.
* Generate charts using Seaborn and Matplotlib.

## Technologies Used

* **Python** — Core programming language
* **Pandas** — Dataset loading and data manipulation
* **NumPy** — Numerical computing library
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical data visualization

## Project Structure

```text
Zomato-Data-Analysis/
│
├── Zomato data .csv
├── zomato_analysis.py
├── Restraunt_Rating.png
└── README.md
```

The Python script generates the chart image files when executed. The same filename is currently used for both charts, so the second chart overwrites the first one.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Zomato-Data-Analysis
```

Replace `<your-repository-url>` with your actual GitHub repository URL.

### 2. Install dependencies

```bash
pip install numpy pandas matplotlib seaborn
```

### 3. Add the dataset

Place `Zomato data .csv` in the same directory as the Python script.

### 4. Run the project

```bash
python zomato_analysis.py
```

## Data Visualizations

### 1. Restaurant Type Distribution

Uses a count plot to show how restaurant records are distributed across different restaurant types.

### 2. Restaurant Ratings vs. Votes

Uses a scatter plot to explore the relationship between restaurant ratings and the number of votes received.

## Data Processing

The project performs the following preprocessing steps:

1. Loads the CSV dataset into a Pandas DataFrame.
2. Removes leading and trailing whitespace from column names.
3. Displays the dataset columns and sample records.
4. Converts restaurant ratings such as `4.1/5` into numeric values such as `4.1`.

## Learning Outcomes

This project demonstrates practical knowledge of:

* CSV file handling
* Pandas DataFrame operations
* Basic data cleaning
* Numeric data conversion
* Exploratory data analysis (EDA)
* Count plots and scatter plots
* Saving visualizations as image files

## Future Improvements

* Add missing-value handling and dataset validation.
* Analyze ratings by online ordering and table booking availability.
* Explore restaurant pricing and rating patterns.
* Generate additional statistical summaries.
* Build an interactive dashboard using Streamlit.

## Author

**Aditya Upadhayay**
=

## License

This project is intended for educational and portfolio purposes. Ensure that the dataset is used in accordance with its original license and terms.
