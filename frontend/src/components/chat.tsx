import React, { useState, useEffect, useMemo, memo } from "react";
import { Button, Input, Layout, theme } from "antd";
import { SendOutlined, ReloadOutlined } from "@ant-design/icons";
import { DarkModeSwitch } from "react-toggle-dark-mode";
import { useChat } from "../hooks/useChat";
import { MessageList } from "./MessageList";
import { Suggestions } from "./Suggestions";
import { Particles, initParticlesEngine } from "@tsparticles/react";
import type { Engine } from "@tsparticles/engine";
import { loadSlim } from "@tsparticles/slim";
import type { MoveDirection, OutMode } from "@tsparticles/engine";

const { Header } = Layout;

// Feature flag for particles
const ENABLE_PARTICLES = import.meta.env.VITE_ENABLE_PARTICLES === "true";
const APP_NAME = import.meta.env.VITE_APP_NAME || "AI Kostadin";

// Reusable particles component
const ParticleBackground = memo(({ id }: { id: string }) => {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== "undefined" ? window.innerWidth : 1200,
    height: typeof window !== "undefined" ? window.innerHeight : 800,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const particlesOptions = useMemo(
    () => ({
      fullScreen: {
        enable: false,
      },
      fpsLimit: 60,
      particles: {
        color: {
          value: "#e89a3c",
        },
        links: {
          color: "#e89a3c",
          distance: windowSize.width < 480 ? 100 : 150,
          enable: true,
          opacity: 0.8,
          width: 2,
        },
        move: {
          enable: true,
          speed: 2,
          direction: "none" as MoveDirection,
          random: false,
          straight: false,
          outModes: {
            default: "bounce" as OutMode,
            bottom: "bounce" as OutMode,
            left: "bounce" as OutMode,
            right: "bounce" as OutMode,
            top: "bounce" as OutMode,
          },
        },
        number: {
          value: windowSize.width < 480 ? 24 : 100,
          density: {
            enable: false,
          },
        },
        opacity: {
          value: 1,
        },
        size: {
          value: { min: 2, max: 5 },
        },
      },
      detectRetina: true,
    }),
    [windowSize.width]
  );

  return <Particles id={id} options={particlesOptions} />;
});

ParticleBackground.displayName = "ParticleBackground";

const ChatComponent: React.FC = () => {
  const { token } = theme.useToken();
  const [isDarkMode, setIsDarkMode] = useState<boolean>(
    localStorage.getItem("theme") === "dark"
  );
  const [init, setInit] = useState(false);

  // Initialize tsParticles
  useEffect(() => {
    initParticlesEngine(async (engine: Engine) => {
      await loadSlim(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);

  const {
    messages,
    input,
    setInput,
    isSending,
    isTyping,
    suggestions,
    clearChat,
    sendMessage,
    onMessagesLoad,
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
    position: "relative",
    zIndex: 10,
  };

  const logoStyle: React.CSSProperties = {
    fontFamily: '"Goldman", serif',
    fontWeight: 400,
    fontStyle: "normal",
    fontSize: "2rem",
    cursor: "pointer",
    color: token.colorText,
    textShadow: "0 1px 2px rgba(255, 255, 255, 0.7)",
  };

  return (
    <div
      className="flex flex-col h-screen w-full transition-colors duration-200"
      style={{ backgroundColor: token.colorBgLayout }}
    >
      <Header style={headerStyle}>
        <div className="flex justify-center w-full">
          <div className="flex justify-between items-center w-full lg:max-w-4xl lg:px-4">
            <div style={logoStyle} className="goldman-bold lg:pl-4">
              <a
                href="/"
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: "inherit",
                  textDecoration: "none",
                  transition: "opacity 0.2s ease-in-out",
                }}
                className="hover:opacity-80"
              >
                {APP_NAME}
              </a>
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
          </div>
        </div>
      </Header>

      <div className="flex justify-center w-full h-full relative">
        {ENABLE_PARTICLES && init && (
          <div className="hidden lg:block absolute inset-0 overflow-hidden">
            <ParticleBackground id="tsparticles-chat" />
          </div>
        )}
        <div className="flex flex-col w-full lg:max-w-4xl lg:px-4 relative z-10">
          <div className="flex flex-col flex-1 overflow-hidden">
            <div
              className="flex-1 overflow-hidden transition-shadow duration-200 shadow-sm lg:shadow-md"
              style={{
                backgroundColor: token.colorBgContainer,
                border: `1px solid ${token.colorBorder}`,
                borderRadius: token.borderRadius,
                position: "relative",
              }}
            >
              <div
                style={{
                  position: "relative",
                  zIndex: 1,
                  height: "100%",
                  backgroundColor: "transparent",
                }}
              >
                <MessageList
                  messages={messages}
                  isDarkMode={isDarkMode}
                  onPromptSelect={sendMessage}
                  onScroll={() => {}}
                  isTyping={isTyping}
                  onMessagesLoad={onMessagesLoad}
                />
              </div>
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  background: token.colorBorder,
                  opacity: 0.12,
                  pointerEvents: "none",
                  zIndex: 0,
                  maskImage: `url("data:image/svg+xml,%3Csvg width='104' height='240' viewBox='0 0 104 240' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='52,8 100,40 100,200 52,232 4,200 4,40' fill='none' stroke='%23000' stroke-width='4'/%3E%3C/svg%3E")`,
                  WebkitMaskImage: `url("data:image/svg+xml,%3Csvg width='104' height='240' viewBox='0 0 104 240' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='52,8 100,40 100,200 52,232 4,200 4,40' fill='none' stroke='%23000' stroke-width='4'/%3E%3C/svg%3E")`,
                  maskSize: "104px 240px",
                  WebkitMaskSize: "104px 240px",
                  maskRepeat: "repeat",
                  WebkitMaskRepeat: "repeat",
                  maskPosition: "0 0",
                  WebkitMaskPosition: "0 0",
                }}
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
      </div>
    </div>
  );
};

export default ChatComponent;
