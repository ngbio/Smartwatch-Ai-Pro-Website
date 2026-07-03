import { Card, Col, Row } from "react-bootstrap";

const featureIcons = {
  heart: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M20.8 4.9a5.5 5.5 0 0 0-7.8 0L12 5.9l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.3 1-1a5.5 5.5 0 0 0 0-7.8Z" />
    </svg>
  ),
  "map-pin": (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 22s7-5.4 7-12a7 7 0 1 0-14 0c0 6.6 7 12 7 12Z" />
      <circle cx="12" cy="10" r="2.5" />
    </svg>
  ),
  "battery-charging": (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v1h1.5a1.5 1.5 0 0 1 0 3H19v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8Z" />
      <path d="m12.5 8-4 5h3l-1 4 4-5h-3l1-4Z" />
    </svg>
  ),
  droplets: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7.5 3.5S3 8.4 3 12a4.5 4.5 0 0 0 9 0c0-3.6-4.5-8.5-4.5-8.5Z" />
      <path d="M16.5 6S13 9.8 13 12.7a3.5 3.5 0 0 0 7 0C20 9.8 16.5 6 16.5 6Z" />
    </svg>
  ),
  AI: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 2 14 8l6 2-6 2-2 6-2-6-6-2 6-2 2-6Z" />
      <path d="M18 15 19 18l3 1-3 1-1 3-1-3-3-1 3-1 1-3Z" />
    </svg>
  ),
};

function getFeatureIcon(icon) {
  return featureIcons[icon] || featureIcons.AI;
}

function Features({ features }) {
  if (!features.length)
    return null;

  return (
    <section className="section-block premium-section reveal">
      <div className="section-heading">
        <span className="section-kicker">Designed for daily health</span>
        <h2 className="section-title">Tính năng nổi bật</h2>
        <p>Mọi cảm biến, thông báo và tính năng luyện tập được sắp xếp để người dùng hiểu sản phẩm ngay trong vài giây.</p>
      </div>
      <Row className="g-4">
        {features.map(f => (
          <Col md={6} lg={3} key={f.title}>
            <Card className="feature-card h-100">
              <Card.Body>
                <div className="feature-icon">{getFeatureIcon(f.icon)}</div>
                <Card.Title>{f.title}</Card.Title>
                <Card.Text>{f.description}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </section>
  );
}

export default Features;
