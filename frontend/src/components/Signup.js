import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";

import FormControlLabel from "@material-ui/core/FormControlLabel";
import {
  Link,
  Checkbox,
  Modal,
  TextField,
  Grid,
  Button,
} from "@material-ui/core";

import { createUser } from "../api";
const sha256 = require("../Mysha256.js");

function getModalStyle() {
  const top = 50;
  const left = 50;

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  };
}

const useStyles = makeStyles((theme) => ({
  paper: {
    position: "absolute",
    width: 800,
    backgroundColor: theme.palette.background.paper,
    border: "2px solid #000",
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
    margin: theme.spacing(1),
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
    },
  },
}));

function SignUp(props) {
  const classes = useStyles();
  // getModalStyle is not a pure function, we roll the style only on the first render
  const [modalStyle, setModalStyle] = useState(getModalStyle);
  const open = props.open;
  const setOpen = props.setOpen;
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [gender, setGender] = useState("");
  const [address, setAddress] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const setAlert = props.setAlert;
  const handleClose = () => {
    setOpen(false);
    props.setSignIn(true);
  };

  const handleSignUp = (e) => {
    e.preventDefault();

    if (password === password2) {
      createUser(
        0,
        firstname,
        lastname,
        email,
        phone,
        gender,
        address,
        password
      ).then((data) => {
        if (data.message === "Successfully create") {
          props.setSignIn(true);
          setAlert({
            open: true,
            severity: "success",
            msg: data.message,
          });
        } else {
          setAlert({
            open: true,
            severity: "error",
            msg: data.message,
          });
        }
      });
    } else {
      setAlert({
        open: true,
        severity: "error",
        msg: "confirmed password are the same.",
      });
    }
  };

  const body = (
    <div style={modalStyle} className={classes.paper}>
      <form className={classes.form} noValidate>
        <div>
          <TextField
            variant="outlined"
            margin="normal"
            required
            halfWidth
            id="firstname"
            label="firstname"
            name="firstname"
            autoComplete="firstName"
            autoFocus
            onInput={(e) => {
              setFirstname(e.target.value);
            }}
            onClick={() => {}}
            value={firstname}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            halfWidth
            id="lastname"
            label="lastname"
            name="lastname"
            autoComplete="lastname"
            autoFocus
            onInput={(e) => {
              setLastname(e.target.value);
            }}
            onClick={() => {}}
            value={lastname}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            halfWidth
            id="gender"
            label="gender"
            name="gender"
            autoComplete="gender"
            autoFocus
            onInput={(e) => {
              setGender(e.target.value);
            }}
            onClick={() => {}}
            value={gender}
          />
        </div>
        <div>
          <TextField
            variant="outlined"
            margin="normal"
            required
            halfWidth
            id="email"
            label="email"
            name="email"
            autoComplete="email"
            autoFocus
            onInput={(e) => {
              setEmail(e.target.value);
            }}
            value={email}
            onClick={() => {}}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            halfWidth
            id="phone"
            label="phone"
            name="phone"
            autoComplete="phone"
            autoFocus
            onInput={(e) => {
              setPhone(e.target.value);
            }}
            value={phone}
            onClick={() => {}}
          />
        </div>
        <TextField
          variant="outlined"
          margin="normal"
          fullWidth
          name="address"
          label="address"
          type="address"
          id="address"
          autoComplete="current-address"
          onInput={(e) => {
            setAddress(e.target.value);
          }}
          value={address}
          onClick={() => {}}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          name="password"
          label="password"
          type="password"
          id="password"
          autoComplete="current-password"
          onInput={(e) => {
            setPassword(e.target.value);
          }}
          value={password}
          onClick={() => {}}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          name="password"
          label="Confirmed password"
          type="password"
          id="password"
          autoComplete="current-password"
          onInput={(e) => {
            setPassword2(e.target.value);
          }}
          value={password2}
          onClick={() => {}}
        />
        <FormControlLabel
          control={<Checkbox value="accept" color="primary" />}
          label="I accept the rule"
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          onClick={handleSignUp}
        >
          Sign Up
        </Button>
        <Grid container justify="flex-end">
          <Grid item>
            <Link
              href="#"
              variant="body2"
              onClick={() => {
                props.setSignIn(true);
              }}
            >
              {"Already have an account? Sign in"}
            </Link>
          </Grid>
        </Grid>
      </form>
    </div>
  );

  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="simple-modal-title"
        aria-describedby="simple-modal-description"
      >
        {body}
      </Modal>
    </div>
  );
}

export default SignUp;
