import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.title("상품 관리")


# Create
st.subheader("상품 추가")

with st.form("create_form"):
    name = st.text_input("상품명")
    price = st.number_input("가격", min_value=0, step=1000)
    stock = st.number_input("재고", min_value=0, step=1)

    create_button = st.form_submit_button("추가")

    if create_button:
        response = requests.post(
            f"{API_URL}/products",
            json={
                "name": name,
                "price": int(price),
                "stock": int(stock),
            },
        )

        if response.status_code == 200:
            st.success("상품이 추가되었습니다.")
        else:
            st.error("상품 추가에 실패했습니다.")


# Update
st.subheader("상품 수정")

with st.form("update_form"):
    update_id = st.number_input(
        "수정할 상품 ID",
        min_value=1,
        step=1,
    )
    update_name = st.text_input("새 상품명")
    update_price = st.number_input(
        "새 가격",
        min_value=0,
        step=1000,
    )
    update_stock = st.number_input(
        "새 재고",
        min_value=0,
        step=1,
    )

    update_button = st.form_submit_button("수정")

    if update_button:
        response = requests.put(
            f"{API_URL}/products/{int(update_id)}",
            json={
                "name": update_name,
                "price": int(update_price),
                "stock": int(update_stock),
            },
        )

        if response.status_code == 200:
            st.success("상품이 수정되었습니다.")
        else:
            st.error("상품을 찾을 수 없습니다.")


# Delete
st.subheader("상품 삭제")

with st.form("delete_form"):
    delete_id = st.number_input(
        "삭제할 상품 ID",
        min_value=1,
        step=1,
    )

    delete_button = st.form_submit_button("삭제")

    if delete_button:
        response = requests.delete(
            f"{API_URL}/products/{int(delete_id)}"
        )

        if response.status_code == 200:
            st.success("상품이 삭제되었습니다.")
        else:
            st.error("상품을 찾을 수 없습니다.")


# Read
st.subheader("상품 목록")

try:
    response = requests.get(f"{API_URL}/products")

    if response.status_code == 200:
        products = response.json()

        if products:
            st.dataframe(products, use_container_width=True)
        else:
            st.info("등록된 상품이 없습니다.")

except requests.exceptions.ConnectionError:
    st.error("FastAPI 서버가 실행 중인지 확인하세요.")