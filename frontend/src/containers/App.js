import React, { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MenuAppBar from "./MenuAppBar";
import BookTable from "./BookTable";
import Book from "../components/Book";
import User from "../components/User";
import { Alert } from "@mui/material";
import { Snackbar } from "@material-ui/core";

function App() {
  const [user, setUser] = useState(null);
  const [alert, setAlert] = useState({});
  return (
    <BrowserRouter>
      <Routes>
        <Route
          exact
          path="/"
          element={
            <>
              <Snackbar
                anchorOrigin={{ vertical: "top", horizontal: "center" }}
                open={alert?.open}
                autoHideDuration={3000}
                onClose={() => setAlert({ ...alert, open: false })}
              >
                <Alert variant="filled" severity={alert?.severity}>
                  {alert?.msg}
                </Alert>
              </Snackbar>
              <MenuAppBar user={user} setUser={setUser} setAlert={setAlert} />{" "}
              <BookTable user={user} setAlert={setAlert} />
            </>
          }
        />

        {/* <Home /> */}
        <Route
          exact
          path="/user/:userId"
          element={<User user={user} />}
        ></Route>
        <Route exact path="/book/:bookId" element={<Book />}></Route>
        <Route exact path="/order/:orderId"></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
