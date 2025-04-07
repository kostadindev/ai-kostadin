import React from "react";
import { Card, Typography } from "antd";

const { Title, Paragraph } = Typography;

interface Props {
  onPromptSelect: (prompt: string) => void;
}

const prompts = [
  "What’s Kostadin working on?",
  "Explain his honors thesis on Recursive QA.",
  "Which ML courses has Kostadin taken?",
  "What is Deep Gestures about?",
];

const DefaultPrompts: React.FC<Props> = ({ onPromptSelect }) => {
  return (
    <div className="flex flex-col items-center text-center p-6 max-w-2xl mx-auto">
      <Paragraph className="text-gray-600 dark:text-gray-300 mb-6">
        Ask about Kostadin’s work, education, or research.
      </Paragraph>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        {prompts.map((prompt, idx) => (
          <Card
            key={idx}
            className="hover:shadow-lg cursor-pointer transition"
            onClick={() => onPromptSelect(prompt)}
          >
            {prompt}
          </Card>
        ))}
      </div>
    </div>
  );
};

export default DefaultPrompts;
