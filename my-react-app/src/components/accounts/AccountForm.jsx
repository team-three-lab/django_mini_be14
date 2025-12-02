import { useState } from "react";
import apiClient from "../../api/client";

export default function AccountForm({ onCreated }) {
  const [form, setForm] = useState({
    account_name: "",
    account_number: "",
    bank_code: "",
    is_primary: false,
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await apiClient.post("/account/", form);
      onCreated?.(res.data);
      setForm({
        account_name: "",
        account_number: "",
        bank_code: "",
        is_primary: false,
      });
    } catch (err) {
      console.error(err);
      setError("계좌 생성에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="field-group">
        <label className="field-label">계좌 이름</label>
        <input
          name="account_name"
          className="field-input"
          value={form.account_name}
          onChange={handleChange}
          placeholder="예: 월급통장, 생활비통장"
          required
        />
      </div>

      <div className="field-group">
        <label className="field-label">계좌 번호</label>
        <input
          name="account_number"
          className="field-input"
          value={form.account_number}
          onChange={handleChange}
          placeholder="숫자와 '-'만 입력"
          required
        />
      </div>

      <div className="field-group">
        <label className="field-label">은행</label>
        <select
          name="bank_code"
          className="field-select"
          value={form.bank_code}
          onChange={handleChange}
          required
        >
          <option value="">은행 선택</option>
          <option value="004">국민은행</option>
          <option value="088">신한은행</option>
          <option value="081">하나은행</option>
          <option value="020">우리은행</option>
          <option value="011">농협은행</option>
          <option value="090">카카오뱅크</option>
          <option value="089">케이뱅크</option>
          <option value="092">토스뱅크</option>
        </select>
      </div>

      <div className="field-checkbox-row">
        <input
          id="is_primary"
          type="checkbox"
          name="is_primary"
          checked={form.is_primary}
          onChange={handleChange}
        />
        <label htmlFor="is_primary">이 계좌를 주계좌로 설정</label>
      </div>

      {error && <p className="auth-error">{error}</p>}

      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? "추가 중..." : "계좌 추가"}
      </button>
    </form>
  );
}
