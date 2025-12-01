import { useEffect, useState } from "react";
import apiClient from "../../api/client";

const periodOptions = [
  { value: "DAILY", label: "일간" },
  { value: "WEEKLY", label: "주간" },
  { value: "MONTHLY", label: "월간" },
  { value: "YEARLY", label: "연간" },
];

export default function AnalysisForm({ analysis, onDone }) {
  const [accounts, setAccounts] = useState([]);
  const [loadingAccounts, setLoadingAccounts] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const [form, setForm] = useState({
    account: "",
    is_income: true,
    period: "MONTHLY",
    start_date: "",
    end_date: "",
    description: "",
  });

  useEffect(() => {
    // 계좌 목록 불러오기
    const fetchAccounts = async () => {
      setLoadingAccounts(true);
      try {
        const res = await apiClient.get("/account/");
        setAccounts(res.data);
      } catch (err) {
        console.error("계좌 목록 로딩 실패", err);
      } finally {
        setLoadingAccounts(false);
      }
    };
    fetchAccounts();
  }, []);

  useEffect(() => {
    if (!analysis) {
      setForm((prev) => ({
        ...prev,
        description: "",
      }));
      return;
    }
    setForm({
      account: analysis.account,
      is_income: analysis.is_income,
      period: analysis.period,
      start_date: analysis.start_date?.slice(0, 10) || "",
      end_date: analysis.end_date?.slice(0, 10) || "",
      description: analysis.description || "",
    });
  }, [analysis]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "is_income") {
      setForm((prev) => ({ ...prev, is_income: value === "income" }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);

    const payload = {
      account: form.account,
      is_income: form.is_income,
      period: form.period,
      start_date: form.start_date
        ? form.start_date + "T00:00:00"
        : null,
      end_date: form.end_date
        ? form.end_date + "T23:59:59"
        : null,
      description: form.description,
      result_image: "FRONT_CHART", // 일단 placeholder 값
    };

    try {
      let res;
      if (analysis) {
        res = await apiClient.put(`/analysis/${analysis.id}/`, payload);
      } else {
        res = await apiClient.post("/analysis/", payload);
      }
      onDone?.(res.data);
    } catch (err) {
      console.error(err);
      if (err.response?.data) {
        setError(JSON.stringify(err.response.data));
      } else {
        setError("저장 중 오류가 발생했습니다.");
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="analysis-form" onSubmit={handleSubmit}>
      {error && <p className="auth-error">{error}</p>}

      <div className="analysis-form-grid">
        <div className="field-group">
          <label className="field-label">계좌</label>
          {loadingAccounts ? (
            <p className="dashboard-card-subtitle">계좌 불러오는 중...</p>
          ) : (
            <select
              name="account"
              className="field-select"
              value={form.account}
              onChange={handleChange}
              required
            >
              <option value="">계좌 선택</option>
              {accounts.map((acc) => (
                <option key={acc.id} value={acc.id}>
                  {acc.account_name} ({acc.masked_account_number})
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="field-group">
          <label className="field-label">분석 대상</label>
          <select
            name="is_income"
            className="field-select"
            value={form.is_income ? "income" : "expense"}
            onChange={handleChange}
          >
            <option value="income">수입</option>
            <option value="expense">지출</option>
          </select>
        </div>

        <div className="field-group">
          <label className="field-label">분석 기간 타입</label>
          <select
            name="period"
            className="field-select"
            value={form.period}
            onChange={handleChange}
          >
            {periodOptions.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </div>

        <div className="field-group">
          <label className="field-label">시작 날짜</label>
          <input
            type="date"
            name="start_date"
            className="field-input"
            value={form.start_date}
            onChange={handleChange}
            required
          />
        </div>

        <div className="field-group">
          <label className="field-label">종료 날짜</label>
          <input
            type="date"
            name="end_date"
            className="field-input"
            value={form.end_date}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <div className="field-group">
        <label className="field-label">분석 설명</label>
        <input
          name="description"
          className="field-input"
          placeholder="예: 11월 편의점 지출 분석"
          value={form.description}
          onChange={handleChange}
        />
      </div>

      <div style={{ display: "flex", justifyContent: "flex-end", gap: 8 }}>
        <button type="submit" className="btn-primary" disabled={saving}>
          {saving
            ? "저장 중..."
            : analysis
            ? "설정 수정 저장"
            : "새 분석 저장"}
        </button>
      </div>
    </form>
  );
}
