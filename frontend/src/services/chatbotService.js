import Apis, { endpoints } from "../configs/Apis";

// TODO: Send chatbot messages to the backend later.
export function sendMessage() {
  return Apis.post(endpoints.chat);
}
