/* Kalendari i formularit të kërkimit (faqja kryesore + Cars).
   I njëjti kalendar (flatpickr) dhe i njëjti format si te faqja e rezervimit. */
(() => {
    "use strict";

    const pickup = document.getElementById("tripPickup");
    const ret = document.getElementById("tripReturn");
    if (!pickup || !ret || typeof flatpickr === "undefined") return;

    const MS_DAY = 864e5;
    const nextDay = (iso) => new Date(Date.parse(iso) + MS_DAY).toISOString().slice(0, 10);

    const base = {
        dateFormat: "Y-m-d",   // vlera që i dërgohet Django-s
        altInput: true,
        altFormat: "d/m/Y",    // ajo që sheh përdoruesi
        altInputClass: "form-control",
        minDate: "today",
        disableMobile: true,
        locale: { firstDayOfWeek: 1 },
        // input-i i dukshëm merr id-në që label[for] të funksionojë
        onReady: (_, __, fp) => {
            fp.altInput.id = `${fp.input.id}Alt`;
            fp.altInput.placeholder = fp.input.placeholder;
            fp.altInput.autocomplete = "off";
        },
    };

    const returnFp = flatpickr(ret, {
        ...base,
        minDate: pickup.value ? nextDay(pickup.value) : "today",
    });

    flatpickr(pickup, {
        ...base,
        onChange: () => {
            if (!pickup.value) return;
            returnFp.set("minDate", nextDay(pickup.value));
            if (ret.value && ret.value <= pickup.value) returnFp.clear();
            // pasi zgjedh datën e marrjes, hap direkt kalendarin e kthimit
            if (!ret.value) setTimeout(() => returnFp.open(), 0);
        },
    });

    // nëse është zgjedhur vetëm njëra datë, mos e dërgo formularin gjysmë të plotë
    pickup.form.addEventListener("submit", (e) => {
        if (!!pickup.value !== !!ret.value) {
            e.preventDefault();
            (pickup.value ? returnFp : pickup._flatpickr).open();
        }
    });
})();
