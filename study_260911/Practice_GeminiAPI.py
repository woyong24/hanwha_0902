from google import genai
from google.genai import types

client = genai.Client()

# 요청 부분 토큰나간당
# response = client.models.generate_content(
#     model="gemini-3.5-flash-lite",
#     contents="파이썬이 무엇인지 한 문장으로 설명해줘.",
#     config=types.GenerateContentConfig(
#         temperature=0.5
#     )
# )

#출력 부분
print(response.text)
print(response.usage_metadata)
print("입력 토큰:", response.usage_metadata.prompt_token_count)
print("출력 토큰:", response.usage_metadata.candidates_token_count)
print("전체 토큰:", response.usage_metadata.total_token_count)

