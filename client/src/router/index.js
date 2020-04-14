import Vue from "vue";
import VueRouter from "vue-router";
import store from '../store'

Vue.use(VueRouter);

const routes = [{
    path: "/",
    name: "Home",
    component: () =>
      import("../views/Home.vue"),
    beforeEnter: (to, from, next) => {
      if (store.state.isAuthenticated !== true) {
        next('/login')
      } else {
        next()
      }
    }
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import("../views/Login.vue"),
    beforeEnter: (to, from, next) => {
      if (store.state.isAuthenticated !== true) {
        next()
      } else {
        next("/")
      }
    }
  }, {
    path: "/signup",
    name: "Signup",
    component: () =>
      import("../views/Signup.vue"),
    beforeEnter: (to, from, next) => {
      if (store.state.isAuthenticated !== true) {
        next()
      } else {
        next("/")
      }
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;