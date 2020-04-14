<template>
  <div class="login">
    <div v-show="showError" class="general_error">
      <p :class="message_type">
        <v-icon name="info"></v-icon>
        <span>{{ error.general }}</span>
        <span @click="closeError" class="close-error-container">
          <v-icon name="x" base-class="close-error"></v-icon>
        </span>
      </p>
    </div>

    <div class="login_banner">
      <img src="../assets/login.svg" alt="login-banner" />
    </div>

    <form action="#" class="login-form" @submit.prevent="login">
      <h1>Todo Login</h1>

      <div class="form-group">
        <v-icon name="user" base-class="user_icon icon"></v-icon>
        <input
          type="email"
          name="email"
          placeholder="Email"
          autocomplete="off"
          required
          v-model="formData.email"
        />
        <span class="bar"></span>
        <!-- <small class="error">invalid email</small> -->
      </div>
      <div class="form-group">
        <v-icon name="lock" base-class="pwd_icon icon"></v-icon>
        <input
          type="password"
          name="password"
          placeholder="Password"
          required
          v-model="formData.password"
        />
        <span @click="togglePwdVisibility">
          <v-icon
            v-show="showPassword"
            name="eye"
            base-class="icon_pwd"
          ></v-icon>
          <v-icon
            v-show="!showPassword"
            name="eye-off"
            base-class="icon_pwd"
          ></v-icon>
        </span>
        <span class="bar"></span>
        <!-- <small class="error">invalid password</small> -->
      </div>

      <div class="submit">
        <button type="submit">Login</button>
        <router-link to="/signup">create an account</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Login",
  data() {
    return {
      formData: {
        email: "",
        password: ""
      },
      pwd_eye: false,
      message_type: "", // can be "success" or "error"
      showError: false,
      error: {
        general: ""
      },
      showPassword: false
    };
  },
  updated() {
    console.log("updating...");
  },
  mounted() {
    let message = this.$store.state.message.message;

    if (message.length !== 0) {
      this.setGeneralMessage(message, "success");

      setTimeout(() => {
        this.$store.dispatch("clearMessageAction");
        this.clearGeneralMessage();
      }, 5000);
    }
  },
  methods: {
    ...mapActions(["loginAction", "setLoader"]),
    closeError() {
      this.showError = !this.showError;
    },
    async login() {
      let payload = JSON.stringify(this.formData);
      this.setLoader(true);
      await this.loginAction(payload);
      // this.$route.name = "Home";
      let error = this.$store.state.error;
      if (error !== null) {
        Object.values(error).forEach(val => {
          this.setGeneralMessage(val, "error");

          setTimeout(() => {
            this.$store.dispatch("clearError");
            this.clearGeneralMessage();
          }, 3000);
        });
      } else {
        let message = this.$store.state.message.message;

        if (message.length !== 0) {
          this.setGeneralMessage(message, "success");

          setTimeout(() => {
            this.$store.dispatch("clearMessageAction");
            this.clearGeneralMessage();
          }, 5000);
        }

        // redirect to home page
        this.$router.push({ name: "Home" });
      }
    },
    setGeneralMessage(message, type) {
      console.log("here...", type);
      this.error.general = message;
      this.showError = true;
      this.message_type = type;
    },
    clearGeneralMessage() {
      this.error.general = "";
      this.showError = false;
      this.message_type = "";
    },
    togglePwdVisibility(event) {
      this.showPassword = !this.showPassword;
      console.log(event.currentTarget.previousElementSibling.type);
      if (this.showPassword) {
        event.currentTarget.previousElementSibling.type = "text";
      } else {
        event.currentTarget.previousElementSibling.type = "password";
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.login
  display: flex
  justify-content: center
  align-items: center
  max-height: 500px !important
  position: absolute
  top: 50%
  left: 50%
  transform: translate(-50%, -50%)

  .general_error
    position: absolute
    top: -20%
    left: 50%
    transform: translate(-50%, -20%)

    p
      display: flex
      justify-content: center
      align-items: center

      @media (max-width: 700px)
        font-size: 13px

      svg
        width: 20px
        margin-right: 10px

      .close-error-container
        display: flex
        justify-content: center
        align-items: center

        .close-error
          margin: unset !important
          margin-left: 20px !important
          cursor: pointer

    p.error
      background: #ff00009e
      color: #fff
      border-radius: 5px
      padding: 5px 8px
      white-space: nowrap

    p.success
      background: #e4f0fb
      color: #2362a1
      border-radius: 5px
      padding: 5px 8px
      white-space: nowrap

  .login_banner
    max-width: 500px
    min-width: 300px

    @media (max-width: 700px)
      margin-top: 30px

  .login-form
    // border: 1px solid red
    // position: relative

    .form-group
      position: relative
      margin: 30px auto
      width: 370px

      .icon
        width: 20px
        position: absolute
        top: 15%
        left: 1%

      .icon_pwd
        width: 20px
        position: absolute;
        right: 10px;
        top: 15%
        left: unset;
        cursor: pointer;

      .bar
        display: block
        background: var(--primary_bold_color)
        position: relative
        bottom: 0
        left: 0

        &::before
          content: ''
          height: 1px
          width: 0
          left: 50%
          position: absolute
          background: var(--primary_bold_color)
          transition: left 0.28s ease, width 0.28s ease

      input
        border: none
        outline: none
        width: 100%
        padding: 10px 0px 10px 35px
        background: #e8f0fe82

        &:focus ~ .bar::before
          // color: red
          display: block
          width: 370px
          left: 0

      input[type='password']
          padding-right: 30px

      .error
        color: red
        font-size: 12px

  .submit
    display: flex
    justify-content: space-between
    align-items: flex-end
    margin-top: 40px

    button
      outline: none
      cursor: pointer
      padding: 10px 30px
      border-radius: 5px
      border: none
      // background: #6c63ff
      background: #3f3d56
      color: #fff

    a
      font-size: 14px

  @media (max-width: 700px)
    flex-direction: column-reverse
</style>
