import React from 'react';
import { useEffect, useState } from 'react';

const GraphPage = () => {

    const [imgSrc, setImgSrc] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/graph")
      .then(res => res.blob())
      .then(blob => setImgSrc(URL.createObjectURL(blob)))
      .catch(err => console.error(err));
  }, []);

//   return <div style={{ color: 'white' }}>그래프 페이지입니다.</div>;
  return (
    <div style={{ color: 'white', textAlign: 'center', marginTop: '40px' }}>
      <h2>📊 그래프 페이지</h2>
      {imgSrc ? (
        <img src={imgSrc} alt="그래프" style={{ maxWidth: '80%', borderRadius: '12px' }} />
      ) : (
        <p>그래프를 불러오는 중입니다...</p>
      )}
    </div>
  );
};

export default GraphPage;