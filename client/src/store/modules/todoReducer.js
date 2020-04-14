import {
    HTTP
} from '../../config/axios'


export default {
    state: {
        todos: []
    },
    getters: {
        todos: (state) => state.todos
    },
    mutations: {
        setTodosReducer: (state, todos) => {
            state.todos = todos
        },
        addTododReducer: (state, todo) => {
            console.log(state.todos, 'this is me...')
            console.log(typeof (state.todos))
            state.todos.unshift(todo)
        },
        checkTodoReducer: (state, todo) => {
            let index = state.todos.findIndex(value => todo.id === value.id)
            console.log(index)
            if (index !== -1) {
                state.todos.splice(index, 1, todo)
            }
        },
        deleteTodoReducer: (state, todo) => {
            state.todos = state.todos.filter(value => {
                return value.id !== todo.id
            })
        },
        updateTodoReducer: (state, todo) => {
            let index = state.todos.findIndex(value => todo.id === value.id)
            if (index !== -1) {
                state.todos.splice(index, 1, todo)
            }
        }
    },
    actions: {
        fetchAllTodos: async (context) => {
            await HTTP.get(`/${context.rootState.user.public_id}/todo`, {
                    headers: {
                        'Authorization': `Bearer ${context.rootState.token}`
                    }
                })
                .then(res => {
                    console.log(res.data)
                    context.commit('setTodosReducer', res.data.data)
                })
                .catch(err => {
                    console.log(err.response.data)
                })
        },
        createTodo: async (context, todo) => {
            await HTTP.post(`/${context.rootState.user.public_id}/todo`, todo, {
                    headers: {
                        'Authorization': `Bearer ${context.rootState.token}`
                    }
                })
                .then(res => {
                    console.log(res.data)
                    context.commit('addTododReducer', res.data.data)
                    context.dispatch("setMessageAction", res.data["message"]);

                    context.dispatch("setLoader", true)

                    // reset loader
                    setTimeout(() => {
                        context.dispatch("setLoader", false)
                    }, 700)
                })
                .catch(err => {
                    console.log(err.response.data)
                })
        },
        checkTodo: async (context, todo) => {
            await HTTP.put(`/${context.rootState.user.public_id}/todo/${todo.id}/done`, todo, {
                    headers: {
                        'Authorization': `Bearer ${context.rootState.token}`
                    }
                })
                .then(res => {
                    console.log(res.data)
                    context.commit('checkTodoReducer', res.data.data)
                })
                .catch(err => {
                    console.log(err.response.data)
                })
        },
        deleteTodo: async (context, todo) => {
            await HTTP.delete(`/${context.rootState.user.public_id}/todo/${todo.id}`, {
                    headers: {
                        'Authorization': `Bearer ${context.rootState.token}`
                    }
                })
                .then(res => {
                    console.log(res.data)
                    context.commit('deleteTodoReducer', todo)
                    context.dispatch("setLoader", true)

                    // reset loader
                    setTimeout(() => {
                        context.dispatch("setLoader", false)
                    }, 700)
                })
                .catch(err => {
                    console.log(err.response.data)
                })
        },
        updateTodo: async (context, payload) => {
            await HTTP.put(`/${context.rootState.user.public_id}/todo/${payload.todo.id}`, JSON.stringify(payload.data), {
                    headers: {
                        'Authorization': `Bearer ${context.rootState.token}`
                    }
                })
                .then(res => {
                    console.log(res.data)
                    context.commit('updateTodoReducer', res.data.data)
                    context.dispatch("setLoader", true)

                    // reset loader
                    setTimeout(() => {
                        context.dispatch("setLoader", false)
                    }, 400)
                })
                .catch(err => {
                    console.log(err.response.data)
                })
        }
    }
}