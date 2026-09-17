requests = ["첫 번째 질문", "두 번째 질문"]

# 응답 데이터를 딕셔너리 형태로 구성
response = {
    "status": "success",       # 처리 상태
    "count": len(requests),    # 요청 개수
    "items": requests,         # 요청 목록
}

# 딕셔너리에서 count 값을 꺼내 출력
print(response["count"], end="개")

# 결과
# 2개