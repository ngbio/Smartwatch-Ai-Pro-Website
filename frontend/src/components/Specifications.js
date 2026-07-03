import { ListGroup } from "react-bootstrap";

function Specifications({ specifications }) {
  if (!specifications.length)
    return null;

  return (
    <section className="section-block specs-section reveal">
      <div className="section-heading">
        <span className="section-kicker">Hardware clarity</span>
        <h2 className="section-title">Thông số kỹ thuật</h2>
        <p>Các thông số quan trọng được trình bày rõ ràng để khách hàng so sánh nhanh trên desktop và mobile.</p>
      </div>
      <ListGroup className="spec-grid">
        {specifications.map(s => (
          <ListGroup.Item className="spec-item" key={s.name}>
            <strong>{s.name}</strong>
            <span>{s.value}</span>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </section>
  );
}

export default Specifications;
