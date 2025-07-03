import React, { useState, useRef, useEffect } from 'react';
import '../css/SearchBox.css';
import axios from 'axios';

export default function SearchBox() {

    const [input, setInput] = useState('');
    const [chatLog, setChatLog] = useState([]);
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [theme, setTheme] = useState('');
    const [loading, setLoading] = useState(false);
    const [modalImage, setModalImage] = useState(null);
    const [duration, setDuration] = useState('');

    const chatEndRef = useRef(null);

    const handleSend = async () => {
        if (!input.trim()) return;

        // 사용자 메시지 추가
        setChatLog((prev) => [...prev, { role: 'user', message: input }]);
        setInput('');
        setLoading(true);

        // "답변 작성 중..." 임시 메시지
        setChatLog((prev) => [...prev, { role: 'bot', message: '답변 작성 중...' }]);

        try {
        const res = await axios.post('http://localhost:8000/api/chat', {
            message: input,
            age,
            gender,
            theme,
            duration
        });

        const replyMessage = {
          role: 'bot',
          message: res.data.reply,
          image: res.data.image_url || null
        }

        // 마지막 메시지 업데이트
        setChatLog((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = replyMessage;
            return updated;
        });
        } catch (err) {
        console.error(err);
        setChatLog((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = { role: 'bot', message: '⚠️ 서버 오류가 발생했습니다.' };
            return updated;
        });
        }

        setLoading(false);
    };






  // 자동 스크롤 맨 아래로
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatLog]);

  const hasChat = chatLog.length > 0;




  return (
    <div className={`main-container ${hasChat ? 'shifted' : ''}`}>
      <h1 className="title">
        Search with <span className="highlight">TourMate</span>
      </h1>

      {/* 필터 UI */}
      <div className="filters">
        <select value={age} onChange={(e) => setAge(e.target.value)}>
          <option value="">연령대</option>
          <option value="20대">20대</option>
          <option value="30대">30대</option>
          <option value="40대">40대</option>
          <option value="50대">50대</option>
          <option value="60대">60대</option>
          <option value="70대 이상">70대 이상</option>
        </select>

        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="">성별</option>
          <option value="남성">남성</option>
          <option value="여성">여성</option>
        </select>

        <select value={theme} onChange={(e) => setTheme(e.target.value)}>
          <option value="">여행 테마</option>
          <option value="자연">자연</option>
          <option value="역사">역사</option>
          <option value="휴양">휴양</option>
          <option value="맛집 탐방">맛집 탐방</option>
          <option value="액티비티">액티비티</option>
          <option value="쇼핑">쇼핑</option>
          <option value="관광">관광</option>
        </select>

        <select value={duration} onChange={(e) => setDuration(e.target.value)}>
          <option value="">여행 기간</option>
          <option value="하루">하루</option>
          <option value="1박 2일">1박 2일</option>
          <option value="2박 3일">2박 3일</option>
          <option value="3박 4일">3박 4일</option>
          <option value="4박 5일">4박 5일</option>
          <option value="5일 이상">5일 이상</option>
        </select>
      </div>

      {hasChat && (
        <div className="chat-box">
          <div className="chat-scroll">
            {chatLog.map((chat, idx) => (
              <div
                key={idx}
                className={`chat-msg ${chat.role === 'user' ? 'right' : 'left'}`}
              >
                <div className="msg-wrapper">
                  <div className="bubble">{chat.message}</div>
                    {chat.image && (
                    <img
                      src={chat.image}
                      alt="추천 이미지"
                      className="chat-image"
                      onClick={() => setModalImage(chat.image)}
                    />
                    )}
                  </div>
                </div>
              
            ))}
            <div ref={chatEndRef} />
          </div>
        </div>
      )}

      <div className="search-box">
        <span className="icon">🔍</span>
        <input
          type="text"
          placeholder="Ask a question"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="submit-btn">➤</button>
      </div>
      {modalImage && (
        <div className="image-modal" onClick={() => setModalImage(null)}>
          <div className="image-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={() => setModalImage(null)}>×</button>
            <img src={modalImage} alt="확대 이미지" />
          </div>
        </div>
      )}
    </div>
  );
}