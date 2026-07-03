import { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";

function Hero({ product }) {
  const [imageError, setImageError] = useState(false);
  const productImage = product.image || product.image_url || "";
  const shouldShowProductImage = productImage && !imageError;
  const specifications = product.heroSpecifications || [];

  const findExactSpecification = (...names) => specifications.find(spec => {
    const specName = (spec.name || "").toLowerCase();
    return names.some(name => specName === name);
  });

  const findSpecification = (...keywords) => specifications.find(spec => {
    const specName = (spec.name || "").toLowerCase();
    return keywords.some(keyword => specName.includes(keyword));
  });

  const healthSpec = findExactSpecification("health score")
    || findSpecification("health", "score", "suc khoe");
  const batterySpec = findExactSpecification("battery")
    || findSpecification("battery", "pin");

  useEffect(() => {
    setImageError(false);
  }, [productImage]);

  return (
    <section className="hero-panel reveal">
      <Row className="align-items-center justify-content-center g-5">
        <Col lg={8} className="hero-copy text-center">
          <div className="hero-badge">AI Wearable</div>
          <h1>{product.name}</h1>
          <p className="lead">{product.subtitle}</p>
          <p className="hero-description">{product.description}</p>
        </Col>
        <Col lg={9}>
          <div className="product-showcase hero-showcase">
            <div className="hero-radial-glow"></div>
            <div className="hero-glass-orbit"></div>
            {shouldShowProductImage && (
              <div className="hero-product-layer">
                <img
                  className="hero-product-image"
                  src={productImage}
                  alt={product.name}
                  onError={() => setImageError(true)}
                />
              </div>
            )}
            {healthSpec && (
              <div className="showcase-chip chip-health">
                <span>{healthSpec.name}</span>
                <strong>{healthSpec.value}</strong>
              </div>
            )}
            {batterySpec && (
              <div className="showcase-chip chip-battery">
                <span>{batterySpec.name}</span>
                <strong>{batterySpec.value}</strong>
              </div>
            )}
            <div className="showcase-chip chip-price">
              <span>Giá bán</span>
              <strong>{product.price}</strong>
            </div>
          </div>
        </Col>
      </Row>
    </section>
  );
}

export default Hero;
