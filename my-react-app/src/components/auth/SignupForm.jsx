import { useState } from "react";
import apiClient from "../../api/client";

export default function SignupForm({ onSuccess }) {
  const [form, setForm] = useState({
    email: "",
    nickname: "",
    name: "",
    phone_number: "",
    password: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await apiClient.post("/auth/signup/", form);
      if (onSuccess) onSuccess();
    } catch (err) {
      console.error(err);
      setError("회원가입에 실패했습니다. 입력값을 다시 확인해 주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <div>
        <label className="auth-label">이메일</label>
        <input
          type="email"
          name="email"
          className="auth-input"
          value={form.email}
          onChange={handleChange}
          placeholder="you@example.com"
          required
        />
      </div>

      <div>
        <label className="auth-label">닉네임</label>
        <input
          type="text"
          name="nickname"
          className="auth-input"
          value={form.nickname}
          onChange={handleChange}
          placeholder="가계부에서 쓸 이름"
          required
        />
      </div>

      <div>
        <label className="auth-label">이름</label>
        <input
          type="text"
          name="name"
          className="auth-input"
          value={form.name}
          onChange={handleChange}
          placeholder="실제 이름"
          required
        />
      </div>

      <div>
        <label className="auth-label">전화번호</label>
        <input
          type="tel"
          name="phone_number"
          className="auth-input"
          value={form.phone_number}
          onChange={handleChange}
          placeholder="010-0000-0000"
          required
        />
      </div>

      <div>
        <label className="auth-label">비밀번호</label>
        <input
          type="password"
          name="password"
          className="auth-input"
          value={form.password}
          onChange={handleChange}
          placeholder="최소 8자리 이상"
          required
        />
      </div>

      {error && <p className="auth-error">{error}</p>}

      <button type="submit" disabled={loading} className="auth-button">
        {loading ? "가입 중..." : "회원가입"}
      </button>
    </form>
  );
}
