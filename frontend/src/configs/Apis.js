import axios from "axios";

// TODO: Store backend endpoint paths for the SmartWatch AI Pro frontend.
export const endpoints = {
  product: "/product",
  features: "/features",
  specifications: "/specifications",
  subscribers: "/subscribers",
  chat: "/chat",
  analytics: "/analytics",
};

// TODO: Configure the shared Axios client for API calls.
const Apis = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api",
});

export default Apis;
