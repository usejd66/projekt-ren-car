/* DriveOn - script.js
   Vetëm ajo që përdoret: navbar-i gjatë scroll-it, butoni "kthehu lart",
   shfaqja e butë e seksioneve dhe butoni i fjalëkalimit. */
(() => {
    "use strict";

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const navbar = document.querySelector(".navbar-enhanced");

    /* Butoni "kthehu lart" */
    const toTop = document.createElement("button");
    toTop.id = "backToTop";
    toTop.type = "button";
    toTop.setAttribute("aria-label", "Back to top");
    toTop.innerHTML =
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
    toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" }));
    document.body.appendChild(toTop);

    /* Scroll: një përditësim për frame, pa matje të rënda */
    let ticking = false;
    const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
            const y = window.scrollY;
            if (navbar) navbar.classList.toggle("scrolled", y > 50);
            toTop.classList.toggle("show", y > 600);
            ticking = false;
        });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    /* Shfaqja e butë e elementeve kur hyjnë në ekran.
       Elementet që janë tashmë në ekran në ngarkim nuk animohen (pa "flash"). */
    if (reducedMotion || !("IntersectionObserver" in window)) return;

    const REVEAL = [
        ".section-head", ".category-tile", ".car-tile", ".step", ".why-list li", ".why-image",
        ".review", ".faq .accordion-item", ".cta-band-inner",
        ".car-card", ".about-section .row > *", "footer .row.g-4 > *",
    ].join(",");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
        });
    }, { rootMargin: "0px 0px -40px 0px", threshold: 0.05 });

    const vh = window.innerHeight;
    const groups = new Map();
    document.querySelectorAll(REVEAL).forEach((el) => {
        if (el.getBoundingClientRect().top < vh) return; // tashmë në ekran
        const parent = el.parentElement;
        const index = groups.get(parent) || 0;
        groups.set(parent, index + 1);
        el.classList.add("reveal");
        el.style.transitionDelay = `${Math.min(index, 4) * 60}ms`; // radhë e lehtë brenda një grupi
        observer.observe(el);
    });
})();

/* Butoni "shfaq/fshih fjalëkalimin" (Sign Up) */
function togglePassword(id, button) {
    const input = document.getElementById(id);
    const use = button.querySelector("use");
    if (!input) return;

    const show = input.type === "password";
    input.type = show ? "text" : "password";
    if (use) {
        const href = use.getAttribute("href").replace(/#i-eye(-slash)?$/, show ? "#i-eye-slash" : "#i-eye");
        use.setAttribute("href", href);
    }
}
