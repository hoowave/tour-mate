import './App.css';
import SearchBox from './components/SearchBox';
import Sidebar from './components/Sidebar';
import GraphPage from './pages/graph';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { useState } from 'react';

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  return (
    <BrowserRouter>
    {/* 로고 버튼 */}
        <img
          src={"/logo.png"}
          alt="로고"
          onClick={toggleSidebar}
          className="logo-button"
        />

        <Sidebar isOpen={isSidebarOpen} />
      <Routes>


        <Route path='/' element={<SearchBox />} />
        <Route path='/graph' element={<GraphPage />} />
      </Routes>
      
    </BrowserRouter>
  );
}

export default App;