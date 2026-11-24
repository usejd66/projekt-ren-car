/* Formulari i kërkimit (faqja kryesore + Cars): kalendari me interval. */
(() => {
    "use strict";

    const $ = (id) => document.getElementById(id);
    const start = $("tripPickup"), end = $("tripReturn");
    if (!start || !end || !window.RangePicker) return;

    const range = RangePicker.attach({
        start, end,
        startDisplay: $("tripPickupAlt"),
        endDisplay: $("tripReturnAlt"),
    });

    // vetëm njëra datë: mos e dërgo formularin gjysmë të plotë
    start.form.addEventListener("submit", (e) => {
        if (!!start.value !== !!end.value) {
            e.preventDefault();
            range.openFor(start.value ? "end" : "start");
        }
    });
})();
