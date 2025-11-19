# streamlit_tsunami_plot.py
# Streamlit app that displays tsunami occurrences by region using Plotly.
# Drop this file into Streamlit Cloud (or run locally with `streamlit run streamlit_tsunami_plot.py`).
# The app also writes a requirements.txt automatically when first run.

import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os

# --- Write requirements.txt (helpful for Streamlit Cloud) ---
req_content = """streamlit
pandas
plotly
"""
if not os.path.exists("requirements.txt"):
    with open("requirements.txt", "w") as f:
        f.write(req_content)

# --- Page config ---
st.set_page_config(page_title="Tsunami occurrences by region", layout="wide")

st.title("🌊 Tsunami occurrences — interactive explorer")
st.markdown(
    "Upload a CSV with at least these columns: `region`, `tsunami_count`.\n"
    "Optional columns: `latitude`, `longitude` (for plotting on a map), `year` (to filter by time)."
)

# --- Sample data (used if user doesn't upload) ---
SAMPLE_CSV = "region,tsunami_count,latitude,longitude\n" \
             "Japan,120,36.2048,138.2529\n" \
             "Indonesia,95,-0.7893,113.9213\n" \
             "Chile,60,-35.6751,-71.5430\n" \
             "Philippines,50,12.8797,121.7740\n" \
             "USA (Alaska),45,64.2008,-149.4937\n" \
             "New Zealand,22,-40.9006,174.8860\n" \
             "Mexico,18,23.6345,-102.5528\n" \
             "Peru,16,-9.189967,-75.015152\n" \
             "Italy,8,41.8719,12.5674\n" \
             "India,5,20.5937,78.9629\n"

uploaded_file = st.file_uploader("Upload CSV", type=["csv"], help="CSV must include columns: region, tsunami_count")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()
else:
    st.info("샘플 데이터를 사용하고 있습니다 — CSV를 업로드하면 해당 데이터로 그래프가 갱신됩니다.")
    df = pd.read_csv(io.StringIO(SAMPLE_CSV))

# Basic validation
required_cols = {"region", "tsunami_count"}
if not required_cols.issubset(set(df.columns.str.lower())):
    # Try to be flexible with column name case
    cols_lower = {c.lower(): c for c in df.columns}
    if required_cols.issubset(set(cols_lower.keys())):
        # rename
        df = df.rename(columns={cols_lower[c]: c for c in cols_lower if c in required_cols})
    else:
        st.error("CSV에 'region'과 'tsunami_count' 컬럼이 반드시 포함되어야 합니다.")
        st.stop()

# normalize column names to expected ones
cols_map = {c: c for c in df.columns}
# if user used different case, rename
if 'region' not in df.columns and any(c.lower()=='region' for c in df.columns):
    for c in df.columns:
        if c.lower()=='region':
            df = df.rename(columns={c:'region'})
            break
if 'tsunami_count' not in df.columns and any(c.lower()=='tsunami_count' for c in df.columns):
    for c in df.columns:
        if c.lower()=='tsunami_count':
            df = df.rename(columns={c:'tsunami_count'})
            break

# ensure tsunami_count numeric
df['tsunami_count'] = pd.to_numeric(df['tsunami_count'], errors='coerce').fillna(0).astype(int)

# Optional lat/lon columns handling
has_latlon = ('latitude' in df.columns) and ('longitude' in df.columns)

# Controls
st.sidebar.header("Controls")
min_count = int(df['tsunami_count'].min())
max_count = int(df['tsunami_count'].max())

top_n = st.sidebar.slider("Top N regions to show", min_value=1, max_value=min(50, len(df)), value=min(10, len(df)))
sort_order = st.sidebar.radio("Sort order", options=["Descending (most tsunamis first)", "Ascending (least tsunamis first)"], index=0)

# Optional year filtering if 'year' exists
if 'year' in df.columns:
    yr_min = int(df['year'].min())
    yr_max = int(df['year'].max())
    year_range = st.sidebar.slider("Year range", value=(yr_min, yr_max), min_value=yr_min, max_value=yr_max)
    df = df[df['year'].between(year_range[0], year_range[1])]

# Aggregate by region (in case input has multiple rows per region)
agg = df.groupby('region', as_index=False).agg({
    'tsunami_count': 'sum',
    **({'latitude':'mean','longitude':'mean'} if has_latlon else {})
})

# Sort
ascending = (sort_order.startswith('Ascending'))
agg = agg.sort_values(by='tsunami_count', ascending=ascending)
agg_top = agg.tail(top_n) if not ascending else agg.head(top_n)
# If descending, tail will give top N but maintain ascending index, so reorder for plot
agg_top = agg_top.sort_values(by='tsunami_count', ascending=False)

# Main layout: two columns
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Bar chart — regions ordered by tsunami occurrences")
    fig_bar = px.bar(
        agg_top,
        x='tsunami_count',
        y='region',
        orientation='h',
        labels={'tsunami_count':'Tsunami count', 'region':'Region'},
        title=f"Top {len(agg_top)} regions by tsunami occurrences",
        hover_data={'tsunami_count':True}
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

    if has_latlon and len(agg_top)>0:
        st.subheader("Map — locations of regions (if latitude/longitude provided)")
        fig_map = px.scatter_geo(
            agg_top,
            lat='latitude',
            lon='longitude',
            hover_name='region',
            size='tsunami_count',
            projection='natural earth',
            title='Region locations sized by tsunami count'
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("CSV에 latitude/longitude 컬럼이 없거나 부족하여 지도를 표시할 수 없습니다. (선택사항)")

with col2:
    st.subheader("Data table")
    st.dataframe(agg.sort_values(by='tsunami_count', ascending=False).reset_index(drop=True))

st.markdown("---")
st.markdown("**파일 포맷 예시:**\n`region,tsunami_count,latitude,longitude,year`\n(년은 선택사항)\n\nCSV 예시는 앱 상단에서 다운로드/업로드 없이 미리 로드됩니다.")

st.sidebar.markdown("---")
st.sidebar.markdown("App automatically creates a requirements.txt for Streamlit Cloud. If you'd rather provide your own, remove the generated file.")

# Provide a CSV download of the aggregated results
@st.cache_data
def to_csv_bytes(df_):
    return df_.to_csv(index=False).encode('utf-8')

csv_bytes = to_csv_bytes(agg.sort_values(by='tsunami_count', ascending=False))
st.download_button(label='Download aggregated CSV', data=csv_bytes, file_name='tsunami_by_region_aggregated.csv', mime='text/csv')

# footer: helpful hint for user
st.caption("Tip: upload a CSV with rows per event or per region — the app will aggregate by region and show the top regions interactively.")
