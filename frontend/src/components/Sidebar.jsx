import React from 'react';
import '../css/Sidebar.css';
import { Link } from 'react-router-dom'

const Sidebar = ({ isOpen, toggleSidebar }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <ul>
        <li><Link to="/">홈</Link></li>
        <li><Link to="/graph">그래프</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
