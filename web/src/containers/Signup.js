import React, { Component } from "react";
import {
  //HelpBlock,
  FormGroup,
  FormControl,
  FormLabel
} from "react-bootstrap";

import { Auth } from "aws-amplify";
import LoaderButton from "../components/LoaderButton";
import "./Signup.css";

export default class Signup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      email: "",
      password: "",
      confirmPassword: "",
      confirmationCode: "",
      newUser: null,
      first_name: "",
      last_name: "",
      telephone: "",
      company_name: "",
      job_title: "",
      address: "",
      city: "",
      state: ""
    };
  }

  validateForm() {
    return (
      this.state.email.length > 0 &&
      this.state.password.length > 0 &&
      this.state.password === this.state.confirmPassword
    );
  }

  validateConfirmationForm() {
    return this.state.confirmationCode.length > 0;
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
      const newUser = await Auth.signUp({
        username: this.state.email,
        password: this.state.password,
        attributes: {
          "custom:first_name": this.state.first_name,
          "custom:last_name": this.state.last_name,
          "custom:telephone_number": this.state.telephone,
          "custom:company_name": this.state.company_name,
          "custom:job_title": this.state.job_title,
          "custom:address": this.state.address,
          "custom:city": this.state.city,
          "custom:state": this.state.state
        }
      });
      this.setState({
        newUser
      });
    } catch (e) {
      alert(e.message);
      this.setState({ isLoading: false });
    }

    this.setState({ isLoading: false });
  };

  handleConfirmationSubmit = async event => {
    event.preventDefault();

    this.setState({ isLoading: true });

    try {
      await Auth.confirmSignUp(this.state.email, this.state.confirmationCode);
      await Auth.signIn(this.state.email, this.state.password);

      this.props.userHasAuthenticated(true);
      this.props.history.push("/");
    } catch (e) {
      alert(e.message);
      this.setState({ isLoading: false });
    }
  };

  renderConfirmationForm() {
    return (
      <form onSubmit={this.handleConfirmationSubmit}>
        <FormGroup controlId="confirmationCode">
          <FormLabel>Confirmation Code</FormLabel>
          <FormControl
            autoFocus
            type="tel"
            value={this.state.confirmationCode}
            onChange={this.handleChange}
          />
          {/* <HelpBlock>Please check your email for the code.</HelpBlock> */}
        </FormGroup>
        <LoaderButton
          block
         
          disabled={!this.validateConfirmationForm()}
          type="submit"
          isLoading={this.state.isLoading}
          text="Verify"
          loadingText="Verifying…"
        />
      </form>
    );
  }

  renderForm() {
    return (
      <form onSubmit={this.handleSubmit}>
        <h1>Create an account</h1>
        <FormGroup controlId="first_name">
          <FormLabel>First Name</FormLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.first_name}
            onChange={this.handleChange}
          />
        </FormGroup>

        <FormGroup controlId="last_name">
          <FormLabel>Last Name</FormLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.last_name}
            onChange={this.handleChange}
          />
        </FormGroup>

        <FormGroup controlId="telephone">
          <FormLabel>Telephone</FormLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.telephone}
            onChange={this.handleChange}
          />
        </FormGroup>

        <FormGroup controlId="company_name">
          <FormLabel>Company</FormLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.company_name}
            onChange={this.handleChange}
          />
        </FormGroup>

        <FormGroup controlId="city">
          <FormLabel>City</FormLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.city}
            onChange={this.handleChange}
          />
        </FormGroup>

        <FormGroup controlId="state">
          <FormLabel>State</FormLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.state}
            onChange={this.handleChange}
          />
        </FormGroup>

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
          <p className="helper">
            must be at least 8 characters long, contain two numbers and two
            special characters
          </p>
          <FormControl
            value={this.state.password}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <FormGroup controlId="confirmPassword">
          <FormLabel>Confirm Password</FormLabel>
          <FormControl
            value={this.state.confirmPassword}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <LoaderButton
          block
         
          disabled={!this.validateForm()}
          type="submit"
          isLoading={this.state.isLoading}
          text="Signup"
          loadingText="Signing up…"
        />
      </form>
    );
  }

  render() {
    return (
      <div className="Signup">
        {this.state.newUser === null
          ? this.renderForm()
          : this.renderConfirmationForm()}
      </div>
    );
  }
}
