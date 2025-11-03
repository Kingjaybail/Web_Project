import React, { useState } from 'react';
import './login.scss';
import router_functions from '../../Routes/routes';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const res = await router_functions.loginUser(formData.username, formData.password);
      console.log('Login response:', res);

      if (res.data === true) {
        setMessage({ type: 'success', text: 'Logging in...' });

        setTimeout(() => {
          localStorage.setItem('isLoggedIn', 'true');
          localStorage.setItem("username", username);
          window.location.href = '/';
        }, 1500);
      } else {
        setMessage({ type: 'error', text: 'Invalid username or password.' });
      }
    } catch (error) {
      console.error('Login failed:', error);
      setMessage({
        type: 'error',
        text: 'Unable to connect to server. Please try again later.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Welcome Back</h2>

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
            disabled={loading}
          />
        </div>

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
            disabled={loading}
          />
        </div>

        {message && (
          <div
            className={`feedback-message ${
              message.type === 'error' ? 'error' : 'success'
            }`}
          >
            {message.text}
          </div>
        )}

        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? 'Logging in...' : 'Log In'}
        </button>

        <div className="login-footer">
          Don’t have an account?<a href="/signup">Sign up</a>
        </div>
      </form>
    </div>
  );
};

export default Login;
