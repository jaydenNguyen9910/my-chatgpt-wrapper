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

import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { useNavigate, Link } from "react-router-dom";
import { Container, Button, Row, Col, Form } from "react-bootstrap";

import { login } from "./LoginActions.js";

const Login = (props) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const onLoginClick = async () => {
    const userData = {
      username,
      password
    };
    await props.login(userData);
  };

  useEffect(() => {
    if (props.isAuthenticated) {
      navigate('/dashboard');
    }
  }, [props.isAuthenticated]);

  return (
    <Container>
      <Row>
        <Col md="4">
          <h1>Login</h1>
          <Form>
            <Form.Group controlId="usernameId">
              <Form.Label>User name</Form.Label>
              <Form.Control
                type="text"
                name="username"
                placeholder="Enter user name"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Form.Group>

            <Form.Group controlId="passwordId">
              <Form.Label>Your password</Form.Label>
              <Form.Control
                type="password"
                name="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
          </Form>
          <Button color="primary" onClick={onLoginClick}>
            Login
          </Button>
          <p className="mt-2">
            Don't have account? <Link to="/signup">Signup</Link>
          </p>
        </Col>
      </Row>
    </Container>
  );
};

Login.propTypes = {
  login: PropTypes.func.isRequired,
  isAuthenticated: Boolean,
};

const mapStateToProps = state => ({
  isAuthenticated: state.loginReducer.isAuthenticated
});

function mapDispatchToProps(dispatch) {
  return {
    login: (userData) => dispatch(login(userData)),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Login);