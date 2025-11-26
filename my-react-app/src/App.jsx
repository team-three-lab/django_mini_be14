// src/App.jsx
import AccountList from "./components/AccountList";
import TransactionList from "./components/TransactionList";

function App() {
  return (
    <div className="app-container">
      <h1>가계부 대시보드</h1>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "24px" }}>
        <AccountList />
        <TransactionList />
      </div>
    </div>
  );
}

export default App;
