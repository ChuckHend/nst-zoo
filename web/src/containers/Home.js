import React, { Component } from "react";
import { LinkContainer } from "react-router-bootstrap";
import LoaderButton from "../components/LoaderButton";
import "./Home.css";
import "../config";

export default class Home extends Component {
  render() {
    return (
      <div className="Home">
        <div className="lander">
          <h1>NST</h1>
          <p>Zoo</p>
        </div>
      </div>
    );
  }
}
