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

# ── 자동 계산 문구 ────────────────────────────────────────────────────────────
top_movie    = df.loc[df["total_audi"].idxmax(), "movieNm"]
top_audi     = df["total_audi"].max()

bin_size     = 1_000_000
df["audi_bin"] = (df["total_audi"] // bin_size) * bin_size
most_bin     = df["audi_bin"].value_counts().idxmax()
most_bin_cnt = df["audi_bin"].value_counts().max()
bin_label_low = int(most_bin // 10_000)
bin_label_hi  = int((most_bin + bin_size) // 10_000)

st.info(
    f"💡 **이 그래프로 알 수 있는 것** : "
    f"216편 중 가장 많은 영화({most_bin_cnt}편)가 "
    f"**{bin_label_low}만 ~ {bin_label_hi}만 명** 구간에 몰려 있으며, "
    f"총 관객이 가장 많은 영화는 **「{top_movie}」** "
    f"({int(top_audi):,}명)입니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 4 : 개봉일 스크린 수 vs 총 관객 수 - 산점도 (장르별 색상)
# ══════════════════════════════════════════════════════════════════════════════
st.header("🎯 그래프 4 : 개봉일 스크린 수 vs 총 관객 수 (산점도)")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객 수의 관계 (장르별 색상)",
    labels={
        "first_scrn" : "개봉일 스크린 수 (개)",
        "total_audi" : "총 관객 수 (명)",
        "genre"      : "장르",
    },
    color_discrete_sequence=px.colors.qualitative.Bold,
    opacity=0.8,
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
    xaxis_tickformat=",",
    yaxis_tickformat=",",
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "개봉 첫날 확보한 스크린 수가 많을수록 총 관객 수도 많아지는 양의 상관관계가 나타나며, "
    "대규모 스크린 배정이 흥행의 중요한 요인임을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 5 : 장르별 총 관객 수 박스플롯 (10편 이상 장르만)
# ══════════════════════════════════════════════════════════════════════════════
st.header("📦 그래프 5 : 장르별 총 관객 수 분포 (박스플롯, 10편 이상 장르)")

genre_10 = (
    df["genre"]
    .value_counts()
    .loc[lambda x: x >= 10]
    .index.tolist()
)
df_box = df[df["genre"].isin(genre_10)].copy()

fig5 = px.box(
    df_box,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="장르별 총 관객 수 분포 (10편 이상 장르)",
    labels={
        "genre"      : "장르",
        "total_audi" : "총 관객 수 (명)",
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
    points="outliers",
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,}명<extra></extra>"
    ),
)

fig5.update_layout(
    title_font_size=18,
    xaxis_title="장르",
    yaxis_title="총 관객 수 (명)",
    yaxis_tickformat=",",
    showlegend=False,
    height=520,
    xaxis_tickangle=-20,
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "장르마다 총 관객 수의 중앙값과 분포 범위가 크게 다르며, "
    "상자 밖으로 튀어나온 점은 같은 장르 안에서도 유독 흥행한 예외적인 작품임을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 6 : 버블 그래프 (스크린 수 vs 총 관객, 버블 크기 = 첫 주 관객)
# ══════════════════════════════════════════════════════════════════════════════
st.header("🫧 그래프 6 : 개봉일 스크린 수 vs 총 관객 수 (버블 크기 = 첫 주 관객)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수 vs 총 관객 수 버블 그래프 (버블 크기 = 개봉 첫 주 관객)",
    labels={
        "first_scrn"      : "개봉일 스크린 수 (개)",
        "total_audi"      : "총 관객 수 (명)",
        "first_week_audi" : "첫 주 관객 수",
        "genre"           : "장르",
    },
    color_discrete_sequence=px.colors.qualitative.Bold,
    opacity=0.75,
    size_max=55,
)

fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "스크린 수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명<extra></extra>"
    ),
)

fig6.update_layout(
    title_font_size=18,
    height=560,
    legend_title_text="장르",
    xaxis_tickformat=",",
    yaxis_tickformat=",",
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "버블이 클수록 개봉 첫 주에 많은 관객을 모은 영화이며, "
    "스크린을 많이 확보하고 첫 주 흥행까지 성공한 영화일수록 최종 관객도 많아지는 경향을 확인할 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 7 : 국가 → 장르 선버스트 그래프 (크기 = 영화 편수)
# ══════════════════════════════════════════════════════════════════════════════
st.header("☀️ 그래프 7 : 제작 국가 → 장르 선버스트 (크기 = 영화 편수)")

sunburst_df = (
    df.groupby(["nation", "genre"])
    .size()
    .reset_index(name="편수")
)

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    values="편수",
    title="제작 국가 → 장르 선버스트 (칸 크기 = 영화 편수)",
    color="nation",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percentRoot:.1%}<extra></extra>"
    ),
    textfont_size=13,
)

fig7.update_layout(
    title_font_size=18,
    height=600,
    margin=dict(t=60, l=10, r=10, b=10),
)

st.plotly_chart(fig7, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "안쪽 원은 제작 국가, 바깥 원은 장르를 나타내며, "
    "국가마다 주력 장르가 다르고 한국 영화와 해외 영화가 서로 다른 장르 분포를 보임을 알 수 있습니다."
)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# 그래프 8 : 개봉일 스크린 수 vs 10위권 머문 날수 - 산점도 (장르별 색상)
# ══════════════════════════════════════════════════════════════════════════════
st.header("📅 그래프 8 : 개봉일 스크린 수 vs 10위권 머문 날수 (산점도)")

fig8 = px.scatter(
    df,
    x="first_scrn",
    y="days_in_top10",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 10위권 머문 날수의 관계 (장르별 색상)",
    labels={
        "first_scrn"    : "개봉일 스크린 수 (개)",
        "days_in_top10" : "10위권 머문 날수 (일)",
        "genre"         : "장르",
    },
    color_discrete_sequence=px.colors.qualitative.Safe,
    opacity=0.8,
)

fig8.update_traces(
    marker=dict(size=8, line=dict(width=0.5, color="white")),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "스크린 수: %{x:,}개<br>"
        "10위권 날수: %{y}일<extra></extra>"
    ),
)

fig8.update_layout(
    title_font_size=18,
    height=520,
    legend_title_text="장르",
    xaxis_tickformat=",",
)

st.plotly_chart(fig8, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "개봉일 스크린 수가 많다고 해서 반드시 오래 10위권에 머무는 것은 아니며, "
    "초반에 스크린을 많이 확보한 영화 중에도 단기간에 순위권에서 사라지는 경우가 있어 "
    "스크린 수보다 작품성과 입소문이 흥행 지속력에 더 큰 영향을 줄 수 있음을 알 수 있습니다."
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
