# OpenAI 모델 불러오기
from langchain_openai import ChatOpenAI

# LLM 객체 생성 및 옵션 설정
llm = ChatOpenAI(
    temperature=0.1,
    max_tokens=2048,
    model_name="gpt-5-nano"
)

# 질문 작성
question = "안녕하세요"

# 스트리밍 방식으로 모델 호출
# response = llm.stream(question)

# 생성되는 답변을 실시간으로 출력
# for token in response:
#     print(token.content, end="", flush=True)