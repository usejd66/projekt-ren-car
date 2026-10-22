/* DriveOn - script.js */

(function () {
    "use strict";

    function init() {
        /* Config */
        const reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
        const mobileQuery = window.matchMedia("(max-width: 768px)");
        const touchQuery = window.matchMedia("(hover: none), (pointer: coarse)");

        const prefersReduced = () => reducedQuery.matches;
        const isMobile = () => mobileQuery.matches;
        const isTouch = () => touchQuery.matches;
        const parallaxEnabled = () => !prefersReduced() && !isMobile() && !isTouch();

        const doc = document.documentElement;
        const viewportHeight = () => doc.clientHeight || window.innerHeight;
        const getScrollY = () => window.pageYOffset || doc.scrollTop || 0;

        /* Elements */
        const progressBar = document.createElement("div");
        progressBar.id = "scrollProgress";
        progressBar.setAttribute("aria-hidden", "true");
        progressBar.style.cssText = "width:100%;transform-origin:left center;transform:scaleX(0);will-change:transform";
        document.body.appendChild(progressBar);

        const backToTop = document.createElement("button");
        backToTop.id = "backToTop";
        backToTop.type = "button";
        backToTop.setAttribute("aria-label", "Kthehu lart");
        backToTop.innerHTML =
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
            '<path d="M12 19V5M5 12l7-7 7 7"/></svg>';
        document.body.appendChild(backToTop);

        backToTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: prefersReduced() ? "auto" : "smooth" });
        });

        /* Cache */
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

        /* Scroll */
        let ticking = false;

        function render() {
            ticking = false;

            const y = getScrollY();
            const progress = maxScroll > 0 ? Math.min(1, Math.max(0, y / maxScroll)) : 0;

            progressBar.style.transform = "scaleX(" + progress + ")";
            backToTop.classList.toggle("show", y > 600);

            if (navbar) navbar.classList.toggle("scrolled", y > 50);

            if (heroContent && heroSection) {
                if (!parallaxEnabled() || heroLimit <= 0) {
                    if (heroContent.style.transform || heroContent.style.opacity) resetHero();
                } else {
                    const clamped = Math.min(y, heroLimit);
                    heroContent.style.willChange = "transform, opacity";
                    heroContent.style.transform =
                        "translate3d(0," + (clamped * 0.18).toFixed(1) + "px,0)";
                    heroContent.style.opacity =
                        Math.max(0, 1 - clamped / (heroLimit * 0.9)).toFixed(3);
                }
            }
        }

        function onScroll() {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(render);
        }

        window.addEventListener("scroll", onScroll, { passive: true });

        /* Resize */
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

        if ("ResizeObserver" in window) {
            new ResizeObserver(onResize).observe(document.body);
        }

        measure();
        render();

        /* Reveal */
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

        const REVEAL_CLASSES = [
            "reveal",
            "visible",
            "reveal-up",
            "reveal-left",
            "reveal-right",
            "reveal-zoom"
        ];

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

            let done = false;

            const finish = () => {
                if (done) return;
                done = true;
                el.removeEventListener("transitionend", onEnd);
                cleanupReveal(el);
            };

            const onEnd = (e) => {
                if (
                    e.target === el &&
                    (e.propertyName === "opacity" || e.propertyName === "transform")
                ) {
                    finish();
                }
            };

            el.addEventListener("transitionend", onEnd);
            setTimeout(finish, 2200);
        }

        const revealObserver = canObserve
            ? new IntersectionObserver(
                  (entries) => {
                      entries.forEach((entry) => {
                          if (entry.isIntersecting) showReveal(entry.target);
                      });
                  },
                  { threshold: 0.05, rootMargin: "0px 0px -40px 0px" }
              )
            : null;

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

        function revealInitial(elements) {
            const mobile = isMobile();
            const vh = viewportHeight();
            const rects = elements.map((el) => el.getBoundingClientRect());

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

            void document.body.offsetHeight;
            revealInitial(initial);

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
                }).observe(document.body, {
                    childList: true,
                    subtree: true
                });
            }
        }

        function revealStragglers() {
            if (!revealObserver) return;

            const vh = viewportHeight();

            document.querySelectorAll(".reveal:not(.visible)").forEach((el) => {
                const rect = el.getBoundingClientRect();

                if (rect.top < vh * 0.92 && rect.bottom > 0) {
                    showReveal(el);
                }
            });
        }

        /* Reveal API */
        window.driveonRefreshReveal = function () {
            const fresh = registerReveals(document);

            if (fresh.length) {
                void document.body.offsetHeight;
                revealInitial(fresh);
            }
        };

        /* Counters */
        function prepareCounter(el) {
            const match = el.textContent.trim().match(/^(\d+)(\D*)$/);
            if (!match) return null;

            return {
                el,
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
                items.forEach((item) => {
                    item.el.textContent = "0" + item.suffix;
                });

                if ("IntersectionObserver" in window) {
                    const counterObserver = new IntersectionObserver(
                        (entries) => {
                            entries.forEach((entry) => {
                                if (!entry.isIntersecting) return;

                                const item = items.find((i) => i.el === entry.target);

                                counterObserver.unobserve(entry.target);

                                if (item) setTimeout(() => runCounter(item), 250);
                            });
                        },
                        { threshold: 0.3 }
                    );

                    items.forEach((item) => counterObserver.observe(item.el));
                } else {
                    items.forEach((item) => {
                        item.el.textContent = item.finalText;
                    });
                }
            }
        }

        /* Load */
        window.addEventListener("load", () => {
            measure();
            render();
            revealStragglers();
            setTimeout(revealStragglers, 600);
        });

        /* Back / cache */
        window.addEventListener("pageshow", (e) => {
            if (e.persisted) {
                measure();
                render();
                revealStragglers();
            }
        });
    }

    /* Init */
    if (document.body) {
        init();
    } else {
        document.addEventListener("DOMContentLoaded", init);
    }
})();