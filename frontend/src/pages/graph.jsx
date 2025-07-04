import React, { useEffect, useState } from 'react';
import '../css/graph.css'; // css 파일 import

const GraphPage = () => {
  const [imgSrc, setImgSrc] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/graph")
      .then(res => {
        if (!res.ok) {
          throw new Error("그래프를 그릴 수 없습니다.");
        }
        return res.blob();
      })
      .then(blob => {
        setImgSrc(URL.createObjectURL(blob));
      })
      .catch(err => {
        console.error(err);
        setError(true);
      });
  }, []);

  return (
    <div className="graph-container">
      <h2 className="graph-title">여행 목록 만족도 그래프</h2>
      {error ? (
        <p className="graph-error">⚠️ 그래프를 그릴 수 없습니다.</p>
      ) : imgSrc ? (
        <img src={imgSrc} alt="그래프" className="graph-image" />
      ) : (
        <p className="graph-loading">그래프를 불러오는 중입니다...</p>
      )}
    </div>
  );
};

export default GraphPage;