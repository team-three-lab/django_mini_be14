import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AnalysisList from "../components/analysis/AnalysisList";
import AnalysisForm from "../components/analysis/AnalysisForm";
import AnalysisResultPanel from "../components/analysis/AnalysisResultPanel";

export default function AnalysisPage() {
  const { logout } = useAuth();
  const [selectedId, setSelectedId] = useState(null);
  const [editingAnalysis, setEditingAnalysis] = useState(null);
  const [reloadKey, setReloadKey] = useState(0); // 목록 다시 로딩 트리거

  const handleCreatedOrUpdated = (analysis) => {
    setReloadKey((k) => k + 1); // 목록 리프레시
    setSelectedId(analysis.id);
    setEditingAnalysis(null);
  };

  const handleCreateNew = () => {
    setEditingAnalysis(null);
    setSelectedId(null);
  };

  const handleEdit = (analysis) => {
    setEditingAnalysis(analysis);
    setSelectedId(analysis.id);
  };

  const handleDeleted = () => {
    setReloadKey((k) => k + 1);
    setSelectedId(null);
    setEditingAnalysis(null);
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <span className="app-title">소비 분석</span>
          <span className="app-subtitle">
            기간·계좌·입출금 조건을 저장해 두고, 언제든지 다시 분석해볼 수 있어요.
          </span>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <Link to="/accounts">
            <button className="btn-ghost">← 가계부로</button>
          </Link>
          <button className="app-logout-btn" onClick={logout}>
            로그아웃
          </button>
        </div>
      </header>

      <main className="app-main">
        <section className="dashboard-card">
          <div className="dashboard-card-header">
            <div>
              <div className="dashboard-card-title">분석 프리셋 목록</div>
              <div className="dashboard-card-subtitle">
                자주 보는 분석 설정을 저장해 두고, 클릭 한 번으로 다시 실행해 보세요.
              </div>
            </div>
            <button className="btn-ghost" onClick={handleCreateNew}>
              + 새 분석 만들기
            </button>
          </div>

          <AnalysisList
            key={reloadKey}
            selectedId={selectedId}
            onSelect={setSelectedId}
            onEdit={handleEdit}
            onDeleted={handleDeleted}
          />
        </section>

        <section className="dashboard-card">
          <div className="dashboard-card-header">
            <div>
              <div className="dashboard-card-title">
                {editingAnalysis ? "분석 설정 수정" : "분석 설정"}
              </div>
              <div className="dashboard-card-subtitle">
                계좌·기간·입출금 조건을 선택하고 분석을 실행해 보세요.
              </div>
            </div>
          </div>

          <AnalysisForm
            analysis={editingAnalysis}
            onDone={handleCreatedOrUpdated}
          />

          <hr className="card-divider" />

          <AnalysisResultPanel analysisId={selectedId} />
        </section>
      </main>
    </div>
  );
}
