import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Modal from "@material-ui/core/Modal";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

// import { createUser } from "../axios";
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
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
    },
  },
}));

function SignUp(props) {
  const classes = useStyles();
  // getModalStyle is not a pure function, we roll the style only on the first render
  const [modalStyle, setModalStyle] = useState(getModalStyle);
  const [open, setOpen] = useState(true);
  const [firstname, setFirstname] = useState("");
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [validfirstname, setValidFirstname] = useState(true);
  const [firstnameHelpText, setFirstnameHelpText] = useState("");
  const [validId, setValidId] = useState(true);
  const [idHelpText, setIdHelpText] = useState("");
  const [validPassword, setValidPassword] = useState(true);
  const [passwordHelpText, setPasswordHelpText] = useState("");
  const [validPassword2, setValidPassword2] = useState(true);
  const [password2HelpText, setPassword2HelpText] = useState("");
  const [address, setAddress] = useState("");
  const [validAddress, setValidAddress] = useState(true);
  const [addressHelpText, setAddressHelpText] = useState("");
  // console.log("props", props);
  const handleClose = () => {
    setOpen(false);
    props.setSignIn(false);
    // props.setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const handleSignUp = (e) => {
    e.preventDefault();
    if (firstname.length === 0) {
      setValidFirstname(false);
      setFirstname("");
      setFirstnameHelpText("firstname is empty");
    } else if (firstname.length > 14) {
      setValidFirstname(false);
      setFirstname("");
      setFirstnameHelpText("firstname can only contain at most 14 characters!");
    } else if (!id.match(/[A-Za-z]+[0-9]+/)) {
      setIdHelpText("Invalid Id!\nDon't try to hack me!");
      setValidId(false);
      setId("");
    } else if (String(password).length < 6) {
      setPasswordHelpText("Password is at least 6 characters!");
      setValidPassword(false);
      setPassword("");
      setPassword2("");
    } else if (String(password) !== String(password2)) {
      setPassword2HelpText("Confirm password is different!");
      setValidPassword2(false);
      setPassword2("");
    } else if (!String(password).match(/[A-Za-z0-9]+/)) {
      setPasswordHelpText("Password can only conatain characters and numbers!");
      setValidPassword(false);
      setPassword("");
      setPassword2("");
    } else {
      // createUser({
      //   name: firstname,
      //   id: id,
      //   password: sha256(password),
      //   sessionId: "123",
      //   courses: JSON.stringify([]),
      // }).then((msg) => {
      //   if (msg === "success") {
      //     props.setSignup(false);
      //   } else {
      //     setfirstnameHelpText("User create fail!");
      //     setValidfirstname(false);
      //     setfirstname("");
      //     setId("");
      //     setPassword("");
      //     setPassword2("");
      //   }
      // });
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
          error={!validfirstname}
          halfWidth
          id="first name"
          label="first name"
          name="first name"
          autoComplete="firstName"
          autoFocus
          onInput={(e) => {
            setFirstname(e.target.value);
          }}
          helperText={firstnameHelpText}
          onClick={() => {
            setValidFirstname(true);
            setFirstnameHelpText("");
          }}
          value={firstname}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          error={!validfirstname}
          halfWidth
          id="last name"
          label="last name"
          name="last name"
          autoComplete="lastName"
          autoFocus
          onInput={(e) => {
            setFirstname(e.target.value);
          }}
          helperText={firstnameHelpText}
          onClick={() => {
            setValidFirstname(true);
            setFirstnameHelpText("");
          }}
          value={firstname}
        />
        </div>
        <div>
        <TextField
          variant="outlined"
          margin="normal"
          required
          error={!validId}
          halfWidth
          id="id"
          label="學號"
          name="id"
          autoComplete="id"
          autoFocus
          onInput={(e) => {
            setId(e.target.value);
          }}
          value={id}
          helperText={idHelpText}
          onClick={() => {
            setValidId(true);
            setIdHelpText("");
          }}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          error={!validId}
          halfWidth
          id="phone"
          label="phone"
          name="phone"
          autoComplete="phone"
          autoFocus
          onInput={(e) => {
            setId(e.target.value);
          }}
          value={id}
          helperText={idHelpText}
          onClick={() => {
            setValidId(true);
            setIdHelpText("");
          }}
        />
        </div>
        <TextField
          variant="outlined"
          margin="normal"
          error={!validAddress}
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
          helperText={addressHelpText}
          onClick={() => {
            setValidAddress(true);
            setAddressHelpText("");
          }}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          error={!validPassword}
          fullWidth
          name="password"
          label="密碼"
          type="password"
          id="password"
          autoComplete="current-password"
          onInput={(e) => {
            setPassword(e.target.value);
          }}
          value={password}
          helperText={passwordHelpText}
          onClick={() => {
            setValidPassword(true);
            setPasswordHelpText("");
          }}
        />
        <TextField
          variant="outlined"
          margin="normal"
          required
          error={!validPassword2}
          fullWidth
          name="password"
          label="密碼確認"
          type="password"
          id="password"
          autoComplete="current-password"
          onInput={(e) => {
            setPassword2(e.target.value);
          }}
          value={password2}
          helperText={password2HelpText}
          onClick={() => {
            setValidPassword2(true);
            setPassword2HelpText("");
          }}
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