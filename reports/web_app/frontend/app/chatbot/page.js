"use client";

import { useState } from "react";
import axios from "axios";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Append user's message
    setMessages((prev) => [...prev, { sender: "You", text: input }]);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        new URLSearchParams({ user_message: input })
      );
      setMessages((prev) => [
        ...prev,
        { sender: "MedBot", text: response.data.response },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "MedBot", text: "Error connecting to chatbot" },
      ]);
    }

    setInput("");
  };

  return (
    <main style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Chat with MedBot</h1>
      <div
        style={{
          border: "2px solid #ccc",
          padding: "1rem",
          margin: "1rem auto",
          width: "60%",
          minHeight: "200px",
          background: "white",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, idx) => (
          <p
            key={idx}
            style={{
              textAlign: msg.sender === "You" ? "right" : "left",
              margin: "0.5rem 0",
            }}
          >
            <strong>{msg.sender}: </strong>
            {msg.text}
          </p>
        ))}
      </div>
      <div style={{ display: "flex", justifyContent: "center", gap: "0.5rem" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          style={{ padding: "0.5rem", width: "40%" }}
        />
        <button onClick={sendMessage} style={{ padding: "0.5rem 1rem", cursor: "pointer" }}>
          Send
        </button>
      </div>
    </main>
  );
}
