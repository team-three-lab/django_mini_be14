import { useEffect, useState } from "react";
import apiClient from "../../api/client";

function BarList({ title, data }) {
  const entries = Object.entries(data || {});
  if (entries.length === 0) {
    return null;
  }
  const maxVal = Math.max(...entries.map(([, v]) => v || 0));

  return (
    <div className="analysis-chart-block">
      <div className="analysis-chart-title">{title}</div>
      <div className="analysis-chart-list">
        {entries.map(([label, value]) => {
          const width =
            maxVal > 0 ? Math.round((value / maxVal) * 100) : 0;
          return (
            <div key={label} className="analysis-chart-row">
              <span className="analysis-chart-label">{label}</span>
              <div className="analysis-chart-bar-wrapper">
                <div
                  className="analysis-chart-bar-fill"
                  style={{ width: `${width}%` }}
                />
              </div>
              <span className="analysis-chart-value">
                {value.toLocaleString()}원
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function AnalysisResultPanel({ analysisId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!analysisId) {
      setData(null);
      setError(null);
      return;
    }
    const fetchResult = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await apiClient.get(`/analysis/${analysisId}/result/`);
        setData(res.data);
      } catch (err) {
        console.error(err);
        setError("분석 결과를 불러오지 못했습니다.");
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [analysisId]);

  if (!analysisId) {
    return (
      <p className="dashboard-card-subtitle">
        왼쪽에서 분석 프리셋을 선택하거나 새 분석을 저장한 뒤 결과를 확인해 보세요.
      </p>
    );
  }

  if (loading) {
    return (
      <p className="dashboard-card-subtitle">분석 결과를 계산하는 중...</p>
    );
  }

  if (error) {
    return <p className="auth-error">{error}</p>;
  }

  if (!data) {
    return null;
  }

  const { analysis, summary, daily_chart, type_chart, description_chart } =
    data;

  return (
    <div className="analysis-result">
      <div className="analysis-summary-row">
        <div className="analysis-summary-item">
          <div className="analysis-summary-label">총 금액</div>
          <div className="analysis-summary-value">
            {summary.total_amount.toLocaleString()}원
          </div>
        </div>
        <div className="analysis-summary-item">
          <div className="analysis-summary-label">거래 건수</div>
          <div className="analysis-summary-value">
            {summary.transactions_count}건
          </div>
        </div>
      </div>

      <BarList title="일자별 합계" data={daily_chart} />
      <BarList title="거래 타입별 합계" data={type_chart} />
      <BarList title="설명(메모)별 합계" data={description_chart} />
    </div>
  );
}
