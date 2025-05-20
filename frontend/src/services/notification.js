import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

// ====================== user-profile services ====================
export const notificationService = {
    async getNotifications(params) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/notifications/`,
                methodType: 'get',
                payload: {},
                queryParams: params,
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async clearAllNotifications() {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/notifications/mark-as-read/`,
                methodType: 'post',
                payload: {},
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
}
