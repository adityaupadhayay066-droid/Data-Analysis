"""
Zomato Restaurant Analytics & Executive Intelligence Dashboard
A senior-grade, interactive business intelligence dashboard built with Streamlit & Plotly.
Features official Zomato branding, responsive Dark/Light mode design, 4-quadrant value matrix,
smart filter error recovery, and executive hospitality insights.

Author: Aditya Upadhayay & Senior BI Dashboard Architect
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import base64
import textwrap

# Safe HTML Renderer (Strips leading indentation to prevent Markdown code-block parsing)
def render_html(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME
# ==============================================================================
LOGO_PNG_PATH = "zomato_logo.png"
WORDMARK_SVG_PATH = "zomato_wordmark_white.svg"

# Use official logo as favicon if available
favicon_icon = LOGO_PNG_PATH if os.path.exists(LOGO_PNG_PATH) else "🍽️"

st.set_page_config(
    page_title="Zomato Analytics | Restaurant Intelligence Dashboard",
    page_icon=favicon_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Prepare clean Data URI for official Zomato white logo in hero banner
logo_img_tag = ""
if os.path.exists(WORDMARK_SVG_PATH):
    try:
        with open(WORDMARK_SVG_PATH, "rb") as f:
            svg_b64 = base64.b64encode(f.read()).decode("utf-8")
        logo_img_tag = f'<img src="data:image/svg+xml;base64,{svg_b64}" style="height:36px; width:auto; vertical-align:middle; display:inline-block;" alt="Zomato" />'
    except Exception:
        logo_img_tag = ""
elif os.path.exists(LOGO_PNG_PATH):
    try:
        with open(LOGO_PNG_PATH, "rb") as f:
            png_b64 = base64.b64encode(f.read()).decode("utf-8")
        logo_img_tag = f'<img src="data:image/png;base64,{png_b64}" style="height:42px; border-radius:8px; vertical-align:middle; display:inline-block;" alt="Zomato" />'
    except Exception:
        logo_img_tag = ""

if not logo_img_tag:
    logo_img_tag = "<span style='font-size:2.2rem; font-weight:900; color:#FFFFFF; letter-spacing:-1px;'>zomato</span>"

# Adaptive Design System CSS (Engineered for both Dark Mode & Light Mode)
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    :root {
        --zomato-red: #E23744;
        --zomato-red-dark: #CB202D;
        --zomato-red-light: rgba(226, 55, 68, 0.12);
        --accent-emerald: #10B981;
        --accent-emerald-light: rgba(16, 185, 129, 0.12);
        --accent-amber: #F59E0B;
        --accent-amber-light: rgba(245, 158, 11, 0.12);
        --accent-blue: #3B82F6;
        --accent-blue-light: rgba(59, 130, 246, 0.12);
        --accent-purple: #8B5CF6;
        --accent-purple-light: rgba(139, 92, 246, 0.12);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container padding */
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    /* Brand Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #E23744 0%, #CB202D 45%, #960D18 100%);
        border-radius: 18px;
        padding: 28px 36px;
        color: #FFFFFF;
        box-shadow: 0 10px 28px -5px rgba(226, 55, 68, 0.38);
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        right: -30px;
        bottom: -40px;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-logo-row {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
    }

    .hero-logo-svg {
        max-width: 165px;
        display: inline-block;
    }

    .hero-logo-svg svg {
        width: 100%;
        height: auto;
        display: block;
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: rgba(255, 255, 255, 0.92);
        margin-top: 6px;
        margin-bottom: 14px;
        font-weight: 400;
        max-width: 780px;
        line-height: 1.5;
    }

    .hero-badges {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .hero-badge {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border: 1px solid rgba(255, 255, 255, 0.28);
        color: #FFFFFF;
    }

    /* KPI Metric Cards (Adaptive for Dark & Light Themes) */
    .kpi-card {
        background: var(--secondary-background-color, #1E232F);
        border: 1px solid rgba(226, 55, 68, 0.22);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 24px rgba(226, 55, 68, 0.16);
        border-color: rgba(226, 55, 68, 0.5);
    }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .kpi-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 700;
        opacity: 0.85;
    }

    .kpi-icon-pill {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
    }

    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 4px 0;
    }

    .kpi-subtext {
        font-size: 0.78rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 5px;
        margin-top: 4px;
        opacity: 0.9;
    }

    .pill-red { background: var(--zomato-red-light); color: var(--zomato-red); }
    .pill-emerald { background: var(--accent-emerald-light); color: var(--accent-emerald); }
    .pill-amber { background: var(--accent-amber-light); color: var(--accent-amber); }
    .pill-blue { background: var(--accent-blue-light); color: var(--accent-blue); }
    .pill-purple { background: var(--accent-purple-light); color: var(--accent-purple); }

    /* Natural Insights Callout Box */
    .insights-box {
        background: var(--secondary-background-color, #1E232F);
        border: 1px solid rgba(226, 55, 68, 0.3);
        border-left: 6px solid var(--zomato-red);
        border-radius: 14px;
        padding: 20px 24px;
        margin: 18px 0 24px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }

    .insights-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.12rem;
        font-weight: 800;
        color: var(--zomato-red);
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }

    .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 12px;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    .insight-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        background: rgba(125, 125, 125, 0.08);
        padding: 12px 14px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Section Header */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 10px;
        margin-bottom: 16px;
    }

    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0;
    }

    .section-desc {
        font-size: 0.86rem;
        opacity: 0.8;
        margin: 2px 0 0 0;
    }

    /* Restaurant Card Grid */
    .restaurant-card {
        background: var(--secondary-background-color, #1E232F);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 14px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .restaurant-card:hover {
        border-color: var(--zomato-red);
        box-shadow: 0 6px 18px rgba(226, 55, 68, 0.18);
        transform: translateY(-2px);
    }

    .restaurant-name {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 6px 0;
    }

    .badge-tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.74rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--secondary-background-color, #1E232F);
        padding: 6px;
        border-radius: 14px;
        margin-bottom: 18px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 8px 18px;
        border: none;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--zomato-red) !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 10px rgba(226, 55, 68, 0.35);
    }

    /* Empty state card */
    .empty-state-card {
        background: var(--secondary-background-color, #1E232F);
        border: 2px dashed rgba(226, 55, 68, 0.4);
        border-radius: 18px;
        padding: 36px 30px;
        text-align: center;
        margin: 20px 0;
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 12px;
    }

    .empty-state-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--zomato-red);
        margin-bottom: 8px;
    }

    .empty-state-text {
        font-size: 0.94rem;
        opacity: 0.85;
        max-width: 600px;
        margin: 0 auto 18px auto;
        line-height: 1.5;
    }

    .empty-state-tip {
        background: rgba(226, 55, 68, 0.08);
        border: 1px solid rgba(226, 55, 68, 0.2);
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 0.86rem;
        max-width: 620px;
        margin: 0 auto 20px auto;
        text-align: left;
    }

    /* Dashboard Footer */
    .dashboard-footer {
        text-align: center;
        padding: 24px 0 10px 0;
        font-size: 0.82rem;
        opacity: 0.75;
        border-top: 1px solid rgba(125, 125, 125, 0.18);
        margin-top: 40px;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. DATA PIPELINE & FEATURE ENGINEERING
# ==============================================================================
@st.cache_data
def load_and_preprocess_data():
    csv_candidates = [
        "Zomato data .csv",
        "Zomato data.csv",
        "zomato_data.csv",
        os.path.join(os.path.dirname(__file__), "Zomato data .csv")
    ]
    csv_path = None
    for path in csv_candidates:
        if os.path.exists(path):
            csv_path = path
            break

    if csv_path is None:
        for f in os.listdir("."):
            if f.endswith(".csv") and "zomato" in f.lower():
                csv_path = f
                break

    if csv_path is None:
        st.error("⚠️ Dataset 'Zomato data .csv' not found. Please place it in the project root.")
        st.stop()

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Clean string columns
    for col in ['name', 'online_order', 'book_table', 'listed_in(type)']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df['online_order'] = df['online_order'].str.capitalize()
    df['book_table'] = df['book_table'].str.capitalize()

    # Rename columns to standard identifiers
    df = df.rename(columns={
        'approx_cost(for two people)': 'cost_for_two',
        'listed_in(type)': 'dining_type'
    })

    type_map = {
        'other': 'Delivery / Other',
        'Cafes': 'Cafes',
        'Dining': 'Dining',
        'Buffet': 'Buffet'
    }
    df['dining_type'] = df['dining_type'].replace(type_map)

    # Clean rating numbers
    def parse_rating(val):
        try:
            return float(str(val).split('/')[0].strip())
        except (ValueError, IndexError):
            return np.nan

    df['rate_num'] = df['rate'].apply(parse_rating)
    df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)
    df['cost_for_two'] = pd.to_numeric(df['cost_for_two'], errors='coerce').fillna(df['cost_for_two'].median())

    # Feature 1: Rating Tiers
    def assign_tier(r):
        if r >= 4.2:
            return '🌟 Elite (4.2 - 5.0)'
        elif r >= 3.8:
            return '🟢 Good (3.8 - 4.1)'
        elif r >= 3.3:
            return '🟡 Average (3.3 - 3.7)'
        else:
            return '🔴 Needs Attention (< 3.3)'

    df['rating_tier'] = df['rate_num'].apply(assign_tier)

    # Feature 2: Value for Money Score (Rating per ₹100 spend)
    df['value_score'] = np.round((df['rate_num'] / df['cost_for_two']) * 100, 2)

    # Feature 3: Strategic Value Quadrant
    median_cost = df['cost_for_two'].median()
    median_rate = df['rate_num'].median()

    def assign_quadrant(row):
        high_rate = row['rate_num'] >= median_rate
        high_cost = row['cost_for_two'] > median_cost
        if high_rate and not high_cost:
            return '💎 Best Value Champion'
        elif high_rate and high_cost:
            return '👑 Premium Gourmet'
        elif not high_rate and not high_cost:
            return '🥪 Budget Casual'
        else:
            return '⚠️ Overpriced / Review Needed'

    df['value_quadrant'] = df.apply(assign_quadrant, axis=1)

    return df

raw_df = load_and_preprocess_data()

# Palette mappings
COLOR_PALETTE = ['#E23744', '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6', '#EC4899']
TYPE_COLOR_MAP = {
    'Dining': '#E23744',
    'Cafes': '#F59E0B',
    'Buffet': '#10B981',
    'Delivery / Other': '#3B82F6'
}

# ==============================================================================
# 3. SIDEBAR WITH OFFICIAL LOGO & GUARANTEED FILTER RESET
# ==============================================================================
all_types = sorted(raw_df['dining_type'].unique().tolist())
min_cost = int(raw_df['cost_for_two'].min())
max_cost = int(raw_df['cost_for_two'].max())
min_rate = float(raw_df['rate_num'].min())
max_rate = float(raw_df['rate_num'].max())
max_votes_all = int(raw_df['votes'].max())

# Callback function to reset all filters cleanly
def do_reset_filters():
    st.session_state["filter_search"] = ""
    st.session_state["filter_types"] = all_types
    st.session_state["filter_online"] = "All"
    st.session_state["filter_booking"] = "All"
    st.session_state["filter_cost"] = (min_cost, max_cost)
    st.session_state["filter_rating"] = (min_rate, max_rate)
    st.session_state["filter_votes"] = 0

with st.sidebar:
    # Official Zomato Logo in Sidebar
    if os.path.exists(LOGO_PNG_PATH):
        st.image(LOGO_PNG_PATH, width=150)
    else:
        st.markdown("<h2 style='color:#E23744; margin:0;'>zomato</h2>", unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top:4px; margin-bottom:14px;">
            <div style="font-family:'Outfit',sans-serif; font-size:1.1rem; font-weight:800; letter-spacing:-0.3px;">Restaurant Intelligence</div>
            <div style="font-size:0.75rem; opacity:0.75; font-weight:600;">Interactive BI & Analytics Hub</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Filter 1: Restaurant Name Search
    search_query = st.text_input(
        "🔍 Search Restaurant Name",
        value=st.session_state.get("filter_search", ""),
        key="filter_search",
        placeholder="e.g. Onesta, Empire..."
    )

    # Filter 2: Dining Format Multiselect
    selected_types = st.multiselect(
        "🍴 Restaurant Category",
        options=all_types,
        default=st.session_state.get("filter_types", all_types),
        key="filter_types"
    )

    # Filter 3 & 4: Online Order & Table Booking Selectors
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        online_order_filter = st.selectbox(
            "🛵 Online Order",
            options=["All", "Yes", "No"],
            index=["All", "Yes", "No"].index(st.session_state.get("filter_online", "All")),
            key="filter_online"
        )
    with col_s2:
        table_booking_filter = st.selectbox(
            "🪑 Book Table",
            options=["All", "Yes", "No"],
            index=["All", "Yes", "No"].index(st.session_state.get("filter_booking", "All")),
            key="filter_booking",
            help="Note: Table reservation outlets are premium spots with cost >= ₹500."
        )

    # Filter 5: Cost Range Slider
    st.markdown("##### 💵 Cost for Two (₹)")
    selected_cost_range = st.slider(
        "Cost Range",
        min_value=min_cost,
        max_value=max_cost,
        value=st.session_state.get("filter_cost", (min_cost, max_cost)),
        step=50,
        key="filter_cost",
        label_visibility="collapsed"
    )

    # Filter 6: Rating Range Slider
    st.markdown("##### ⭐ Rating Range")
    selected_rate_range = st.slider(
        "Rating Range",
        min_value=min_rate,
        max_value=max_rate,
        value=st.session_state.get("filter_rating", (min_rate, max_rate)),
        step=0.1,
        key="filter_rating",
        label_visibility="collapsed"
    )

    # Filter 7: Minimum Votes Threshold
    st.markdown("##### 🗳️ Min Customer Votes")
    selected_min_votes = st.slider(
        "Minimum Votes",
        min_value=0,
        max_value=max_votes_all,
        value=st.session_state.get("filter_votes", 0),
        step=50,
        key="filter_votes",
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    st.button("🔄 Reset All Filters", on_click=do_reset_filters, use_container_width=True, type="secondary")

    st.markdown("---")

    # Dataset status chip in sidebar
    st.markdown(f"""
        <div style="background:rgba(125,125,125,0.08); border-radius:12px; padding:12px 14px; border:1px solid rgba(255,255,255,0.08); font-size:0.78rem;">
            <div style="font-weight:700; margin-bottom:4px;">📊 Catalog Status</div>
            <div style="opacity:0.8;">Total Records: <b>{len(raw_df)} restaurants</b></div>
            <div style="opacity:0.8; margin-top:2px;">Target Market: <b>Bangalore Hub</b></div>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 4. FILTERING PIPELINE & EMPTY STATE HANDLER
# ==============================================================================
filtered_df = raw_df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]

if selected_types:
    filtered_df = filtered_df[filtered_df['dining_type'].isin(selected_types)]
else:
    filtered_df = filtered_df.iloc[0:0]

if online_order_filter != "All":
    filtered_df = filtered_df[filtered_df['online_order'] == online_order_filter]

if table_booking_filter != "All":
    filtered_df = filtered_df[filtered_df['book_table'] == table_booking_filter]

filtered_df = filtered_df[
    (filtered_df['cost_for_two'] >= selected_cost_range[0]) &
    (filtered_df['cost_for_two'] <= selected_cost_range[1]) &
    (filtered_df['rate_num'] >= selected_rate_range[0]) &
    (filtered_df['rate_num'] <= selected_rate_range[1]) &
    (filtered_df['votes'] >= selected_min_votes)
]

total_all = len(raw_df)
total_active = len(filtered_df)
pct_active = (total_active / total_all * 100) if total_all > 0 else 0

# Safe rating string to prevent 'nan' in banner
if total_active > 0 and not pd.isna(filtered_df['rate_num'].mean()):
    avg_rate_val = filtered_df['rate_num'].mean()
    avg_rate_banner = f"{avg_rate_val:.2f}/5.0"
else:
    avg_rate_val = 0.0
    avg_rate_banner = "N/A"

# ==============================================================================
# 5. BRAND HERO BANNER WITH OFFICIAL ZOMATO LOGO
# ==============================================================================
banner_html = f"""
<div class="hero-banner">
    <div class="hero-logo-row">
        {logo_img_tag}
        <div style="height:28px; width:2px; background:rgba(255,255,255,0.4); margin:0 4px;"></div>
        <h1 class="hero-title">Dining & Restaurant Intelligence</h1>
    </div>
    <p class="hero-subtitle">
        Executive restaurant decision dashboard uncovering consumer dining preferences, pricing equilibrium, 
        online ordering lift, and restaurant performance metrics across Bangalore's culinary ecosystem.
    </p>
    <div class="hero-badges">
        <span class="hero-badge">📊 {total_active} of {total_all} Outlets ({pct_active:.1f}%) Active</span>
        <span class="hero-badge">⭐ Avg Rating: {avg_rate_banner}</span>
        <span class="hero-badge">🛵 {len(filtered_df[filtered_df['online_order']=='Yes'])} Online Enabled</span>
        <span class="hero-badge">🪑 {len(filtered_df[filtered_df['book_table']=='Yes'])} Table Reservation Outlets</span>
    </div>
</div>
"""
render_html(banner_html)


# ==============================================================================
# 6. GRACEFUL EMPTY STATE RECOVERY (If 0 records match)
# ==============================================================================
if filtered_df.empty:
    st.markdown("""
        <div class="empty-state-card">
            <div class="empty-state-icon">🔍</div>
            <div class="empty-state-title">No Restaurants Match This Filter Combination</div>
            <div class="empty-state-text">
                Your current sidebar filter criteria returned 0 matching restaurants. This usually happens when combining 
                filters with mutually exclusive ranges (such as high-end reservation venues with budget price sliders).
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Diagnostic insight for the user
    tip_msg = "💡 <b>Hospitality Data Diagnostic:</b><br>"
    if table_booking_filter == "Yes" and selected_cost_range[1] < 500:
        tip_msg += f"• You have <b>Book Table = 'Yes'</b> with max spend capped at <b>₹{selected_cost_range[1]}</b>. In this dataset, all 8 table-reservation outlets are premium venues costing between <b>₹500 and ₹800</b>.<br>"
    if len(selected_types) == 0:
        tip_msg += "• No restaurant categories are currently selected.<br>"
    if selected_rate_range[0] > 4.6:
        tip_msg += "• High minimum rating slider: the highest rated restaurant in this catalog is 4.6★.<br>"

    st.markdown(f"<div class='empty-state-tip'>{tip_msg} Click the button below to restore the full dataset.</div>", unsafe_allow_html=True)

    # 1-Click Recovery Actions
    rec_c1, rec_c2, rec_c3 = st.columns([1, 1, 1])
    with rec_c1:
        st.button("🔄 Reset All Filters (View 148 Restaurants)", on_click=do_reset_filters, type="primary", use_container_width=True)
    with rec_c2:
        def expand_price():
            st.session_state["filter_cost"] = (min_cost, 950)
            st.session_state["filter_booking"] = "All"
        st.button("🔓 Auto-Expand Cost & Booking", on_click=expand_price, use_container_width=True)
    with rec_c3:
        def select_all_cats():
            st.session_state["filter_types"] = all_types
        st.button("🍴 Select All Categories", on_click=select_all_cats, use_container_width=True)

    st.stop()


# ==============================================================================
# 7. NATURAL INTELLIGENCE & EXECUTIVE TAKEAWAYS
# ==============================================================================
avg_rate = filtered_df['rate_num'].mean()
avg_cost = filtered_df['cost_for_two'].mean()
median_cost_filt = filtered_df['cost_for_two'].median()
total_votes = filtered_df['votes'].sum()

# Online delivery lift
df_online_yes = filtered_df[filtered_df['online_order'] == 'Yes']
df_online_no = filtered_df[filtered_df['online_order'] == 'No']
online_rate_diff = (df_online_yes['rate_num'].mean() - df_online_no['rate_num'].mean()) if len(df_online_yes) > 0 and len(df_online_no) > 0 else 0
online_vote_mult = (df_online_yes['votes'].mean() / df_online_no['votes'].mean()) if len(df_online_no) > 0 and df_online_no['votes'].mean() > 0 else 1

# Table booking lift
df_table_yes = filtered_df[filtered_df['book_table'] == 'Yes']
df_table_no = filtered_df[filtered_df['book_table'] == 'No']
table_rate_diff = (df_table_yes['rate_num'].mean() - df_table_no['rate_num'].mean()) if len(df_table_yes) > 0 and len(df_table_no) > 0 else 0
table_cost_diff = (df_table_yes['cost_for_two'].mean() - df_table_no['cost_for_two'].mean()) if len(df_table_yes) > 0 and len(df_table_no) > 0 else 0

top_cat = filtered_df['dining_type'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
top_cat_share = (filtered_df['dining_type'].value_counts().iloc[0] / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

star_performer = filtered_df.sort_values(by='votes', ascending=False).iloc[0]

render_html(f"""
<div class="insights-box">
    <div class="insights-title">
        <span>💡</span> Executive Natural Intelligence & Strategic Observations
    </div>
    <div class="insights-grid">
        <div class="insight-item">
            <span style="font-size:1.3rem;">🛵</span>
            <div>
                <b>Digital Ordering Premium:</b> Venues with Online Delivery achieve 
                <span style="color:#E23744; font-weight:700;">{'+' if online_rate_diff >= 0 else ''}{online_rate_diff:.2f}★ higher ratings</span> 
                and capture <b>{online_vote_mult:.1f}x more customer votes</b> on average than offline-only venues.
            </div>
        </div>
        <div class="insight-item">
            <span style="font-size:1.3rem;">🪑</span>
            <div>
                <b>Table Reservation Lift:</b> Booking-enabled spots command 
                <span style="color:#10B981; font-weight:700;">{'+₹' if table_cost_diff >= 0 else '-₹'}{abs(table_cost_diff):.0f} higher ticket size</span> 
                and score an impressive <b>{'+' if table_rate_diff >= 0 else ''}{table_rate_diff:.2f}★ rating boost</b>.
            </div>
        </div>
        <div class="insight-item">
            <span style="font-size:1.3rem;">🏆</span>
            <div>
                <b>Category & Market Dominance:</b> <b>{top_cat}</b> is the leading dining format ({top_cat_share:.0f}% of selection). 
                Market anchor <b>'{star_performer['name']}'</b> leads engagement with <b>{star_performer['votes']:,} votes</b> ({star_performer['rate_num']}★).
            </div>
        </div>
    </div>
</div>
""")


# ==============================================================================
# 8. HIGH-IMPACT KPI CARDS
# ==============================================================================
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Active Outlets</span>
            <div class="kpi-icon-pill pill-red">🏪</div>
        </div>
        <div class="kpi-value">{total_active:,}</div>
        <div class="kpi-subtext">
            <span>{pct_active:.1f}% of catalog</span>
        </div>
    </div>
    """)

with kpi2:
    bench_diff = avg_rate - 3.5
    bench_color = "#10B981" if bench_diff >= 0 else "#EF4444"
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Average Rating</span>
            <div class="kpi-icon-pill pill-amber">⭐</div>
        </div>
        <div class="kpi-value">{avg_rate:.2f}<span style="font-size:1.1rem; opacity:0.6;">/5.0</span></div>
        <div class="kpi-subtext" style="color:{bench_color};">
            <span>{'▲' if bench_diff>=0 else '▼'} {abs(bench_diff):.2f} vs 3.5 benchmark</span>
        </div>
    </div>
    """)

with kpi3:
    avg_votes_per_place = total_votes / total_active if total_active > 0 else 0
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Customer Votes</span>
            <div class="kpi-icon-pill pill-blue">🗳️</div>
        </div>
        <div class="kpi-value">{total_votes:,.0f}</div>
        <div class="kpi-subtext">
            <span>~{avg_votes_per_place:.0f} avg / restaurant</span>
        </div>
    </div>
    """)

with kpi4:
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Avg Cost (2 Pax)</span>
            <div class="kpi-icon-pill pill-emerald">💵</div>
        </div>
        <div class="kpi-value">₹{avg_cost:,.0f}</div>
        <div class="kpi-subtext">
            <span>Median: ₹{median_cost_filt:,.0f}</span>
        </div>
    </div>
    """)

with kpi5:
    online_count = len(filtered_df[filtered_df['online_order'] == 'Yes'])
    online_pct = (online_count / total_active * 100) if total_active > 0 else 0
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Online Delivery</span>
            <div class="kpi-icon-pill pill-red">🛵</div>
        </div>
        <div class="kpi-value">{online_pct:.0f}%</div>
        <div class="kpi-subtext" style="color:#E23744;">
            <span>{online_count} enabled outlets</span>
        </div>
    </div>
    """)

with kpi6:
    table_count = len(filtered_df[filtered_df['book_table'] == 'Yes'])
    table_pct = (table_count / total_active * 100) if total_active > 0 else 0
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Table Booking</span>
            <div class="kpi-icon-pill pill-purple">🪑</div>
        </div>
        <div class="kpi-value">{table_pct:.1f}%</div>
        <div class="kpi-subtext" style="color:#8B5CF6;">
            <span>{table_count} premium outlets</span>
        </div>
    </div>
    """)

render_html("<div style='margin-bottom:26px;'></div>")

# Helper function to style Plotly figures cleanly for both themes
def apply_clean_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans, sans-serif')
    )
    return fig

# ==============================================================================
# 9. ANALYTICAL TABS
# ==============================================================================
tab_overview, tab_ratings, tab_pricing, tab_finder, tab_data = st.tabs([
    "📊 Executive Overview",
    "🎯 Rating & Votes Dynamics",
    "💰 Pricing & Value Matrix",
    "🔍 Restaurant Finder & Compare",
    "📑 Data Explorer & Export"
])

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ------------------------------------------------------------------------------
with tab_overview:
    col_t1_left, col_t1_right = st.columns([1, 1], gap="large")

    with col_t1_left:
        st.markdown("""
            <div class="section-header">
                <div>
                    <h3 class="section-title">🍴 Restaurant Category Breakdown</h3>
                    <p class="section-desc">Distribution of outlets across dining formats and service types.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        cat_counts = filtered_df['dining_type'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Outlets']

        fig_cat = px.pie(
            cat_counts,
            names='Category',
            values='Outlets',
            hole=0.62,
            color='Category',
            color_discrete_map=TYPE_COLOR_MAP
        )
        fig_cat.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#FFFFFF', width=2)),
            hovertemplate='<b>%{label}</b><br>Outlets: %{value}<br>Share: %{percent}<extra></extra>'
        )
        fig_cat.update_layout(
            margin=dict(t=15, b=45, l=15, r=15),
            height=370,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.08,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            annotations=[dict(
                text=f"<b>{total_active}</b><br><span style='font-size:12px; opacity:0.8;'>Venues</span>",
                x=0.5, y=0.5, font_size=19, showarrow=False
            )]
        )
        apply_clean_layout(fig_cat)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_t1_right:
        st.markdown("""
            <div class="section-header">
                <div>
                    <h3 class="section-title">⭐ Rating Health & Sentiment Distribution</h3>
                    <p class="section-desc">Frequency distribution of customer ratings with satisfaction benchmark.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        fig_hist = px.histogram(
            filtered_df,
            x='rate_num',
            nbins=15,
            color='dining_type',
            color_discrete_map=TYPE_COLOR_MAP,
            marginal="box",
            labels={'rate_num': 'Customer Rating (★)', 'dining_type': 'Format'}
        )
        fig_hist.add_vline(
            x=avg_rate,
            line_dash="dash",
            line_color="#E23744",
            annotation_text=f"Mean: {avg_rate:.2f}★",
            annotation_position="top right"
        )
        fig_hist.update_layout(
            margin=dict(t=25, b=55, l=25, r=20),
            height=370,
            barmode='stack',
            showlegend=False,  # Donut chart on the left already displays category legend!
            xaxis=dict(
                title=dict(text="Customer Rating (★)", standoff=15),
                range=[2.0, 5.0],
                dtick=0.5
            ),
            yaxis=dict(title=dict(text="Number of Restaurants", standoff=10))
        )
        apply_clean_layout(fig_hist)
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid rgba(125,125,125,0.2);'/>", unsafe_allow_html=True)

    # Convenience Adoption Across Formats
    st.markdown("""
        <div class="section-header">
            <div>
                <h3 class="section-title">🛵 Online Delivery & 🪑 Table Booking Adoption</h3>
                <p class="section-desc">Comparing adoption rates of digital delivery and reservations across dining formats.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    service_agg = filtered_df.groupby('dining_type').agg(
        Total=('name', 'count'),
        Online_Yes=('online_order', lambda x: (x == 'Yes').sum()),
        Booking_Yes=('book_table', lambda x: (x == 'Yes').sum())
    ).reset_index()

    service_agg['Online Delivery %'] = (service_agg['Online_Yes'] / service_agg['Total']) * 100
    service_agg['Table Reservation %'] = (service_agg['Booking_Yes'] / service_agg['Total']) * 100

    fig_serv = go.Figure()
    fig_serv.add_trace(go.Bar(
        name='Online Delivery Enabled',
        x=service_agg['dining_type'],
        y=service_agg['Online Delivery %'],
        marker_color='#E23744',
        text=service_agg['Online Delivery %'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside'
    ))
    fig_serv.add_trace(go.Bar(
        name='Table Booking Available',
        x=service_agg['dining_type'],
        y=service_agg['Table Reservation %'],
        marker_color='#8B5CF6',
        text=service_agg['Table Reservation %'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside'
    ))
    fig_serv.update_layout(
        barmode='group',
        height=380,
        margin=dict(t=45, b=55, l=35, r=20),
        yaxis=dict(
            title=dict(text="Adoption Percentage (%)", standoff=10),
            range=[0, 115],
            gridcolor="rgba(125,125,125,0.15)"
        ),
        xaxis=dict(
            title=dict(text="Dining Format", standoff=15),
            tickfont=dict(size=12)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1.0,
            font=dict(size=12)
        )
    )
    apply_clean_layout(fig_serv)
    st.plotly_chart(fig_serv, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 2: RATING & VOTES DYNAMICS
# ------------------------------------------------------------------------------
with tab_ratings:
    st.markdown("""
        <div class="section-header">
            <div>
                <h3 class="section-title">🎯 Rating vs Customer Engagement (Votes Momentum)</h3>
                <p class="section-desc">Interactive correlation map showing how customer feedback volume scales with restaurant quality.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    ctrl_col1, ctrl_col2, _ = st.columns([1, 1, 2])
    with ctrl_col1:
        use_log_scale = st.checkbox("📐 Logarithmic Scale for Votes", value=True)
    with ctrl_col2:
        show_trendline = st.checkbox("📈 Show Regression Trendline", value=True)

    fig_scatter = px.scatter(
        filtered_df,
        x='rate_num',
        y='votes',
        color='dining_type',
        size='cost_for_two',
        hover_name='name',
        color_discrete_map=TYPE_COLOR_MAP,
        log_y=use_log_scale,
        size_max=22,
        labels={
            'rate_num': 'Rating (★)',
            'votes': 'Customer Votes',
            'cost_for_two': 'Cost for 2 (₹)',
            'dining_type': 'Category'
        },
        custom_data=['online_order', 'book_table', 'cost_for_two']
    )

    # Robust OLS Regression Trendline using pure NumPy (Independent of statsmodels)
    if show_trendline and len(filtered_df) >= 3:
        try:
            clean_pts = filtered_df.dropna(subset=['rate_num', 'votes'])
            clean_pts = clean_pts[clean_pts['votes'] > 0]
            if len(clean_pts) >= 3 and clean_pts['rate_num'].nunique() > 1:
                x_pts = clean_pts['rate_num'].values
                y_pts = np.log10(np.maximum(clean_pts['votes'].values, 1)) if use_log_scale else clean_pts['votes'].values.astype(float)
                
                # Fit linear regression: y = slope * x + intercept
                slope, intercept = np.polyfit(x_pts, y_pts, 1)
                x_line = np.linspace(x_pts.min(), x_pts.max(), 50)
                y_line_fit = slope * x_line + intercept
                y_line = (10 ** y_line_fit) if use_log_scale else y_line_fit

                fig_scatter.add_trace(go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode='lines',
                    name='OLS Trendline',
                    line=dict(color='#E23744', width=2.5, dash='dash'),
                    hoverinfo='skip'
                ))
        except Exception:
            pass

    fig_scatter.update_traces(
        marker=dict(opacity=0.82, line=dict(width=1, color='#FFFFFF')),
        hovertemplate="""
        <b>%{hovertext}</b><br>
        ⭐ Rating: <b>%{x:.1f}/5.0</b><br>
        🗳️ Votes: <b>%{y:,}</b><br>
        💵 Approx Cost (2): <b>₹%{customdata[2]}</b><br>
        🛵 Online Order: %{customdata[0]}<br>
        🪑 Table Booking: %{customdata[1]}
        <extra></extra>
        """
    )
    fig_scatter.update_layout(
        height=480,
        margin=dict(t=45, b=55, l=45, r=20),
        xaxis=dict(title=dict(text="Customer Rating (★)", standoff=15), dtick=0.2),
        yaxis=dict(title=dict(text="Customer Votes (Engagement Count)", standoff=10)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=12)
        )
    )
    apply_clean_layout(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid rgba(125,125,125,0.2);'/>", unsafe_allow_html=True)

    col_r_left, col_r_right = st.columns([1, 1], gap="large")

    with col_r_left:
        st.markdown("""
            <div class="section-header">
                <div>
                    <h3 class="section-title">🏆 Top 10 Most Voted Powerhouses</h3>
                    <p class="section-desc">Bangalore's most socially proven culinary destinations.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        top10_voted = filtered_df.sort_values(by='votes', ascending=True).tail(10)
        fig_top10 = px.bar(
            top10_voted,
            x='votes',
            y='name',
            orientation='h',
            color='rate_num',
            color_continuous_scale='Reds',
            labels={'votes': 'Total Votes', 'name': 'Restaurant', 'rate_num': 'Rating ★'},
            text='votes'
        )
        fig_top10.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Votes: %{x:,}<br>Rating: %{marker.color}★<extra></extra>'
        )
        fig_top10.update_layout(
            height=380,
            margin=dict(t=10, b=10, l=10, r=40),
            xaxis=dict(title="Customer Votes"),
            yaxis=dict(title="", tickfont=dict(size=11)),
            coloraxis_colorbar=dict(title="Rating ★", len=0.7)
        )
        apply_clean_layout(fig_top10)
        st.plotly_chart(fig_top10, use_container_width=True)

    with col_r_right:
        st.markdown("""
            <div class="section-header">
                <div>
                    <h3 class="section-title">🛵 Online Delivery Impact on Rating</h3>
                    <p class="section-desc">Comparative box plot validating quality perception with delivery enablement.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        fig_box = px.box(
            filtered_df,
            x='online_order',
            y='rate_num',
            color='online_order',
            color_discrete_map={'Yes': '#E23744', 'No': '#6B7280'},
            points="all",
            labels={'online_order': 'Offers Online Delivery', 'rate_num': 'Customer Rating (★)'}
        )
        fig_box.update_traces(jitter=0.3, marker=dict(size=6, opacity=0.7))
        fig_box.update_layout(
            height=380,
            margin=dict(t=10, b=10, l=10, r=10),
            yaxis=dict(title="Rating Score (★)", range=[2.0, 5.0]),
            xaxis=dict(title="Online Delivery Available"),
            showlegend=False
        )
        apply_clean_layout(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 3: PRICING & VALUE MATRIX
# ------------------------------------------------------------------------------
with tab_pricing:
    st.markdown("""
        <div class="section-header">
            <div>
                <h3 class="section-title">💎 Strategic Value-for-Money 4-Quadrant Matrix</h3>
                <p class="section-desc">Classifying outlets by customer satisfaction vs pricing threshold to isolate bargains & luxury leaders.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    med_cost_all = raw_df['cost_for_two'].median()
    med_rate_all = raw_df['rate_num'].median()

    fig_quad = px.scatter(
        filtered_df,
        x='cost_for_two',
        y='rate_num',
        color='value_quadrant',
        size='votes',
        hover_name='name',
        size_max=24,
        color_discrete_map={
            '💎 Best Value Champion': '#10B981',
            '👑 Premium Gourmet': '#3B82F6',
            '🥪 Budget Casual': '#F59E0B',
            '⚠️ Overpriced / Review Needed': '#EF4444'
        },
        labels={
            'cost_for_two': 'Approx Cost for Two (₹)',
            'rate_num': 'Customer Rating (★)',
            'value_quadrant': 'Strategic Quadrant',
            'votes': 'Votes'
        }
    )

    fig_quad.add_hline(y=med_rate_all, line_dash="dot", line_color="#9CA3AF", annotation_text=f"Median Rate ({med_rate_all}★)", annotation_position="bottom right")
    fig_quad.add_vline(x=med_cost_all, line_dash="dot", line_color="#9CA3AF", annotation_text=f"Median Cost (₹{med_cost_all:.0f})", annotation_position="top left")

    fig_quad.update_traces(
        marker=dict(opacity=0.82, line=dict(width=1, color='#FFFFFF')),
        hovertemplate="<b>%{hovertext}</b><br>Rating: <b>%{y}★</b><br>Cost: <b>₹%{x}</b><br>Votes: %{marker.size:,}<extra></extra>"
    )

    fig_quad.update_layout(
        height=480,
        margin=dict(t=45, b=55, l=45, r=20),
        xaxis=dict(title=dict(text="Approx Cost for Two People (₹)", standoff=15), dtick=100),
        yaxis=dict(title=dict(text="Customer Rating (out of 5.0)", standoff=10), range=[2.4, 5.0]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=12)
        )
    )
    apply_clean_layout(fig_quad)
    st.plotly_chart(fig_quad, use_container_width=True)

    st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid rgba(125,125,125,0.2);'/>", unsafe_allow_html=True)

    col_p_left, col_p_right = st.columns([1, 1], gap="large")

    with col_p_left:
        st.markdown("""
            <div class="section-header">
                <div>
                    <h3 class="section-title">📊 Average Dining Spend by Format</h3>
                    <p class="section-desc">Comparison of typical cost for two across restaurant types.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        cost_by_type = filtered_df.groupby('dining_type')['cost_for_two'].agg(['mean', 'median', 'std', 'count']).reset_index()
        fig_cost_bar = px.bar(
            cost_by_type,
            x='dining_type',
            y='mean',
            color='dining_type',
            color_discrete_map=TYPE_COLOR_MAP,
            text='mean',
            labels={'mean': 'Average Cost (₹)', 'dining_type': 'Format'}
        )
        fig_cost_bar.update_traces(
            texttemplate='₹%{text:.0f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Spend: ₹%{y:.0f}<extra></extra>'
        )
        fig_cost_bar.update_layout(
            height=340,
            margin=dict(t=10, b=10, l=10, r=10),
            yaxis=dict(title="Average Cost for Two (₹)", range=[0, cost_by_type['mean'].max() * 1.25]),
            xaxis=dict(title=""),
            showlegend=False
        )
        apply_clean_layout(fig_cost_bar)
        st.plotly_chart(fig_cost_bar, use_container_width=True)

    with col_p_right:
        st.markdown("""
            <div class="section-header">
                <div>
                    <h3 class="section-title">🌟 Top 5 Value-for-Money Champions</h3>
                    <p class="section-desc">Highest star rating delivered per rupee spent.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        top_val = filtered_df.sort_values(by=['value_score', 'rate_num'], ascending=False).head(5)
        for _, row in top_val.iterrows():
            st.markdown(f"""
                <div style="background:var(--secondary-background-color, #1E232F); border:1px solid rgba(255,255,255,0.08); border-left:4px solid #10B981; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; font-size:0.95rem;">{row['name']}</div>
                        <div style="font-size:0.78rem; opacity:0.75;">{row['dining_type']} • {row['votes']:,} votes</div>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:rgba(16,185,129,0.15); color:#10B981; padding:3px 8px; border-radius:6px; font-weight:700; font-size:0.85rem;">{row['rate_num']}★</span>
                        <div style="font-size:0.8rem; font-weight:700; margin-top:2px;">₹{row['cost_for_two']:.0f} (2 pax)</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: RESTAURANT FINDER & HEAD-TO-HEAD COMPARE
# ------------------------------------------------------------------------------
with tab_finder:
    st.markdown("""
        <div class="section-header">
            <div>
                <h3 class="section-title">⚖️ Head-to-Head Restaurant Faceoff</h3>
                <p class="section-desc">Select 2 to 4 restaurants for a direct comparative scorecard & radar analysis.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    available_names = sorted(filtered_df['name'].unique().tolist())
    default_select = available_names[:2] if len(available_names) >= 2 else available_names

    selected_compare = st.multiselect(
        "Select Restaurants to Compare",
        options=available_names,
        default=default_select,
        max_selections=4
    )

    if len(selected_compare) >= 2:
        compare_df = filtered_df[filtered_df['name'].isin(selected_compare)].drop_duplicates(subset=['name'])
        
        comp_cols = st.columns(len(compare_df))
        for idx, (_, row) in enumerate(compare_df.iterrows()):
            with comp_cols[idx]:
                st.markdown(f"""
                    <div class="restaurant-card" style="border-top: 4px solid #E23744;">
                        <div class="restaurant-name">{row['name']}</div>
                        <div style="margin-bottom:8px;">
                            <span class="badge-tag" style="background:rgba(226,55,68,0.15); color:#E23744;">⭐ {row['rate_num']}/5.0</span>
                            <span class="badge-tag" style="background:rgba(125,125,125,0.12);">₹{row['cost_for_two']:.0f} for 2</span>
                        </div>
                        <div style="font-size:0.82rem; line-height:1.6; opacity:0.9;">
                            <b>Category:</b> {row['dining_type']}<br>
                            <b>Total Votes:</b> {row['votes']:,}<br>
                            <b>Online Order:</b> {'✅ Enabled' if row['online_order']=='Yes' else '❌ No'}<br>
                            <b>Book Table:</b> {'✅ Available' if row['book_table']=='Yes' else '❌ No'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        categories = ['Rating (out of 5)', 'Engagement Index', 'Affordability Index', 'Service Score']
        fig_radar = go.Figure()
        max_v = max(raw_df['votes'].max(), 1)
        
        for idx, (_, row) in enumerate(compare_df.iterrows()):
            norm_rating = (row['rate_num'] / 5.0) * 100
            norm_votes = min((np.log1p(row['votes']) / np.log1p(max_v)) * 100, 100)
            norm_afford = max(100 - (row['cost_for_two'] / 1000 * 100), 10)
            service_pts = (50 if row['online_order'] == 'Yes' else 10) + (50 if row['book_table'] == 'Yes' else 10)
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[norm_rating, norm_votes, norm_afford, service_pts],
                theta=categories,
                fill='toself',
                name=row['name'],
                marker=dict(color=COLOR_PALETTE[idx % len(COLOR_PALETTE)])
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9))
            ),
            showlegend=True,
            height=380,
            margin=dict(t=20, b=20, l=40, r=40)
        )
        apply_clean_layout(fig_radar)
        st.plotly_chart(fig_radar, use_container_width=True)

    else:
        st.info("💡 Please select at least 2 restaurants from the selector above to trigger the comparison matrix.")

    st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid rgba(125,125,125,0.2);'/>", unsafe_allow_html=True)

    st.markdown("""
        <div class="section-header">
            <div>
                <h3 class="section-title">🍽️ Active Restaurant Showcase</h3>
                <p class="section-desc">Explore filtered restaurant profiles with operational badges.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    sort_choice = st.selectbox(
        "Sort Catalog By",
        options=["Highest Rated (★)", "Most Customer Votes", "Most Affordable (₹)", "Most Premium (₹)", "Name (A-Z)"],
        index=0
    )

    sorted_df = filtered_df.copy()
    if sort_choice == "Highest Rated (★)":
        sorted_df = sorted_df.sort_values(by=['rate_num', 'votes'], ascending=[False, False])
    elif sort_choice == "Most Customer Votes":
        sorted_df = sorted_df.sort_values(by='votes', ascending=False)
    elif sort_choice == "Most Affordable (₹)":
        sorted_df = sorted_df.sort_values(by='cost_for_two', ascending=True)
    elif sort_choice == "Most Premium (₹)":
        sorted_df = sorted_df.sort_values(by='cost_for_two', ascending=False)
    else:
        sorted_df = sorted_df.sort_values(by='name', ascending=True)

    cols_grid = st.columns(3)
    for i, (_, row) in enumerate(sorted_df.head(18).iterrows()):
        col_target = cols_grid[i % 3]
        rate_val = row['rate_num']
        star_pill_class = "pill-emerald" if rate_val >= 4.0 else ("pill-amber" if rate_val >= 3.5 else "pill-red")

        with col_target:
            st.markdown(f"""
                <div class="restaurant-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <h4 class="restaurant-name">{row['name']}</h4>
                        <span class="kpi-icon-pill {star_pill_class}" style="width:auto; padding:2px 8px; height:24px; font-size:0.8rem; font-weight:700;">
                            ★ {row['rate_num']}
                        </span>
                    </div>
                    <div style="margin: 6px 0;">
                        <span class="badge-tag" style="background:rgba(125,125,125,0.12);">{row['dining_type']}</span>
                        <span class="badge-tag" style="background:rgba(16,185,129,0.15); color:#10B981;">₹{row['cost_for_two']:.0f} for 2</span>
                        <span class="badge-tag" style="background:rgba(59,130,246,0.15); color:#3B82F6;">🗳️ {row['votes']:,}</span>
                    </div>
                    <div style="font-size:0.75rem; opacity:0.75; margin-top:6px; display:flex; gap:8px;">
                        <span>{'🛵 Online' if row['online_order']=='Yes' else '🚫 No Delivery'}</span>
                        <span>•</span>
                        <span>{'🪑 Reservations' if row['book_table']=='Yes' else '🚫 No Booking'}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    if len(sorted_df) > 18:
        st.caption(f"Showing top 18 of {len(sorted_df)} filtered restaurants. Refine filters on the sidebar to narrow down your search.")


# ------------------------------------------------------------------------------
# TAB 5: DATA EXPLORER & EXPORT
# ------------------------------------------------------------------------------
with tab_data:
    st.markdown("""
        <div class="section-header">
            <div>
                <h3 class="section-title">📑 Comprehensive Dataset & Export</h3>
                <p class="section-desc">Search, inspect, and export clean structured data for presentations or ML pipelines.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📊 View Descriptive Summary Statistics"):
        st.dataframe(filtered_df[['rate_num', 'votes', 'cost_for_two', 'value_score']].describe().T, use_container_width=True)

    display_cols = ['name', 'dining_type', 'rate_num', 'votes', 'cost_for_two', 'online_order', 'book_table', 'rating_tier', 'value_quadrant']
    st.dataframe(
        filtered_df[display_cols].rename(columns={
            'name': 'Restaurant Name',
            'dining_type': 'Format',
            'rate_num': 'Rating (★)',
            'votes': 'Votes',
            'cost_for_two': 'Cost for 2 (₹)',
            'online_order': 'Online Delivery',
            'book_table': 'Book Table',
            'rating_tier': 'Rating Tier',
            'value_quadrant': 'Value Quadrant'
        }),
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="zomato_analytics_filtered.csv",
        mime="text/csv",
        use_container_width=False
    )

# ==============================================================================
# 10. FOOTER
# ==============================================================================
st.markdown("""
    <div class="dashboard-footer">
        <b>Zomato Restaurant Business Intelligence Dashboard</b> • Official Zomato Branding • Built with Streamlit & Plotly<br>
        Hospitality Executive Decision Support System • Author: <b>Aditya Upadhayay</b>
    </div>
""", unsafe_allow_html=True)
