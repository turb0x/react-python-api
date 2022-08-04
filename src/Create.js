import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Create = () => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [status, setStatus] = useState("Inactive");
  const [isPending, setIsPending] = useState(false);
  const token = sessionStorage.getItem("token");
  const navigate = useNavigate();

  const handleSumbit = (e) => {
    e.preventDefault();
    const product = { name, description, quantity, price, status };

    setIsPending(true);

    fetch("http://localhost:5000/api/products/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
      },
      body: JSON.stringify(product),
    }).then(() => {
      setIsPending(false);
      navigate("/");
    });
  };
  return (
    <div className="create">
      <h2>Add a New Product</h2>
      <form onSubmit={handleSumbit}>
        <label>Name:</label>
        <input
          type="text"
          placeholder="Ex. T-Shirt"
          required
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <label>Description:</label>
        <textarea
          required
          placeholder="Ex. Blue, Size M"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
        <label>Quantity:</label>
        <input
          type="number"
          placeholder="Ex. 100"
          required
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
        <label>Price:</label>
        <input
          type="number"
          placeholder="Ex. 50"
          required
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />
        <label>Status:</label>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        {!isPending && <button>Add Product</button>}
        {isPending && <button disabled>Adding...</button>}
      </form>
    </div>
  );
};

export default Create;
