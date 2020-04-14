export default {
    state: {
        message: ""
    },
    mutations: {
        // message management
        setMessageReducer: (state, message) => {
            state.message = message
        },
        clearMessageReducer: (state) => {
            state.message = ""
        },
    },
    actions: {
        setMessageAction: (context, message) => {
            context.commit('setMessageReducer', message)
        },
        clearMessageAction: (context) => {
            context.commit('clearMessageReducer')
        }
    }
}