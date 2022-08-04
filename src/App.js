import Navbar from "./Navbar";
import Home from "./Home";
import Create from "./Create";
import NotFound from "./NotFound";
import { Route, Routes } from "react-router-dom";
import ProductDetails from "./ProductDetails";
import Login from "./Login";
import Register from "./Register";

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<Create />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/products/:id" element={<ProductDetails />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
