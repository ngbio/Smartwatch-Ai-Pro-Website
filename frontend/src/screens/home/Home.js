import Chatbot from "../../components/Chatbot";
import Features from "../../components/Features";
import Hero from "../../components/Hero";
import Specifications from "../../components/Specifications";
import SubscribeForm from "../../components/SubscribeForm";

// TODO: Compose all SmartWatch AI Pro landing page sections.
function Home() {
  return (
    <>
      <Hero />
      <Features />
      <Specifications />
      <SubscribeForm />
      <Chatbot />
    </>
  );
}

export default Home;
