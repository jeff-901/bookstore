import React, { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MenuAppBar from "./MenuAppBar"

function App() {
  const [user, setUser] = useState(null);
  return (
    <BrowserRouter>
        <Routes>
            <Route exact path="/" element={<MenuAppBar user={user} setUser={setUser}/>} />
                
                {/* <Home /> */}
            <Route exact path="/user/:userId">
                
            </Route>
            <Route exact path="/book/:bookId">
                
            </Route>
            <Route exact path="/order/:orderId">
                
            </Route>
        </Routes>
    </BrowserRouter>
  );
}

export default App;
