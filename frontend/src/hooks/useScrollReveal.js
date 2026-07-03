import { useEffect } from "react";

function useScrollReveal() {
  useEffect(() => {
    const observed = new WeakSet();

    const markVisible = element => {
      element.classList.add("is-visible");
    };

    const revealElements = () => document.querySelectorAll(".reveal");

    if (!window.IntersectionObserver) {
      revealElements().forEach(markVisible);
      return undefined;
    }

    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            markVisible(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 }
    );

    const syncObservedElements = () => {
      revealElements().forEach(element => {
        if (!observed.has(element)) {
          observed.add(element);
          observer.observe(element);
        }
      });
    };

    syncObservedElements();

    const mutationObserver = new MutationObserver(syncObservedElements);
    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true,
    });

    return () => {
      mutationObserver.disconnect();
      observer.disconnect();
    };
  }, []);
}

export default useScrollReveal;
