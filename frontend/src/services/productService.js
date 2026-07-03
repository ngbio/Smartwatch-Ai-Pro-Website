import Apis, { endpoints } from "../configs/Apis";

export function getProduct() {
    return Apis.get(endpoints['product']);
}
