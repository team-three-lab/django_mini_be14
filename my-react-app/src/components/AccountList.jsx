import { useEffect, useState } from "react";

function AccountList() {
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/account/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MTQxNDMyLCJpYXQiOjE3NjQxMzk2MzIsImp0aSI6Ijg4NjRlMGE3YjA5MjQ4MDE5ZmNiNWM1ZDFkN2ZjZTdjIiwidXNlcl9pZCI6IjEiLCJuaWNrbmFtZSI6ImRkZGQiLCJlbWFpbCI6ImRhaW5kakBnbWFpbC5jb20iLCJpc19hZG1pbiI6dHJ1ZX0.UDAuDHBqBtKmHq-wGeDuZ1B5y541R25CZTm9nJz4sFo"
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("응답:", data);w

        // DRF pagination 여부 처리
        if (Array.isArray(data)) {
          setAccounts(data);
        } else if (Array.isArray(data.results)) {
          setAccounts(data.results);
        } else {
          setAccounts([]);
        }
      })
      .catch((err) => {
        console.error("계좌 불러오기 실패:", err);
      });
  }, []);

  return (
    <div>
      <h2>내 계좌 목록</h2>
      <ul>
        {accounts.map((acc) => (
          <li key={acc.id} style={{ marginBottom: "10px" }}>
            <strong>{acc.account_name}</strong> <br />
            은행: {acc.bank_code} <br />
            계좌번호: {acc.masked_account_number} <br />
            주계좌 여부: {acc.is_primary ? "예" : "아니오"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AccountList;
