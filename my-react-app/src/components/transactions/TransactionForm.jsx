import { useState } from "react";
import apiClient from "../../api/client";

const typeOptions = [
  { value: "ATM", label: "ATM" },
  { value: "TRANSFER", label: "계좌이체" },
  { value: "AUTOMATIC_TRANSFER", label: "자동이체" },
  { value: "CARD", label: "카드결제" },
  { value: "INTEREST", label: "이자" },
];

export default function TransactionForm({ accountId, onCreated }) {
  const [form, setForm] = useState({
    amount: "",
    description: "",
    is_deposit: true,
    transaction_type: "CARD",
    transacted_at: new Date().toISOString().slice(0, 16), // datetime-local
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!accountId) {
    return (
      <p className="dashboard-card-subtitle">
        거래를 등록하려면 먼저 계좌를 선택해 주세요.
      </p>
    );
  }

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
      const payload = {
        amount: Number(form.amount),
        description: form.description,
        is_deposit: form.is_deposit,
        transaction_type: form.transaction_type,
        transacted_at: new Date(form.transacted_at).toISOString(),
      };

      const res = await apiClient.post(
        `/account/${accountId}/transactions/`,
        payload
      );
      onCreated?.(res.data);
      // 필요하면 폼 리셋
    } catch (err) {
      console.error(err);
      setError("거래 등록에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="field-group">
        <label className="field-label">금액</label>
        <input
          name="amount"
          type="number"
          className="field-input"
          value={form.amount}
          onChange={handleChange}
          required
        />
      </div>

      {/* balance 입력칸 삭제 ✅ */}

      <div className="field-group">
        <label className="field-label">설명</label>
        <input
          name="description"
          className="field-input"
          value={form.description}
          onChange={handleChange}
          placeholder="예: 편의점, 월급, 카페 등"
        />
      </div>

      <div className="field-checkbox-row">
        <input
          id="is_deposit"
          type="checkbox"
          name="is_deposit"
          checked={form.is_deposit}
          onChange={handleChange}
        />
        <label htmlFor="is_deposit">입금이면 체크 (해제 시 출금)</label>
      </div>

      <div className="field-group">
        <label className="field-label">거래 타입</label>
        <select
          name="transaction_type"
          className="field-select"
          value={form.transaction_type}
          onChange={handleChange}
        >
          {typeOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div className="field-group">
        <label className="field-label">거래 일시</label>
        <input
          type="datetime-local"
          name="transacted_at"
          className="field-datetime"
          value={form.transacted_at}
          onChange={handleChange}
        />
      </div>

      {error && <p className="auth-error">{error}</p>}

      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? "등록 중..." : "거래 등록"}
      </button>
    </form>
  );
}
