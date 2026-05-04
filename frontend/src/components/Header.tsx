import React from "react";

const Header: React.FC = () => {
  return (
    <header className="site-header">
      <nav className="nav-container">
        <h1 className="logo">Interneers Lab</h1>
        <ul className="nav-links">
          <li>Home</li>
          <li>Products</li>
          <li>About</li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
