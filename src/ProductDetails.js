import { useNavigate, useParams } from "react-router-dom";
import useFetch from "./useFetch";

const ProductDetails = () => {
  const { id } = useParams();
  const token = sessionStorage.getItem("token");
  const {
    data: products,
    error,
    isPending,
  } = useFetch("http://localhost:5000/api/products/" + id, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token,
    },
  });
  const navigate = useNavigate();
  const handleClick = () => {
    fetch("http://localhost:5000/api/products/" + id, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
      },
    }).then(() => {
      navigate("/");
    });
  };

  return (
    <div className="product-details">
      {isPending && <div>Loading...</div>}
      {error && <div>{error}</div>}
      {products && (
        <article>
          {products.map((product) => (
            <div key={product.category_id}>
              <h2>{product.name}</h2>
              <p>
                Description: {product.description} <br />
                Quantity: {product.quantity} <br />
                Price: {product.price} <br />
                Status: {product.status}
              </p>
            </div>
          ))}
          <button onClick={handleClick}>Delete</button>
        </article>
      )}
    </div>
  );
};

export default ProductDetails;
