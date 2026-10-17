(() => {
"use strict";

const $ = (id) => document.getElementById(id);
const set = (id, text) => ($(id).textContent = text);
const [form, carSel, pickup, ret, pickLoc, retLoc, err] =
    ["reservationForm", "carSelect", "pickupDate", "returnDate", "id_pickup_location", "returnLocation", "formError"].map($);
const booked = JSON.parse($("bookedData").textContent); // {car_id: [{from, to}]}
const MS_DAY = 864e5;

/* ---------- Ndihmëse ---------- */
const car = () => {
    const o = carSel.selectedOptions[0];
    return o && o.value ? { ...o.dataset, price: parseFloat(o.dataset.price) || 0, booked: booked[o.value] || [] } : null;
};
// Skajet përfshihen, njësoj si Reservation.overlapping() në server
const conflict = (c) => c && pickup.value && ret.value &&
    c.booked.find((b) => pickup.value <= b.to && ret.value >= b.from);
const isBooked = (iso) => (car()?.booked || []).some((b) => iso >= b.from && iso <= b.to);
const fmt = (iso) => iso.split("-").reverse().join("/");
const nextDay = (iso) => new Date(Date.parse(iso) + MS_DAY).toISOString().slice(0, 10);
const showError = (msg) => { err.textContent = msg; err.classList.toggle("d-none", !msg); };

/* ---------- Përmbledhja ---------- */
function update() {
    const c = car(), hit = conflict(c);
    const days = pickup.value && ret.value
        ? Math.max(0, Math.round((Date.parse(ret.value) - Date.parse(pickup.value)) / MS_DAY)) : 0;

    showError(hit ? `Makina është e zënë nga ${fmt(hit.from)} deri më ${fmt(hit.to)}. Zgjidhni data të tjera.` : "");
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
    set("summaryPickup", pickLoc.value || "—");
    set("summaryReturn", retLoc.value || "—");
    set("summaryTotal", `€${((c ? c.price : 0) * days).toLocaleString(undefined, { maximumFractionDigits: 2 })}`);
}

/* ---------- Kalendarët ---------- */
const base = {
    dateFormat: "Y-m-d", // vlera që dërgohet te Django
    altInput: true,
    altFormat: "d/m/Y",  // si e sheh përdoruesi
    altInputClass: "form-control form-control-lg rounded-3",
    minDate: "today",
    disableMobile: true,
    locale: { firstDayOfWeek: 1 },
    onDayCreate: (_, __, fp, el) => isBooked(fp.formatDate(el.dateObj, "Y-m-d")) && el.classList.add("booked"),
    onChange: update,
};
const returnFp = flatpickr(ret, {
    ...base,
    onOpen: () => returnFp.set("minDate", pickup.value ? nextDay(pickup.value) : "today"),
});
const pickupFp = flatpickr(pickup, {
    ...base,
    onChange: () => { if (ret.value <= pickup.value) returnFp.clear(); update(); },
});

/* ---------- Ngjarjet ---------- */
const onCar = () => {
    const ranges = car()?.booked || [];
    pickupFp.set("disable", ranges);
    returnFp.set("disable", ranges);
    update();
};
carSel.addEventListener("change", onCar);
[pickLoc, retLoc].forEach((el) => el.addEventListener("change", update));

form.addEventListener("submit", (e) => {
    const c = car();
    const msg = !c ? "Ju lutem zgjidhni një makinë."
        : !pickLoc.value ? "Ju lutem zgjidhni vendin e marrjes."
        : !pickup.value || !ret.value ? "Ju lutem zgjidhni datat."
        : ret.value <= pickup.value ? "Data e kthimit duhet të jetë pas datës së marrjes."
        : conflict(c) ? "Makina është e zënë në datat e zgjedhura." : "";

    if (msg) {
        e.preventDefault();
        showError(msg);
        err.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
        $("confirmReservation").disabled = true; // pengon dërgimin e dyfishtë
    }
});

onCar(); // makina vjen e zgjedhur nga ?car=ID ose pas një gabimi të serverit
})();