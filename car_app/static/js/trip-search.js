/* Formulari i kërkimit (faqja kryesore + Cars): kalendari me interval. */
(() => {
    "use strict";

    const $ = (id) => document.getElementById(id);
    const start = $("tripPickup"), end = $("tripReturn");
    if (!start || !end || !window.DriveOnRange) return;

    const range = DriveOnRange.attach({
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
