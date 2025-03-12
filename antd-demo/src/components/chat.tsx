import React, { useState, useEffect, useCallback, ChangeEvent } from "react";
import { Button, Card, Input, Layout, theme } from "antd";
import { SendOutlined } from "@ant-design/icons";
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

  // Send a message and simulate a system response
  const handleSendMessage = () => {
    if (isSending || !input.trim()) return;

    const userMessage: Message = { content: input.trim(), role: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsSending(true);

    // Simulate a system response after a short delay
    setTimeout(() => {
      const systemMessage: Message = {
        content: "This is a simulated response from the system.",
        role: "system",
      };
      setMessages((prev) => [...prev, systemMessage]);
      setIsSending(false);
      scrollToBottom();
    }, 1000);
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

  // Use bodyBg for non-chat blocks
  const headerStyle: React.CSSProperties = {
    height: "80px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.1)",
    padding: "0 20px",
    // backgroundColor: token.colorBgContainer,
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
      {/* Header with Logo and Theme Switch */}
      <Header style={headerStyle}>
        <div style={logoStyle}>AI Kostadin</div>
        <div>
          <DarkModeSwitch
            checked={isDarkMode}
            onChange={toggleDarkMode}
            size={25}
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
              backgroundColor: token.bodyBg || token.colorBgContainer,
              borderColor: token.colorBorder,
            }}
          >
            <Input.TextArea
              autoSize
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyPress}
              placeholder="Type your message here..."
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
