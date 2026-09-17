# 260914 LangChain / LangSmith 정리

> **오늘 핵심**
>
> OpenAI 모델 객체 생성 → `invoke()` / `stream()`으로 호출 → LangSmith로 실행 기록 확인 → 이미지도 함께 입력 → Python Logging으로 로컬 로그 저장

---

# 1. ChatOpenAI 객체 생성

LangChain에서 OpenAI 모델을 사용하기 위한 객체를 만든다.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    temperature=0.1,
    model_name="gpt-5-nano"
)
```

| 옵션 | 의미 |
|---|---|
| `model_name` | 사용할 OpenAI 모델 |
| `temperature` | 답변의 무작위성 정도 |

### temperature

```text
낮음 → 비교적 일정하고 안정적인 답변
높음 → 조금 더 다양하고 창의적인 답변
```

> **중요**
>
> `ChatOpenAI()` 객체를 만드는 것만으로는 API 비용이 발생하지 않는다.  
> `invoke()`, `stream()` 등으로 실제 요청을 보낼 때 비용이 발생한다.

---

# 2. invoke와 stream

## 일반 응답

```python
response = llm.invoke("안녕하세요")

print(response.content)
```

`invoke()`는 **답변이 완성된 뒤 한 번에 받는 방식**이다.

---

## Stream 응답

```python
answer = llm.stream("안녕하세요")

for token in answer:
    print(token.content, end="", flush=True)
```

`stream()`은 **답변이 생성되는 대로 조금씩 받아서 출력하는 방식**이다.

```text
invoke()
질문 → 답변 완성 → 한 번에 출력

stream()
질문 → 답변 생성 → 조금씩 실시간 출력
```

---

## Stream 출력 + 최종 답변 저장

```python
answer = llm.stream(
    "대한민국의 아름다운 관광지 10곳을 알려주세요."
)

final_answer = ""

for token in answer:
    print(token.content, end="", flush=True)
    final_answer += token.content
```

### 역할

```text
print()
→ 화면에 실시간 출력

final_answer += token.content
→ 스트리밍 답변을 하나의 문자열로 계속 저장
```

나중에 전체 답변은 다음처럼 확인한다.

```python
print(final_answer)
```

---

# 3. API Key와 .env

API Key를 Python 코드에 직접 작성하면 GitHub에 노출될 수 있다.

따라서 **환경변수로 관리하는 것이 안전하다.**

LangSmith 설정 예시:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=ex0914
```

`.env`를 Python에서 읽을 때:

```python
from dotenv import load_dotenv

load_dotenv()
```

Windows 시스템 환경변수에 저장한 값은 다음처럼 확인할 수 있다.

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

---

## GitHub에 올리면 안 되는 것

`.gitignore`에 반드시 추가한다.

```gitignore
.env
.venv/
```

> **주의**
>
> `.env`에는 API Key가 들어갈 수 있으므로 GitHub에 업로드하지 않는다.  
> `.venv` 역시 용량이 크고 다른 PC에서 그대로 사용할 필요가 없으므로 업로드하지 않는다.

---

# 4. LangSmith란?

LangSmith는 **LangChain 프로그램의 실행 기록을 확인하는 서비스**이다.

쉽게 말하면:

```text
VS Code에서 LLM 실행
        ↓
OpenAI API 호출
        ↓
LangSmith에 실행 기록 전송
        ↓
웹에서 기록 확인
```

이 기능을 **Tracing**이라고 한다.

---

## LangSmith에서 확인 가능한 내용

- 어떤 질문을 보냈는지
- 어떤 답변이 생성됐는지
- 실행 시간이 얼마나 걸렸는지
- 사용한 토큰 수
- API 비용
- Tool 호출 여부
- 오류 발생 여부

예를 들어:

```env
LANGSMITH_PROJECT=ex0914
```

라고 설정하면 실행 기록을 LangSmith의 `ex0914` 프로젝트에서 확인한다.

> **Tracing = VS Code에서 실행한 LLM의 실행 기록을 LangSmith에 남기는 것**

---

# 5. LangSmith Endpoint 오류

오늘 발생한 오류:

```text
Failed to resolve 'api.langchain.com'
```

원인은 LangSmith 서버 주소가 잘못 설정되어 있었기 때문이다.

### 잘못된 주소

```env
LANGSMITH_ENDPOINT=https://api.langchain.com
```

### 올바른 주소

```env
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

---

## .env 수정 후 값이 안 바뀔 때

```python
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()

load_dotenv(
    env_path,
    override=True
)
```

현재 환경변수 확인:

```python
import os

print(os.getenv("LANGSMITH_ENDPOINT"))
```

정상 결과:

```text
https://api.smith.langchain.com
```

> `.env`를 수정했는데 이전 값이 계속 사용된다면 VS Code Notebook의 **Kernel Restart**를 한 번 해주는 것이 좋다.

---

# 6. MultiModal

MultiModal은 **텍스트뿐만 아니라 이미지 같은 다른 형태의 데이터도 함께 처리하는 방식**이다.

예:

```text
이미지
+
"이 이미지를 설명해 주세요."
        ↓
LLM
        ↓
이미지 분석 결과
```

---

## HumanMessage에 이미지와 질문 넣기

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "이미지를 설명해 주세요."
        },
        {
            "type": "image_url",
            "image_url": {
                "url": IMAGE_URL
            }
        },
    ]
)
```

여기서는:

```text
text
→ 사용자 질문

image_url
→ 모델에게 보여줄 이미지
```

두 가지를 하나의 사용자 메시지로 묶는다.

---

## 모델에 이미지 보내기

```python
answer = llm.stream([message])

for token in answer:
    print(token.content, end="", flush=True)
```

전체 흐름:

```text
이미지 URL 준비
        ↓
질문 작성
        ↓
HumanMessage로 질문 + 이미지 묶기
        ↓
LLM에 전달
        ↓
이미지 분석 답변 출력
```

---

# 7. 로컬 이미지를 모델에 전달하기

인터넷 이미지 URL은 그대로 사용할 수 있다.

하지만 내 PC에 저장된 이미지 파일은 API가 바로 읽을 수 없기 때문에 문자열 형태로 변환할 수 있다.

```python
def image_url(image_source):
    if str(image_source).startswith(("http://", "https://")):
        return str(image_source)

    image_path = Path(image_source)

    mimetype = (
        "image/png"
        if image_path.suffix.lower() == ".png"
        else "image/jpeg"
    )

    encoded_image = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    return f"data:{mimetype};base64,{encoded_image}"
```

### 흐름

```text
인터넷 이미지
→ URL 그대로 사용

PC에 저장된 이미지
→ 파일 읽기
→ Base64 문자열로 변환
→ 모델에 전달 가능한 형태로 변경
```

---

# 8. Python Logging

Logging은 **프로그램 실행 기록을 파일에 남기는 기능**이다.

LangSmith와 비슷해 보이지만 역할이 다르다.

| 구분 | 역할 |
|---|---|
| LangSmith | LLM 실행 기록을 웹에서 확인 |
| Python Logging | 내가 원하는 프로그램 실행 기록을 로컬 파일에 저장 |

---

## Logging 기본 설정

```python
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
```

### 각 옵션

```text
filename
→ 로그를 저장할 파일

level
→ 어떤 수준의 로그부터 기록할지 설정

format
→ 로그가 저장되는 형식

encoding
→ 한글 깨짐 방지
```

---

## Logger 만들기

```python
logger = logging.getLogger("MyMultimodalApp")
```

`MyMultimodalApp`이라는 이름의 로그 기록기를 만든다.

---

## INFO 로그 남기기

```python
logger.info("애플리케이션 시작")
```

`app.log`에는 대략 다음처럼 기록된다.

```text
2026-09-14 17:15:00 - INFO - 애플리케이션 시작
```

---

# 9. try / except로 오류 기록

프로그램을 실행하다 오류가 발생했을 때 로그 파일에 기록할 수 있다.

```python
try:
    # 실행할 코드

except Exception as e:
    logger.error(
        f"실행 중 에러 발생: {str(e)}",
        exc_info=True
    )
```

### 의미

```text
try
→ 일단 코드를 실행

except
→ 오류가 발생하면 여기로 이동

str(e)
→ 실제 오류 메시지

exc_info=True
→ Traceback까지 app.log에 저장
```

오류 원인을 나중에 확인할 때 유용하다.

---

# 10. requirements.txt

현재 가상환경에 설치된 Python 패키지 목록을 저장하는 파일이다.

생성:

```bash
python -m pip freeze > requirements.txt
```

다른 가상환경에서 동일한 패키지를 설치:

```bash
pip install -r requirements.txt
```

### 사용하는 이유

```text
현재 개발 환경
→ requirements.txt에 패키지 목록 저장
→ 다른 폴더나 다른 PC로 이동
→ 같은 패키지를 다시 설치
```

---

# 전체 흐름 한 번에 보기

```text
1. API Key를 환경변수로 설정
        ↓
2. .env에서 LangSmith 설정
        ↓
3. ChatOpenAI 객체 생성
        ↓
4. invoke() / stream()으로 LLM 호출
        ↓
5. 필요하면 이미지까지 함께 전달
        ↓
6. LangSmith에서 Tracing 확인
        ↓
7. Python Logging으로 app.log 저장
        ↓
8. requirements.txt 생성
        ↓
9. 코드와 필요한 자료 GitHub 업로드
```

---

# 꼭 기억할 것

> **API**
>
> `ChatOpenAI()`는 모델 객체 생성이다.  
> `invoke()`나 `stream()`을 실행해야 실제 API가 호출된다.

> **Stream**
>
> 답변을 완성될 때까지 기다리지 않고 생성되는 대로 받는 방식이다.

> **LangSmith**
>
> LLM의 질문, 답변, 토큰, 시간 등의 실행 기록을 웹에서 확인한다.

> **MultiModal**
>
> 텍스트뿐 아니라 이미지를 함께 모델에 전달할 수 있다.

> **Logging**
>
> Python 프로그램의 실행 과정과 오류를 `app.log` 같은 로컬 파일에 저장한다.

> **GitHub**
>
> `.env`, `.venv`는 올리지 않는다.  
> API Key가 캡처 화면이나 로그에 노출되지 않았는지도 확인한다.

> **requirements.txt**
>
> 현재 개발환경에 설치된 패키지를 나중에 다시 설치할 수 있도록 기록한다.