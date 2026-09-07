def normalize_question(question: str, max_length: int = 100) -> str:

    # 질문 앞뒤의 불필요한 공백 제거
    cleaned = question.strip()

    # 내용이 없으면 잘못된 질문으로 판단
    if not cleaned:
        raise ValueError("질문을 입력하세요.")

    # 길이가 너무 길 경우 최대 100자까지만 사용
    return cleaned[:max_length]


def build_responses(questions: list[str]) -> list[dict[str, str]]:

    # 처리 결과를 저장할 리스트
    responses = []

    # enumerate()를 사용해 질문과 번호를 함께 가져옴
    for index, question in enumerate(questions, start=1):

        try:
            # 질문을 정리하고 정상 여부 확인
            cleaned = normalize_question(question)

            # 정상 질문은 ready 상태로 저장
            responses.append({
                "id": str(index),
                "question": cleaned,
                "status": "ready"
            })

        except ValueError:

            # 빈 질문 등 오류가 발생하면 invalid 상태로 저장
            responses.append({
                "id": str(index),
                "question": "",
                "status": "invalid"
            })

    return responses


items = build_responses(["Pydantic이란?", " ", "FastAPI란?"])

# 만들어진 결과를 하나씩 출력
for item in items:
    print(item)


# 결과
# {'id': '1', 'question': 'Pydantic이란?', 'status': 'ready'}
# {'id': '2', 'question': '', 'status': 'invalid'}
# {'id': '3', 'question': 'FastAPI란?', 'status': 'ready'}