import Vue from 'vue'
import Vuetify from 'vuetify'
import VueFlip from 'vue-flip'
import App from './App'
import router from './router'
import colors from 'vuetify/es5/util/colors'



Vue.config.productionTip = false

Vue.use(VueFlip);
Vue.use(Vuetify, {
  theme: {
    primary: colors.blue.darken4,
    secondary: colors.amber.lighten2
  }
})


export const dataBus = new Vue();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
