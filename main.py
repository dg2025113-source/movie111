import streamlit as st
import pandas as pd
import plotly.express as px

# ── 페이지 기본 설정 ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide",
)

# ── 제목 ──────────────────────────────────────────────────────────────────────
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    """
    1년간 박스오피스 10위권에 든 영화 가운데 이 기간에 개봉한 **216편**의 데이터를 활용합니다.  
    각 그래프를 살펴보며 영화 산업의 특징을 탐구해 보세요! 🔍
    """
)
st.divider()

# ── 데이터 불러오기 ───────────────────────────────────────────────────────────
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()
    df["openDt"] = df["openDt"].astype(str).str.zfill(8)
    df["open_year"] = df["openDt"].str[:4]
    return df

df = load_data(DATA_URL)

with st.expander("📋 원본 데이터 미리보기 (클릭하여 열기)"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 1 : 장르별 영화 편수 - 도넛 그래프
# ══════════════════════════════════════════════════════════════════════════════
st.header("🍩 그래프 1 : 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "genre", "count": "편수", "genre": "장르"})
)

if "장르" not in genre_counts.columns:
    genre_counts.columns = ["장르", "편수"]

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.45,
    title="장르별 영화 편수 (도넛 차트)",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig1.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

fig1.update_layout(
    title_font_size=18,
    legend_title_text="장르",
    height=520,
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "박스오피스 상위권에 오른 영화들은 특정 장르에 편중되어 있으며, "
    "가장 많은 편수를 차지하는 장르가 흥행 시장을 주도하고 있음을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 2 : 장르 안에 영화가 들어 있는 트리맵 (크기 = 총 관객)
# ══════════════════════════════════════════════════════════════════════════════
st.header("🗺️ 그래프 2 : 장르별 영화 트리맵 (크기 = 총 관객 수)")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 트리맵 (칸 크기 = 총 관객 수)",
    color="total_audi",
    color_continuous_scale="Blues",
    labels={
        "genre"      : "장르",
        "movieNm"    : "영화명",
        "total_audi" : "총 관객 수",
    },
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명<br>"
        "상위 항목: %{parent}<extra></extra>"
    ),
    texttemplate="%{label}<br>%{value:,}명",
    textfont_size=12,
)

fig2.update_layout(
    title_font_size=18,
    height=600,
    coloraxis_colorbar=dict(
        title="총 관객 수",
        tickformat=",",
    ),
    margin=dict(t=60, l=10, r=10, b=10),
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "장르별로 묶인 칸의 크기를 통해 어떤 장르가 전체 관객을 많이 동원했는지, "
    "그 안에서 어떤 영화가 흥행을 주도했는지 한눈에 파악할 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 3 : 총 관객 수 분포 - 히스토그램
# ══════════════════════════════════════════════════════════════════════════════
st.header("📊 그래프 3 : 총 관객 수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객 수 분포",
    labels={"total_audi": "총 관객 수 (명)", "count": "영화 편수"},
    color_discrete_sequence=["#6C9BCF"],
)

fig3.update_traces(
    hovertemplate="총 관객: %{x:,}명<br>편수: %{y}편<extra></extra>"
)

fig3.update_layout(
    title_font_size=18,
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 편수",
    bargap=0.05,
    height=480,
)

st.plotly_chart(fig3, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "총 관객 수는 오른쪽으로 긴 꼬리를 가진 분포를 보이며, "
    "소수의 영화가 압도적으로 많은 관객을 모으는 '흥행 쏠림 현상'이 존재함을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 4 : 개봉일 스크린 수 vs 총 관객 수 - 산점도
# ══════════════════════════════════════════════════════════════════════════════
st.header("🎯 그래프 4 : 개봉일 스크린 수 vs 총 관객 수 (산점도)")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객 수의 관계",
    labels={
        "first_scrn" : "개봉일 스크린 수",
        "total_audi" : "총 관객 수 (명)",
        "genre"      : "장르",
    },
    color_discrete_sequence=px.colors.qualitative.Bold,
    opacity=0.75,
)

fig4.update_traces(
    marker=dict(size=8, line=dict(width=0.5, color="white")),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "스크린 수: %{x:,}개<br>"
        "총 관객: %{y:,}명<extra></extra>"
    ),
)

fig4.update_layout(
    title_font_size=18,
    height=520,
    legend_title_text="장르",
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "개봉 첫날 확보한 스크린 수가 많을수록 총 관객 수도 많아지는 양의 상관관계가 나타나며, "
    "대규모 스크린 배정이 흥행의 중요한 요인임을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 5 : 10위권 머문 날수 분포 - 박스플롯 (장르별)
# ══════════════════════════════════════════════════════════════════════════════
st.header("📦 그래프 5 : 장르별 10위권 머문 날수 분포 (박스플롯)")

genre_filter = genre_counts[genre_counts["편수"] >= 2]["장르"].tolist()
df_filtered = df[df["genre"].isin(genre_filter)]

fig5 = px.box(
    df_filtered,
    x="genre",
    y="days_in_top10",
    color="genre",
    title="장르별 10위권 머문 날수 분포",
    labels={
        "genre"         : "장르",
        "days_in_top10" : "10위권 머문 날수",
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
    points="all",
)

fig5.update_traces(
    hovertemplate="장르: %{x}<br>날수: %{y}일<extra></extra>"
)

fig5.update_layout(
    title_font_size=18,
    xaxis_title="장르",
    yaxis_title="10위권 머문 날수 (일)",
    showlegend=False,
    height=520,
    xaxis_tickangle=-30,
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "장르에 따라 10위권 유지 기간의 중앙값과 분포 범위가 다르며, "
    "특정 장르는 단기 흥행에 집중되고 다른 장르는 더 오래 관객의 선택을 받는 경향이 있음을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 6 : 개봉 첫 주 관객 vs 총 관객 - 산점도 (국가별 색상)
# ══════════════════════════════════════════════════════════════════════════════
st.header("🌟 그래프 6 : 개봉 첫 주 관객 vs 총 관객 (산점도)")

fig6 = px.scatter(
    df,
    x="first_week_audi",
    y="total_audi",
    color="nation",
    hover_name="movieNm",
    title="개봉 첫 주 관객과 총 관객 수의 관계",
    labels={
        "first_week_audi" : "개봉 첫 주 관객 수 (명)",
        "total_audi"      : "총 관객 수 (명)",
        "nation"          : "제작 국가",
    },
    color_discrete_sequence=px.colors.qualitative.Safe,
    opacity=0.8,
)

fig6.update_traces(
    marker=dict(size=8, line=dict(width=0.5, color="white")),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "첫 주 관객: %{x:,}명<br>"
        "총 관객: %{y:,}명<extra></extra>"
    ),
)

fig6.update_layout(
    title_font_size=18,
    height=520,
    legend_title_text="제작 국가",
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "개봉 첫 주 관객 수와 최종 총 관객 수 사이에 강한 양의 상관관계가 존재하며, "
    "초반 흥행 성적이 영화의 전체 흥행을 예측하는 중요한 지표임을 알 수 있습니다."
)

st.divider()

# ── 푸터 ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; color:gray; font-size:13px;'>
        📽️ 데이터 출처: KOBIS 박스오피스 | 당곡고등학교 영화 데이터 그래프 도감 2
    </div>
    """,
    unsafe_allow_html=True,
)
