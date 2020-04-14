import Vue from "vue";
import Vuex from "vuex";
import VuexPersist from "vuex-persist";
import {
  HTTP
} from "../config/axios"
import todoReducer from './modules/todoReducer'
import messageReducer from './modules/messageReducer'


Vue.use(Vuex);

const vuexLocalStorage = new VuexPersist({
  key: "vuex", // The key to store the state on in the storage provider.
  storage: window.localStorage, // or window.sessionStorage or localForage
  // Function that passes the state and returns the state with only the objects you want to store.
  reducer: state => ({
    todos: state.todos,
    isAuthenticated: state.isAuthenticated,
    loading: state.loading,
    user: state.user,
    token: state.token,
    message: state.message,
    validationRequired: state.validationRequired
  })
});

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",
  state: {
    isAuthenticated: false,
    loading: false,
    user: {},
    token: "",
    error: null,
    validationRequired: false
  },
  getters: {
    isAuthenticated: (state) => {
      return state.isAuthenticated
    },
    accountValidated: state => {
      return state.validationRequired
    },
    loading: state => {
      return state.loading
    },
  },
  mutations: {
    // login
    loginReducer: (state, payload) => {
      state.user = payload;
    },
    clearUser: (state) => {
      state.user = {}
    },
    loginError: (state, payload) => {
      state.error = payload;
    },

    // token management
    setTokenReducer: (state, payload) => {
      state.token = payload;
    },
    clearTokenReducer: state => {
      state.token = "";
    },

    // error management
    setErrorReducer: (state, payload) => {
      state.error = payload;
    },
    clearErrorReducer: state => {
      state.error = null;
    },

    // isAuthenticated
    setAuthenticationReducer: (state, payload) => {
      state.isAuthenticated = payload;
    },

    // validationRequired
    setValidationReducer: (state, payload) => {
      state.validationRequired = payload;
    },

    // loader
    setLoaderReducer: (state, payload) => {
      state.loading = payload;
    },
  },
  actions: {
    // account management
    loginAction: async (context, payload) => {
      await HTTP.post("/login", payload)
        .then(res => {
          console.log(res.data);
          context.commit("setTokenReducer", res.data.data["token"]);
          context.commit("setTodosReducer", res.data.data["todos"]);
          context.dispatch("setMessageAction", res.data["message"]);

          delete res.data.data["password"];
          delete res.data.data["todos"];
          delete res.data.data["token"];
          context.commit("loginReducer", res.data.data);
          context.dispatch("setAuthentication", true);

          // reset loader
          setTimeout(() => {
            context.dispatch("setLoader", false)
          }, 1000)
        })
        .catch(err => {
          console.log(err.response.data);
          context.commit("loginError", err.response.data.error);

          // reset loader
          setTimeout(() => {
            context.dispatch("setLoader", false)
          }, 500)
        });
    },
    signupAction: async (context, payload) => {
      await HTTP.post("/signup", payload)
        .then(res => {
          console.log(res.data);
          context.dispatch("setMessageAction", res.data["message"]);
          context.dispatch("setAccountValidator", true);

          // reset loader
          setTimeout(() => {
            context.dispatch("setLoader", false)
          }, 1000)
        })
        .catch(err => {
          console.log(err.response.data);
          context.dispatch("setError", err.response.data.error);

          // reset loader
          setTimeout(() => {
            context.dispatch("setLoader", false)
          }, 500)
        });
    },

    validateAccount: async (context, payload) => {
      await HTTP.put('/account_confirmation', payload)
        .then(res => {
          console.log(res.data)
          context.dispatch("setMessageAction", res.data["message"]);
          context.dispatch("setAccountValidator", false);

          // reset loader
          setTimeout(() => {
            context.dispatch("setLoader", false)
          }, 1000)
        })
        .catch(err => {
          console.log(err.response.data);
          context.dispatch("setError", err.response.data.error);

          // reset loader
          setTimeout(() => {
            context.dispatch("setLoader", false)
          }, 500)
        })
    },

    logout: (context) => {
      context.dispatch('setLoader', true)
      context.dispatch('setAuthentication', false)
      context.dispatch('setLoader', false)
      context.commit('clearTokenReducer')
      context.commit('clearErrorReducer')
      context.commit('clearUser')
      context.dispatch('setMessageAction', 'Logout was successful')

    },

    setAuthentication: (context, payload) => {
      context.commit('setAuthenticationReducer', payload)
    },

    setAccountValidator: (context, payload) => {
      context.commit('setValidationReducer', payload)
    },

    setLoader: (context, payload) => {
      context.commit('setLoaderReducer', payload)
    },

    // error actions
    setError: (context, payload) => {
      context.commit("setErrorReducer", payload);
    },
    clearError: context => {
      context.commit("clearErrorReducer");
    }
  },
  modules: {
    todos: todoReducer,
    message: messageReducer
  },
  plugins: [vuexLocalStorage.plugin]
});