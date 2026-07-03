import { Link } from "react-router-dom";

function Header({ theme, onToggleTheme }) {
  return (
    <header className="site-navbar">
      <nav className="container header-nav" aria-label="Main navigation">
        <Link to="/" className="navbar-brand fw-bold">
          SmartWatch AI Pro
        </Link>

        <div className="header-links">
          <Link to="/" className="nav-link">Trang chủ</Link>
          <Link to="/product" className="nav-link">Sản phẩm</Link>
          <Link to="/subscribe" className="nav-link">Đăng ký</Link>
          <button className="btn btn-outline-info btn-sm theme-toggle" type="button" onClick={onToggleTheme}>
            {theme === "dark" ? "Light" : "Dark"}
          </button>
        </div>
      </nav>
    </header>
  );
}

export default Header;
