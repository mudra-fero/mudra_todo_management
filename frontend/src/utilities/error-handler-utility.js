import { removeUnderScoreAndCapitalize } from "./helpers-utility";

/**
 * Utility for handling errors from API responses.
 * Specifically designed to process errors from Django and Django Rest Framework (DRF) backends.
 */

export const errorHandlerUtility = {
    /**
     * Processes an error object to extract meaningful information such as status code and error messages.
     *
     * @param {Object} error - The error object typically returned from Axios.
     * @returns {Object} - An object containing:
     *  - `statusCode` {number}: The HTTP status code of the error.
     *  - `messages` {Array<string>}: A list of user-friendly error messages.
     */
    handleError(error) {

        let statusCode = 500; // Default status code for unexpected errors
        let messages = ["An unexpected error occurred. Please try again later."]; // Default error message

        if (error.response) {
            // Extract HTTP status code from the response
            statusCode = error.response.status;

            // Extract error details from Django/DRF's common error response structures
            let responseData = error.response.data;


            /* for mobile app errors -> some endpoints have the structure like:
            *    {  
            *        "errors":{
            *            "non_field_errors" : [ "Error Message"  ],
            *            "field_errors" : [  "Error message"  ],
            *        }
            *    }
            * 
            */
            if (responseData.errors) {
                responseData = responseData.errors;
            }

            if (responseData.detail) {
                // Handle DRF's standard error messages (e.g., authentication errors)
                messages = [responseData.detail];
            } else if (typeof responseData === "object" && !Array.isArray(responseData)) {
                // Handle field-level validation errors, non-field errors, or complex error objects
                const fieldErrors = Object.entries(responseData)
                    .filter(([key]) => key !== "non_field_errors") // Exclude non-field errors temporarily
                    .flatMap(([field, errors]) => errors.map((message) => `${removeUnderScoreAndCapitalize(field)}: ${message}`));

                const nonFieldErrors = responseData.non_field_errors || []; // Extract non-field errors if they exist

                // Combine field and non-field errors
                messages = [...nonFieldErrors, ...fieldErrors];
            }
        } else if (error.request) {
            // Handle network or server connectivity issues
            messages = ["Network error. Please check your connection."];
        } else {
            // Handle unexpected errors with a fallback message
            messages = [error.message || messages[0]];
        }

        return { statusCode, messages };
    },


    /**
     * Processes errors specifically for bulk uploads.
     *
     * @param {Object} error - The error object typically returned from Axios.
     * @returns {Object} - An object containing:
     *  - `statusCode` {number}: The HTTP status code of the error.
     *  - `messages` {Object or Array<string>}: The raw error response data.
     */
    handleErrorForBulkUpload(error) {
        const statusCode = error.response.status || 500;
        const messages = error.response.data || { message: "An unexpected error occurred." };
        return { statusCode, messages };
    },
};