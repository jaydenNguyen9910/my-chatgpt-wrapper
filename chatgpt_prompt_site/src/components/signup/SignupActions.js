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
import { toast } from "react-toastify";
import {
  CREATE_USER_ERROR,
  CREATE_USER_SUBMITTED,
  CREATE_USER_SUCCESS
} from "./SignupTypes";

export const signupNewUser = userData => dispatch => {
  dispatch({ type: CREATE_USER_SUBMITTED }); // set submitted state
  axios
    .post("/register", userData)
    .then(response => {
      toast.success(
        "Account for " +
          userData.username +
          " created successfully. Please login."
      );
      dispatch({ type: CREATE_USER_SUCCESS });
    })
    .catch(error => {
      if (error.resposne) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        toast.error(JSON.stringify(error.response.data));
        dispatch({
          type: CREATE_USER_ERROR,
          errorData: error.response.data
        });
      } else if (error.message) {
        // the error message is available,
        // let's display it on error toast
        toast.error(JSON.stringify(error.message));
      } else {
        // strange error, just show it
        toast.error(JSON.stringify(error));
      }
    });
};