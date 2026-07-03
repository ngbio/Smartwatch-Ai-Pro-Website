export function normalizeSubscriber(form) {
  return {
    full_name: form.full_name.trim().replace(/\s+/g, " "),
    email: form.email.trim().toLowerCase(),
    phone: form.phone.trim(),
  };
}

export function validateSubscriber(form) {
  const data = normalizeSubscriber(form);
  const errors = {};

  if (!data.full_name) {
    errors.full_name = "Vui lòng nhập họ tên.";
  } else if (data.full_name.length < 2) {
    errors.full_name = "Họ tên cần có ít nhất 2 ký tự.";
  } else if (!/^[A-Za-zÀ-ỹ\s'.-]+$/.test(data.full_name)) {
    errors.full_name = "Họ tên không nên chứa số hoặc ký tự đặc biệt.";
  }

  if (!data.email) {
    errors.email = "Vui lòng nhập email.";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.email = "Email không hợp lệ.";
  }

  if (data.phone && !/^(0|\+84)[0-9]{9}$/.test(data.phone)) {
    errors.phone = "Số điện thoại phải bắt đầu bằng 0 hoặc +84 và có đúng 10 chữ số Việt Nam.";
  }

  return {
    data,
    errors,
    isValid: Object.keys(errors).length === 0,
  };
}
