import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./containers/Home";
import NotFound from "./containers/NotFound";
import Login from "./containers/Login";
import AppliedRoute from "./components/AppliedRoute";
import AuthenticatedRoute from "./components/AuthenticatedRoute";
import UnauthenticatedRoute from "./components/UnauthenticatedRoute";

import Signup from "./containers/Signup";
import ResetPassword from "./containers/ResetPassword";
import About from "./containers/About";


export default ({ childProps }) =>
  <Switch>
    <AppliedRoute path="/" exact component={Home} props={childProps} />
    <AppliedRoute path="/about" exact component={About} props={childProps} />
    
    <UnauthenticatedRoute path="/login" exact component={Login} props={childProps} />
    <UnauthenticatedRoute path="/signup" exact component={Signup} props={childProps} />
    <UnauthenticatedRoute path="/login/reset" exact component={ResetPassword} props={childProps} />

    { /* catch all unmatched routes */ }
    <Route component={NotFound} />
  </Switch>;
