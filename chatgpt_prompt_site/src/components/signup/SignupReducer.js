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

// import needed actions
import {
    CREATE_USER_ERROR,
    CREATE_USER_SUBMITTED,
    CREATE_USER_SUCCESS
} from "./SignupTypes";

// define the initial state of the signup store
const initialState = {
    usernameError: "",
    passwordError: "",
    isSubimtted: false
};

// define how action will change the state of the store
export const signupReducer = (state = initialState, action) => {
    switch (action.type) {
        case CREATE_USER_SUBMITTED:
            return {
            usernameError: "",
            passwordError: "",
            isSubimtted: true
            };
        case CREATE_USER_ERROR:
            const errorState = {
            usernameError: "",
            passwordError: "",
            isSubimtted: false
            };
            if (action.errorData.hasOwnProperty("username")) {
            errorState.usernameError = action.errorData["username"];
            }
            if (action.errorData.hasOwnProperty("password")) {
            errorState.passwordError = action.errorData["password"];
            }
            return errorState;
        case CREATE_USER_SUCCESS:
            return {
            usernameError: "",
            passwordError: "",
            isSubimtted: false
            };
        default:
            return state;
    }
}