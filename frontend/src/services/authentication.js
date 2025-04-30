import axios from "axios";

export const authenticationservice = {
    async register(payload) {
        axios.post(`http://127.0.0.1:8000/users/`, {
            "username":payload.username,
            "password": payload.password,
            "email": payload.email,
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }
}
