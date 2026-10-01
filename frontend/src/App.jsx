import { useEffect, useState } from "react";
import { getProducts, getOrders, createOrder, createProduct, getShipments } from "./api";
import "./App.css";

function App() {
    const [products, setProducts] = useState([]);
    const [orders, setOrders] = useState([]);
    const [shipments, setShipments] = useState([]);

    const [productName, setProductName] = useState("");
    const [productPrice, setProductPrice] = useState("");
    const [productStock, setProductStock] = useState("");

    async function loadData() {
        const [productsData, ordersData, shipmentData] = await Promise.all([
            getProducts(),
            getOrders(),
            getShipments(),
        ]);

        setProducts(productsData);
        setOrders(ordersData);
        setShipments(shipmentData);
    }

    async function handleAddProduct(event) {
    event.preventDefault();

    await createProduct(
        productName,
        productPrice,
        productStock
    );

    setProductName("");
    setProductPrice("");
    setProductStock("");

    await loadData();
    }

    useEffect(() => {
        loadData();
    }, []);

    async function handleBuy(productId) {
        await createOrder(productId, 1);
        await loadData();
    }

    return (
        <div>
            <h1>Mini Marketplace</h1>

           <h2>Products</h2>

            <form onSubmit={handleAddProduct}>
                <input
                    type="text"
                    placeholder="Product name"
                    value={productName}
                    onChange={(e) => setProductName(e.target.value)}
                />

                <input
                    type="number"
                    placeholder="Price (pence)"
                    value={productPrice}
                    onChange={(e) => setProductPrice(e.target.value)}
                />

                <input
                    type="number"
                    placeholder="Stock"
                    value={productStock}
                    onChange={(e) => setProductStock(e.target.value)}
                />

                <button type="submit">
                    Add Product
                </button>
            </form>

            {products.map((product) => (
                <div key={product.id}>
                    <h3>{product.name}</h3>
                    <p>£{(product.price / 100).toFixed(2)}</p>
                    <p>Stock: {product.stock}</p>

                    <button
                        onClick={() => handleBuy(product.id)}
                        disabled={product.stock <= 0}
                    >
                        {product.stock > 0 ? "Buy" : "Out of stock"}
                    </button>
                </div>
            ))}
        <div className="data-panels">
        <div>
            <h2>Orders</h2>

            <button onClick={() => loadData()}>
                Refresh Orders
            </button>

            {orders.length === 0 ? (
                <p>No orders yet.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        {orders.map((order) => (
                            <tr key={order.id}>
                                <td>{order.id}</td>
                                <td>{order.product_id}</td>
                                <td>{order.quantity}</td>
                                <td>{order.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            </div>

            <div>
            <h2>Shipments</h2>

            {shipments.length === 0 ? (
                <p>No shipments yet.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Order</th>
                            <th>Status</th>
                            <th>Created</th>
                        </tr>
                    </thead>

                    <tbody>
                        {shipments.map((shipment) => (
                            <tr key={shipment.id}>
                                <td>{shipment.id}</td>
                                <td>{shipment.order_id}</td>
                                <td>{shipment.status}</td>
                                <td>{shipment.created_at}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
        </div>
        </div>
    );
}

export default App;