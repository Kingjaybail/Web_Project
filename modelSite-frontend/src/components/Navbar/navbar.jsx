import { Link } from 'react-router-dom';
import './navbar.scss';

const Navbar = () => {
  return (
    <nav className="navbar">
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
          <Link to="/visualize" className="navbar-link">
            Visualize
          </Link>
        </li>
        <li className="navbar-item">
          <Link to="/about" className="navbar-link">
            About
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;