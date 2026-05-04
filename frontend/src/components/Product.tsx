import React, { useState } from "react";
import { ProductData } from "../types/product";

interface ProductProps {
  product: ProductData;
}

const Product: React.FC<ProductProps> = ({ product }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div
      className={`product-tile ${isExpanded ? "expanded" : ""}`}
      onClick={toggleExpand}
    >
      <div className="product-basic-info">
        <h3>{product.name}</h3>
        <span className="price">${product.price.toFixed(2)}</span>
      </div>
      <div className="brand">{product.brand}</div>

      {isExpanded && (
        <div className="product-details">
          <hr />
          <p>{product.description}</p>
          <button className="buy-btn">Add to Cart</button>
        </div>
      )}
    </div>
  );
};

export default Product;
