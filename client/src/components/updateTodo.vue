<template>
  <div class="update">
    <form action="#" class="update-form" @submit.prevent="updateMyTodo">
      <h1>Update Todo</h1>

      <div class="form-group">
        <v-icon name="edit" base-class="user_icon icon"></v-icon>
        <input
          type="text"
          name="code"
          value
          placeholder="Enter new todo title"
          autocomplete="off"
          required
          v-model="myData.title"
        />
        <span class="bar"></span>
        <small class="error">{{ error.title }}</small>
      </div>

      <div class="submit">
        <button type="submit">Update Todo</button>
        <button @click.prevent="cancelUpdate()" type="button" class="cancel">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    cancelUpdate: {
      required: true,
      type: Function
    },
    todo: {
      type: Object
    }
  },
  data() {
    return {
      error: {
        general: "",
        title: ""
      },
      myData: {
        title: this.todo.title
      }
    };
  },
  methods: {
    async updateMyTodo() {
      console.log("updating...");
      let payload = { todo: this.todo, data: this.myData };
      await this.$store.dispatch("updateTodo", payload);

      // remove popup
      this.cancelUpdate();
    }
  }
};
</script>

<style lang="sass">
.update
    background: rgba(0,0,0,0.2);
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    display: grid;
    justify-content: center;
    align-content: center;

    form
        background: #fff;
        padding: 20px;
        .form-group
            position: relative
            margin: 30px auto
            width: 370px

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
                    width: 370px
                    left: 0

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
            button.cancel
                background: unset !important
                color: #333
                border: 1px solid rebeccapurple

            a
                font-size: 14px
</style>
