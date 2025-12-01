import { Link } from "react-router-dom";
import SignupForm from "../components/auth/SignupForm";

export default function SignupPage() {
  return (
    <div className="auth-layout">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title">회원가입</h1>
          <p className="auth-subtitle">
            이메일 한 번만 등록해두면, 어디서든 가계부를 이어서 볼 수 있어요 📒
          </p>
        </div>

        <SignupForm onSuccess={() => alert("회원가입 완료! 로그인 해주세요 :)")} />

        <p className="auth-footnote">
          이미 계정이 있다면{" "}
          <Link to="/login" className="auth-link">
            로그인 하러가기
          </Link>
        </p>
      </div>
    </div>
  );
}
