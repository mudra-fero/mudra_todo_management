import router from "@/router";
import { axiosUtility } from "@/utilities/axios-utility";
import { errorHandlerUtility } from "@/utilities/error-handler-utility";
import { localStorageUtility } from "@/utilities/local-storage-utility";

export const authenticationService = {

    async register(payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: '/users/',
                methodType: 'post',
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

    async login(payload) {
        try {
            const response = await axiosUtility.getResponse({
                apiName: '/login/',
                methodType: 'post',
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
    async logout() {
        localStorageUtility.clearLocalStorage();
        router.push({ name: 'login' });
    }
}