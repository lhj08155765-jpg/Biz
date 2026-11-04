import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    # 파일 이름 및 시트 이름 지정
    file_path = "Sales.xlsx"
    sheet_name = "supermarket_sales_test"
    
    try:
        # Excel 데이터 읽기
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # 결측치 제거
        df = df.dropna()
        # 컬럼 양 끝 공백 제거
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None:
    st.title("🏪 Supermarket Sales Dashboard")
    st.markdown("---")

    # 사이드바에서 지점(Branch) 선택
    st.sidebar.header("필터 설정")
    branches = sorted(df['Branch'].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch)을 선택하세요:", branches)

    # 선택한 지점의 데이터로 필터링
    filtered_df = df[df['Branch'] == selected_branch]

    # 메트릭 계산
    # 'Total' 컬럼은 매출액, 'Rating' 컬럼은 평점 기준
    total_sales = filtered_df['Total'].sum()
    avg_sales = filtered_df['Total'].mean()
    avg_rating = filtered_df['Rating'].mean()

    # 상단 지표(Metric) 시각화
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="총 매출 (Total Sales)", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="평균 매출 (Average Sales)", value=f"${avg_sales:,.2f}")
    with col3:
        st.metric(label="평균 평점 (Average Rating)", value=f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 상품 카테고리(Product line)별 평균 매출 계산
    category_sales = filtered_df.groupby('Product line')['Total'].mean().reset_index()
    category_sales = category_sales.rename(columns={'Total': 'Average Sales'})
    # 내림차순 정렬
    category_sales = category_sales.sort_values(by='Average Sales', ascending=False)

    # Plotly를 이용한 막대그래프 시각화
    st.subheader(f"📍 {selected_branch} 지점 상품 카테고리별 평균 매출")
    fig = px.bar(
        category_sales,
        x='Product line',
        y='Average Sales',
        text_auto='.2s',
        labels={'Product line': '상품 카테고리', 'Average Sales': '평균 매출 ($)'},
        color='Average Sales',
        color_continuous_scale='Blues'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Sales.xlsx 파일이 올바른 경로에 존재하는지 확인해주세요.")
