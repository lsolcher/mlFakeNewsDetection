import Vue from 'vue'
import Router from 'vue-router'
import Vuetify from 'vuetify'
import VueFlip from 'vue-flip'
const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '*', component: 'NotFound' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)
Vue.use(VueFlip);
Vue.use(Vuetify);

export default new Router({
  routes,
  mode: 'history'
})
