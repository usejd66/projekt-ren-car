// Scroll Reveal Animation
const elements = document.querySelectorAll('.scroll-reveal');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
            observer.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.15
});

elements.forEach(element => {
    observer.observe(element);
});

// Navbar Active Link
const navLinks = document.querySelectorAll('.navbar .nav-link');

navLinks.forEach(link => {
    link.addEventListener('click', function() {
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// Close navbar on link click (mobile)
const navbarToggle = document.querySelector('.navbar-toggler');
const navbarCollapse = document.querySelector('.navbar-collapse');

navLinks.forEach(link => {
    link.addEventListener('click', function() {
        if (navbarCollapse.classList.contains('show')) {
            navbarToggle.click();
        }
    });
});

// Add smooth hover effects to cards
const cards = document.querySelectorAll('.card, .car-card');
cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
});
