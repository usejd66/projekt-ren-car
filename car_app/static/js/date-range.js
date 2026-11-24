/* Kalendari me interval (marrja + kthimi në një kalendar), i përbashkët për
   kërkimin dhe faqen e rezervimit.

   HTML-i: dy input-e të fshehura (vlerat YYYY-MM-DD që shkojnë te Django) dhe
   dy fusha të dukshme vetëm-për-lexim (dd/mm/yyyy) që hapin të njëjtin kalendar.

   RangePicker.attach({
       start, end,                 // input-et e fshehura
       startDisplay, endDisplay,   // fushat e dukshme
       isBooked(iso) -> bool,      // opsionale: ditët e zëna (vizatohen me vijë)
       onChange()                  // opsionale: thirret pas çdo ndryshimi
   }) -> instanca flatpickr
*/
window.RangePicker = (() => {
    "use strict";

    const MS_DAY = 864e5;
    const iso = (d) => flatpickr.formatDate(d, "Y-m-d");
    const nice = (value) => (value ? value.split("-").reverse().join("/") : "");
    const mobile = window.matchMedia("(max-width: 575.98px)");

    /* Pozicionimi i kalendarit. Pozicionimi i vetë flatpickr, kur kalendari nuk nxë në
       ekran, lexon CSS-në e domain-eve të tjera (Google Fonts, CDN) dhe hedh SecurityError. */
    function place(inst, customElement) {
        const cal = inst.calendarContainer;
        if (mobile.matches) { cal.style.top = cal.style.left = cal.style.right = ""; return; } // CSS: panel poshtë
        const el = customElement || inst._positionElement;
        const r = el.getBoundingClientRect();
        const w = cal.offsetWidth, h = cal.offsetHeight;
        const viewW = document.documentElement.clientWidth;
        // gjithmonë poshtë fushës (si Airbnb): nuk mbulon navbar-in dhe nuk "kërcen"
        // kur ndryshon lartësia; nëse s'nxë, faqja lëviz pak që të duket i gjithë
        const left = Math.max(8, Math.min(r.left, viewW - w - 8));
        cal.style.left = `${left + window.scrollX}px`;
        cal.style.right = "auto";
        cal.style.top = `${r.bottom + 6 + window.scrollY}px`;
        const overflow = r.bottom + 6 + h + 16 - window.innerHeight;
        if (overflow > 0 && !inst._scrolled) {
            inst._scrolled = true;
            window.scrollBy({ top: Math.min(overflow, r.top - 100), behavior: "smooth" });
        }
    }

    function attach({ start, end, startDisplay, endDisplay, isBooked = () => false, onChange = () => {} }) {
        // instanca lidhet me një input ndihmës që nuk shihet
        const anchor = document.createElement("input");
        anchor.type = "text";
        anchor.className = "range-anchor";
        anchor.tabIndex = -1;
        anchor.setAttribute("aria-hidden", "true");
        startDisplay.parentNode.appendChild(anchor);

        let active = startDisplay; // cila fushë po zgjidhet (për theksimin)
        let hint = null;            // udhëzimi sipër kalendarit

        const show = () => {
            startDisplay.value = nice(start.value);
            endDisplay.value = nice(end.value);
            if (hint) {
                const pickingEnd = active === endDisplay && start.value;
                hint.firstChild.textContent = pickingEnd ? "Select return date" : "Select pickup date";
                hint.lastChild.textContent = pickingEnd ? `Pickup: ${nice(start.value)}` : "Then choose the return date";
            }
            startDisplay.classList.toggle("is-picking", active === startDisplay && fp.isOpen);
            endDisplay.classList.toggle("is-picking", active === endDisplay && fp.isOpen);
        };

        const fp = flatpickr(anchor, {
            mode: "range",
            dateFormat: "Y-m-d",
            minDate: "today",
            showMonths: window.innerWidth >= 768 ? 2 : 1,
            disableMobile: true,
            clickOpens: false,
            positionElement: startDisplay,
            position: place,
            locale: { firstDayOfWeek: 1, rangeSeparator: " – " },
            disable: [(d) => isBooked(iso(d))],
            onDayCreate: (_, __, inst, el) => { if (isBooked(iso(el.dateObj))) el.classList.add("booked"); },
            onReady: (_, __, inst) => {
                hint = document.createElement("div");
                hint.className = "range-hint";
                hint.append(document.createTextNode(""), document.createElement("span"));
                inst.calendarContainer.prepend(hint);
            },
            onOpen: (_, __, inst) => {
                inst.calendarContainer.classList.toggle("range-sheet", mobile.matches);
                document.body.classList.toggle("range-open", mobile.matches);
                show();
            },
            onClose: (dates, _, inst) => {
                inst._scrolled = false;
                document.body.classList.remove("range-open");
                // vetëm data e marrjes: mbetet e zgjedhur, kthimi bosh
                if (dates.length === 1) { start.value = iso(dates[0]); end.value = ""; }
                active = startDisplay;
                show();
                onChange();
            },
            onChange: (dates) => {
                if (dates.length === 1) {
                    start.value = iso(dates[0]);
                    end.value = "";
                    active = endDisplay;
                } else if (dates.length === 2) {
                    // e njëjta ditë dy herë = vetëm marrja
                    if (+dates[0] === +dates[1]) { fp.setDate([dates[0]], false); return; }
                    start.value = iso(dates[0]);
                    end.value = iso(dates[1]);
                    setTimeout(() => fp.close(), 150);
                }
                show();
                onChange();
            },
        });

        // vlerat ekzistuese (nga serveri ose nga URL-ja)
        if (start.value) fp.setDate(end.value ? [start.value, end.value] : [start.value], false);
        show();

        const open = (field) => () => {
            active = field;
            // te "Return" pa datë marrjeje: fillo nga marrja
            if (field === endDisplay && !start.value) active = startDisplay;
            fp.set("positionElement", field);
            fp.open();
            show();
        };
        [startDisplay, endDisplay].forEach((field) => {
            field.readOnly = true;
            field.addEventListener("click", open(field));
            field.addEventListener("keydown", (e) => {
                if (e.key === "Enter" || e.key === " " || e.key === "ArrowDown") { e.preventDefault(); open(field)(); }
            });
        });

        // telefon: sfond i errët pas kalendarit; prekja e tij e mbyll
        let backdrop = document.querySelector(".range-backdrop");
        if (!backdrop) {
            backdrop = document.createElement("div");
            backdrop.className = "range-backdrop";
            document.body.appendChild(backdrop);
        }
        backdrop.addEventListener("click", () => fp.close());

        fp.nights = () => (start.value && end.value
            ? Math.round((Date.parse(end.value) - Date.parse(start.value)) / MS_DAY) : 0);
        fp.openFor = (which) => open(which === "end" ? endDisplay : startDisplay)();
        return fp;
    }

    return { attach, nice };
})();
