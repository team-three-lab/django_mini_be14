import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import AccountsPage from "./pages/AccountsPage";
import TransactionsPage from "./pages/TransactionsPage";
import TransactionDetailPage from "./pages/TransactionDetailPage";
import AnalysisPage from "./pages/AnalysisPage";

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* 인증 필요 없는 페이지 */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />

          {/* 계좌 목록 */}
          <Route
            path="/accounts"
            element={
              <PrivateRoute>
                <AccountsPage />
              </PrivateRoute>
            }
          />

          {/* 계좌별 거래 목록 */}
          <Route
            path="/accounts/:accountId/transactions"
            element={
              <PrivateRoute>
                <TransactionsPage />
              </PrivateRoute>
            }
          />

          {/* 거래 상세 */}
          <Route
            path="/accounts/:accountId/transactions/:transactionId"
            element={
              <PrivateRoute>
                <TransactionDetailPage />
              </PrivateRoute>
            }
          />

          {/* 소비 분석 페이지 */}
          <Route
            path="/analysis"
            element={
              <PrivateRoute>
                <AnalysisPage />
              </PrivateRoute>
            }
          />

          {/* 기본은 로그인으로 리다이렉트 */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
