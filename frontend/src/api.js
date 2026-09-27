const API_URL = "http://localhost:8000";

export async function getProduct(productId) {
    const response = await fetch(`${API_URL}/products/${productId}`);

    if (!response.ok) {
        throw new Error("Failed to fetch product");
    }

    return response.json();
}

export async function getProducts() {
    const response = await fetch(`${API_URL}/products`);

    if (!response.ok) {
        throw new Error("Failed to fetch products");
    }

    return response.json();
}

export async function createProduct(name, price, stock) {
    const response = await fetch(`${API_URL}/products`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name,
            price: Number(price),
            stock: Number(stock),
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to create product");
    }

    return response.json();
}

export async function createOrder(productId, quantity) {
    const response = await fetch(`${API_URL}/orders`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to create order");
    }

    return response.json();
}

export async function getOrders() {
    const response = await fetch(`${API_URL}/orders`);

    if (!response.ok) {
        throw new Error("Failed to fetch orders");
    }

    return response.json();
}