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
        });

        // 마지막 메시지 업데이트
        setChatLog((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = { role: 'bot', message: res.data.reply };
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

      {hasChat && (
        <div className="chat-box">
          <div className="chat-scroll">
            {chatLog.map((chat, idx) => (
              <div
                key={idx}
                className={`chat-msg ${chat.role === 'user' ? 'right' : 'left'}`}
              >
                <div className="bubble">{chat.message}</div>
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
    </div>
  );
}