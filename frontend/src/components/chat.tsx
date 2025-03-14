import React, { useState, useEffect, useCallback, ChangeEvent } from "react";
import { Button, Card, Input, Layout, theme } from "antd";
import {
  SendOutlined,
  DeleteOutlined,
  ReloadOutlined,
} from "@ant-design/icons";
import { DarkModeSwitch } from "react-toggle-dark-mode";
import MarkdownRenderer from "./markdown-renderer";

const { Header } = Layout;

interface Message {
  content: string;
  role: "user" | "system";
}

const primaryColor = "#e89a3c";

const ChatComponent: React.FC = () => {
  const { token } = theme.useToken();

  // Chat state
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [isUserScrolling, setIsUserScrolling] = useState(false);
  const messageContainerRef = React.useRef<HTMLDivElement>(null);

  // Dark mode state (initialize based on localStorage)
  const [isDarkMode, setIsDarkMode] = useState<boolean>(
    localStorage.getItem("theme") !== "light"
  );

  // Theme toggle handler
  const toggleDarkMode = (checked: boolean) => {
    setIsDarkMode(checked);
    const newTheme = checked ? "dark" : "light";
    localStorage.setItem("theme", newTheme);
    window.dispatchEvent(new Event("themeChanged"));
  };

  // Clear chat handler
  const handleClearChat = () => {
    setMessages([]);
  };

  // Scroll helper
  const scrollToBottom = useCallback(() => {
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTo({
        top: messageContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, []);

  // When the user scrolls the messages container
  const handleScroll = useCallback(() => {
    if (messageContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } =
        messageContainerRef.current;
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 50;
      setIsUserScrolling(!isAtBottom);
    }
  }, []);

  // Send a message and stream the system's response
  const handleSendMessage = async () => {
    if (isSending || !input.trim()) return;

    const question = input.trim();
    const userMessage: Message = { content: question, role: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsSending(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`Network error: ${response.statusText}`);
      }

      // Add an empty system message placeholder to update as chunks arrive
      setMessages((prev) => [...prev, { content: "", role: "system" }]);

      // Use the stream reader to process incoming chunks
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      if (reader) {
        let done = false;
        while (!done) {
          const { done: doneReading, value } = await reader.read();
          done = doneReading;
          const chunkValue = decoder.decode(value, { stream: !done });
          // Update the last system message with the new chunk
          setMessages((prev) => {
            const newMessages = [...prev];
            const lastIndex = newMessages.length - 1;
            newMessages[lastIndex] = {
              ...newMessages[lastIndex],
              content: newMessages[lastIndex].content + chunkValue,
            };
            return newMessages;
          });
        }
      }
    } catch (error: any) {
      const errorMessage: Message = {
        content: "Error fetching response: " + error.message,
        role: "system",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsSending(false);
      scrollToBottom();
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isSending) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    if (!isUserScrolling) {
      scrollToBottom();
    }
  }, [messages, scrollToBottom, isUserScrolling]);

  // Header style
  const headerStyle: React.CSSProperties = {
    height: "80px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.1)",
    padding: "0 20px",
  };

  const logoStyle: React.CSSProperties = {
    fontFamily: '"Goldman", serif',
    fontWeight: 400,
    fontStyle: "normal",
    fontSize: "2rem",
    cursor: "pointer",
    color: token.colorText,
  };

  return (
    <div className="flex flex-col h-full w-full">
      {/* Header with Logo, Reset Button, and Theme Switch */}
      <Header style={headerStyle}>
        <div style={logoStyle} className="goldman-bold">
          AI Kostadin
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <DarkModeSwitch
            checked={isDarkMode}
            onChange={toggleDarkMode}
            size={25}
          />
          <Button
            icon={<ReloadOutlined />}
            onClick={handleClearChat}
            title="Clear Chat"
            onMouseDown={(e) => e.preventDefault()}
          />
        </div>
      </Header>

      {/* Chat Area */}
      <div className="flex flex-col flex-1">
        {/* Messages Container */}
        <div
          className="flex-1 overflow-auto p-4"
          ref={messageContainerRef}
          onScroll={handleScroll}
          style={{
            backgroundColor: token.colorBgContainer,
            border: `1px solid ${token.colorBorder}`,
            borderRadius: token.borderRadius,
          }}
        >
          {messages.length === 0 && (
            <div
              className="text-center mb-4"
              style={{ color: token.colorTextSecondary }}
            >
              No messages yet. Start the conversation!
            </div>
          )}
          {messages.map((msg, index) => (
            <div key={index} className="my-2 pb-1">
              {msg.role === "user" ? (
                <div
                  className="inline-block p-2 px-4 rounded-lg break-words text-white"
                  style={{ backgroundColor: primaryColor, maxWidth: "100%" }}
                >
                  {msg.content}
                </div>
              ) : (
                <Card
                  className="inline-block rounded-lg shadow-md text-black w-full break-words"
                  hoverable
                  style={{
                    backgroundColor: isDarkMode
                      ? token.colorBgContainer
                      : "#f0f2f5",
                  }}
                >
                  <MarkdownRenderer content={msg.content} />
                </Card>
              )}
            </div>
          ))}
        </div>

        {/* Sticky Input Area */}
        <div className="sticky bottom-0 w-full">
          <div
            className="p-2 border-t flex items-center gap-3"
            style={{
              backgroundColor: token.colorBgContainer,
              borderColor: token.colorBorder,
            }}
          >
            <Input.TextArea
              autoSize
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyPress}
              placeholder="Ask about anything here.."
              style={{ fontSize: "16px" }}
              maxLength={256}
              disabled={isSending}
              className="flex-1"
            />
            <Button
              icon={<SendOutlined />}
              onClick={handleSendMessage}
              disabled={isSending}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;
