import { Link } from "react-router-dom";

const productList = ({ products, title }) => {
  return (
    <div className="product-list">
      <h2>{title}</h2>
      {products.map((product) => (
        <div className="product-preview" key={product.category_id}>
          <Link to={`/products/${product.category_id}`}>
            <h2>{product.name} | {product.quantity}</h2>
            <p>{product.description}</p>
          </Link>
        </div>
      ))}
    </div> 
  );
};

export default productList;
