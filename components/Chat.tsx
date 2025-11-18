'use client';

import { useState, useRef, useEffect } from 'react';
import { Mensagem } from '@/types';

export default function Chat() {
  const [mensagens, setMensagens] = useState<Mensagem[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Olá! Sou seu assistente de harmonização de vinhos. Descreva um prato e eu recomendarei o vinho perfeito para acompanhá-lo!',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [mensagens]);

  const enviarMensagem = async () => {
    if (!inputValue.trim() || isLoading) return;

    const novaMensagem: Mensagem = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMensagens(prev => [...prev, novaMensagem]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call Python FastAPI backend
      const response = await fetch('http://localhost:8000/api/recomendacao', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensagem: inputValue }),
      });

      const data = await response.json();

      const respostaMensagem: Mensagem = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.mensagem || 'Desculpe, ocorreu um erro ao processar sua solicitação.',
        timestamp: new Date()
      };

      setMensagens(prev => [...prev, respostaMensagem]);
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      const erroMensagem: Mensagem = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Desculpe, não consegui conectar ao servidor. Certifique-se de que a API Python está rodando em http://localhost:8000',
        timestamp: new Date()
      };
      setMensagens(prev => [...prev, erroMensagem]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      enviarMensagem();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🍷 VineChat</h1>
        <p>Recomendação de Vinhos com IA</p>
      </div>

      <div className="chat-messages">
        {mensagens.map((mensagem) => (
          <div
            key={mensagem.id}
            className={`message ${mensagem.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              {mensagem.content}
            </div>
            <div className="message-time">
              {mensagem.timestamp.toLocaleTimeString('pt-BR', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant-message">
            <div className="message-content">
              <span className="typing-indicator">Pensando...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Descreva um prato (ex: salmão grelhado, picanha, risotto...)"
          className="chat-input"
          disabled={isLoading}
        />
        <button
          onClick={enviarMensagem}
          disabled={isLoading || !inputValue.trim()}
          className="send-button"
        >
          Enviar
        </button>
      </div>

      <style jsx>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          max-width: 800px;
          margin: 0 auto;
          background: white;
          box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }

        .chat-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2rem;
          text-align: center;
        }

        .chat-header h1 {
          font-size: 2rem;
          margin-bottom: 0.5rem;
        }

        .chat-header p {
          opacity: 0.9;
          font-size: 0.9rem;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .message {
          display: flex;
          flex-direction: column;
          max-width: 70%;
          animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .user-message {
          align-self: flex-end;
        }

        .assistant-message {
          align-self: flex-start;
        }

        .message-content {
          padding: 1rem 1.25rem;
          border-radius: 1rem;
          word-wrap: break-word;
          line-height: 1.5;
        }

        .user-message .message-content {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 0.25rem;
        }

        .assistant-message .message-content {
          background: #f1f3f5;
          color: #212529;
          border-bottom-left-radius: 0.25rem;
        }

        .message-time {
          font-size: 0.75rem;
          color: #6c757d;
          margin-top: 0.25rem;
          padding: 0 0.5rem;
        }

        .typing-indicator {
          display: inline-block;
        }

        .typing-indicator::after {
          content: '...';
          animation: dots 1.5s steps(4, end) infinite;
        }

        @keyframes dots {
          0%, 20% {
            content: '.';
          }
          40% {
            content: '..';
          }
          60%, 100% {
            content: '...';
          }
        }

        .chat-input-container {
          display: flex;
          gap: 0.5rem;
          padding: 1rem;
          background: white;
          border-top: 1px solid #e9ecef;
        }

        .chat-input {
          flex: 1;
          padding: 0.75rem 1rem;
          border: 2px solid #e9ecef;
          border-radius: 0.5rem;
          font-size: 1rem;
          outline: none;
          transition: border-color 0.2s;
        }

        .chat-input:focus {
          border-color: #667eea;
        }

        .chat-input:disabled {
          background: #f8f9fa;
          cursor: not-allowed;
        }

        .send-button {
          padding: 0.75rem 2rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 0.5rem;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .send-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .send-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        @media (max-width: 768px) {
          .chat-container {
            height: 100vh;
          }

          .message {
            max-width: 85%;
          }

          .chat-header h1 {
            font-size: 1.5rem;
          }
        }
      `}</style>
    </div>
  );
}

