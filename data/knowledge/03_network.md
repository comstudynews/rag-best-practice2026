# AsterDesk 네트워크 요구사항

AsterDesk는 외부 서비스 연결을 위해 TCP 443 포트를 사용한다.
프록시 환경에서는 HTTPS 통신에 대한 프록시 예외 또는 인증 설정이 필요할 수 있다.

클라이언트는 다음 도메인에 접근할 수 있어야 한다.

- api.asterdesk.example
- auth.asterdesk.example
- update.asterdesk.example

ERR-NET-403은 클라이언트가 인증 서버에 연결하지 못할 때 발생한다.
주요 원인은 방화벽 차단, 프록시 인증 실패, DNS 해석 실패이다.

진단 순서:

1. DNS 확인
2. TCP 443 연결 확인
3. 프록시 설정 확인
4. 조직 방화벽 정책 확인
