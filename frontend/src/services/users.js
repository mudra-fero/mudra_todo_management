import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

// ====================== user-profile services ====================
export const userServices = {
    async getUserList(params) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/users/`,
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
    async deleteUser(id) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/users/${id}/`,
                methodType: 'delete',
                payload: {},
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    }
}
