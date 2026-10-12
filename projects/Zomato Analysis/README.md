# Zomato Data Analysis & Visualization

An exploratory data analysis (EDA) script built with Python to clean and visualize restaurant trends from the Zomato dataset.

---

## Overview

This project cleans restaurant rating data and generates key visual insights into:
- The distribution of restaurant service types (`listed_in(type)`).
- The correlation between overall ratings and user vote counts (`rate` vs `votes`).

---

## Features

- **Column Cleaning:** Trims whitespace from dataset headers for consistent column access.
- **Rating Normalization:** Strips denominator formatting (e.g., converting `"4.1/5"` to `4.1` float).
- **Data Visualizations:**
  - Distribution count plot of restaurant types.
  - Scatter plot analyzing user engagement (votes) versus rating scores.

---

## Prerequisites & Installation

Ensure you have Python 3.8+ installed along with the required libraries:

```bash
pip install numpy pandas matplotlib seaborn