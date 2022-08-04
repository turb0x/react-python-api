import ProductList from "./ProductList";
import useFetch from "./useFetch";

const Home = () => {
  const token = sessionStorage.getItem("token");
  const {
    error,
    isPending,
    data: products,
  } = useFetch("http://localhost:5000/api/products/all", {
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token,
    }});
  return (
    <div className="home">
      {error && <div>{error}</div>}
      {isPending && <div>Loading...</div>}
      {products && <ProductList products={products} />}
    </div>
  );
};

export default Home;
