import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import apiClient from "../api/client";
import { useAuth } from "../context/AuthContext";

const typeLabel = {
  ATM: "ATM",
  TRANSFER: "계좌이체",
  AUTOMATIC_TRANSFER: "자동이체",
  CARD: "카드결제",
  INTEREST: "이자",
};

export default function TransactionDetailPage() {
  const { accountId, transactionId } = useParams();
  const navigate = useNavigate();
  const { logout } = useAuth();

  const [tx, setTx] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const res = await apiClient.get(
          `/account/${accountId}/transactions/${transactionId}/`
        );
        setTx(res.data);
      } catch (err) {
        console.error(err);
        setError("거래 정보를 불러오지 못했습니다.");
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [accountId, transactionId]);

  const handleDelete = async () => {
    if (!window.confirm("이 거래 내역을 삭제할까요?")) return;
    setDeleting(true);
    try {
      await apiClient.delete(
        `/account/${accountId}/transactions/${transactionId}/`
      );
      // 삭제 후 해당 계좌의 거래 목록으로 돌아가기
      navigate(`/accounts/${accountId}/transactions`, { replace: true });
    } catch (err) {
      console.error(err);
      alert("삭제에 실패했습니다.");
      setDeleting(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <span className="app-title">거래 상세</span>
          <span className="app-subtitle">
            한 건의 거래를 자세히 확인하고 삭제할 수 있어요.
          </span>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <Link to={`/accounts/${accountId}/transactions`}>
            <button className="btn-ghost">← 거래 목록으로</button>
          </Link>
          <button className="app-logout-btn" onClick={logout}>
            로그아웃
          </button>
        </div>
      </header>

      <main className="app-main">
        <section className="dashboard-card" style={{ maxWidth: 640 }}>
          {loading ? (
            <p className="dashboard-card-subtitle">불러오는 중...</p>
          ) : error ? (
            <p className="auth-error">{error}</p>
          ) : !tx ? (
            <p className="dashboard-card-subtitle">데이터가 없습니다.</p>
          ) : (
            <>
              <div className="dashboard-card-header">
                <div>
                  <div className="dashboard-card-title">
                    {tx.description || "거래 내역"}
                  </div>
                  <div className="dashboard-card-subtitle">
                    {new Date(tx.transacted_at).toLocaleString()} ·{" "}
                    {typeLabel[tx.transaction_type] ?? tx.transaction_type}
                  </div>
                </div>
                <span
                  className={
                    "transaction-amount " +
                    (tx.is_deposit ? "income" : "expense")
                  }
                >
                  {tx.is_deposit ? "+" : "-"}
                  {tx.amount.toLocaleString()}원
                </span>
              </div>

              <div style={{ marginTop: 10, fontSize: 13 }}>
                <div className="field-group">
                  <span className="field-label">거래 후 잔액</span>
                  <span>{tx.balance.toLocaleString()}원</span>
                </div>

                <div className="field-group">
                  <span className="field-label">거래 타입</span>
                  <span>
                    {typeLabel[tx.transaction_type] ?? tx.transaction_type}
                  </span>
                </div>

                <div className="field-group">
                  <span className="field-label">입금 / 출금</span>
                  <span>{tx.is_deposit ? "입금" : "출금"}</span>
                </div>

                <div className="field-group">
                  <span className="field-label">거래 일시</span>
                  <span>
                    {new Date(tx.transacted_at).toLocaleString()}
                  </span>
                </div>

                <div className="field-group">
                  <span className="field-label">기록 생성일</span>
                  <span>
                    {new Date(tx.created_at).toLocaleString()}
                  </span>
                </div>

                <div className="field-group">
                  <span className="field-label">마지막 수정일</span>
                  <span>
                    {new Date(tx.updated_at).toLocaleString()}
                  </span>
                </div>
              </div>

              <div
                style={{
                  marginTop: 18,
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <button
                  type="button"
                  className="btn-ghost"
                  onClick={() =>
                    navigate(`/accounts/${accountId}/transactions`)
                  }
                >
                  목록으로
                </button>
                <button
                  type="button"
                  className="account-delete-btn"
                  onClick={handleDelete}
                  disabled={deleting}
                >
                  {deleting ? "삭제 중..." : "이 거래 삭제"}
                </button>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}
