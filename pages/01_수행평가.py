import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌊 쓰나미 데이터 분석 대시보드")
st.write("Plotly 기반 인터랙티브 분석 + Streamlit Cloud용")

# 1. 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    except:
        df = pd.read_csv(uploaded_file, encoding="cp949")

    st.subheader("🔍 데이터 미리보기")
    st.dataframe(df.head())

    # 지역별 평균 쓰나미 높이 계산
    region_mean = (
        df.groupby("프로젝트지역영문")["쓰나미높이"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.subheader("🏆 지역별 평균 쓰나미 높이 (내림차순)")
    st.dataframe(region_mean)

    # Plotly 막대 그래프
    fig = px.bar(
        region_mean,
        x="프로젝트지역영문",
        y="쓰나미높이",
        title="📊 지역별 평균 쓰나미 높이 (높은 순)",
        labels={"프로젝트지역영문": "지역", "쓰나미높이": "평균 쓰나미 높이"},
        text_auto=True,
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("CSV 파일을 업로드하면 분석이 시작됩니다!")
