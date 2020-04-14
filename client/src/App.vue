<template>
  <div id="app">
    <loading
      :active.sync="this.$store.state.loading"
      :color="loader.loaderColor"
      :background-color="loader.bgColor"
      :is-full-page="loader.fullPage"
    ></loading>

    <div id="nav">
      <span v-if="this.$store.state.isAuthenticated">
        <router-link to="/">Home</router-link>
        <button @click="logoutUser">Logout</button>
      </span>
      <span v-else>
        <router-link to="/login">Login</router-link>
        <router-link to="/signup">Signup</router-link>
      </span>
    </div>
    <router-view />
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "App",
  components: { Loading },
  data() {
    return {
      loader: {
        loaderColor: "rebeccapurple",
        bgColor: "rgba(0,0,0,0.1)",
        fullPage: true
      }
    };
  },
  methods: {
    logoutUser() {
      this.$store.dispatch("logout");
      this.$router.push({ name: "Login" });
    }
  },
  created() {}
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Lato:wght@300&family=Open+Sans:wght@300;400&family=Poppins:wght@200;300&display=swap");

:root {
  --primary_light_color: #c9c7ff7a;
  --primary_bold_color: #6c63ff;
  --poppins_font_family: "Poppins", sans-serif;
  --opensans_font_family: "Open Sans", sans-serif;
  --lato_font_family: "Lato", sans-serif;
}

html,
body,
* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

img {
  object-fit: contain;
  object-position: center;
  width: 100%;
  height: 100%;
}

#app {
  font-family: var(--poppins_font_family);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;

  a {
    font-weight: bold;
    margin: auto 10px;
    border-radius: 5px;
    text-decoration: none;
    padding: 4px 20px;
    border: 1px solid rebeccapurple;
    background: none;

    // color: #fff;
    &:active {
      color: #333;
    }
    &:visited {
      color: #333;
    }

    &.router-link-exact-active {
      color: #fff;
      padding: 5px 20px;
      background: var(--primary_bold_color);
      border: none;
    }
  }

  button {
    outline: none;
    border: 1px solid rebeccapurple;
    margin: auto 10px;
    border-radius: 5px;
    padding: 7px 20px;
    background: none;
    cursor: pointer;

    &:focus {
      outline: none;
    }
  }
}
</style>
