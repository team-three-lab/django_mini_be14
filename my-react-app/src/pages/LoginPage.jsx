import { useNavigate, Link } from "react-router-dom";
import LoginForm from "../components/auth/LoginForm";

export default function LoginPage() {
  const navigate = useNavigate();

  return (
    <div className="auth-layout">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title">나만의 가계부</h1>
          <p className="auth-subtitle">오늘 소비, 내일은 더 잘 쓰자 💸</p>
        </div>

        <LoginForm onSuccess={() => navigate("/accounts")} />

        <p className="auth-footnote">
          아직 계정이 없다면{" "}
          <Link to="/signup" className="auth-link">
            회원가입 하러가기
          </Link>
        </p>
      </div>
    </div>
  );
}
