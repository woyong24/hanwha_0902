def normalize_question(question: str, max_length: int = 100) -> str:

    # 문자열 앞뒤 공백 제거
    cleaned = question.strip()

    # 공백 제거 후 빈 문자열이면 에러 발생
    if not cleaned:
        raise ValueError("질문을 입력하세요.")

    # 최대 max_length 길이까지만 잘라서 반환
    return cleaned[:max_length]


try:
    # 함수 실행
    result = normalize_question("  Python이란?  ")
    print(result)

# ValueError가 발생하면 에러 메시지 출력
except ValueError as error:
    print("입력 오류:", error)

# 결과
# Python이란?