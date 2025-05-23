import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";

// ====================== user-profile services ====================
export const userServices = {
    async getCurrentUser() {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/current/user/`,
                methodType: 'get',
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
    async getAllUserList() {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/all/users/`,
                methodType: 'get',
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
    },
    async updateUser(id, payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/users/${id}/`,
                methodType: 'put',
                payload: payload,
                queryParams: {},
                headers: {}
            });
            return response;
        } catch (error) {
            const { messages } = errorHandlerUtility.handleError(error);
            throw messages;
        }
    },
    async changePassword(id, payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: `/users/${id}/change-password/`,
                methodType: 'patch',
                payload: payload,
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
