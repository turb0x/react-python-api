import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, checkEmail] = useState("");
  const [password, checkPassword] = useState("");
  const [isPending, setIsPending] = useState(false);
  const navigate = useNavigate();

  const handleSumbit = (e) => {
    e.preventDefault();
    const login = { email, password };

    setIsPending(true);

    fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(login),
    }).then((response) => {
        response.json().then((data) => {
            sessionStorage.setItem('token', data.token)
        })
      setIsPending(false);
      navigate('/')
    });
    
  };
  return (
    <div className="create">
      <h2>Login</h2>
      <form onSubmit={handleSumbit}>
        <label>Email:</label>
        <input
          type="text"
          placeholder="someone@domain.com"
          required
          value={email}
          onChange={(e) => checkEmail(e.target.value)}
        />
        <label>Password:</label>
        <input
          type="password"
          required
          value={password}
          onChange={(e) => checkPassword(e.target.value)}
        />
        <a href='/api/forgot-password'>Forgot password?</a>
        <br></br>
        {!isPending && <button>Login</button>}
        {isPending && <button disabled>Logging in...</button>}
      </form>
    </div>
  );
};

export default Login;
