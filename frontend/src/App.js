import { lazy, Suspense, useEffect, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./screens/home/Home";
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

const ProductDetails = lazy(() => import("./screens/home/ProductDetails"));
const Subscribe = lazy(() => import("./screens/subscribe/Subscribe"));

function App() {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme === "light" || savedTheme === "dark" ? savedTheme : "dark";
  });

  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(currentTheme => currentTheme === "dark" ? "light" : "dark");
  }

  return (
    <BrowserRouter>
      <Header theme={theme} onToggleTheme={toggleTheme} />

      <main className="container main-container">
        <Suspense fallback={null}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/product" element={<ProductDetails />} />
            <Route path="/subscribe" element={<Subscribe />} />
          </Routes>
        </Suspense>
      </main>

      <Footer />
    </BrowserRouter>
  );
}

export default App;
