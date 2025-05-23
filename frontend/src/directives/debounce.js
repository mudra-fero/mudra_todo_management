import { debounce } from 'lodash';

export default {
    mounted(el, binding) {
        const event = binding.arg || 'input';
        const { handler, delay = 300 } = binding.value;

        if (typeof handler !== 'function') {
            return;
        }

        const debouncedHandler = debounce(handler, delay);

        el.__debounce_listener__ = debouncedHandler;
        el.addEventListener(event, debouncedHandler);
    },

    unmounted(el, binding) {
        const event = binding.arg || 'input';
        if (el.__debounce_listener__) {
            el.removeEventListener(event, el.__debounce_listener__);
            delete el.__debounce_listener__;
        }
    }
};
