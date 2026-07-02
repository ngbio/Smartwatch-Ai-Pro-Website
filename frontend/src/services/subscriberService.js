import Apis, { endpoints } from "../configs/Apis";

// TODO: Submit subscriber form data to the backend later.
export function subscribe() {
  return Apis.post(endpoints.subscribers);
}

// TODO: Fetch subscribers for testing/admin use later.
export function getSubscribers() {
  return Apis.get(endpoints.subscribers);
}
