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
// import VueDebounce from 'vue-debounce'

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App)

app.use(vuetify);
app.component('VueDatePicker', VueDatePicker);
// app.use(VueDebounce, {
//     lock: true,
//     defaultTime: '500ms',
//   })  
app.use(router);
app.mount('#app');