import React from "react";
import { Card } from "antd";

interface Props {
  onPromptSelect: (prompt: string) => void;
  isDarkMode: boolean;
  cardBackground: string;
}

const prompts = [
  "What’s Kostadin working on?",
  "Explain his honors thesis on Recursive QA.",
  "What formal machine learning courses has Kostadin taken?",
  "What is Deep Gestures about?",
];

const DefaultPrompts: React.FC<Props> = ({
  onPromptSelect,
  cardBackground,
}) => {
  return (
    <div className="flex flex-1 flex-col justify-end items-center text-center px-6 pb-8 max-w-2xl mx-auto h-full">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        {prompts.map((prompt, idx) => (
          <Card
            key={idx}
            hoverable
            onClick={() => onPromptSelect(prompt)}
            style={{
              backgroundColor: cardBackground,
            }}
            bodyStyle={{ padding: "16px" }}
          >
            {prompt}
          </Card>
        ))}
      </div>
    </div>
  );
};

export default DefaultPrompts;
