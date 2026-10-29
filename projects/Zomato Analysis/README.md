# 🍽️ Zomato Restaurant Analytics & Executive Intelligence Dashboard

An end-to-end data analysis and interactive business intelligence dashboard for exploring restaurant dynamics, pricing patterns, online delivery lift, and consumer engagement across Bangalore's dining ecosystem. Built with **Python**, **Streamlit**, **Plotly**, **Pandas**, and **Seaborn**.

---

## 🌟 Dashboard Highlights

The project features a **human-centered, natural dashboard design** adhering to modern BI design principles:

* **Executive KPI Cards**: Real-time metrics for active restaurants, average ratings (with 3.5★ benchmark deltas), total customer votes, average ticket size (cost for two), and digital service adoption.
* **Natural Intelligence & Strategic Observations**: An automated executive commentary panel that dynamically updates insights based on active filter selections.
* **5 Interactive Analytical Views**:
  1. **📊 Executive Overview**: Restaurant type donut chart, rating health distribution with KDE curve, and digital convenience adoption matrix.
  2. **🎯 Rating & Votes Dynamics**: Interactive bubble scatter plot with OLS trendline, top 10 most voted powerhouses, and box plots verifying rating lift from online ordering.
  3. **💰 Pricing & Strategic Value Matrix**: 4-Quadrant Strategic Value Matrix (*Best Value Champions*, *Premium Gourmet*, *Budget Casual*, *Overpriced / Review Needed*), spend-by-format breakdown, and Top 5 Value-for-Money spots.
  4. **🔍 Restaurant Finder & Head-to-Head Faceoff**: Direct side-by-side comparison scorecard with normalized multi-dimensional spider/radar chart and interactive restaurant catalog cards.
  5. **📑 Data Explorer & Export**: Sortable data table with summary statistics and one-click filtered CSV export.
* **Sidebar Controls & Reactive Engine**: Quick text search, restaurant format multi-select, online ordering filter, table booking filter, dual-handle sliders for cost and rating, minimum votes threshold, and one-click filter reset.

---

## 💡 Key Business Insights Discovered

* **Digital Ordering Advantage**: Restaurants offering online delivery achieve an average rating of **3.86★** vs. **3.49★** for offline-only venues (+0.37★ boost) and capture **7.4x more customer reviews and votes** (559 vs. 75 votes on average).
* **Table Booking Premium**: Outlets offering table reservations command a **+Rs. 291 higher average ticket size** (Rs. 694 vs. Rs. 403 for two) and score **4.19★** average customer satisfaction vs. **3.60★** for non-booking spots.
* **Market Composition**: **Dining** accounts for 74.3% of listings, followed by **Cafes** (15.5%), **Buffet** (4.7%), and **Delivery/Other** (5.4%).

---

## 📁 Project Structure

```text
Zomato-Data-Analysis/
│
├── Zomato data .csv            # Source dataset (148 restaurant records)
├── app.py                      # Main Streamlit interactive BI dashboard
├── Zomato.py                   # Python EDA script & CLI analysis runner
├── Restaurant_Types.png        # Saved category distribution visualization
├── Rate_vs_Votes.png           # Saved rating vs customer engagement chart
├── Restraunt_Rating.png        # Backward-compatible chart export
└── README.md                   # Complete documentation
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites

Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies

```bash
pip install streamlit plotly pandas numpy seaborn matplotlib statsmodels
```

### 3. Launch the Interactive Dashboard

Run the Streamlit application in your terminal:

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

*(Alternatively, you can also launch it via: `streamlit run Zomato.py`)*

### 4. Run the Static EDA Script

If you only want to generate static charts and view terminal summaries:

```bash
python Zomato.py
```

---

## 🎨 Design System & Palette

* **Primary Brand Accent**: Zomato Crimson (`#E23744`)
* **Satisfaction & Value**: Emerald Green (`#10B981`)
* **Ratings & Benchmarks**: Amber Gold (`#F59E0B`)
* **Service Badges**: Royal Blue (`#3B82F6`) & Royal Purple (`#8B5CF6`)
* **Typography**: Modern geometric sans-serif (*Plus Jakarta Sans* & *Outfit*)

---

## 👤 Author

**Aditya Upadhayay**
