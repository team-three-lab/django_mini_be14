import { useEffect, useState } from "react";
import apiClient from "../../api/client";

const periodLabel = {
  DAILY: "일간",
  WEEKLY: "주간",
  MONTHLY: "월간",
  YEARLY: "연간",
};

export default function AnalysisList({
  selectedId,
  onSelect,
  onEdit,
  onDeleted,
}) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchAnalyses = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get("/analysis/");
      setItems(res.data);
    } catch (err) {
      console.error("분석 목록 불러오기 실패", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("이 분석 프리셋을 삭제할까요?")) return;
    try {
      await apiClient.delete(`/analysis/${id}/`);
      setItems((prev) => prev.filter((it) => it.id !== id));
      onDeleted?.();
    } catch (err) {
      console.error(err);
      alert("삭제에 실패했습니다.");
    }
  };

  if (loading) {
    return (
      <p className="dashboard-card-subtitle">분석 목록을 불러오는 중...</p>
    );
  }

  if (items.length === 0) {
    return (
      <p className="dashboard-card-subtitle">
        아직 저장된 분석이 없습니다. 오른쪽에서 새 분석을 만들어 보세요.
      </p>
    );
  }

  return (
    <ul className="analysis-list">
      {items.map((item) => {
        const isActive = item.id === selectedId;
        const period = periodLabel[item.period] ?? item.period;
        const start = item.start_date?.slice(0, 10);
        const end = item.end_date?.slice(0, 10);

        return (
          <li
            key={item.id}
            className={
              "analysis-item" + (isActive ? " analysis-item-active" : "")
            }
            onClick={() => onSelect?.(item.id)}
          >
            <div className="analysis-main">
              <div className="analysis-title-row">
                <span className="analysis-title">
                  {item.description || "분석 " + item.id}
                </span>
                <span className="analysis-chip">
                  {item.is_income ? "수입" : "지출"} · {period}
                </span>
              </div>
              <div className="analysis-meta">
                기간: {start} ~ {end}
              </div>
            </div>
            <div className="analysis-actions">
              <button
                type="button"
                className="btn-ghost"
                onClick={(e) => {
                  e.stopPropagation();
                  onEdit?.(item);
                }}
              >
                수정
              </button>
              <button
                type="button"
                className="account-delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(item.id);
                }}
              >
                삭제
              </button>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
