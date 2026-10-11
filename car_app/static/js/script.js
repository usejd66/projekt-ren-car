/* =========================================================
   DRIVEON - SCRIPT I PËRBASHKËT (ngarkohet në të gjitha faqet)
   Animacionet i bën CSS-ja (animations.css), ky skedar i nis.
========================================================= */

const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;


/* =========================================================
   NAVBAR SCROLL
========================================================= */

const navbar = document.querySelector(".navbar-enhanced");

function updateNavbar() {
    if (!navbar) return;
    navbar.classList.toggle("scrolled", window.scrollY > 50);
}


/* =========================================================
   SCROLL PROGRESS BAR + BACK TO TOP (krijohen nga JS)
========================================================= */

const progressBar = document.createElement("div");
progressBar.id = "scrollProgress";
document.body.appendChild(progressBar);

const backToTop = document.createElement("button");
backToTop.id = "backToTop";
backToTop.type = "button";
backToTop.setAttribute("aria-label", "Back to top");
backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
document.body.appendChild(backToTop);

backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: prefersReduced ? "auto" : "smooth" });
});


/* =========================================================
   HERO PARALLAX (përmbajtja lëviz pak dhe zbehet gjatë scroll)
========================================================= */

const heroContent = document.querySelector(".hero .container");
const heroSection = document.querySelector(".hero");

function updateHero() {
    if (!heroContent || !heroSection || prefersReduced) return;

    const y = window.scrollY;
    const limit = heroSection.offsetHeight;

    if (y > limit) return;

    heroContent.style.transform = `translateY(${y * 0.18}px)`;
    heroContent.style.opacity = Math.max(0, 1 - y / (limit * 0.9));
}


/* =========================================================
   SCROLL HANDLER (një herë për frame, pa e ngadalësuar faqen)
========================================================= */

let ticking = false;

function onScroll() {
    if (ticking) return;
    ticking = true;

    requestAnimationFrame(() => {
        const scrollTop = window.scrollY;
        const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

        progressBar.style.width = (maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0) + "%";
        backToTop.classList.toggle("show", scrollTop > 600);

        updateNavbar();
        updateHero();
        if (typeof revealVisible === "function") revealVisible();

        ticking = false;
    });
}

window.addEventListener("scroll", onScroll, { passive: true });
onScroll();


/* =========================================================
   SHFAQJE ME SCROLL (REVEAL)
   [selektori, lloji i animacionit, stagger?]
   Llojet: up, left, right, zoom
========================================================= */

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

function showReveal(el) {

    if (el.classList.contains("visible")) return;

    el.classList.add("visible");

    if (revealObserver) revealObserver.unobserve(el);

    /* Pas animacionit e heqim klasën, që hover-i i kartave të punojë normalisht */
    setTimeout(() => {
        el.classList.remove("reveal", "visible", "reveal-up", "reveal-left", "reveal-right", "reveal-zoom");
        el.style.transitionDelay = "";
    }, 1800);
}

const revealObserver = ("IntersectionObserver" in window && !prefersReduced)
    ? new IntersectionObserver((entries) => {

        entries.forEach(entry => {
            if (entry.isIntersecting) showReveal(entry.target);
        });

    }, { threshold: 0.05, rootMargin: "0px 0px -40px 0px" })
    : null;

/* Siguri shtesë: nëse observer-i nuk e nis një element, e tregojmë vetë kur hyn në ekran */
function revealVisible() {
    document.querySelectorAll(".reveal:not(.visible)").forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) showReveal(el);
    });
}

if (revealObserver) {

    revealConfig.forEach(([selector, type, stagger]) => {

        const groups = new Map();

        document.querySelectorAll(selector).forEach(el => {

            if (el.classList.contains("reveal")) return;
            if (el.parentElement && el.parentElement.closest(".reveal")) return;
            if (el.closest("#selectedCarWrapper")) return;

            const parent = el.parentElement;
            if (!groups.has(parent)) groups.set(parent, []);
            groups.get(parent).push(el);
        });

        groups.forEach(items => {
            items.forEach((el, index) => {

                el.classList.add("reveal", "reveal-" + type);

                if (stagger) {
                    el.style.transitionDelay = Math.min(index, 5) * 0.12 + "s";
                }

                revealObserver.observe(el);
            });
        });
    });
}


/* =========================================================
   ANIMACIONET E FILLIMIT
   Çdo gjë që është tashmë në ekran kur hapet faqja hyn menjëherë,
   me vonesë të vogël mes elementeve (kaskadë), pa pritur scroll.
========================================================= */

if (revealObserver) {

    /* Detyrojmë shfletuesin ta llogarisë gjendjen e fshehur përpara se të nisim animacionin */
    void document.body.offsetHeight;

    let order = 0;

    document.querySelectorAll(".reveal").forEach(el => {

        const rect = el.getBoundingClientRect();

        if (rect.top < window.innerHeight && rect.bottom > 0) {
            el.style.transitionDelay = (0.25 + Math.min(order, 6) * 0.12) + "s";
            order++;
            showReveal(el);
        }
    });
}


/* =========================================================
   NUMËRUESIT TE HERO (50+, 100% ... ; "24/7" mbetet siç është)
========================================================= */

function animateCounter(el) {

    const match = el.textContent.trim().match(/^(\d+)(\D*)$/);
    if (!match) return;

    const target = parseInt(match[1], 10);
    const suffix = match[2];
    const duration = 1800;
    const start = performance.now();

    function frame(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);

        el.textContent = Math.round(target * eased) + suffix;

        if (progress < 1) requestAnimationFrame(frame);
    }

    el.textContent = "0" + suffix;
    requestAnimationFrame(frame);
}

if (!prefersReduced) {
    const counters = document.querySelectorAll(".hero-stat strong");

    if (counters.length) {
        setTimeout(() => counters.forEach(animateCounter), 1000);
    }
}


window.addEventListener("load", () => {
    revealVisible();
    setTimeout(revealVisible, 600);
});