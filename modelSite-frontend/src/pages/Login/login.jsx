import React, { useState } from 'react';
import './login.scss';
import router_functions from '../../Routes/routes';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await router_functions.loginUser(formData.username, formData.password);
    console.log(res);

    if (res.Success) {
      console.log("Successful");
      window.location.href = "/";
    } else {
      console.log("Failed");
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Welcome Back</h2>

        {/* Username Field */}
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Enter your username"
            required
          />
        </div>

        {/* Password Field */}
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
          />
        </div>

        <button type="submit" className="submit-button">
          Log In
        </button>

        <div className="login-footer">
          Don’t have an account?<a href="/signup">Sign up</a>
        </div>
      </form>
    </div>
  );
};

export default Login;
