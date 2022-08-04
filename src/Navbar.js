import { Link } from "react-router-dom";

const Navbar = () => {

  
  return (
    <nav className="navbar">
      <Link to="/">
        <h1>Store</h1>
      </Link>
      <div className="links">
        <Link to="/create">New</Link>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </div>
    </nav>
  );
};

export default Navbar;
