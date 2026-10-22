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
function update() {
    const c = car(), hit = conflict(c);
    const days = pickup.value && ret.value
        ? Math.max(0, Math.round((Date.parse(ret.value) - Date.parse(pickup.value)) / MS_DAY)) : 0;

    showError(hit ? `This car is booked from ${fmt(hit.from)} to ${fmt(hit.to)}. Please choose different dates.` : "");
    $("selectedCarWrapper").classList.toggle("d-none", !c);
    if (c) {
        $("selectedCarImage").src = c.image;
        $("selectedCarImage").alt = c.name;
        set("selectedCarName", c.name);
        set("selectedCarCategory", c.category);
        set("selectedCarTransmission", c.transmission);
        set("selectedCarPrice", `€${c.price}`);
    }
    set("summaryVehicle", c ? c.name : "Select a vehicle");
    set("summaryDays", `${days} ${days === 1 ? "day" : "days"}`);
    set("summaryPickup", pickLoc.value ? pickLoc.value + (pickup.value ? ` · ${fmt(pickup.value)}` : "") : "—");
    set("summaryReturn", ret.value ? fmt(ret.value) : "—");
    set("summaryTotal", `€${((c ? c.price : 0) * days).toLocaleString(undefined, { maximumFractionDigits: 2 })}`);
}

/* ---------- Calendars ---------- */
const base = {
    dateFormat: "Y-m-d", // value sent to Django
    altInput: true,
    altFormat: "d/m/Y",  // what the user sees
    altInputClass: "form-control form-control-lg rounded-3",
    minDate: "today",
    disableMobile: true,
    locale: { firstDayOfWeek: 1 },
    // function rule: reads the currently selected car every time the calendar redraws
    disable: [(d) => isBooked(flatpickr.formatDate(d, "Y-m-d"))],
    onDayCreate: (_, __, fp, el) => isBooked(fp.formatDate(el.dateObj, "Y-m-d")) && el.classList.add("booked"),
    onChange: update,
    // the visible flatpickr input gets an id (pickupDateAlt / returnDateAlt) so label[for] works
    onReady: (_, __, fp) => { fp.altInput.id = `${fp.input.id}Alt`; fp.altInput.autocomplete = "off"; },
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
        $("confirmReservation").disabled = true; // prevents double submit
    }
});

onCar(); // car arrives preselected from ?car=ID or after a server-side error
})();