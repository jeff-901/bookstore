import React, { useState } from "react";
import MenuIcon from "@material-ui/icons/Menu";
import AccountCircle from "@material-ui/icons/AccountCircle";

import { useNavigate } from "react-router-dom";
import {
  Button,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  IconButton,
  Box,
  AppBar,
  Link,
} from "@material-ui/core";

import Login from "../components/Login";
import SignUp from "../components/Signup";

export default function MenuAppBar(props) {
  const user = props.user;
  const setUser = props.setUser;
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [signIn, setSignIn] = useState(true);
  const [signInOpen, setSignInOpen] = useState(false);
  const setAlert = props.setAlert;
  // const [open, setOpen] = useState(false);
  const history = useNavigate();

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleRedirectToUserPage = () => {
    setAnchorEl(null);
    history("/user/" + user.user_id);
  };

  const handleLogout = () => {
    setAnchorEl(null);
    setUser(null);
  };

  const handleOpen = () => {
    setSignInOpen(true);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Bookstore
          </Typography>
          {user ? (
            <div>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={handleRedirectToUserPage}>Profile</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </div>
          ) : signIn ? (
            <>
              <Button color="inherit" align="right" onClick={handleOpen}>
                Login
              </Button>
              <Login
                setUser={setUser}
                setSignIn={setSignIn}
                open={signInOpen}
                setOpen={setSignInOpen}
                setAlert={setAlert}
              />
            </>
          ) : (
            <SignUp
              setSignIn={setSignIn}
              setOpen={setSignInOpen}
              open={signInOpen}
              setAlert={setAlert}
            />
          )}
        </Toolbar>
      </AppBar>
    </Box>
  );
}
