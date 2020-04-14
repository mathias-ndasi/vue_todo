<template>
  <div class="signup">
    <div v-show="showError" class="general_error">
      <p :class="general_info">
        <v-icon name="info"></v-icon>
        <span>{{ error.general }}</span>
        <span @click="closeError" class="close-error-container">
          <v-icon name="x" base-class="close-error"></v-icon>
        </span>
      </p>
    </div>

    <div :class="{ signup_content: true, slide: accountValidated }">
      <div class="signup_banner">
        <img src="../assets/signup.svg" alt="signup-banner" />
      </div>

      <form action="#" class="signup-form" @submit.prevent="signup">
        <h1>Todo Signup</h1>

        <div class="form-group">
          <v-icon name="user" base-class="user_icon icon"></v-icon>
          <input
            type="text"
            name="first_name"
            value
            placeholder="First Name"
            autocomplete="off"
            required
            v-model="formData.first_name"
          />
          <span class="bar"></span>
          <small class="error">{{ error.first_name }}</small>
        </div>
        <div class="form-group">
          <v-icon name="user" base-class="user_icon icon"></v-icon>
          <input
            type="text"
            name="last_name"
            value
            placeholder="Last Name"
            autocomplete="off"
            required
            v-model="formData.last_name"
          />
          <span class="bar"></span>
          <small class="error">{{ error.last_name }}</small>
        </div>
        <div class="form-group">
          <v-icon name="user" base-class="user_icon icon"></v-icon>
          <input
            type="email"
            name="email"
            value
            placeholder="Email"
            autocomplete="off"
            required
            v-model="formData.email"
          />
          <span class="bar"></span>
          <small class="error">{{ error.email }}</small>
        </div>
        <div class="form-group">
          <v-icon name="lock" base-class="pwd_icon icon"></v-icon>
          <input
            type="password"
            name="password"
            value
            placeholder="Password"
            required
            v-model="formData.password"
          />
          <span @click="togglePwdVisibility">
            <v-icon v-show="showPassword" name="eye" base-class="icon_pwd"></v-icon>
            <v-icon v-show="!showPassword" name="eye-off" base-class="icon_pwd"></v-icon>
          </span>
          <span class="bar"></span>
          <small class="error">{{ error.password }}</small>
        </div>

        <div class="submit">
          <button type="submit">Create Account</button>
          <router-link to="/login">already have an account</router-link>
        </div>
      </form>
    </div>

    <div :class="{ account_confirmation: true, slide: accountValidated }">
      <div class="validate_banner">
        <img src="../assets/phone_dial.svg" alt="validate-banner" />
      </div>
      <form action="#" class="signup-form" @submit.prevent="accountValidate">
        <h1>Account Validation</h1>

        <div class="form-group">
          <v-icon name="file-text" base-class="user_icon icon"></v-icon>
          <input
            type="text"
            name="code"
            value
            placeholder="Enter secret code"
            autocomplete="off"
            required
            v-model="validate.secret_code"
          />
          <span class="bar"></span>
          <small class="error">{{ error.secret_code }}</small>
        </div>

        <div class="submit">
          <button type="submit">Validate Account</button>
          <button @click.prevent="clearValidation" type="button" class="back">Back</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Signup",
  data() {
    return {
      formData: {
        first_name: "",
        last_name: "",
        email: "",
        password: ""
      },
      validate: {
        secret_code: ""
      },
      pwd_eye: false,
      general_info: "success", // can be "success" or "error"
      showError: false,
      error: {
        general: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        secret_code: ""
      },
      showPassword: false
    };
  },
  computed: {
    ...mapGetters(["accountValidated"])
  },
  methods: {
    ...mapActions([
      "setLoader",
      "validateAccount",
      "signupAction",
      "clearError",
      "clearMessageAction",
      "setAccountValidator"
    ]),
    closeError() {
      this.showError = !this.showError;
    },
    async accountValidate() {
      let payload = JSON.stringify(this.validate);
      this.setLoader(true);

      await this.validateAccount(payload);

      // redirect back to login
      this.$router.push({ name: "Login" });
    },
    async signup() {
      let payload = JSON.stringify(this.formData);
      this.setLoader(true);
      await this.signupAction(payload);

      let error = this.$store.state.error;
      if (error !== null) {
        let errorKeys = Object.keys(this.error);
        for (let [key, value] of Object.entries(error)) {
          if (errorKeys.includes(key)) {
            if (typeof value == "string") {
              this.error[`${key}`] = value;
            } else {
              this.error[`${key}`] = value[0];
            }

            setTimeout(() => {
              this.clearError();
              this.error[`${key}`] = "";
            }, 5000);
          }
        }
      } else {
        let message = this.$store.state.message.message;

        if (message.length !== 0) {
          this.setGeneralMessage(message, "success");

          setTimeout(() => {
            this.clearMessageAction();
            this.clearGeneralMessage();
          }, 5000);
        }
      }
    },
    clearValidation() {
      this.setAccountValidator(false);
    },
    setGeneralMessage(message, type) {
      console.log(message, "setting error...");
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
.signup
  .account_confirmation
    transform: translate(5000px, 50%)

  .signup_content, .account_confirmation
    display: flex
    justify-content: center
    align-items: center
    max-height: 500px !important
    // overflow: hidden;
    position: absolute
    top: 50%
    left: 50%
    transform: translate(-50%, -50%)

  .account_confirmation
    position: fixed
    transform: translate(6000px, -50%)
    transition: transform 0.4s ease, left 1s ease-in
    .validate_banner
      max-width: 500px
      min-width: 300px

      @media (max-width: 700px)
        margin-top: 30px

    @media (max-width: 700px)
      flex-direction: column-reverse

  .account_confirmation.slide
    transform: translate(-50%, -50%)

  .signup_content
    transition: transform 1s ease, left 1s ease-in

  .general_error
    position: absolute
    top: 130px
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

  .signup_banner
    max-width: 500px
    min-width: 300px

    @media (max-width: 700px)
      margin-top: 30px

  .signup-form
    // border: 1px solid red
    // position: relative

    .form-group
      position: relative
      margin: 30px auto
      width: 390px

      .icon
        width: 20px
        position: absolute
        top: 15%
        left: 1%

      .icon_pwd
        width: 20px
        position: absolute
        right: 10px
        top: 15%
        left: unset
        cursor: pointer

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
          width: 390px
          left: 0

      input[type='password']
          padding-right: 30px

          ~ .pwd_eye
            position: absolute
            right: 5px
            cursor: pointer
            left: unset

            &:hover
              ::before
                content: 'view password'
                background: #333
                color: #fff
                position: absolute

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
    button.back
      background: unset !important
      color: #333
      border: 1px solid rebeccapurple

    a
      font-size: 14px

  .signup_content
    @media (max-width: 700px)
      flex-direction: column-reverse

  .signup_content.slide
    transform: translate(-6000px, -50%)
</style>
