import { useParams, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import TransactionList from "../components/transactions/TransactionList";
import TransactionForm from "../components/transactions/TransactionForm";

export default function TransactionsPage() {
  const { accountId } = useParams();
  const { logout } = useAuth();

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <span className="app-title">거래 내역</span>
          <span className="app-subtitle">
            계좌 ID {accountId}의 거래 흐름을 확인할 수 있어요.
          </span>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <Link to="/accounts">
            <button className="btn-ghost">← 계좌 목록으로</button>
          </Link>
          <button className="app-logout-btn" onClick={logout}>
            로그아웃
          </button>
        </div>
      </header>

      <main className="app-main">
        <div className="dashboard-column">
          <section className="dashboard-card">
            <div className="dashboard-card-header">
              <div>
                <div className="dashboard-card-title">거래 내역</div>
                <div className="dashboard-card-subtitle">
                  검색과 필터로 원하는 거래만 골라볼 수 있어요.
                </div>
              </div>
            </div>
            <TransactionList accountId={Number(accountId)} />
          </section>

          <section className="dashboard-card">
            <div className="dashboard-card-header">
              <div>
                <div className="dashboard-card-title">새 거래 등록</div>
              </div>
            </div>
            <TransactionForm accountId={Number(accountId)} />
          </section>
        </div>
      </main>
    </div>
  );
}
