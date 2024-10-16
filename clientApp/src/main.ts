import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import '@/assets/less/index.less'
import App from './App.vue'
const app= createApp(App)
app.use(ElementPlus)
app.mount('#app')
