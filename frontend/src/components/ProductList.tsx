import React from "react";
import Product from "./Product";
import { ProductData } from "../types/product";

const DUMMY_PRODUCTS: ProductData[] = [
  {
    id: "1",
    name: "Wireless Headphones",
    description:
      "High-quality wireless headphones with noise-canceling features and 20-hour battery life.",
    price: 199.99,
    brand: "AudioTech",
  },
  {
    id: "2",
    name: "Smart Watch",
    description:
      "A sleek smart watch with heart rate monitoring, GPS, and a vibrant AMOLED display.",
    price: 249.5,
    brand: "WristGenix",
  },
  {
    id: "3",
    name: "Mechanical Keyboard",
    description:
      "RGB mechanical keyboard with tactile blue switches and a premium aluminum frame.",
    price: 129.0,
    brand: "KeyMaster",
  },
];

const ProductList: React.FC = () => {
  return (
    <div className="product-list-container">
      <h2>Featured Products</h2>
      <div className="product-grid">
        {DUMMY_PRODUCTS.map((product) => (
          <Product key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductList;
