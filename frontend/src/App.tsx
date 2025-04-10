import { useState, useEffect } from "react";
import Chat from "./components/chat";
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
          borderRadius: 4,
        },
        components: {
          Layout: {
            headerBg: currentTheme === "light" ? "#f0f2f5" : "#1f1f1f",
            headerColor: currentTheme === "light" ? "#f0f2f5" : "#ffffff",
            bodyBg: currentTheme === "light" ? "#f0f2f5" : "#121212",
            siderBg: "#fff",
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
