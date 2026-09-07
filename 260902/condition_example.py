questions = ["asyncio란?", "", "FastAPI란?"]

# 빈 문자열이 아닌 질문만 저장할 리스트
valid_questions: list[str] = []

for question in questions:

    # strip(): 문자열 양쪽의 공백, 탭, 줄바꿈 제거
    cleaned = question.strip()

    # 빈 문자열이면 현재 반복을 건너뛰고 다음 요소로 이동
    if not cleaned:
        continue

    # 빈 문자열이 아닌 질문만 리스트에 추가
    valid_questions.append(cleaned)

print(valid_questions)

# 결과
# ['asyncio란?', 'FastAPI란?']