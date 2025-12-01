import { useState } from "react";
import { Link } from "react-router-dom";              // ✅ 추가
import { useAuth } from "../context/AuthContext";
import AccountList from "../components/accounts/AccountList";
import AccountForm from "../components/accounts/AccountForm";
import TransactionList from "../components/transactions/TransactionList";
import TransactionForm from "../components/transactions/TransactionForm";

export default function AccountsPage() {
  const { logout } = useAuth();
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleAccountCreated = () => {
    // 단순히 키를 변경해서 AccountList가 다시 fetch하도록
    setRefreshKey((k) => k + 1);
  };

  const handleTransactionCreated = () => {
    // 필요하면 여기서도 트랜잭션 리스트 리프레시 트리거 가능
    setRefreshKey((k) => k + 1);
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <span className="app-title">나만의 가계부</span>
          <span className="app-subtitle">
            계좌별로 소비 패턴을 한눈에 살펴보세요 
          </span>
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          {/*  소비 분석 페이지로 이동 버튼 */}
          <Link to="/analysis">
            <button className="btn-ghost">소비 분석</button>
          </Link>

          <button className="app-logout-btn" onClick={logout}>
            <span>로그아웃</span>
          </button>
        </div>
      </header>

      <main className="app-main">
        <div className="dashboard-grid">
          {/* 왼쪽: 계좌 폼 + 목록 */}
          <div className="dashboard-column">
            <section className="dashboard-card">
              <div className="dashboard-card-header">
                <div>
                  <div className="dashboard-card-title">새 계좌 등록</div>
                  <div className="dashboard-card-subtitle">
                    자주 쓰는 계좌일수록 주계좌로 설정해두면 좋아요.
                  </div>
                </div>
              </div>
              <AccountForm onCreated={handleAccountCreated} />
            </section>

            <section className="dashboard-card">
              <div className="dashboard-card-header">
                <div>
                  <div className="dashboard-card-title">내 계좌 목록</div>
                  <div className="dashboard-card-subtitle">
                    계좌를 클릭하면 오른쪽에서 거래 내역을 볼 수 있어요.
                  </div>
                </div>
              </div>
              <AccountList
                key={refreshKey}
                onSelectAccount={setSelectedAccount}
              />
            </section>
          </div>

          {/* 오른쪽: 선택 계좌 거래 리스트 + 등록 폼 */}
          <div className="dashboard-column">
            <section className="dashboard-card">
              <div className="dashboard-card-header">
                <div>
                  <div className="dashboard-card-title">
                    {selectedAccount
                      ? `${selectedAccount.account_name} 거래 내역`
                      : "계좌를 먼저 선택해 주세요"}
                  </div>
                  <div className="dashboard-card-subtitle">
                    최근 거래부터 순서대로 보여드려요.
                  </div>
                </div>
              </div>
              <TransactionList
                key={selectedAccount?.id ?? "no-account"}
                accountId={selectedAccount?.id}
              />
            </section>

            <section className="dashboard-card">
              <div className="dashboard-card-header">
                <div>
                  <div className="dashboard-card-title">새 거래 등록</div>
                  <div className="dashboard-card-subtitle">
                    월급, 카드값, 이체 등 실제 흐름 그대로 기록해두면 좋아요.
                  </div>
                </div>
              </div>
              <TransactionForm
                accountId={selectedAccount?.id}
                onCreated={handleTransactionCreated}
              />
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
