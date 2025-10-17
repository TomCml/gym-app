import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import loader from './components/Loader.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faList,
  faDumbbell,
  faCirclePlay,
  faSquarePollVertical,
} from '@fortawesome/free-solid-svg-icons'
import { faHouse, faUser } from '@fortawesome/free-regular-svg-icons'

library.add(faHouse, faDumbbell, faList, faUser, faCirclePlay, faSquarePollVertical)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('Loader', loader)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
