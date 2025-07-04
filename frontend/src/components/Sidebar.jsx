import React from 'react';
import '../css/Sidebar.css';
import { Link, useLocation, useNavigate } from 'react-router-dom'

const Sidebar = ({ isOpen, toggleSidebar }) => {

  const location = useLocation();
  const navigate = useNavigate();

  const resetSession = async () => {
    try {
      await fetch("http://localhost:8000/api/session_reset", {
        method: "POST"
      });
    } catch (error) {
      console.error("세션 초기화 실패:", error);
    }
  };

  const handleGraphClick = async (e) => {
    e.preventDefault();
    await resetSession();
    navigate('/graph');
  };

  const handleHomeClick = (e) => {
    if (location.pathname === '/') {
      e.preventDefault();
      window.location.reload(); // 전체 새로고침
    }
    else {
      navigate('/'); // 다른 위치면 이동
    }
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <ul>
        <li><Link to="/" onClick={handleHomeClick}>홈</Link></li>
        <li><Link to="/graph" onClick={handleGraphClick}>그래프</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
