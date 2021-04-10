import React, { Component } from "react";
import { Col, Form, FormGroup, FormControl, FormLabel } from "react-bootstrap";
import "./Login.css";
import { Auth } from "aws-amplify";
import LoaderButton from "../components/LoaderButton";
import { Link } from "react-router-dom";

export default class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      password: ""
    };
  }

  validateForm() {
    return this.state.email.length > 0 && this.state.password.length > 0;
  }

  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  };

  handleSubmit = async event => {
    event.preventDefault();

    this.setState({ isLoading: true });

    try {
      await Auth.signIn(this.state.email, this.state.password);
      this.props.userHasAuthenticated(true);
      this.props.history.push("/");
    } catch (e) {
      alert(e.message);
      this.setState({ isLoading: false });
    }
  };

  render() {
    return (
      <div className="Login">
        
        <form onSubmit={this.handleSubmit}>
        <h1>Login</h1>
        <h2>Don't have an account?{" "}<a href="/signup">Create one!</a></h2>
        <br></br>
          <FormGroup controlId="email">
            <FormLabel>Email</FormLabel>
            <FormControl
              autoFocus
              type="email"
              value={this.state.email}
              onChange={this.handleChange}
            />
          </FormGroup>
          <FormGroup controlId="password">
            <FormLabel>Password</FormLabel>
            <FormControl
              value={this.state.password}
              onChange={this.handleChange}
              type="password"
            />
          </FormGroup>
          <Form.Row>
              <Col>
                  <Link to="/login/reset">Forgot password?</Link>  
              </Col>
              <Col>
                  <Link to="/signup">Signup here</Link>
              </Col>
          </Form.Row>

          <LoaderButton
            block
           
            disabled={!this.validateForm()}
            type="submit"
            isLoading={this.state.isLoading}
            text="Login"
            loadingText="Logging in…"
          />
        </form>
      </div>
    );
  }
}
