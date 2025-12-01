import { useEffect, useState } from "react";
import apiClient from "../../api/client";
import { Link, useParams } from "react-router-dom";


const typeLabel = {
  ATM: "ATM",
  TRANSFER: "계좌이체",
  AUTOMATIC_TRANSFER: "자동이체",
  CARD: "카드결제",
  INTEREST: "이자",
};

export default function TransactionList({ accountId }) {
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [type, setType] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchTransactions = async (paramsOverride = null) => {
    if (!accountId) return;
    setLoading(true);
    try {
      const params = paramsOverride ?? {};
      const res = await apiClient.get(
        `/account/${accountId}/transactions/`,
        { params }
      );
      setItems(res.data);
    } catch (err) {
      console.error("거래 내역 불러오기 실패", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (accountId) fetchTransactions();
  }, [accountId]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    const params = {};
    if (search) params.search = search;
    if (type) params.type = type;
    fetchTransactions(params);
  };

  if (!accountId) {
    return (
      <p className="dashboard-card-subtitle">
        왼쪽에서 계좌를 먼저 선택해 주세요.
      </p>
    );
  }

  return (
    <div>
      <form
        className="card-filter-row"
        onSubmit={handleSearchSubmit}
        style={{ marginBottom: 10 }}
      >
        <input
          className="field-input"
          placeholder="설명으로 검색 (예: 편의점)"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="field-select"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="">전체 타입</option>
          {Object.entries(typeLabel).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
        <button type="submit" className="btn-ghost">
          검색
        </button>
      </form>

      {loading ? (
        <p className="dashboard-card-subtitle">불러오는 중...</p>
      ) : (
    <ul className="transaction-list">
      {items.map((tx) => (
        <li key={tx.id} className="transaction-item">
          <div className="transaction-main">
            <span className="transaction-date">
              {new Date(tx.transacted_at).toLocaleString()}
            </span>
            <span className="transaction-desc">
              {tx.description}
              <span className="transaction-tag">
                {typeLabel[tx.transaction_type] ?? tx.transaction_type}
              </span>
            </span>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <span
              className={
                "transaction-amount " +
                (tx.is_deposit ? "income" : "expense")
              }
            >
              {tx.is_deposit ? "+" : "-"}
              {tx.amount.toLocaleString()}원
            </span>

            <Link
              to={`/accounts/${accountId}/transactions/${tx.id}`}
              style={{ textDecoration: "none" }}
            >
              <button type="button" className="btn-ghost">
                상세
              </button>
            </Link>
          </div>
        </li>
      ))}
          {items.length === 0 && (
            <li className="dashboard-card-subtitle">
              거래 내역이 없습니다.
            </li>
          )}
        </ul>
      )}
    </div>
  );
}
