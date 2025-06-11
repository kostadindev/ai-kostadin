import React, { useRef, useCallback, useEffect, useState } from "react";
import { Card } from "antd";
import { Message } from "../types/chat";
import MarkdownRenderer from "./MarkdownRenderer";
import DefaultPrompts from "./DefaultPrompts";

const bounceKeyframes = `
  @keyframes customBounce {
    0%, 100% { transform: translateY(0); }
    20% { transform: translateY(-2px); }
    40% { transform: translateY(0); }
  }
`;

interface MessageListProps {
  messages: Message[];
  isDarkMode: boolean;
  onPromptSelect: (prompt: string) => void;
  onScroll: (isUserScrolling: boolean) => void;
  isTyping?: boolean;
}

const primaryColor = "#e89a3c";

const TypingIndicator: React.FC<{ isTyping: boolean; isDarkMode: boolean }> = ({
  isTyping,
  isDarkMode,
}) => {
  const [currentWord, setCurrentWord] = useState(0);
  const words = [
    "Thinking",
    "Retrieving Information",
    "Reasoning",
    "Preparing response",
  ];

  useEffect(() => {
    const getRandomInterval = () => Math.random() * (4000 - 2000) + 2000;

    const changeWord = () => {
      setCurrentWord((prev) => {
        if (prev === words.length - 1) {
          return prev; // Stay on Processing
        }
        return prev + 1;
      });

      // Schedule next change if not at the last word and still typing
      if (currentWord < words.length - 1 && isTyping) {
        setTimeout(changeWord, getRandomInterval());
      }
    };

    // Start the sequence if typing
    if (isTyping) {
      const timeoutId = setTimeout(changeWord, getRandomInterval());
      return () => clearTimeout(timeoutId);
    }
  }, [currentWord, words.length, isTyping]);

  const textColor = isDarkMode ? "text-gray-400" : "text-gray-800";
  const dotColor = isDarkMode ? "bg-gray-400" : "bg-gray-800";

  return (
    <div className="flex items-baseline gap-0.5">
      <style>{bounceKeyframes}</style>
      <span
        className={`${textColor} animate-pulse`}
        style={{ animationDuration: "1.5s" }}
      >
        {words[currentWord]}
      </span>
      <div className="flex gap-0.5">
        <div
          className={`w-[3px] h-[3px] rounded-full ${dotColor} animate-pulse`}
          style={{
            animationDuration: "2s",
            animation: "customBounce 2s infinite, pulse 1.5s infinite",
          }}
        ></div>
        <div
          className={`w-[3px] h-[3px] rounded-full ${dotColor} animate-pulse`}
          style={{
            animationDuration: "2s",
            animation: "customBounce 2s infinite, pulse 1.5s infinite",
            animationDelay: "0.4s",
          }}
        ></div>
        <div
          className={`w-[3px] h-[3px] rounded-full ${dotColor} animate-pulse`}
          style={{
            animationDuration: "2s",
            animation: "customBounce 2s infinite, pulse 1.5s infinite",
            animationDelay: "0.8s",
          }}
        ></div>
      </div>
    </div>
  );
};

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isDarkMode,
  onPromptSelect,
  onScroll,
  isTyping = false,
}) => {
  const messageContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTo({
        top: messageContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, []);

  const handleScroll = useCallback(() => {
    if (messageContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } =
        messageContainerRef.current;
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 50;
      onScroll(!isAtBottom);
    }
  }, [onScroll]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  return (
    <div
      className="h-full overflow-auto p-4"
      ref={messageContainerRef}
      onScroll={handleScroll}
    >
      {messages.length === 0 && (
        <DefaultPrompts
          onPromptSelect={onPromptSelect}
          isDarkMode={isDarkMode}
          cardBackground={isDarkMode ? "#1f1f1f" : "#f0f2f5"}
        />
      )}

      {messages.map((msg, index) => (
        <div key={index} className="my-2 pb-1">
          {msg.role === "user" ? (
            <div
              className="inline-block p-2 px-4 break-words rounded-lg text-white"
              style={{
                backgroundColor: primaryColor,
                maxWidth: "85%",
              }}
            >
              {msg.content}
            </div>
          ) : (
            <Card
              className="inline-block rounded-lg shadow-md text-black w-full break-words"
              style={{
                backgroundColor: isDarkMode ? "#1f1f1f" : "#f0f2f5",
              }}
            >
              {msg.content ? (
                <MarkdownRenderer content={msg.content} />
              ) : isTyping ? (
                <TypingIndicator isTyping={isTyping} isDarkMode={isDarkMode} />
              ) : null}
            </Card>
          )}
        </div>
      ))}
    </div>
  );
};
