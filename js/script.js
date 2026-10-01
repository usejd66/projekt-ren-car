/* =========================================================
   NAVBAR SCROLL
========================================================= */

const navbar = document.querySelector(".navbar-enhanced");

if (navbar) {

    function updateNavbar() {

        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }

    }

    window.addEventListener("scroll", updateNavbar);

    updateNavbar();
}

