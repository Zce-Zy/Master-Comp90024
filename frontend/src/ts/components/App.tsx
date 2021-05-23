import React from "react";
import { Header } from "./Header";

import { Map } from "./Map";
import { Visualisation } from "./Visualisation";

function App() {
  return (
    <div className="App">
      <Header />
      <Map />
      <Visualisation />
    </div>
  );
}

export default App;
