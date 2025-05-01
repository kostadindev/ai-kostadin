import { useState, useEffect } from "react";
import Chat from "./components/Chat";
import { ConfigProvider, theme } from "antd";

const App = () => {
  const [currentTheme, setCurrentTheme] = useState<string>(
    localStorage.getItem("theme") || "dark"
  );

  useEffect(() => {
    const handleThemeChange = () => {
      setCurrentTheme(localStorage.getItem("theme") || "dark");
    };
    window.addEventListener("themeChanged", handleThemeChange);
    return () => window.removeEventListener("themeChanged", handleThemeChange);
  }, []);

  return (
    <ConfigProvider
      theme={{
        algorithm:
          currentTheme === "light"
            ? theme.defaultAlgorithm
            : theme.darkAlgorithm,
        token: {
          colorPrimary: "#e89a3c",
          borderRadius: 4, // More rounded corners for all components
        },
        components: {
          Layout: {
            headerBg: currentTheme === "light" ? "#f0f2f5" : "#1f1f1f",
            headerColor: currentTheme === "light" ? "#000000" : "#ffffff",
            bodyBg: currentTheme === "light" ? "#f0f2f5" : "#121212",
            siderBg: currentTheme === "light" ? "#ffffff" : "#1f1f1f",
          },
          Card: {
            borderRadius: 16,
            boxShadow:
              currentTheme === "light"
                ? "0 4px 12px rgba(0, 0, 0, 0.05)"
                : "0 4px 12px rgba(255, 255, 255, 0.05)",
            colorBorderSecondary:
              currentTheme === "light" ? "#d9d9d9" : "rgba(255, 255, 255, 0.1)",
          },
        },
      }}
    >
      <div className="App w-screen h-screen">
        <Chat />
      </div>
    </ConfigProvider>
  );
};

export default App;
