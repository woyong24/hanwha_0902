### 4. Exception Handling: 잘못된 입력 처리하기

핵심 개념

- `strip()`: 문자열 앞뒤 공백 제거
- `if not cleaned`: 입력값이 비어 있는지 확인
- `raise ValueError(...)`: 잘못된 입력이면 직접 오류 발생
- `try`: 오류가 발생할 수 있는 코드 실행
- `except ValueError`: `ValueError`가 발생했을 때 처리
- `cleaned[:max_length]`: 문자열을 최대 길이까지만 잘라서 사용
- 잘못된 입력이 들어와도 프로그램이 바로 종료되지 않도록 처리할 때 활용

### 5. Function + Loop: 여러 질문을 반복해서 처리하기

핵심 개념

- `def`: 특정 작업을 수행하는 함수 만들기
- `list[str]`: 문자열 여러 개가 들어가는 리스트라는 타입 힌트
- `list[dict[str, str]]`: 딕셔너리 여러 개를 담은 리스트라는 타입 힌트
- `enumerate()`: 리스트의 값과 번호를 함께 가져오기
- `start=1`: 번호를 `1`부터 시작
- `append()`: 처리 결과를 리스트에 추가
- `try / except`: 정상 질문과 잘못된 질문을 구분해서 처리
- `"ready"` / `"invalid"`: 질문의 처리 상태를 표시
- 여러 개의 데이터를 하나씩 검사하고 결과를 정리할 때 활용