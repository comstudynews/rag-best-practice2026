# DEMO-RAG-2026 네트워크 요구사항

외부 서비스 연결에는 TCP 443 포트를 사용한다.
프록시 환경에서는 HTTPS 통신에 대한 프록시 예외 또는 인증 설정이 필요할 수 있다.

교육용 예시 도메인:

- api.demo-rag-2026.example
- auth.demo-rag-2026.example
- update.demo-rag-2026.example

ERR-NET-403은 클라이언트가 인증 서버에 연결하지 못할 때 발생한다.
주요 원인은 방화벽 차단, 프록시 인증 실패, DNS 해석 실패이다.

진단 순서:

1. DNS 확인
2. TCP 443 연결 확인
3. 프록시 설정 확인
4. 조직 방화벽 정책 확인
