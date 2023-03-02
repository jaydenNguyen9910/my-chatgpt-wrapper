import React, { Component } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Signup from "./components/signup/Signup";
import Login from "./components/login/Login";
import Dashboard from "./components/dashboard/Dashboard";
import Root from "./Root";
import { ToastContainer } from "react-toastify";
import axios from "axios";

if (window.location.origin === "http://localhost:3000") {
  axios.defaults.baseURL = "http://127.0.0.1:8000";
} else {
  axios.defaults.baseURL = window.location.origin;
}

class App extends Component {
  render() {
    return (
      <div>
        <Root>
          <BrowserRouter>
            <Routes>
              <Route exact path="/" element={<Signup/>} />
              <Route exact path="/signup" element={<Signup/>} />
              <Route exact path="/login" element={<Login/>} />
              <Route exact path="/dashboard" element={<Dashboard/>} />
            </Routes>
          </BrowserRouter>
        </Root>
        <ToastContainer hideProgressBar={true} newestOnTop={true} />
      </div>
    );
  }
}

export default App;
