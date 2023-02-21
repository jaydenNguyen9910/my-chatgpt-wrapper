// Copyright 2023 tringuyen
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import axios from "axios";
// import { push } from "connected-react-router";
import { toast } from "react-toastify";
import { SET_TOKEN, SET_CURRENT_USER, UNSET_CURRENT_USER } from "./LoginTypes";
import { setAxiosAuthToken, toastOnError } from "../../utils/Utils";

export const login = (userData) => dispatch => {
  axios
    .post("/login", userData)
    .then(async response => {
        const auth_token = response.data.token;
        await dispatch(setToken(auth_token));
        await dispatch(getCurrentUser());
    })
    .then(() => toast.success("Login successfully."))
    .catch(error => {
      dispatch(unsetCurrentUser());
      toastOnError(error);
    });
};

export const getCurrentUser = () => dispatch => {
    axios
    .get("/user", {}, {"Authorization": `TOKEN ${localStorage.getItem("user")}`})
    .then(response => {
        const user = response.data;
        dispatch(setCurrentUser(user));
    })
    .catch(error => {
        dispatch(unsetCurrentUser());
        toastOnError(error);
    });
};

export const setCurrentUser = (user) => dispatch => {
    localStorage.setItem("user", JSON.stringify(user));
    dispatch({
        type: SET_CURRENT_USER,
        payload: user
    });
};

export const setToken = token => dispatch => {
    setAxiosAuthToken(token);
    localStorage.setItem("token", token);
    dispatch({
        type: SET_TOKEN,
        payload: token
    });
};

export const unsetCurrentUser = () => dispatch => {
    setAxiosAuthToken("");
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    dispatch({
        type: UNSET_CURRENT_USER
    });
};

export const logout = () => dispatch => {
    dispatch(unsetCurrentUser());
    toast.success("Logout successfully.");
};