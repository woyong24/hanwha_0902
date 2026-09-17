# 환경변수 확인 Gemini
import os
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("Gemini API Key 설정 완료")
else:
    print("설정 안됨 다시해")


# OpenAI API 호출 (토큰 나감 실행 ㄴㄴ)
client = OpenAI()

# response = client.responses.create(
#     model="gpt-5-nano",
#     input="API 키 연결 테스트입니다. '정상 연결'이라고만 답해주세요."
# )

print(response.output_text)