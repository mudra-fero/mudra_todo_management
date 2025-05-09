import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

// ====================== task services ====================
export const taskServices = {
    async getTaskList(params) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/tasks/`,
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
}
