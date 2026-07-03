import { useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import { sendMessage } from "../services/chatbotService";
import MySpinner from "./MySpinner";

function Chatbot() {
  const [opened, setOpened] = useState(false);
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([
    {
      question: "",
      answer: "Xin chào! Mình có thể tư vấn về tính năng, giá và thông số sản phẩm.",
    },
  ]);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  const chat = async (e) => {
    e.preventDefault();

    if (!message.trim())
      return;

    try {
      setLoading(true);
      setErr("");

      let currentMessage = message;
      setMessage("");

      let res = await sendMessage(currentMessage);
      setHistory([
        { question: currentMessage, answer: res.data.reply },
        ...history,
      ]);
    } catch (ex) {
      setErr("Chatbot chưa phản hồi được. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="floating-chatbot">
      {opened === true && (
        <section className="chatbot-box">
          <div className="chatbot-header">
            <strong>Tư vấn bằng AI</strong>
            <Button variant="outline-light" size="sm" onClick={() => setOpened(false)}>Đóng</Button>
          </div>

          {err && <Alert variant="danger" className="mt-2 mb-2">{err}</Alert>}

          <div className="chatbot-history">
            {history.map((item, index) => (
              <div className="chat-message" key={index}>
                {item.question && <p><strong>Bạn:</strong> {item.question}</p>}
                <p className="mb-0"><strong>AI:</strong> {item.answer}</p>
              </div>
            ))}
          </div>

          <Form className="d-flex gap-2 mt-2" onSubmit={chat}>
            <Form.Control
              placeholder="Hỏi về sản phẩm..."
              value={message}
              onChange={e => setMessage(e.target.value)}
            />
            {loading === true ? <MySpinner /> : <Button variant="info" type="submit">Gửi</Button>}
          </Form>
        </section>
      )}

      {opened === false && (
        <Button variant="info" className="chatbot-toggle" onClick={() => setOpened(true)}>
          Chatbot
        </Button>
      )}
    </div>
  );
}

export default Chatbot;
