// src/components/TransactionList.jsx
function TransactionList() {
  const dummyTransactions = [
    { id: 1, description: "점심 식사", amount: -8000 },
    { id: 2, description: "월급", amount: 2000000 },
  ];

  return (
    <div>
      <h2>거래 내역</h2>
      <ul>
        {dummyTransactions.map((tx) => (
          <li key={tx.id}>
            {tx.description} ({tx.amount.toLocaleString()}원)
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TransactionList;