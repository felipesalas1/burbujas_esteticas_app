import React, { Component } from "react";
import { render } from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
  useParams,
} from "react-router-dom";
import Authed from "./Authed";
import Footer from "./Footer";
import Header from "./Header";
import HomePage from "./HomePage";

/**
 * Página principal del front.
 * @constructor
 * React Router a HomePage
 */

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Header/>
        <div class="main">
          <Router>
          <Switch>
            <Route path="/" component={HomePage} />
          </Switch>
          </Router>
        </div>
        <Footer/>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);