class TextService:

    # 객체를 만들 때 최대 글자 수를 설정
    def __init__(self, max_length: int = 100) -> None:
        self.max_length = max_length

    # 입력된 문자열을 정리하고 최대 길이까지만 반환
    def summarize(self, text: str) -> str:
        cleaned = text.strip()

        # 빈 문자열이면 에러 발생
        if not cleaned:
            raise ValueError("본문을 입력하세요.")

        # 설정한 max_length만큼 문자열을 잘라서 반환
        return cleaned[: self.max_length]


# max_length를 20으로 설정한 객체 생성
service = TextService(max_length=20)

# summarize() 메서드 실행
print(service.summarize("클래스는 데이터와 동작을 함께 관리합니다."))

# 결과
# 클래스는 데이터와 동작을 함께 관리합니다.