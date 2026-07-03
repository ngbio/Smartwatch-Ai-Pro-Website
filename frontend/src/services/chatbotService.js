import Apis, { endpoints } from "../configs/Apis";

export function sendMessage(message) {
    return Apis.post(endpoints['chat'], { message });
}
