import { Link } from 'react-router-dom';
import './navbar.scss';
const Navbar = () => {

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    window.location.href = '/login';
  };


  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="navbar-logo">
          <Link to="/" className="navbar-brand">
            <p className="brand-text">ModelSite</p>
          </Link>
        </div>

        <ul className="navbar-list">
          <li className="navbar-item">
            <Link to="/" className="navbar-link">
              Home
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/models" className="navbar-link">
              Models
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/about" className="navbar-link">
              About
            </Link>
          </li>
          <li className="navbar-item">
              <Link to="/comparisons" className="navbar-link">
                Comparisons
              </Link>
          </li>
        </ul>
        {localStorage.getItem('isLoggedIn') === 'true' && (
          <button onClick={handleLogout}>Logout</button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;