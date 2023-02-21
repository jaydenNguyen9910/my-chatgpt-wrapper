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

import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import {
  Container,
  Button,
  Row,
  Col,
  Form,
  FormControl
} from "react-bootstrap";

import { signupNewUser } from "./SignupActions"; // new import

class Signup extends Component {
  constructor(props) {
    super(props);
    console.log(props)
    this.state = {
      username: "",
      password: ""
    };
  }
  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  // update function to call the action
  onSignupClick = () => {
    const userData = {
      username: this.state.username,
      password: this.state.password
    };
    this.props.signup(userData); // <-- signup new user request
  };

  render() {
    return (
      <Container>
        <Row>
          <Col md="4">
            <h1>Sign up</h1>
            <Form>
              <Form.Group controlId="usernameId">
                <Form.Label>User name</Form.Label>
                <Form.Control
                  isInvalid={this.props.signupReducer.usernameError}
                  type="text"
                  name="username"
                  placeholder="Enter user name"
                  value={this.state.username}
                  onChange={this.onChange}
                />
                <FormControl.Feedback type="invalid">
                  {this.props.signupReducer.usernameError}
                </FormControl.Feedback>
              </Form.Group>

              <Form.Group controlId="passwordId">
                <Form.Label>Your password</Form.Label>
                <Form.Control
                  isInvalid={this.props.signupReducer.passwordError}
                  type="password"
                  name="password"
                  placeholder="Enter password"
                  value={this.password}
                  onChange={this.onChange}
                />
                <Form.Control.Feedback type="invalid">
                  {this.props.signupReducer.passwordError}
                </Form.Control.Feedback>
              </Form.Group>
            </Form>
            <Button color="primary" onClick={this.onSignupClick}>
              Sign up
            </Button>
            <p className="mt-2">
              Already have account? <Link to="/login">Login</Link>
            </p>
          </Col>
        </Row>
      </Container>
    );
  }
}

Signup.propTypes = {
  signup: PropTypes.func.isRequired,
  signupReducer: PropTypes.object.isRequired
};

function mapDispatchToProps(dispatch) {
  return {
      signup: (userData) => dispatch(signupNewUser(userData)),
  };
};

const mapStateToProps = state => ({
  signupReducer: state.signupReducer
});

export default connect(mapStateToProps, mapDispatchToProps)(Signup);

