import React, { useState } from "react";

function Home() {

  return (
    <BrowserRouter>
        <Switch>
            <Route exact path="/">
                <Home />
            </Route>
            <Route exact path="/user/:userId">
                
            </Route>
            <Route exact path="/book/:bookId">
                
            </Route>
            <Route exact path="/order/:orderId">
                
            </Route>
        </Switch>
    </BrowserRouter>
  );
}