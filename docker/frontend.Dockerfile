# docker/frontend.Dockerfile

########## 1단계: Vite 빌드 ##########
FROM node:20-alpine AS build

WORKDIR /app

# 패키지 설치
COPY my-react-app/package*.json ./
RUN npm install

# 소스 복사 후 빌드
COPY my-react-app ./
RUN npm run build

########## 2단계: nginx로 정적 파일 서빙 ##########
FROM nginx:1.27-alpine

# 빌드 결과물을 nginx 기본 html 폴더로 복사
COPY --from=build /app/dist /usr/share/nginx/html

# nginx 설정 덮어쓰기 (아래에서 만들 파일)
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
