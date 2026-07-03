import { useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import { subscribe } from "../services/subscriberService";
import { validateSubscriber } from "../utils/subscriberValidator";
import MySpinner from "./MySpinner";

function SubscribeForm() {
  const [form, setForm] = useState({ full_name: "", email: "", phone: "" });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const [variant, setVariant] = useState("info");
  const [loading, setLoading] = useState(false);

  const updateForm = (field, value) => {
    setForm({ ...form, [field]: value });
    setErrors({ ...errors, [field]: "" });
  };

  const registerSubscriber = async (e) => {
    e.preventDefault();
    const result = validateSubscriber(form);

    if (!result.isValid) {
      setErrors(result.errors);
      setVariant("danger");
      setMessage("Vui lòng kiểm tra lại thông tin đăng ký.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const res = await subscribe(result.data);
      setVariant(res.data.success ? "success" : "danger");
      setMessage(res.data.message);

      if (res.data.success === true) {
        setForm({ full_name: "", email: "", phone: "" });
        setErrors({});
      }
    } catch (ex) {
      setVariant("danger");
      setMessage(ex.response?.data?.message || "Đăng ký nhận tin chưa thành công.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section-block subscribe-panel reveal">
      <div className="section-heading">
        <span className="section-kicker">Stay in the loop</span>
        <h2 className="section-title">Đăng ký nhận tin</h2>
        <p>Nhận thông tin mới nhất, chương trình mở bán và tư vấn sản phẩm.</p>
      </div>

      {message && <Alert variant={variant}>{message}</Alert>}

      <Form noValidate onSubmit={registerSubscriber}>
        <Form.Group className="mb-3">
          <Form.Label>Họ tên</Form.Label>
          <Form.Control
            placeholder="Nguyen Van A"
            value={form.full_name}
            onChange={e => updateForm("full_name", e.target.value)}
            isInvalid={Boolean(errors.full_name)}
            required
          />
          <Form.Control.Feedback type="invalid">
            {errors.full_name}
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control
            placeholder="email@example.com"
            type="email"
            value={form.email}
            onChange={e => updateForm("email", e.target.value)}
            isInvalid={Boolean(errors.email)}
            required
          />
          <Form.Control.Feedback type="invalid">
            {errors.email}
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Số điện thoại</Form.Label>
          <Form.Control
            placeholder="0901234567"
            value={form.phone}
            onChange={e => updateForm("phone", e.target.value)}
            isInvalid={Boolean(errors.phone)}
          />
          <Form.Control.Feedback type="invalid">
            {errors.phone}
          </Form.Control.Feedback>
        </Form.Group>
        {loading === true ? <MySpinner /> : <Button variant="info" type="submit">Đăng ký</Button>}
      </Form>
    </section>
  );
}

export default SubscribeForm;
