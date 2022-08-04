import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
const [name, registerName] = useState("");
  const [email, registerEmail] = useState("");
  const [password, checkPassword] = useState("");
  const [password_confirmation, checkPasswordConfirmation] = useState("");
  const [isPending, setIsPending] = useState(false);
  const navigate = useNavigate();

  const handleSumbit = (e) => {
    e.preventDefault();
    const register = { name, email, password, password_confirmation };

    setIsPending(true);

    fetch("http://localhost:5000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(register),
    }).then(() => {
      setIsPending(false);
      navigate('/')
    });
    
  };
  return (
    <div className="create">
      <h2>Register</h2>
      <form onSubmit={handleSumbit}>
      <label>Name:</label>
        <input
          type="text"
          placeholder="John"
          required
          value={name}
          onChange={(e) => registerName(e.target.value)}
        />
        <label>Email:</label>
        <input
          type="text"
          placeholder="someone@domain.com"
          required
          value={email}
          onChange={(e) => registerEmail(e.target.value)}
        />
        <label>Password:</label>
        <input
          type="password"
          required
          value={password}
          onChange={(e) => checkPassword(e.target.value)}
        />
        <label>Password confirmation:</label>
        <input
          type="password"
          required
          value={password_confirmation}
          onChange={(e) => checkPasswordConfirmation(e.target.value)}
        />
        {!isPending && <button>Register</button>}
        {isPending && <button disabled>Registering...</button>}
      </form>
    </div>
  );
};

export default Register;
