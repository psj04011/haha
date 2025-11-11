# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top10 (Foreigners' favorites) 🌏", layout="wide")

st.title("🇰🇷 Seoul — 외국인들이 좋아하는 관광지 Top 10")
st.markdown("아래 지도에서 주요 명소를 클릭해보세요. (데이터 출처: TripAdvisor, VisitSeoul, Klook 등)")

# 중심 좌표 (서울 시청/광화문 인근)
SEOUL_CENTER = (37.5665, 126.9780)

# Top 10 명소 (이름, 위도, 경도, 간단설명)
places = [
    {"name": "Gyeongbokgung Palace (경복궁)", "lat":37.5796, "lon":126.9770,
     "desc":"조선의 대표 궁궐 — 한복 체험/근위병 교대식 인기"},
    {"name": "Bukchon Hanok Village (북촌한옥마을)", "lat":37.5826, "lon":126.9830,
     "desc":"전통 한옥이 모여 있는 마을, 골목 산책 추천"},
    {"name": "Insadong (인사동)", "lat":37.5740, "lon":126.9862,
     "desc":"전통 공예/기념품, 찻집 골목"},
    {"name": "Myeongdong (명동)", "lat":37.5638, "lon":126.9826,
     "desc":"쇼핑·스트리트푸드 명소"},
    {"name": "N Seoul Tower (남산타워)", "lat":37.5512, "lon":126.9882,
     "desc":"서울 전경 전망 명소 — 케이블카/야경 인기"},
    {"name": "Hongdae (홍대)", "lat":37.5563, "lon":126.9220,
     "desc":"젊음의 거리, 클럽·카페·스트리트 퍼포먼스"},
    {"name": "Dongdaemun Design Plaza (DDP, 동대문디자인플라자)", "lat":37.5663, "lon":127.0095,
     "desc":"현대 디자인 랜드마크, 야간 조명·야시장 근처"},
    {"name": "Gwangjang Market (광장시장)", "lat":37.5704, "lon":127.0030,
     "desc":"전통시장 먹거리(빈대떡, 마약김밥 등)"},
    {"name": "Cheonggyecheon Stream (청계천)", "lat":37.5703, "lon":126.9770,
     "desc":"도심 속 산책로, 야경·이벤트 공간"},
    {"name": "Lotte World Tower / COEX (롯데월드타워 / 코엑스)", "lat":37.5116, "lon":127.1026,
     "desc":"롯데월드, 전망대, 코엑스몰·스타필드 등(강남권 쇼핑·전시)"}
]

# Create folium map
m = folium.Map(location=SEOUL_CENTER, zoom_start=12, tiles="OpenStreetMap")

# Add markers
for p in places:
    popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
    folium.Marker(
        location=(p["lat"], p["lon"]),
        popup=popup_html,
        tooltip=p["name"],
        icon=folium.Icon(icon="info-sign")
    ).add_to(m)

# Add a cluster (optional) - commented out; simple markers are fine
# from folium.plugins import MarkerCluster
# marker_cluster = MarkerCluster().add_to(m)
# for p in places:
#     folium.Marker(location=(p["lat"], p["lon"]), popup=p["name"]).add_to(marker_cluster)

# Display map in Streamlit
st.subheader("지도")
st.markdown("지도 내 마커를 클릭하면 간단한 설명이 나옵니다.")
st_data = st_folium(m, width=900, height=600)

# Show list + quick links
st.subheader("명소 목록")
for i, p in enumerate(places, start=1):
    st.markdown(f"**{i}. {p['name']}** — {p['desc']}")

# Show this app's source code so users can copy easily
st.subheader("앱 코드 (복사해서 사용하세요)")
with st.expander("app.py 코드 보기", expanded=True):
    import inspect, sys
    # 안전하게 현재 파일 내용을 보여주기 위해 아래 방법 사용.
    # (Streamlit에서 실행 시 이 파일을 읽어 내용 표시)
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception:
        # 앱을 다른 환경에서 실행할 때 __file__ 접근 불가하면, fallback 텍스트 제공
        code = "# 소스 코드를 여기에 복사해 붙여넣으세요 (app.py)\n"
    st.code(code, language="python")

st.markdown("---")
st.caption("참고자료: TripAdvisor / VisitSeoul / Klook 등에서 외국인 인기 명소로 자주 추천됩니다. :contentReference[oaicite:1]{index=1}")
