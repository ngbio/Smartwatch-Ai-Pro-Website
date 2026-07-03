import { Button, Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";

function Header({ theme, onToggleTheme }) {
  return (
    <Navbar expand="lg" className="site-navbar" variant={theme}>
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold">
          SmartWatch AI Pro
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="main-navbar" />
        <Navbar.Collapse id="main-navbar">
          <Nav className="ms-auto">
            <Link to="/" className="nav-link">Trang chủ</Link>
            <Link to="/product" className="nav-link">Sản phẩm</Link>
            <Link to="/subscribe" className="nav-link">Đăng ký</Link>
          </Nav>
          <Button
            className="theme-toggle"
            variant="outline-info"
            size="sm"
            onClick={onToggleTheme}
          >
            {theme === "dark" ? "Light" : "Dark"}
          </Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
