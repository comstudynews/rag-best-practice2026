# AsterDesk 백업 및 복구

로컬 백업은 기본적으로 매일 오전 2시에 수행한다.
Windows 기본 백업 경로는 `C:\ProgramData\AsterDesk\backup\`이다.
Linux 기본 백업 경로는 `/var/lib/asterdesk/backup/`이다.

기본 보관 기간은 14일이다.
관리자는 정책 설정에서 보관 기간을 최대 90일까지 변경할 수 있다.

복구 전에 AsterDesk 서비스를 중지해야 한다.
복구 완료 후 서비스를 다시 시작하고 데이터 무결성 검사를 수행한다.
