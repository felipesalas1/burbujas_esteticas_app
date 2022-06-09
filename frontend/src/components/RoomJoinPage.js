import React, { Component } from "react";
import { Grid } from "@mui/material";
import { Typography } from "@mui/material";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

export default class RoomJoinPage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return  
    <Grid item xs={12} align="center">
    <Typography variant="h3" compact="h3">
    Proyecto de Grado de Felipe Salas
    </Typography>
  </Grid>;
  }
}