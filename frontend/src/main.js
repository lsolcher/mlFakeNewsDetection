import Vue from 'vue'
import Vuetify from 'vuetify'
import VueFlip from 'vue-flip'
import App from './App'
import router from './router'

Vue.config.productionTip = false

Vue.use(VueFlip);
Vue.use(Vuetify);


export const dataBus = new Vue();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
