/* Faqja e makinës: galeria (rrëshqitje + miniatura) dhe paneli i rezervimit me çmim live. */
(() => {
    "use strict";

    /* ---------- Galeria ---------- */
    const gallery = document.querySelector("[data-gallery]");
    if (gallery) {
        const track = gallery.querySelector(".gallery-track");
        const slides = [...track.children];
        const thumbs = [...document.querySelectorAll(".gallery-thumbs button")];
        const current = gallery.querySelector("[data-current]");
        let index = 0;

        const go = (i) => {
            index = Math.max(0, Math.min(slides.length - 1, i));
            track.scrollTo({ left: slides[index].offsetLeft, behavior: "smooth" });
        };
        const mark = (i) => {
            index = i;
            if (current) current.textContent = i + 1;
            thumbs.forEach((t, n) => t.classList.toggle("active", n === i));
            gallery.querySelector(".gallery-prev")?.toggleAttribute("disabled", i === 0);
            gallery.querySelector(".gallery-next")?.toggleAttribute("disabled", i === slides.length - 1);
        };

        // foto aktive = ajo që zë pjesën më të madhe të galerisë (edhe kur rrëshqet me gisht)
        const io = new IntersectionObserver((entries) => {
            entries.forEach((e) => { if (e.isIntersecting) mark(slides.indexOf(e.target)); });
        }, { root: track, threshold: 0.6 });
        slides.forEach((s) => io.observe(s));

        gallery.querySelector(".gallery-prev")?.addEventListener("click", () => go(index - 1));
        gallery.querySelector(".gallery-next")?.addEventListener("click", () => go(index + 1));
        thumbs.forEach((t) => t.addEventListener("click", () => go(+t.dataset.index)));
        track.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") { e.preventDefault(); go(index - 1); }
            if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1); }
        });
        mark(0);
    }

    /* ---------- Rezervimi ---------- */
    const form = document.getElementById("bookForm");
    if (!form || !window.DriveOnRange) return;

    const $ = (id) => document.getElementById(id);
    const price = parseFloat(form.dataset.price) || 0;
    const booked = JSON.parse($("bookedData").textContent); // [{from, to}]
    const start = $("bookPickup"), end = $("bookReturn");
    const money = (n) => `€${n.toLocaleString("en-US", { maximumFractionDigits: 2 })}`;
    const isBooked = (iso) => booked.some((b) => iso >= b.from && iso <= b.to);
    // skajet përfshihen, njësoj si Reservation.overlapping() në server
    const conflict = () => start.value && end.value && booked.find((b) => start.value <= b.to && end.value >= b.from);
    const err = $("bookError");
    const showError = (msg) => { err.textContent = msg; err.classList.toggle("d-none", !msg); };

    function update() {
        const days = range.nights();
        const hit = conflict();
        showError(hit ? `Booked from ${DriveOnRange.nice(hit.from)} to ${DriveOnRange.nice(hit.to)}. Please choose other dates.` : "");
        $("bookRateLabel").textContent = days ? `${money(price)} × ${days} ${days === 1 ? "day" : "days"}` : "Choose your dates";
        $("bookRate").textContent = days ? money(price * days) : "—";
        $("bookTotal").textContent = money(price * days);

        // shiriti poshtë në telefon
        const barTotal = $("barTotal"), barLabel = $("barLabel"), barBtn = $("barBtn");
        if (barTotal) {
            if (days && !hit) {
                barLabel.textContent = `${days} ${days === 1 ? "day" : "days"} total`;
                barTotal.textContent = money(price * days);
                barBtn.textContent = "Continue";
            } else {
                barLabel.textContent = "From";
                barTotal.innerHTML = `${money(price)}<small> / day</small>`;
                barBtn.textContent = "Check dates";
            }
        }
    }

    const range = DriveOnRange.attach({
        start, end,
        startDisplay: $("bookPickupAlt"),
        endDisplay: $("bookReturnAlt"),
        isBooked,
        onChange: update,
    });

    form.addEventListener("submit", (e) => {
        if (!start.value || !end.value) {
            e.preventDefault();
            range.openFor(start.value ? "end" : "start");
        } else if (conflict()) {
            e.preventDefault();
        }
    });

    // telefon: "Continue" dërgon formularin kur datat janë gati; ndryshe hap kalendarin
    $("barBtn")?.addEventListener("click", (e) => {
        e.preventDefault();
        if (start.value && end.value && !conflict()) form.requestSubmit();
        else {
            document.getElementById("book").scrollIntoView({ behavior: "smooth", block: "center" });
            setTimeout(() => range.openFor(start.value ? "end" : "start"), 450);
        }
    });

    update();
})();
