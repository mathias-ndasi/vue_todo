import axios from 'axios'

export const HTTP = axios.create({
    baseURL: "http://127.0.0.1:5000/account",
    timeout: 8000,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
    }
});