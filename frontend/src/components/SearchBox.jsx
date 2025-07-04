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

    const extractTextImagePairs = (text) => {
      const markdownImgRegex = /!\[.*?\]\((https?:\/\/[^\s)]+)\)/gi;
      const urlRegex = /(https?:\/\/[^\s)]+\.(jpg|jpeg|png|gif|webp)|https?:\/\/images\.unsplash\.com\/[^\s)]+)/gi; // unsplash 빼면 예제 이미지 테스트 못함

      const lines = text.split(/\n+/);

      return lines.flatMap(line => {
        const results = [];

        // 1. 먼저 마크다운 이미지 처리
        let markdownProcessedLine = line;
        const markdownMatches = [...line.matchAll(markdownImgRegex)];

        markdownMatches.forEach((match) => {
          const fullMatch = match[0];
          const url = match[1];
          const index = markdownProcessedLine.indexOf(fullMatch);
          const beforeText = markdownProcessedLine.slice(0, index).trim();
          if (beforeText) results.push({ text: beforeText, image: null });
          results.push({ text: null, image: url });
          markdownProcessedLine = markdownProcessedLine.slice(index + fullMatch.length);
        });

        // 2. 남은 텍스트에 일반 이미지 URL 처리
        const matches = [...markdownProcessedLine.matchAll(urlRegex)];
        let remaining = markdownProcessedLine;

        matches.forEach((match) => {
          const url = match[0];
          const index = remaining.indexOf(url);
          const beforeText = remaining.slice(0, index).trim();
          if (beforeText) {
            results.push({ text: beforeText, image: null });
          }
          results.push({ text: null, image: url });
          remaining = remaining.slice(index + url.length);
        });

        if (remaining.trim()) {
          results.push({ text: remaining.trim(), image: null });
        }

        return results;
      });
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        setChatLog((prev) => [...prev, { role: 'user', message: input }]);
        setInput('');
        setLoading(true);

        setChatLog((prev) => [...prev, { role: 'bot', message: '답변 작성 중...' }]);

        try {
        const res = await axios.post('http://localhost:8000/api/chat', {
            message: input,
            age,
            gender,
            theme,
            duration
        });
        console.log(res.data.reply)
        const pairs = extractTextImagePairs(res.data.reply);

        // const replyMessage = {
        //   role: 'bot',
        //   message: res.data.reply,
        //   image: res.data.image_url || null
        // }
        const replyMessage = {
          role: 'bot',
          message: pairs
        };

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

      {/* 콤보박스 UI */}
      <div className="combobox">
        <select value={age} onChange={(e) => setAge(e.target.value)}>
          <option value="">연령대</option>
          <option value="20">20대</option>
          <option value="30">30대</option>
          <option value="40">40대</option>
          <option value="50">50대</option>
          <option value="60">60대 이상</option>
        </select>

        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="">성별</option>
          <option value="남">남성</option>
          <option value="여">여성</option>
        </select>

        <select value={theme} onChange={(e) => setTheme(e.target.value)}>
          <option value="">여행 테마</option>
          <option value="1">취식</option>
          <option value="2">쇼핑</option>
          <option value="3">체험/입장/관람</option>
          <option value="4">단순 구경/산책</option>
          <option value="5">휴식</option>
          <option value="6">기타활동</option>
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
                  <div className="bubble">
                    {Array.isArray(chat.message) ? (
                      chat.message.map((msg, idx) => (
                        <div key={idx} style={{ marginBottom: '10px' }}>
                          {msg.text && <div style={{ marginBottom: '10px' }}>{msg.text}</div>}
                          {msg.image && (
                            <img
                              src={msg.image}
                              alt={`추천 이미지 ${idx + 1}`}
                              className="chat-image"
                              onClick={() => setModalImage(msg.image)}
                            />
                          )}
                        </div>
                      ))
                    ) : (
                      <div>{chat.message}</div>
                    )}
                  </div>
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
        <button className="submit-btn" onClick={handleSend}>➤</button>
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