import { useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import { subscribe } from "../../services/subscriberService";
import { validateSubscriber } from "../../utils/subscriberValidator";

const Subscribe = () => {
    const [form, setForm] = useState({ full_name: "", email: "", phone: "" });
    const [errors, setErrors] = useState({});
    const [message, setMessage] = useState("");
    const [variant, setVariant] = useState("info");

    const updateForm = (field, value) => {
        setForm({ ...form, [field]: value });
        setErrors({ ...errors, [field]: "" });
    };

    const submit = async (e) => {
        e.preventDefault();
        const result = validateSubscriber(form);

        if (!result.isValid) {
            setErrors(result.errors);
            setVariant("danger");
            setMessage("Vui lòng kiểm tra lại thông tin đăng ký.");
            return;
        }

        try {
            const res = await subscribe(result.data);
            setVariant(res.data.success ? "success" : "danger");
            setMessage(res.data.message);

            if (res.data.success === true) {
                setForm({ full_name: "", email: "", phone: "" });
                setErrors({});
            }
        } catch (ex) {
            setVariant("danger");
            setMessage(ex.response?.data?.message || "Đăng ký chưa thành công.");
        }
    };

    return (
        <>
            <h1 className="text-center text-info mt-3">Đăng ký nhận tin</h1>
            {message && <Alert variant={variant}>{message}</Alert>}
            <Form noValidate className="form-panel" onSubmit={submit}>
                <Form.Group className="mb-3">
                    <Form.Label>Họ tên</Form.Label>
                    <Form.Control
                        value={form.full_name}
                        onChange={e => updateForm("full_name", e.target.value)}
                        isInvalid={Boolean(errors.full_name)}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.full_name}
                    </Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        value={form.email}
                        onChange={e => updateForm("email", e.target.value)}
                        isInvalid={Boolean(errors.email)}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.email}
                    </Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Số điện thoại</Form.Label>
                    <Form.Control
                        value={form.phone}
                        onChange={e => updateForm("phone", e.target.value)}
                        isInvalid={Boolean(errors.phone)}
                    />
                    <Form.Control.Feedback type="invalid">
                        {errors.phone}
                    </Form.Control.Feedback>
                </Form.Group>
                <Button variant="info" type="submit">Đăng ký</Button>
            </Form>
        </>
    );
};

export default Subscribe;
