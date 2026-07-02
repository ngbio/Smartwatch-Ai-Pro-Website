import Footer from "./components/Footer";
import Header from "./components/Header";
import Home from "./screens/home/Home";

// TODO: Keep the main application shell inspired by the reference project.
function App() {
  return (
    <div>
      <Header />
      <main>
        <Home />
      </main>
      <Footer />
    </div>
  );
}

export default App;
