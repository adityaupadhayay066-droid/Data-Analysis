"""
Zomato Restaurant Data Analysis & Dashboard Entrypoint
Author: Aditya Upadhayay

This script performs exploratory data analysis (EDA) on the Zomato restaurant dataset
and provides both static visualizations and an interactive Streamlit dashboard.

Usage:
    - To run EDA & generate static charts:
        python Zomato.py
    - To launch the interactive Streamlit dashboard:
        streamlit run app.py  (or: streamlit run Zomato.py)
"""

import sys
import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_static_analysis():
    print("=" * 65)
    print("[*] ZOMATO RESTAURANT DATA ANALYSIS & EDA")
    print("=" * 65)

    csv_path = "Zomato data .csv"
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "Zomato data .csv")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    
    print("\n[+] Dataset Overview:")
    print(f"    - Total Rows: {len(df)}")
    print(f"    - Columns: {list(df.columns)}")
    print("\n[+] Sample Records (Head):")
    print(df.head(3), "\n")

    # Clean rating values
    def clean_rate(value):
        try:
            return float(str(value).split("/")[0].strip())
        except (ValueError, IndexError):
            return np.nan

    df["rate"] = df["rate"].apply(clean_rate)
    df["approx_cost(for two people)"] = pd.to_numeric(df["approx_cost(for two people)"], errors="coerce")

    # Summary Statistics
    print("[+] Core Business Metrics:")
    print(f"    - Mean Customer Rating: {df['rate'].mean():.2f} / 5.0")
    print(f"    - Total Customer Votes: {df['votes'].sum():,}")
    print(f"    - Avg Cost for Two:     Rs. {df['approx_cost(for two people)'].mean():.0f}")
    
    # Impact of Online Order
    online_group = df.groupby(df['online_order'].str.strip())['rate'].mean()
    print("\n[+] Online Delivery Impact on Rating:")
    for status, r in online_group.items():
        print(f"    - Online Order '{status}': Avg Rating = {r:.2f}")

    # Visualization 1: Restaurant Type Distribution
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")
    ax1 = sns.countplot(x="listed_in(type)", data=df, hue="listed_in(type)", palette="cubehelix", legend=False)
    plt.title("Restaurant Category Distribution", fontweight="bold", size=16)
    plt.xlabel("Restaurant Type", fontweight="bold", size=12)
    plt.ylabel("Number of Outlets", fontweight="bold", size=12)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("Restaurant_Types.png", dpi=200)
    plt.savefig("Restraunt_Rating.png", dpi=200)  # Backwards compatibility
    plt.close()
    print("\n[OK] Saved Category Distribution Chart -> 'Restaurant_Types.png'")

    # Visualization 2: Rate vs Votes
    plt.figure(figsize=(10, 5))
    ax2 = sns.scatterplot(
        x="rate", 
        y="votes", 
        hue="listed_in(type)", 
        size="approx_cost(for two people)", 
        sizes=(40, 200), 
        data=df, 
        palette="viridis"
    )
    plt.title("Rate vs Votes (Customer Engagement)", fontweight="bold", size=16)
    plt.xlabel("Customer Rating", fontweight="bold", size=12)
    plt.ylabel("Customer Votes", fontweight="bold", size=12)
    plt.tight_layout()
    plt.savefig("Rate_vs_Votes.png", dpi=200)
    plt.close()
    print("[OK] Saved Rate vs Votes Scatter Plot  -> 'Rate_vs_Votes.png'")

    print("\n" + "=" * 65)
    print(">> Launch the interactive Streamlit dashboard:")
    print("   streamlit run app.py")
    print("=" * 65)

# If executed inside streamlit run Zomato.py, launch dashboard app
if "streamlit" in sys.modules and __name__ != "__main__":
    import app
elif "streamlit" in sys.argv[0]:
    import app
else:
    if __name__ == "__main__":
        run_static_analysis()
