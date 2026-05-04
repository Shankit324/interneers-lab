import React from "react";
import "./App.scss";
import Header from "./components/Header";
import ProductList from "./components/ProductList";

function App() {
  return (
    <div className="App">
      <Header />
      <main className="content">
        <ProductList />
      </main>
    </div>
  );
}

export default App;
