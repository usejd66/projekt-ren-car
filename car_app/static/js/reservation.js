(() => {
"use strict";

const $ = (id) => document.getElementById(id);
const set = (id, text) => ($(id).textContent = text);
const [form, carSel, pickup, ret, pickLoc, err] =
    ["reservationForm", "carSelect", "pickupDate", "returnDate", "id_pickup_location", "formError"].map($);
const booked = JSON.parse($("bookedData").textContent); // {car_id: [{from, to}]}
const MS_DAY = 864e5;

/* ---------- Helpers ---------- */
const car = () => {
    const o = carSel.selectedOptions[0];
    return o && o.value ? { ...o.dataset, price: parseFloat(o.dataset.price) || 0, booked: booked[o.value] || [] } : null;
};
// Endpoints are inclusive, same as Reservation.overlapping() on the server
const conflict = (c) => c && pickup.value && ret.value &&
    c.booked.find((b) => pickup.value <= b.to && ret.value >= b.from);
const isBooked = (iso) => (car()?.booked || []).some((b) => iso >= b.from && iso <= b.to);
const fmt = (iso) => iso.split("-").reverse().join("/");
const nextDay = (iso) => new Date(Date.parse(iso) + MS_DAY).toISOString().slice(0, 10);
const showError = (msg) => { err.textContent = msg; err.classList.toggle("d-none", !msg); };

/* ---------- Summary ---------- */
const money = (n) => `€${n.toLocaleString("en-US", { maximumFractionDigits: 2 })}`;

function update() {
    const c = car(), hit = conflict(c);
    const days = pickup.value && ret.value
        ? Math.max(0, Math.round((Date.parse(ret.value) - Date.parse(pickup.value)) / MS_DAY)) : 0;
    const total = (c ? c.price : 0) * days;

    showError(hit ? `This car is booked from ${fmt(hit.from)} to ${fmt(hit.to)}. Please choose different dates.` : "");

    // karta e makinës së zgjedhur
    $("selectedCarWrapper").classList.toggle("d-none", !c);
    if (c) {
        $("selectedCarImage").src = c.image;
        $("selectedCarImage").alt = c.name;
        set("selectedCarName", c.name);
        set("selectedCarCategory", c.category);
        set("selectedCarSeats", `${c.seats} seats`);
        set("selectedCarTransmission", c.transmission);
        set("selectedCarFuel", c.fuel);
        set("selectedCarPrice", money(c.price));
    }

    // përmbledhja
    set("summaryVehicle", c ? c.name : "No car selected");
    set("summaryPickup", pickup.value
        ? fmt(pickup.value) + (pickLoc.value ? ` · ${pickLoc.value}` : "")
        : (pickLoc.value || "—"));
    set("summaryReturn", ret.value ? fmt(ret.value) : "—");
    set("summaryRateLabel", c && days ? `${money(c.price)} × ${days} ${days === 1 ? "day" : "days"}` : "Daily rate");
    set("summaryRate", c ? (days ? money(total) : `${money(c.price)} / day`) : "—");
    set("summaryTotal", money(total));
    set("summaryTotalMobile", money(total));
}

/* ---------- Calendars ---------- */
const base = {
    dateFormat: "Y-m-d", // value sent to Django
    altInput: true,
    altFormat: "d/m/Y",  // what the user sees
    altInputClass: "form-control",
    minDate: "today",
    disableMobile: true,
    locale: { firstDayOfWeek: 1 },
    // function rule: reads the currently selected car every time the calendar redraws
    disable: [(d) => isBooked(flatpickr.formatDate(d, "Y-m-d"))],
    onDayCreate: (_, __, fp, el) => isBooked(fp.formatDate(el.dateObj, "Y-m-d")) && el.classList.add("booked"),
    onChange: update,
    // the visible flatpickr input gets an id (pickupDateAlt / returnDateAlt) so label[for] works
    onReady: (_, __, fp) => {
        fp.altInput.id = `${fp.input.id}Alt`;
        fp.altInput.autocomplete = "off";
        // gabimi nga serveri (is-invalid) duhet të duket te input-i i dukshëm
        if (fp.input.classList.contains("is-invalid")) fp.altInput.classList.add("is-invalid");
    },
};
const returnFp = flatpickr(ret, {
    ...base,
    onOpen: () => returnFp.set("minDate", pickup.value ? nextDay(pickup.value) : "today"),
});
const pickupFp = flatpickr(pickup, {
    ...base,
    onChange: () => { if (ret.value <= pickup.value) returnFp.clear(); update(); },
});

/* ---------- Events ---------- */
const onCar = () => {
    pickupFp.redraw();
    returnFp.redraw();
    update();
};
carSel.addEventListener("change", onCar);
pickLoc.addEventListener("change", update);

form.addEventListener("submit", (e) => {
    const c = car();
    const msg = !c ? "Please select a car."
        : !pickLoc.value ? "Please select a pickup location."
        : !pickup.value || !ret.value ? "Please select your dates."
        : ret.value <= pickup.value ? "The return date must be after the pickup date."
        : conflict(c) ? "This car is booked on the selected dates." : "";

    if (msg) {
        e.preventDefault();
        showError(msg);
        err.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
        // parandalon dërgimin dy herë (edhe butoni i shiritit në telefon)
        document.querySelectorAll('button[type="submit"]').forEach((b) => { b.disabled = true; });
    }
});

onCar(); // car arrives preselected from ?car=ID or after a server-side error
})();