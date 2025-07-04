import React from 'react';
import '../css/NotFound.css';

const NotFound = () => {
  return (
    <div className="notfound-container">
      <h1>404 Not Found</h1>
      <p>페이지를 찾을 수 없습니다.</p><br/>
      <p>홈으로 이동해주세요.</p>
    </div>
  );
};

export default NotFound;