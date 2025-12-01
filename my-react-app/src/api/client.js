import axios from "axios";

// PROD / DEV 구분
const isProd = import.meta.env.PROD;

// 1) env에서 읽고, 없으면 PROD/DEV에 따라 기본값
const rawBase =
  import.meta.env.VITE_API_BASE_URL ??
  (isProd ? "" : "http://localhost:8000");

// 2) 끝에 붙은 /는 전부 제거해서 "//api" 안 나오게
const API_BASE_URL = rawBase.replace(/\/+$/, "");

// 👉 여기서 /api 까지 붙여준다
export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`, // PROD: "/api", DEV: "http://localhost:8000/api"
  withCredentials: false,
});

// 요청 인터셉터: 로컬스토리지에서 access token 꺼내서 Authorization 헤더 붙이기
apiClient.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem("access");
    if (access) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
