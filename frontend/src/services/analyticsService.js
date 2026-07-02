import Apis, { endpoints } from "../configs/Apis";

// TODO: Track landing page analytics events later.
export function trackEvent() {
  return Apis.post(endpoints.analytics);
}
