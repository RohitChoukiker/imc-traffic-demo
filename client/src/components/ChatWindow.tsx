

import React, { useState, useRef, useEffect } from "react";
import Header from "./Header";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";
import TypingIndicator from "./TypingIndicator";



interface Message {
  id: string;
  content: string;
  sender: "user" | "assistant";
  timestamp: Date;
  table?: {   // 👈 new optional field
    columns: string[];
    rows: string[][];
  };
}

interface ChatWindowProps {
  onLogout: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onLogout }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const hasUserMessages = messages.some((msg) => msg.sender === "user");

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

const handleSendMessage = async (content: string) => {
  if (!content.trim()) return;

  const userMessage: Message = {
    id: Date.now().toString(),
    content,
    sender: "user",
    timestamp: new Date(),
  };

  setMessages((prev) => [...prev, userMessage]);
  setIsTyping(true);

  try {
    const response = await fetch("http://localhost:8000/rag/query", { // Local FastAPI
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: content,  
        top_k: 10
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    // const data = await response.json();

    // const assistantMessage: Message = {
    //   id: (Date.now() + 1).toString(),
    //   content: data.answer || "No answer found.",
    //   sender: "assistant",
    //   timestamp: new Date(),
    // };

    // setMessages((prev) => [...prev, assistantMessage]);

    const data = await response.json();

const assistantMessage: Message = {
  id: (Date.now() + 1).toString(),
  content: data.answer || "No answer found.",
  sender: "assistant",
  timestamp: new Date(),
  table: data.table || null,   // 👈 table inject kar diya
};

setMessages((prev) => [...prev, assistantMessage]);

  } catch (error: any) {
    console.error("Error sending message:", error);
    setMessages((prev) => [
      ...prev,
      {
        id: (Date.now() + 1).toString(),
        content: `Error: ${error.message || "Please try again."}`,
        sender: "assistant",
        timestamp: new Date(),
      },
    ]);
  } finally {
    setIsTyping(false);
  }
};


  if (!hasUserMessages) {
    return (
      <div className="flex flex-col h-screen max-w-full mx-auto bg-white shadow-lg">
        <Header onLogout={onLogout} />
        <div className="flex-1 flex flex-col items-center justify-center px-4 py-8">
          <div className="text-center mb-12 max-w-3xl">
            <img
             src="/images/main_logo.png"
             alt="Smart City Logo"
             className="h-20 w-auto mx-auto mb-4"
/>

             <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Welcome to Indore Smart AI-Assistant 
            </h1> 

            
            
              {/* <span style={{ fontSize: "18px", fontWeight: "normal", color: "gray" }}>
                Powered by IMC
              </span> */}
           
            <p className="text-lg text-gray-600 leading-relaxed mb-8">
              Your trusted AI assistant for all Indore Smart City services. Start by asking me anything!
            </p>
          </div>
          <div className="w-full max-w-3xl">
            <InputBar
              onSendMessage={handleSendMessage}
              isDisabled={isTyping}
              isCentered
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen max-w-full mx-auto bg-white shadow-lg">
      <Header onLogout={onLogout} />
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <InputBar onSendMessage={handleSendMessage} isDisabled={isTyping} />
    </div>
  );
};

export default ChatWindow;
