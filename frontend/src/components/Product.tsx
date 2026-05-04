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

  const handleClk = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
  };

  return (
    <div className={`product-tile ${isExpanded ? "expanded" : ""}`}>
      <div className="product-basic-info">
        <h3>{product.name}</h3>
        <span className="price">${product.price.toFixed(2)}</span>
      </div>
      <div className="brand">{product.brand}</div>

      {!isExpanded && (
        <button className="buy-btn" onClick={toggleExpand}>
          View Details
        </button>
      )}

      {isExpanded && (
        <>
          <div className="product-details">
            <hr />
            <p>{product.description}</p>
            <button className="buy-btn" onClick={handleClk}>
              Add to Cart
            </button>
          </div>
          <br />
          <button className="buy-btn" onClick={toggleExpand}>
            Close
          </button>
        </>
      )}
    </div>
  );
};

export default Product;
