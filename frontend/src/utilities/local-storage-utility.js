/**
 * Utility functions for interacting with localStorage.
 */
export const localStorageUtility = {
    /**
     * Retrieves an item from localStorage.
     * If the item exists, it is parsed from JSON and returned.
     * If the item does not exist or an error occurs, returns null.
     * 
     * @param {string} key - The key of the item to retrieve from localStorage.
     * @returns {any|null} - The parsed value from localStorage or null if the item doesn't exist or an error occurs.
     */
    getItemFromLocalStorage(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error(`Error reading key "${key}" from localStorage:`, error);
        }
    },

    /**
     * Sets an item in localStorage.
     * If the value is an object, it is serialized into a JSON string.
     * 
     * @param {string} key - The key under which to store the item.
     * @param {any} value - The value to store in localStorage. Can be any type, but if it's an object, it will be stringified.
     */
    setItemToLocalStorage(key, value) {
        try {
            const valueToStore = (typeof value === String) ? value : JSON.stringify(value);
            localStorage.setItem(key, valueToStore);
        } catch (error) {
            console.error(`Error setting key "${key}" in localStorage:`, error);
        }
    },

    /**
     * Removes an item from localStorage.
     * 
     * @param {string} key - The key of the item to remove from localStorage.
     */
    removeItemFromLocalStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error(`Error removing key "${key}" from localStorage:`, error);
        }
    },

    /**
     * Clears all items from localStorage.
     * This will remove every key-value pair in localStorage.
     */
    clearLocalStorage() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error("Error clearing localStorage:", error);
        }
    }
}