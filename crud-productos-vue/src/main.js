import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import '@/assets/css/app.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

createApp(App).use(router).use(i18n).mount('#app')
