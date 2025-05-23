import { authenticationService } from "@/services/authentication";
import axios from "axios";
import { localStorageUtility } from "./local-storage-utility";


// Create an Axios instance with a base URL
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Set up request interceptor to add authorization token to headers
axiosInstance.interceptors.request.use((config) => {
  const token = localStorageUtility.getItemFromLocalStorage('access_token');  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Set up response interceptor to handle 401 errors (Unauthorized)
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (err) => {
    if (err.response && err.response.status === 401) {
      authenticationService.logout();
    }
    return Promise.reject(err);
  }
);

// Wrapper for API calls that supports various HTTP methods, query parameters, and custom headers
export const axiosUtility = {
  async getResponse({ apiName, methodType, payload = {}, queryParams = {}, headers = {} }) {
    try {
      let response;

      const config = {
        headers: { ...axiosInstance.defaults.headers.common, ...headers },
        params: queryParams,
      };

      // Switch statement to handle different HTTP methods
      switch (methodType.toLowerCase()) {
        case "get":
          response = await axiosInstance.get(apiName, config);
          break;
        case "post":
          response = await axiosInstance.post(apiName, payload, config);
          break;
        case "put":
          response = await axiosInstance.put(apiName, payload, config);
          break;
        case "patch":
          response = await axiosInstance.patch(apiName, payload, config);
          break;
        case "delete":
          response = await axiosInstance.delete(apiName, { data: payload }, config);
          break;
        default:
          throw new Error(`Unsupported HTTP method: ${methodType}`);
      }
      return response;
    } catch (error) {
      throw error;
    }
  },
};