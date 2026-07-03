import { useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import Chatbot from "../../components/Chatbot";
import Features from "../../components/Features";
import Hero from "../../components/Hero";
import MySpinner from "../../components/MySpinner";
import Specifications from "../../components/Specifications";
import SubscribeForm from "../../components/SubscribeForm";
import useScrollReveal from "../../hooks/useScrollReveal";
import { getProduct } from "../../services/productService";

const Home = () => {
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useScrollReveal();

    const loadProduct = async () => {
        try {
            setLoading(true);
            setError("");

            const res = await getProduct();

            const loadedProduct = res.data || null;
            setProduct(loadedProduct && Object.keys(loadedProduct).length ? loadedProduct : null);
        } catch (ex) {
            setProduct(null);
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

    const currentProduct = product
        ? {
            ...product,
            features: product.features || [],
            specifications: product.specifications || [],
            heroSpecifications: product.specifications || [],
            image: product.image || "",
            image_url: product.image_url || "",
        }
        : null;

    return (
        <>
            {error && (
                <Alert variant="warning" className="mt-3">
                    {error}
                </Alert>
            )}

            {currentProduct && <Hero product={currentProduct} />}
            <Features features={currentProduct?.features || []} />
            <Specifications specifications={currentProduct?.specifications || []} />
            <SubscribeForm />
            <Chatbot />
        </>
    );
};
export default Home;
