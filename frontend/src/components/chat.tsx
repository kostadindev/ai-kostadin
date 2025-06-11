import React, { useState } from "react";
import { Button, Input, Layout, theme } from "antd";
import { SendOutlined, ReloadOutlined } from "@ant-design/icons";
import { DarkModeSwitch } from "react-toggle-dark-mode";
import { useChat } from "../hooks/useChat";
import { MessageList } from "./MessageList";
import { Suggestions } from "./Suggestions";

const { Header } = Layout;

const ChatComponent: React.FC = () => {
  const { token } = theme.useToken();
  const [isDarkMode, setIsDarkMode] = useState<boolean>(
    localStorage.getItem("theme") === "dark"
  );

  const {
    messages,
    input,
    setInput,
    isSending,
    isTyping,
    suggestions,
    clearChat,
    sendMessage,
  } = useChat();

  const toggleDarkMode = (checked: boolean) => {
    setIsDarkMode(checked);
    const newTheme = checked ? "dark" : "light";
    localStorage.setItem("theme", newTheme);
    window.dispatchEvent(new Event("themeChanged"));
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isSending) {
      e.preventDefault();
      sendMessage(input);
    }
  };

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
    <div className="flex flex-col h-screen w-full">
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
            onClick={clearChat}
            title="Clear Chat"
            onMouseDown={(e) => e.preventDefault()}
          />
        </div>
      </Header>

      <div className="flex flex-col flex-1 overflow-hidden">
        <div
          className="flex-1 overflow-hidden"
          style={{
            backgroundColor: token.colorBgContainer,
            border: `1px solid ${token.colorBorder}`,
            borderRadius: token.borderRadius,
          }}
        >
          <MessageList
            messages={messages}
            isDarkMode={isDarkMode}
            onPromptSelect={sendMessage}
            onScroll={() => {}}
            isTyping={isTyping}
          />
        </div>

        <Suggestions
          suggestions={suggestions}
          isDarkMode={isDarkMode}
          onSuggestionClick={sendMessage}
        />

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
              onClick={() => sendMessage(input)}
              disabled={isSending}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;
