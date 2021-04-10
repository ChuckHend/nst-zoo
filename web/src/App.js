import React, { Component, Fragment } from "react";
import { withRouter } from "react-router-dom";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import Routes from "./Routes";
import "./App.css";
import { Auth } from "aws-amplify";


class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isAuthenticated: false,
      isAuthenticating: true,
    };
  }

  async componentDidMount() {
    this.get_auth_info();
  }

  async get_auth_info() {
    try {
      await Auth.currentSession().then(data => {
        this.setState({
          sub: data.idToken.payload.sub,
          JWT: "bearer " + data.accessToken.jwtToken,
          email: data.idToken.payload.email
        })
      });
      this.userHasAuthenticated(true);
    } catch (e) {
      if (e !== "No current user") {
        alert(e);
      }
    }
    this.setState({ isAuthenticating: false });
  }

  userHasAuthenticated = authenticated => {
    this.setState({ isAuthenticated: authenticated });
    this.updateLicenses();
  };

  handleLogout = async event => {
    await Auth.signOut();

    this.userHasAuthenticated(false);
    this.setState({ numLicenses: 0 });

    this.props.history.push("/login");
  };

  render() {
    const childProps = {
      isAuthenticated: this.state.isAuthenticated,
      userHasAuthenticated: this.userHasAuthenticated,
    };

    return (
      <div className="App container">
        <Navbar
          collapseOnSelect
          expand="lg"
          bg="dark"
          variant="dark"
          fixed="top"
        >
          <Navbar.Brand href="/"> Neural Style Transfer</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse
            id="responsive-navbar-nav"
            className="justify-content-end"
          >
            <Nav>
              <LinkContainer to="/about">
                <Nav.Link>About</Nav.Link>
              </LinkContainer>
              {this.state.isAuthenticated ? (
                <Fragment>
                  <LinkContainer to="/info">
                    <Nav.Link>Info</Nav.Link>
                  </LinkContainer>
                  <Nav.Link onClick={this.handleLogout}>Logout</Nav.Link>
                </Fragment>
              ) : (
                <Fragment>
                  <LinkContainer to="/signup">
                    <Nav.Link>Signup</Nav.Link>
                  </LinkContainer>
                  <LinkContainer to="/login">
                    <Nav.Link>Login</Nav.Link>
                  </LinkContainer>
                </Fragment>
              )}
            </Nav>
          </Navbar.Collapse>
        </Navbar>

        <Routes childProps={childProps} />

        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
          <Nav>
            {this.state.isAuthenticated ? (
              <Fragment>
                <LinkContainer to="/settings/billing">
                  <Nav.Link>
                    {this.state.email}'s credit balance: {this.state.numLicenses}
                  </Nav.Link>
                </LinkContainer>
              </Fragment>
            ) : (
              <Fragment>
                <LinkContainer to="/signup">
                  <Nav.Link></Nav.Link>
                </LinkContainer>
              </Fragment>
            )}
          </Nav>
          <Navbar.Toggle />

          <Navbar.Collapse id="nav-bottom" className="justify-content-end">
            <Navbar.Text className="contact">contact@nst-zoo.io</Navbar.Text>
          </Navbar.Collapse>
        </Navbar>
      </div>
    );
  }
}

export default withRouter(App);
