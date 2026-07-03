import axios from "axios";

export const endpoints = {
    'product': '/product',
    'subscribers': '/subscribers',
    'chat': '/chat',
};

export default axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:5000/api"
})
