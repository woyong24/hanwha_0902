# Chapter 6 복습 노트: 출력 형식과 Pandas 데이터

## 한눈에 보는 목표

AI의 답변을 그냥 문장으로 받는 데서 끝내지 않고, **목록·JSON·날짜·정해진 선택지·표 데이터**처럼 프로그램이 바로 쓸 수 있는 형태로 바꾸는 방법을 배웁니다.

`질문 만들기 → 모델 호출 → Output Parser로 형식 검사·변환 → Python에서 활용`

| 파일 | 핵심 | 결과 형태 |
|---|---|---|
| 6-1 | Pydantic 출력 파서 | 정해진 항목을 가진 객체 |
| 6-2 | `with_structured_output()` | Pydantic 객체를 바로 반환 |
| 6-3 | 파일 없음 | 폴더에 노트북이 없음 |
| 6-4 | 쉼표 목록 파서 | Python 리스트 |
| 6-5 | 구조화 출력 파서 | `answer`, `source` 같은 딕셔너리 |
| 6-6 | JSON 파서 | JSON/딕셔너리 |
| 6-7 | Pandas DataFrame 파서 | 표 조회·계산 결과 |
| 6-8 | 날짜 파서 | Python 날짜 객체 |
| 6-9 | Enum 파서 | 허용된 선택지 하나 |

## 1. Output Parser가 필요한 이유

AI는 보통 자연스러운 문장으로 답합니다. 하지만 화면에 칸별로 표시하거나, 데이터베이스에 저장하거나, 다음 코드로 계산하려면 일정한 형식이 필요합니다.

```python
chain = prompt | model | output_parser
```

- `prompt`: AI에게 질문과 답변 형식을 안내합니다.
- `model`: 답변을 생성합니다.
- `output_parser`: 답변을 읽어 Python에서 쓸 수 있는 자료형으로 바꾸고 형식을 확인합니다.

`get_format_instructions()`의 안내문을 프롬프트에 넣는 것이 중요합니다. AI가 어떤 모양으로 답해야 하는지 알아야 파서가 안전하게 읽을 수 있습니다.

## 2. 자주 쓰는 출력 형식

| 도구 | 언제 쓰나 | 예시 |
|---|---|---|
| `PydanticOutputParser` | 항목 이름과 자료형을 엄격히 정할 때 | 발신자, 이메일, 제목, 요약, 날짜 |
| `with_structured_output()` | 모델이 Pydantic 형식으로 바로 답하게 할 때 | `answer.person`처럼 필드 사용 |
| `CommaSeparatedListOutputParser` | 여러 항목의 목록이 필요할 때 | 관광지 5개 → 리스트 |
| `StructuredOutputParser` | 원하는 항목을 직접 설계할 때 | `answer`, `source` |
| `JsonOutputParser` | JSON으로 여러 값을 주고받을 때 | 설명과 해시태그 |
| `DatetimeOutputParser` | 날짜 계산·정렬에 쓸 때 | `YYYY-MM-DD` 날짜 객체 |
| `EnumOutputParser` | 답을 정해진 값으로 제한할 때 | 빨강·초록·파랑 중 하나 |

### Pydantic과 Enum 쉽게 보기

- **Pydantic 모델**: “이 결과에는 이름은 글자, 날짜도 글자처럼 이 항목들이 꼭 있어야 해”라고 정한 결과 양식입니다.
- **Enum**: 선택 가능한 답을 미리 정해 두는 목록입니다. 예를 들어 색상은 빨강·초록·파랑만 허용할 수 있습니다.

형식이 맞지 않으면 파서가 오류를 내므로, 틀린 결과를 조용히 다음 단계에 넘기는 일을 줄일 수 있습니다.

## 3. `invoke()`와 `stream()`

- `invoke()`: 답변이 완성된 뒤 한 번에 받습니다. 파싱하거나 저장할 때 알맞습니다.
- `stream()`: 답변 조각이 생기는 대로 받습니다. 사용자에게 긴 답변을 바로 보여 줄 때 알맞습니다.

구조화된 결과를 확실히 처리해야 한다면 보통 `invoke()`가 더 단순합니다.

## 4. Pandas: 표 데이터를 다루는 기본

Pandas의 `DataFrame`은 엑셀 시트처럼 **행과 열로 된 표**입니다. 6-7에서는 Titanic CSV 파일을 표로 읽고, AI 질문과 직접 Pandas 계산을 함께 사용합니다.

```python
import pandas as pd
df = pd.read_csv("./data/titanic.csv")
```

### 꼭 기억할 Pandas 문법

| 코드 | 뜻 |
|---|---|
| `df.head()` | 첫 5행으로 데이터가 제대로 읽혔는지 확인 |
| `df.info()` | 열 이름·자료형·비어 있지 않은 값 확인 |
| `df.shape` | `(행 수, 열 수)` 확인 |
| `df["Age"]` | `Age` 열 하나 선택 |
| `df[["Name", "Sex"]]` | 여러 열 선택 |
| `df[df["Sex"] == "female"]` | 조건에 맞는 행만 선택 |
| `df["Fare"].mean()` | `Fare` 열의 평균 계산 |
| `df.iloc[100:200]` | 위치 100~199행 선택 |

AI에게 표를 질문할 수는 있지만, 평균·합계처럼 중요한 수치는 `mean()` 같은 Pandas 계산으로 한 번 더 확인하는 습관이 안전합니다.

## 실행 전 체크

1. `.env`에 `OPENAI_API_KEY`가 있는가?
2. 프롬프트의 `{question}` 같은 이름과 `invoke({"question": ...})`의 키가 같은가?
3. 파서의 `format_instructions`를 프롬프트에 넣었는가?
4. CSV 경로와 열 이름(`Age`, `Fare` 등)이 실제 파일과 같은가?
5. AI 결과는 특히 숫자·집계 작업에서 Pandas로 검증했는가?

