import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import '@/assets/less/index.less'
import App from './App.vue'
import router from './router/index'
const app= createApp(App)
app.use(ElementPlus)
app.use(router).mount('#app')
