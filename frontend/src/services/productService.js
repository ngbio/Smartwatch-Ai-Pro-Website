import Apis, { endpoints } from "../configs/Apis";

// TODO: Fetch SmartWatch AI Pro product information from the backend later.
export function getProduct() {
  return Apis.get(endpoints.product);
}
