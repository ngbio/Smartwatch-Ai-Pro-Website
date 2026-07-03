import { lazy, Suspense, useEffect, useState } from "react";
import Hero from "../../components/Hero";
import MySpinner from "../../components/MySpinner";
import useScrollReveal from "../../hooks/useScrollReveal";
import { getProduct } from "../../services/productService";

const Chatbot = lazy(() => import("../../components/Chatbot"));
const Features = lazy(() => import("../../components/Features"));
const Specifications = lazy(() => import("../../components/Specifications"));
const SubscribeForm = lazy(() => import("../../components/SubscribeForm"));

const Home = () => {
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [showDeferredSections, setShowDeferredSections] = useState(false);

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

    useEffect(() => {
        if (!product)
            return undefined;

        const schedule = window.requestIdleCallback || ((callback) => window.setTimeout(callback, 800));
        const cancel = window.cancelIdleCallback || window.clearTimeout;
        const handle = schedule(() => setShowDeferredSections(true));

        return () => cancel(handle);
    }, [product]);
    
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
                <div className="alert alert-warning mt-3" role="alert">
                    {error}
                </div>
            )}

            {currentProduct && <Hero product={currentProduct} />}
            {showDeferredSections && (
                <Suspense fallback={null}>
                    <Features features={currentProduct?.features || []} />
                    <Specifications specifications={currentProduct?.specifications || []} />
                    <SubscribeForm />
                    <Chatbot />
                </Suspense>
            )}
        </>
    );
};
export default Home;
