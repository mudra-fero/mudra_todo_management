import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import debounce from './directives/debounce';

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App)
app.directive('debounce', debounce);
app.use(vuetify);
app.component('VueDatePicker', VueDatePicker);
app.use(router);
app.mount('#app');