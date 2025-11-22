# 📌 Django 가계부 시스템 프로젝트

> Django + DRF + PostgreSQL 기반의 기록 중심 가계부 웹 서비스
사용자는 계좌 관리, 입출금 기록 관리, 소비 분석 기능을 이용할 수 있습니다.

## ✨ 프로젝트 개요
이 프로젝트는 개인 소비 관리를 위한 가계부 시스템입니다.
사용자는 계좌를 등록하고, 입금·출금 내역을 기록하며,
소비 데이터를 조회·분석할 수 있는 API 기반 백엔드 서비스를 제공합니다.

## 🚀 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| Backend Framework | Django, Django REST Framework |
| ORM | Django ORM |
| DB | PostgreSQL |
| Auth | JWT 인증 |
| Background Task (도전) | Celery + Redis |
| Docs | Swagger / drf-spectacular (예정) |
| VCS | Git / GitHub |
| Dependency 관리 | Poetry |

## 📂 프로젝트 구조

```
project_root/
 ┣ accounts/
 ┣ transactions/
 ┣ users/
 ┣ config/
 ┣ README.md
 ┗ pyproject.toml
```

## 🧠 주요 기능

### 👤 사용자 인증
- 회원가입
- 로그인 / 로그아웃 (JWT)
- Django Admin 기반 관리

### 💰 계좌(Account) 기능

| 기능 | 설명 |
|------|------|
| ✔ 계좌 생성 | 계좌를 신규 등록 |
| ✔ 계좌 조회 | 사용자 전체 계좌 조회 |
| ✔ 계좌 삭제 | 계좌 삭제 |

### 🔁 거래내역(Transaction) 기능

| 기능 | 설명 |
|------|------|
| ✔ 거래 생성 | 입금/출금 기록 생성 |
| ✔ 거래 조회 | 전체/단일 조회 |
| ✔ 거래 수정 | 금액/타입/설명 수정 |
| ✔ 거래 삭제 | 특정 거래 삭제 |

### 🔍 거래 필터링
- 날짜별, 계좌별, 타입별 필터링 가능

### 📊 (도전) 소비 분석 기능
- 주간/월간 소비 분석
- 시각화 JSON 제공

### 🕒 (도전) Celery 기반 스케줄링
- 자동 리포트 생성

### 🔔 (도전) 알림 기능
- 특정 소비 조건 시 알림

## 🗂 ERD
```

```

## 🛠 개발 단계 로드맵

### 1단계 — 개발/협업 환경 준비
- Poetry, Git 전략, 프로젝트 구조 설정

### 2단계 — ERD 설계 & 모델 구축
- Users / Accounts / Transactions 모델

### 3단계 — API 개발
- 인증 + 계좌 + 거래내역 CRUD

### 4~5단계 — (도전)
- Celery 활용 자동 통계, 알림 기능

### 6단계 — 배포
- AWS 등 배포 환경 세팅 예정

## 🔧 설치 & 실행

### 1) 클론
```
git clone <repo_url>
cd django_mini_be14
```

### 2) Poetry
```
poetry install
poetry shell
```

### 3) Django 실행
```
python manage.py migrate
python manage.py runserver
```

## 🤝 협업 규칙

### Branch 전략
| 브랜치 | 설명 |
|--------|------|
| main | 배포 |
| develop | 통합 |
| feature/* | 기능 단위 |

### Commit 컨벤션
```
✨ feat: 기능 추가
🐛 fix: 버그 수정
📝 docs: 문서 변경
🎨 style: 포맷팅
🔨 refactor: 리팩토링
🧪 test: 테스트
🔧 chore: 기타 설정
```

## 👥 팀 구성

| 이름 | 역할 |
|------|------|
| 최건희 | 프로젝트 총괄 / DB 및 구조 설계 / 환경설정 / README |
| 김준호 | 계좌 API |
| 이성현 | 거래내역 CRUD / Admin |
| 김재진 | 권한 / JWT인증 |
| 조우석 | Celery·알림 담당 |

## 🌱 회고


## 📞 Contact

| 항목 | 정보 |
|------|------|
GitHub | https://github.com/oz-union-be-14-team3
Email | 
