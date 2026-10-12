/* =========================================================
   DRIVEON - SCRIPT I PËRBASHKËT (versioni i optimizuar)
   Animacionet i bën CSS-ja (animations.css), ky skedar i nis.
   Funksionon në telefon, tablet dhe PC.
   Ngarkoje me:  <script src="script.js" defer></script>
========================================================= */

(function () {
    "use strict";

    function init() {

        /* =====================================================
           KONFIGURIME & GJENDJA E PAJISJES
        ===================================================== */

        const reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
        const mobileQuery = window.matchMedia("(max-width: 768px)");
        const touchQuery = window.matchMedia("(hover: none), (pointer: coarse)");

        const prefersReduced = () => reducedQuery.matches;
        const isMobile = () => mobileQuery.matches;
        const isTouch = () => touchQuery.matches;

        /* Parallax vetëm në desktop me maus (kursen bateri dhe CPU në telefon/tablet) */
        const parallaxEnabled = () => !prefersReduced() && !isMobile() && !isTouch();

        const doc = document.documentElement;
        const viewportHeight = () => doc.clientHeight || window.innerHeight;
        const getScrollY = () => window.pageYOffset || doc.scrollTop || 0;


        /* =====================================================
           ELEMENTET E KRIJUARA NGA JS
        ===================================================== */

        /* Progress bar: përdor transform (GPU), jo width (shkakton layout) */
        const progressBar = document.createElement("div");
        progressBar.id = "scrollProgress";
        progressBar.setAttribute("aria-hidden", "true");
        progressBar.style.width = "100%";
        progressBar.style.transformOrigin = "left center";
        progressBar.style.transform = "scaleX(0)";
        progressBar.style.willChange = "transform";
        document.body.appendChild(progressBar);

        /* Back to top: SVG inline, pra nuk varet nga Font Awesome */
        const backToTop = document.createElement("button");
        backToTop.id = "backToTop";
        backToTop.type = "button";
        backToTop.setAttribute("aria-label", "Kthehu lart");
        backToTop.innerHTML =
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
            'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
            '<path d="M12 19V5M5 12l7-7 7 7"/></svg>';
        document.body.appendChild(backToTop);

        backToTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: prefersReduced() ? "auto" : "smooth" });
        });


        /* =====================================================
           ELEMENTET & MATJET E CACHE-UARA
           (lexohen rrallë, jo në çdo frame të scroll-it)
        ===================================================== */

        const navbar = document.querySelector(".navbar-enhanced");
        const heroSection = document.querySelector(".hero");
        const heroContent = document.querySelector(".hero .container");

        let heroLimit = 0;
        let maxScroll = 0;

        function measure() {
            heroLimit = heroSection ? heroSection.offsetHeight : 0;
            maxScroll = Math.max(0, doc.scrollHeight - viewportHeight());
        }

        function resetHero() {
            if (!heroContent) return;
            heroContent.style.transform = "";
            heroContent.style.opacity = "";
            heroContent.style.willChange = "";
        }


        /* =====================================================
           SCROLL HANDLER (një herë për frame)
        ===================================================== */

        let ticking = false;

        function render() {
            ticking = false;

            const y = getScrollY();

            /* Progress bar */
            const progress = maxScroll > 0 ? Math.min(1, Math.max(0, y / maxScroll)) : 0;
            progressBar.style.transform = "scaleX(" + progress + ")";

            /* Back to top */
            backToTop.classList.toggle("show", y > 600);

            /* Navbar */
            if (navbar) navbar.classList.toggle("scrolled", y > 50);

            /* Hero parallax (vetëm desktop) */
            if (heroContent && heroSection) {
                if (!parallaxEnabled() || heroLimit <= 0) {
                    if (heroContent.style.transform || heroContent.style.opacity) resetHero();
                } else {
                    const clamped = Math.min(y, heroLimit);
                    heroContent.style.willChange = "transform, opacity";
                    heroContent.style.transform = "translate3d(0," + (clamped * 0.18).toFixed(1) + "px,0)";
                    heroContent.style.opacity = Math.max(0, 1 - clamped / (heroLimit * 0.9)).toFixed(3);
                }
            }
        }

        function onScroll() {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(render);
        }

        window.addEventListener("scroll", onScroll, { passive: true });


        /* =====================================================
           RESIZE / ORIENTIM / NDRYSHIM I PËRMBAJTJES
        ===================================================== */

        let resizeTimer = null;

        function onResize() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                measure();
                render();
            }, 120);
        }

        window.addEventListener("resize", onResize, { passive: true });
        window.addEventListener("orientationchange", onResize, { passive: true });

        /* Kur faqja bëhet më e gjatë/shkurtër (p.sh. kartat ngarkohen me JS) rimatet vetë */
        if ("ResizeObserver" in window) {
            new ResizeObserver(onResize).observe(document.body);
        }

        measure();
        render();


        /* =====================================================
           SHFAQJE ME SCROLL (REVEAL)
           [selektori, lloji i animacionit, stagger?]
           Llojet: up, left, right, zoom
        ===================================================== */

        const revealConfig = [
            [".process-section .text-center.mb-5", "up", false],
            [".process-section .row > [class*='col-']", "up", true],

            ["section.py-5 .text-center.mb-5", "up", false],
            [".row.g-4 > [class*='col-']", "up", true],
            [".text-center.mt-5", "up", false],

            [".why-image", "left", false],
            [".why-label, .why-title, .why-description", "up", true],
            [".why-text-item", "left", true],

            [".accordion-item", "up", true],

            [".cta-section .col-lg-8", "left", false],
            [".cta-section .col-lg-4", "right", false],

            ["section.py-5 .img-fluid", "zoom", false],

            ["footer .row.g-4 > [class*='col-']", "up", true]
        ];

        const REVEAL_CLASSES = ["reveal", "visible", "reveal-up", "reveal-left", "reveal-right", "reveal-zoom"];

        /* Elementet që janë përpunuar një herë nuk riprocesohen kurrë (pa animacion të dyfishtë) */
        const processed = new WeakSet();

        const canObserve = "IntersectionObserver" in window && !prefersReduced();

        function cleanupReveal(el) {
            el.classList.remove.apply(el.classList, REVEAL_CLASSES);
            el.style.transitionDelay = "";
        }

        function showReveal(el) {
            if (el.classList.contains("visible")) return;

            el.classList.add("visible");
            if (revealObserver) revealObserver.unobserve(el);

            /* Pas animacionit e heqim klasën, që hover-i i kartave të punojë normalisht.
               Përdorim transitionend (ndjek CSS-në), me timeout si rezervë. */
            let done = false;
            const finish = () => {
                if (done) return;
                done = true;
                el.removeEventListener("transitionend", onEnd);
                cleanupReveal(el);
            };
            const onEnd = (e) => {
                if (e.target === el && (e.propertyName === "opacity" || e.propertyName === "transform")) {
                    finish();
                }
            };
            el.addEventListener("transitionend", onEnd);
            setTimeout(finish, 2200);
        }

        const revealObserver = canObserve
            ? new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) showReveal(entry.target);
                });
            }, { threshold: 0.05, rootMargin: "0px 0px -40px 0px" })
            : null;

        /* Regjistron elementet e reja. Mund të thirret sa herë që shtohet përmbajtje dinamike. */
        function registerReveals(root) {
            if (!revealObserver) return [];

            const scope = root || document;
            const added = [];
            const mobile = isMobile();

            revealConfig.forEach(([selector, type, stagger]) => {
                const groups = new Map();

                scope.querySelectorAll(selector).forEach((el) => {
                    if (processed.has(el)) return;
                    if (el.classList.contains("reveal")) return;
                    if (el.parentElement && el.parentElement.closest(".reveal")) return;
                    if (el.closest("#selectedCarWrapper")) return;

                    const parent = el.parentElement;
                    if (!groups.has(parent)) groups.set(parent, []);
                    groups.get(parent).push(el);
                });

                groups.forEach((items) => {
                    items.forEach((el, index) => {
                        processed.add(el);
                        el.classList.add("reveal", "reveal-" + type);

                        /* Stagger vetëm në ekran të gjerë; në telefon çdo kartë del menjëherë kur hyn në ekran */
                        if (stagger && !mobile) {
                            el.style.transitionDelay = Math.min(index, 5) * 0.12 + "s";
                        }

                        revealObserver.observe(el);
                        added.push(el);
                    });
                });
            });

            return added;
        }

        /* Elementet që janë tashmë në ekran kur hapet faqja hyjnë menjëherë, me kaskadë të lehtë */
        function revealInitial(elements) {
            const mobile = isMobile();
            const vh = viewportHeight();
            const rects = elements.map((el) => el.getBoundingClientRect()); /* një lexim i vetëm */

            let order = 0;
            elements.forEach((el, i) => {
                const rect = rects[i];
                if (rect.top < vh && rect.bottom > 0) {
                    el.style.transitionDelay = mobile
                        ? Math.min(order, 3) * 0.05 + "s"
                        : 0.15 + Math.min(order, 6) * 0.1 + "s";
                    order++;
                    showReveal(el);
                }
            });
        }

        if (revealObserver) {
            const initial = registerReveals(document);

            /* Detyrojmë llogaritjen e gjendjes së fshehur para se të nisë animacioni */
            void document.body.offsetHeight;
            revealInitial(initial);

            /* Përmbajtje dinamike (p.sh. karta makinash të shtuara me JS) */
            if ("MutationObserver" in window) {
                let mutationTimer = null;
                new MutationObserver((mutations) => {
                    const hasNewNodes = mutations.some((m) => m.addedNodes.length > 0);
                    if (!hasNewNodes) return;

                    clearTimeout(mutationTimer);
                    mutationTimer = setTimeout(() => {
                        const fresh = registerReveals(document);
                        if (fresh.length) {
                            void document.body.offsetHeight;
                            revealInitial(fresh);
                        }
                    }, 80);
                }).observe(document.body, { childList: true, subtree: true });
            }
        }

        /* Rezervë: nëse observer-i nuk nisi ndonjë element që është në ekran, e tregojmë një herë pas ngarkimit.
           (Nuk thirret më në çdo scroll.) */
        function revealStragglers() {
            if (!revealObserver) return;
            const vh = viewportHeight();
            document.querySelectorAll(".reveal:not(.visible)").forEach((el) => {
                const rect = el.getBoundingClientRect();
                if (rect.top < vh * 0.92 && rect.bottom > 0) showReveal(el);
            });
        }

        /* API për përdorim manual nga skriptet e tjera: window.driveonRefreshReveal() */
        window.driveonRefreshReveal = function () {
            const fresh = registerReveals(document);
            if (fresh.length) {
                void document.body.offsetHeight;
                revealInitial(fresh);
            }
        };


        /* =====================================================
           NUMËRUESIT TE HERO (50+, 100% ... ; "24/7" mbetet siç është)
           Vendosen në 0 menjëherë (pa vezullim), niset kur hyjnë në ekran.
        ===================================================== */

        function prepareCounter(el) {
            const match = el.textContent.trim().match(/^(\d+)(\D*)$/);
            if (!match) return null;

            return {
                el: el,
                target: parseInt(match[1], 10),
                suffix: match[2],
                finalText: el.textContent
            };
        }

        function runCounter(item) {
            const duration = 1600;
            const start = performance.now();

            function frame(now) {
                const t = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - t, 3);

                item.el.textContent = Math.round(item.target * eased) + item.suffix;

                if (t < 1) {
                    requestAnimationFrame(frame);
                } else {
                    item.el.textContent = item.finalText;
                }
            }

            requestAnimationFrame(frame);
        }

        if (!prefersReduced()) {
            const items = Array.from(document.querySelectorAll(".hero-stat strong"))
                .map(prepareCounter)
                .filter(Boolean);

            if (items.length) {
                items.forEach((item) => { item.el.textContent = "0" + item.suffix; });

                if ("IntersectionObserver" in window) {
                    const counterObserver = new IntersectionObserver((entries) => {
                        entries.forEach((entry) => {
                            if (!entry.isIntersecting) return;
                            const item = items.find((i) => i.el === entry.target);
                            counterObserver.unobserve(entry.target);
                            if (item) setTimeout(() => runCounter(item), 250);
                        });
                    }, { threshold: 0.3 });

                    items.forEach((item) => counterObserver.observe(item.el));
                } else {
                    items.forEach((item) => { item.el.textContent = item.finalText; });
                }
            }
        }


        /* =====================================================
           NGARKIMI I PLOTË
        ===================================================== */

        window.addEventListener("load", () => {
            measure();
            render();
            revealStragglers();
            setTimeout(revealStragglers, 600);
        });

        /* Kthimi nga cache (butoni Back, sidomos në iPhone/Safari) */
        window.addEventListener("pageshow", (e) => {
            if (e.persisted) {
                measure();
                render();
                revealStragglers();
            }
        });
    }

    /* Siguri: nëse skedari ngarkohet në <head> pa defer, presim DOM-in */
    if (document.body) {
        init();
    } else {
        document.addEventListener("DOMContentLoaded", init);
    }
})();