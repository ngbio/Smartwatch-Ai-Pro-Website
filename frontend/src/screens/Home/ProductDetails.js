import { useEffect, useState } from "react";
import { Alert, Button, Card, Col, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import Features from "../../components/Features";
import MySpinner from "../../components/MySpinner";
import Specifications from "../../components/Specifications";
import useScrollReveal from "../../hooks/useScrollReveal";
import { getProduct } from "../../services/productService";

const ProductDetails = () => {
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [productImage, setProductImage] = useState("");
    const [imageError, setImageError] = useState(false);
    const shouldShowProductImage = productImage && !imageError;

    useScrollReveal();

    const loadProduct = async () => {
        try {
            setLoading(true);
            setError("");
            const res = await getProduct();
            const loadedProduct = res.data || null;

            setProduct(loadedProduct && Object.keys(loadedProduct).length ? loadedProduct : null);
            setProductImage(loadedProduct?.image || loadedProduct?.image_url || "");
            setImageError(false);
        } catch (ex) {
            setProduct(null);
            setProductImage("");
            setImageError(false);
            setError("Chưa tải được dữ liệu sản phẩm từ API.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProduct();
    }, []);

    if (loading && !product) {
        return <MySpinner />;
    }

    if (!product) {
        return (
            <main className="product-page">
                {error && <Alert variant="warning" className="mt-3">{error}</Alert>}
            </main>
        );
    }

    const currentProduct = {
        ...product,
        features: product.features || [],
        specifications: product.specifications || [],
        image: product.image || "",
        image_url: product.image_url || "",
    };

    return (
        <main className="product-page">
            {error && <Alert variant="warning" className="mt-3">{error}</Alert>}
            {loading && <MySpinner />}

            <section className="section-block product-detail-section">
                <Row className="align-items-center g-4">
                    <Col md={5}>
                        <Card className="product-image-card">
                            <Card.Body>
                                <div className="product-showcase detail-showcase">
                                    <div className="showcase-glow"></div>
                                    <div className="hero-glass-orbit detail-glass-orbit"></div>
                                    {shouldShowProductImage && (
                                        <div className="hero-product-layer detail-product-layer">
                                            <img
                                                alt={currentProduct.name}
                                                className="hero-product-image detail-product-image"
                                                src={productImage}
                                                onError={() => setImageError(true)}
                                            />
                                        </div>
                                    )}
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={7}>
                        <span className="section-kicker">Smart wearable</span>
                        <h1 className="product-detail-title">{currentProduct.name}</h1>
                        <h4 className="text-info">{currentProduct.price}</h4>
                        <p className="product-detail-subtitle">{currentProduct.subtitle}</p>
                        <p className="text-muted">{currentProduct.description}</p>
                        <div className="product-detail-actions">
                            <Button as={Link} to="/subscribe" variant="info">
                                Đăng ký nhận tin
                            </Button>
                        </div>
                    </Col>
                </Row>
            </section>

            <Features features={currentProduct.features || []} />
            <Specifications specifications={currentProduct.specifications || []} />
        </main>
    );
};

export default ProductDetails;
