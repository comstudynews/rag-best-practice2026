# AsterDesk 보안 운영 가이드

관리자 계정에는 MFA를 반드시 적용한다.
API Key와 Access Token은 소스 코드나 Git 저장소에 저장하지 않는다.

운영 환경의 비밀정보는 환경변수 또는 승인된 Secret Manager를 사용한다.

로그에는 비밀번호, Access Token, API Key를 기록하지 않는다.
보안 감사 로그는 기본 180일 보관한다.

공용 PC에서는 사용 후 반드시 로그아웃하고 저장된 로그인 정보를 삭제한다.
