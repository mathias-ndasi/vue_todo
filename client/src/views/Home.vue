<template>
  <div class="home">
    <div class="todo-container">
      <div v-show="showError" class="general_error">
        <p :class="general_info">
          <v-icon name="info"></v-icon>
          <span>{{ message }}</span>
          <span @click="closeError" class="close-error-container">
            <v-icon name="x" base-class="close-error"></v-icon>
          </span>
        </p>
      </div>

      <div class="todo-content">
        <div class="todo-header">
          <h2>My Todo List</h2>
          <form action="#" @submit.prevent="addTodo">
            <div class="form-group">
              <v-icon name="edit" base-class="user_icon icon"></v-icon>

              <input
                type="text"
                name="addTodo"
                id="addTodo"
                placeholder="Add a new todo"
                autocomplete="off"
                required
                v-model="formData.title"
              />
              <span class="bar"></span>
              <!-- <small class="error">invalid email</small> -->
            </div>
          </form>
        </div>

        <div class="tips">
          <p>
            <v-icon name="alert-octagon" base-class="user_icon icon"></v-icon>
            Double click todo title to edit
          </p>
        </div>

        <div v-if="todos.length !== 0" class="todos">
          <div class="todo" v-for="todo in todos" :key="todo.id">
            <p
              @dblclick="updateMyTodo(todo)"
              :class="{ text: true, strike: todo.done }"
            >
              {{ todo.title }}
            </p>
            <p>
              <span>
                <div class="checkbox">
                  <label>
                    <input
                      @change="checkMyTodo(todo, $event)"
                      :checked="todo.done"
                      type="checkbox"
                      name="done"
                      id="done"
                    />
                    <i class="helper"></i>
                  </label>
                </div>
              </span>
              <span @click="deleteMyTodo(todo)">
                <v-icon name="trash" base-class="todo-delete icon"></v-icon>
              </span>
            </p>
          </div>
        </div>
        <div v-else class="todos">
          <!-- if no todo available -->
          <div class="no-todo">
            <center>
              <b>No Todos Available</b>
            </center>
          </div>
        </div>
      </div>
      <div class="todo-avatar">
        <img src="../assets/todo.svg" alt="todo" />
      </div>
    </div>

    <updateTodo
      :todo="todo"
      :cancelUpdate="cancelUpdate"
      v-if="updatePopup"
    ></updateTodo>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import updateTodo from "../components/updateTodo";

export default {
  name: "Home",
  components: { updateTodo },
  data() {
    return {
      general_info: "success", // can be "success" or "error"
      showError: false,
      formData: {
        title: ""
      },
      message: "",
      updatePopup: false,
      todo: null
    };
  },
  computed: {
    ...mapGetters(["todos"])
  },
  created() {
    this.fetchAllTodos();
  },
  methods: {
    ...mapActions([
      "fetchAllTodos",
      "checkTodo",
      "createTodo",
      "deleteTodo",
      "updateTodo"
    ]),
    closeError() {
      this.showError = !this.showError;
    },
    async deleteMyTodo(todo) {
      console.log("deleting todo...");
      await this.deleteTodo(todo);
    },
    async updateMyTodo(todo) {
      console.log("updating todo...");
      this.todo = todo;
      this.updatePopup = true;
    },
    cancelUpdate() {
      this.updatePopup = false;
    },
    async addTodo() {
      let payload = JSON.stringify(this.formData);
      await this.createTodo(payload);
      let message = this.$store.state.message.message;
      this.formData.title = "";

      if (message.length !== 0) {
        this.setGeneralMessage(message, "success");

        setTimeout(() => {
          this.$store.dispatch("clearMessage");
          this.clearGeneralMessage();
        }, 5000);
      }
    },
    setGeneralMessage(message, type) {
      this.message = message;
      this.showError = true;
      this.message_type = type;
    },
    clearGeneralMessage() {
      this.message = "";
      this.showError = false;
      this.message_type = "";
    },
    async checkMyTodo(todo, event) {
      console.log("checking todo....");
      await this.checkTodo(todo);
      let todoText =
        event.target.parentElement.parentElement.parentElement.parentElement
          .previousElementSibling;
      if (event.target.checked) {
        todoText.classList.add("strike");
      } else {
        todoText.classList.remove("strike");
      }
    }
  }
};
</script>

<style lang="sass">
.home
  .todo-container
    position: absolute
    top: 100px
    left: 50%
    transform: translateX(-50%)

    .icon
      width: 20px

    .general_error
      width: fit-content
      margin: auto auto 30px auto

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
    .tips
        margin-bottom: 20px;
        p
            text-align: center;
            width: fit-content;
            border-radius: 5px;
            padding: 2px 10px;
            background: #f9cc9d87;
            margin: auto
            display: flex
            svg
              margin-right: 5px

    .todo-header
      h2
        text-align: center

      .form-group
        position: relative
        margin: 20px auto
        width: 390px

        .icon
          width: 20px
          position: absolute
          top: 15%
          left: 1%

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

    .todos
      margin: auto auto 30px auto

      .no-todo
        font-size: 20px
        margin-top: 50px !important

      .todo
        display: flex
        justify-content: space-between
        align-items: center
        background: #e5e4ff
        padding: 10px 30px
        cursor: pointer
        transition: background 0.5s ease
        margin: auto
        margin-bottom: 1px
        max-width: 600px

        &:hover
          background: #e5e4ff5e

        .text
          margin-right: 30px
          position: relative

        .text.strike::before
          content: ""
          height: 1px
          width: 100%
          position: absolute
          left: 0
          top: 50%
          right: 0
          border-top: 1px solid
          border-color: inherit

        p:last-child
          display: flex
          align-items: center
          justify-content: center

          span:last-child
            margin-left: 12px

            svg
              color: #ff000096
        .checkbox
          width: 100%
          label
            position: relative
            cursor: pointer
            &:hover
              .helper
                color: #3acc6c
          input
            width: auto
            opacity: 0.00000001
            &:checked
              ~ .helper
                color: #3acc6c
              ~ .helper::after, ~ .helper::before
                opacity: 1
                transition: height 0.28s ease
              ~ .helper::after
                height: 0.5rem
              ~ .helper::before
                height: 1.2rem
                transition-delay: 0.28s
          .helper
            color: #999
            position: absolute
            top: 0
            left: 0
            width: 1rem
            height: 1rem
            z-index: 0
            border: 0.125rem solid currentColor
            border-radius: 0.0625rem
            transition: border-color 0.28s ease
            &::before, &::after
              position: absolute
              height: 0
              width: 0.2rem
              background-color: #3acc6c
              display: block
              transform-origin: left top
              border-radius: 0.25rem
              content: ''
              transition: opacity 0.28s ease, height 0s linear 0.28s
              opacity: 0
            &::before
              top: 0.65rem
              left: 0.38rem
              transform: rotate(-135deg)
              box-shadow: 0 0 0 0.0625rem #fff
            &::after
              top: 0.3rem
              left: 0
              transform: rotate(-45deg)
</style>
