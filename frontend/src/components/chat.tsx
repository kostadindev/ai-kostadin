import React, { useState, useEffect, useCallback, ChangeEvent } from "react";
import { Button, Card, Input, Layout, theme } from "antd";
import { SendOutlined, ReloadOutlined } from "@ant-design/icons";
import { DarkModeSwitch } from "react-toggle-dark-mode";
import MarkdownRenderer from "./markdown-renderer";
import DefaultPrompts from "./default-prompts";

const { Header } = Layout;

const api = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
  const handleSendMessage = async (overrideInput?: string) => {
    const messageToSend = overrideInput?.trim() || input.trim();
    if (isSending || !messageToSend) return;

    const userMessage: Message = { content: messageToSend, role: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput(""); // clear visible input
    setIsSending(true);

    try {
      const response = await fetch(`${api}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: messageToSend }),
      });

      if (!response.ok) {
        throw new Error(`Network error: ${response.statusText}`);
      }

      setMessages((prev) => [...prev, { content: "", role: "system" }]);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      if (reader) {
        let done = false;
        while (!done) {
          const { done: doneReading, value } = await reader.read();
          done = doneReading;
          const chunkValue = decoder.decode(value, { stream: !done });
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
    // Wake up the backend when the component mounts
    const wakeUpServer = async () => {
      try {
        await fetch(`${api}/ping`, {
          method: "GET",
        });
      } catch (err) {
        console.warn("Server wake-up failed:", err);
      }
    };

    wakeUpServer();
  }, []);

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
            <DefaultPrompts
              onPromptSelect={(prompt) => handleSendMessage(prompt)}
              isDarkMode={isDarkMode}
              cardBackground={isDarkMode ? token.colorBgContainer : "#f0f2f5"}
            />
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
              placeholder="Ask about Kostadin's work"
              style={{ fontSize: "16px" }}
              maxLength={256}
              disabled={isSending}
              className="flex-1"
            />
            <Button
              icon={<SendOutlined />}
              onClick={() => handleSendMessage()}
              disabled={isSending}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;
