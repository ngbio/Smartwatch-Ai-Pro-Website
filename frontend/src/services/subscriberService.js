import Apis, { endpoints } from "../configs/Apis";

export function subscribe(data) {
    return Apis.post(endpoints['subscribers'], data);
}

export function getSubscribers() {
    return Apis.get(endpoints['subscribers']);
}
