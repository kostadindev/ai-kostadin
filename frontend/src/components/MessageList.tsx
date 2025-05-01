import React, { useRef, useCallback, useEffect } from "react";
import { Card } from "antd";
import { Message } from "../types/chat";
import MarkdownRenderer from "./MarkdownRenderer";
import DefaultPrompts from "./DefaultPrompts";

interface MessageListProps {
  messages: Message[];
  isDarkMode: boolean;
  onPromptSelect: (prompt: string) => void;
  onScroll: (isUserScrolling: boolean) => void;
}

const primaryColor = "#e89a3c";

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isDarkMode,
  onPromptSelect,
  onScroll,
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
              <MarkdownRenderer content={msg.content} />
            </Card>
          )}
        </div>
      ))}
    </div>
  );
};
