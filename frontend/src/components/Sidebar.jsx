import React from 'react';
import '../css/Sidebar.css';
import { Link, useLocation } from 'react-router-dom'

const Sidebar = ({ isOpen, toggleSidebar }) => {

  const location = useLocation();

  const handleHomeClick = (e) => {
    if (location.pathname === '/') {
      e.preventDefault();
      window.location.reload(); // 전체 새로고침
    }
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <ul>
        <li><Link to="/" onClick={handleHomeClick}>홈</Link></li>
        <li><Link to="/graph">그래프</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
