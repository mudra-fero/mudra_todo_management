import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export const toastUtility = {
    /**
     * Shows an error message using vue-3-toastify.
     * @param {string} message - The message to display.
     */
    showError(messages, options = {}) {

        const svgIcon = `<?xml version="1.0" ?><!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.0//EN'  'http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd'><svg height="14" style="padding-top:1px;overflow:visible;enable-background:new 0 0 32 32" viewBox="0 0 32 32" width="14" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g><g id="Error_1_"><g id="Error"><circle cx="16" cy="16" id="BG" r="16" style="fill:#D72828;"/><path d="M14.5,25h3v-3h-3V25z M14.5,6v13h3V6H14.5z" id="Exclamatory_x5F_Sign" style="fill:#E6E6E6;"/></g></g></g></svg>`;

        const formattedMessage = Array.isArray(messages)
            ? messages.map((msg) => `<span style="font-size: 16px; margin-right: 8px;">${svgIcon}</span>${msg} <br>`).join("") // Replace bullet points with a custom icon
            : `<span style="font-size: 16px; margin-right: 8px;">${svgIcon}</span>${messages}`; // Single message with custom icon

        toast.error(
            `<ul style="font-size: large">${formattedMessage}</ul>`,
            {
                position: "top-right", // Position in the center
                autoClose: 5000, // Disable automatic timeout
                closeOnClick: false, // Allow user to close manually
                pauseOnHover: true, // Keep toast visible while hovering
                draggable: false, // Disable drag for better readability
                closeButton: true, // Ensure the close button is visible
                dangerouslyHTMLString: true,
                style: {
                    width: "auto", // Automatically adjust width based on content
                    maxWidth: "90%", // Limit the maximum width for better readability on larger screens
                },
                hideProgressBar: true,
                theme: "dark",
                icon: false,
                ...options
            }
        );
    },

    /**
     * Shows a success message using vue-3-toastify.
     * @param {string} message - The message to display.
     */
    showSuccess(message, options = {}) {
        toast.success(message, {
            position: "top-right", // Default position for success
            autoClose: 2000, // Default timeout
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true,
            style: {
                width: "auto", // Automatically adjust width based on content
                maxWidth: "90%", // Limit the maximum width for better readability on larger screens
            },
            hideProgressBar: true,
            theme: "dark",
            ...options
        });
    },

    /**
     * Shows an informational message using vue-3-toastify.
     * @param {string} message - The message to display.
     */
    showInfo(message, options={}) {
        toast.info(message, {
            position: "top-right", // Default position for info
            autoClose: 2000,
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true,
            style: {
                width: "auto", // Automatically adjust width based on content
                maxWidth: "90%", // Limit the maximum width for better readability on larger screens
            },
            hideProgressBar: true,
            theme: "dark",
            ...options
        });
    },
};
