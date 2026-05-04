const fetchBtn = document.getElementById("fetch-btn");
const container = document.getElementById("product-container");

const API_URL = "http://localhost:8000/api/products/";

async function loadProducts() {
  console.log("--- API Fetch Started ---");
  try {
    const response = await fetch(API_URL);

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    console.log("Data successfully received:", data);

    displayProductList(data.items);
  } catch (error) {
    console.error("Critical Fetch Error:", error);
    container.innerHTML = `
      <div style="color: #721c24; background: #f8d7da; padding: 15px; border-radius: 5px; width: 100%;">
      <strong>Connection Failed!</strong><br>
      Could not reach the Django API at ${API_URL}. <br>
      <em>Hint: Run "python manage.py runserver" in your backend folder.</em>
      </div>
    `;
  }
}

function displayProductList(products) {
  if (products.length === 0) {
    container.innerHTML = "<p>No products found in the database.</p>";
    return;
  }

  console.log(products)

  products.forEach((product, index) => {
    const productTile = document.createElement("div");
    productTile.className = "product-tile";

    productTile.style.animationDelay = `${index * 0.1}s`;

    productTile.innerHTML = `
      <div class="product-badge">Active</div>
      <h3>${product.name}</h3>
      <p class="description">${product.description || "No description provided."}</p>
      <div class="price">$${parseFloat(product.price).toFixed(2)}</div>
      <div class="brand">Brand: ${product.brand}</div>
    `;

    container.appendChild(productTile);
  });
}

fetchBtn.addEventListener("click", loadProducts);
