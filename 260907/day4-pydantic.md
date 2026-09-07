### 1. Pydantic BaseModel: 데이터 형식 정의하고 자동 검증하기

핵심 개념

- `BaseModel`: 데이터의 구조와 타입을 정의하는 Pydantic 기본 클래스
- `id: int`, `name: str`: 각 데이터가 어떤 타입이어야 하는지 지정
- `User(**external_data)`: 딕셔너리 데이터를 `User` 모델로 변환
- Pydantic은 가능한 경우 문자열을 숫자나 날짜 타입으로 자동 변환
- `PositiveInt`: 0보다 큰 정수만 허용
- `datetime | None`: 날짜 또는 `None`을 허용
- 입력 데이터를 정해진 형식으로 검사하고 변환할 때 활용


### 2. Pydantic Validation: 잘못된 데이터 검증하기

핵심 개념

- `ValidationError`: 데이터가 지정한 조건에 맞지 않을 때 발생하는 오류
- `try / except`: 검증 오류가 발생해도 프로그램이 종료되지 않도록 처리
- `e.errors()`: 어떤 항목에서 오류가 발생했는지 확인
- `Literal['red', 'green']`: 정해진 값만 입력 가능
- `Annotated[float, Gt(0)]`: 0보다 큰 실수만 허용
- 복잡한 `dict`, `list`, `tuple` 구조도 타입을 지정해 검증 가능


### 3. Pydantic model_dump: 데이터를 딕셔너리나 JSON으로 변환하기

핵심 개념

- `model_dump()`: Pydantic 객체를 딕셔너리로 변환
- `exclude_unset=True`: 직접 입력하지 않은 값은 제외
- `exclude={'where'}`: 특정 항목을 결과에서 제외
- `mode='json'`: JSON에서 사용할 수 있는 형태로 변환
- `model_dump_json()`: 데이터를 JSON 문자열로 변환
- API 응답이나 데이터 저장을 위해 객체를 변환할 때 활용


### 4. Pydantic Type Conversion: 입력값 자동 변환하기

핵심 개념

- `age: int`: `age`를 정수형으로 사용한다고 지정
- `age="25"`: 문자열 `"25"`도 가능한 경우 정수 `25`로 자동 변환
- `type(user.age)`: 실제 변환된 자료형 확인
- 외부에서 들어온 데이터를 원하는 타입으로 정리할 때 활용


### 5. Field / Optional / Nested Model: 세부 조건과 중첩 데이터 만들기

핵심 개념

- `Field()`: 데이터에 추가적인 검증 조건 설정
- `ge=0`: 0 이상만 허용
- `le=150`: 150 이하만 허용
- `str | None = None`: 값이 없어도 되는 선택 항목
- `address: Address`: 다른 Pydantic 모델을 내부에 포함
- 딕셔너리로 입력한 데이터도 자동으로 내부 모델로 변환
- 복잡한 데이터를 구조적으로 관리할 때 활용


### 6. API Request Validation: 요청 데이터 검증하기

핵심 개념

- `SignupRequest`: 회원가입 요청 데이터의 형식을 정의
- `min_length=3`: 최소 3글자 이상
- `max_length=20`: 최대 20글자 이하
- `Field(min_length=8)`: 비밀번호 최소 8글자
- `Field(ge=14)`: 나이 14 이상
- `signup(data: SignupRequest)`: 검증이 끝난 데이터만 함수에서 사용
- API에 잘못된 데이터가 들어오는 것을 미리 막을 때 활용