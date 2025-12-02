import { useEffect, useState } from "react";
import apiClient from "../../api/client";

export default function AccountList({ onSelectAccount }) {
  const [accounts, setAccounts] = useState([]);
  const [search, setSearch] = useState("");
  const [bank, setBank] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchAccounts = async (paramsOverride = null) => {
    setLoading(true);
    try {
      const params = paramsOverride ?? {};
      const res = await apiClient.get("/account/", { params });
      setAccounts(res.data);
    } catch (err) {
      console.error("계좌 목록 불러오기 실패", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // 최초 로딩
    fetchAccounts();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    const params = {};
    if (search) params.search = search;
    if (bank) params.bank = bank;
    fetchAccounts(params);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("정말 이 계좌를 삭제할까요?")) return;
    try {
      await apiClient.delete(`/account/${id}`);
      setAccounts((prev) => prev.filter((acc) => acc.id !== id));
    } catch (err) {
      console.error(err);
      alert("삭제에 실패했습니다.");
    }
  };

  return (
    <div>
      {/* 여기서 제목 + 필터 같이 보여줄 거라
          AccountsPage 쪽에서는 그냥 <AccountList />만 렌더하면 됨 */}
      <form
        className="card-filter-row"
        onSubmit={handleSearchSubmit}
        style={{ marginBottom: 10 }}
      >
        <input
          className="field-input"
          placeholder="계좌명/번호 검색"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="field-select"
          value={bank}
          onChange={(e) => setBank(e.target.value)}
        >
          <option value="">전체 은행</option>
          <option value="004">국민은행</option>
          <option value="088">신한은행</option>
          <option value="081">하나은행</option>
          <option value="020">우리은행</option>
          <option value="011">농협은행</option>
          <option value="090">카카오뱅크</option>
          <option value="089">케이뱅크</option>
          <option value="092">토스뱅크</option>
        </select>
        <button type="submit" className="btn-ghost">
          검색
        </button>
      </form>

      {loading ? (
        <p className="dashboard-card-subtitle">불러오는 중...</p>
      ) : (
        <ul className="account-list">
          {accounts.map((acc) => (
            <li
              key={acc.id}
              className="account-item"
              onClick={() => onSelectAccount?.(acc)}
            >
              <div className="account-main">
                <div className="account-name-row">
                  <span className="account-name">{acc.account_name}</span>
                  {acc.is_primary && (
                    <span className="account-chip-primary">주계좌</span>
                  )}
                </div>
                <span className="account-sub">
                  {(acc.bank_name ?? acc.bank_code) +
                    " · " +
                    acc.masked_account_number}
                </span>
              </div>
              <button
                className="account-delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(acc.id);
                }}
              >
                삭제
              </button>
            </li>
          ))}
          {accounts.length === 0 && (
            <li className="dashboard-card-subtitle">
              등록된 계좌가 없습니다.
            </li>
          )}
        </ul>
      )}
    </div>
  );
}
