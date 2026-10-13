/* ========== ELEMENTET ========== */
const carDropdownText = document.getElementById("carDropdownText");
const selectedCarWrapper = document.getElementById("selectedCarWrapper");
const selectedCarImage = document.getElementById("selectedCarImage");
const selectedCarName = document.getElementById("selectedCarName");
const selectedCarType = document.getElementById("selectedCarType");
const selectedCarCategory = document.getElementById("selectedCarCategory");
const selectedCarTransmission = document.getElementById("selectedCarTransmission");
const selectedCarSeats = document.getElementById("selectedCarSeats");
const selectedCarFuel = document.getElementById("selectedCarFuel");
const selectedCarLuggage = document.getElementById("selectedCarLuggage");
const selectedCarPrice = document.getElementById("selectedCarPrice");

const pickupLocationText = document.getElementById("pickupLocationText");
const pickupLocation = document.getElementById("pickupLocation");
const returnLocationText = document.getElementById("returnLocationText");
const returnLocation = document.getElementById("returnLocation");
const pickupDate = document.getElementById("pickupDate");
const returnDate = document.getElementById("returnDate");

const summaryVehicle = document.getElementById("summaryVehicle");
const summaryDays = document.getElementById("summaryDays");
const summaryPickup = document.getElementById("summaryPickup");
const summaryReturn = document.getElementById("summaryReturn");
const summaryTotal = document.getElementById("summaryTotal");
const confirmReservation = document.getElementById("confirmReservation");

let selectedCar = null;

/* ========== MAKINAT ========== */
const cars = {
    bmw5: { name: "BMW 5 Series", type: "Luxury Sedan", category: "Luxury", image: "image/cars/bmw5.jpg", transmission: "Automatic", seats: "5 Seats", fuel: "Petrol", luggage: "Unlimited", price: "€360" },
    "audi-rsq8": { name: "Audi RS Q8", type: "Performance SUV", category: "Performance", image: "image/cars/rsq8.jpg", transmission: "Automatic", seats: "5 Seats", fuel: "Petrol", luggage: "Unlimited", price: "€390" },
    "mercedes-cclass": { name: "Mercedes C-Class", type: "Premium Sedan", category: "Premium", image: "image/cars/mb.jpg", transmission: "Automatic", seats: "5 Seats", fuel: "Petrol", luggage: "Unlimited", price: "€230" },
    "range-rover": { name: "Range Rover Sport", type: "Luxury SUV", category: "Luxury", image: "image/cars/range.jpg", transmission: "Automatic", seats: "5 Seats", fuel: "Petrol", luggage: "Unlimited", price: "€200" },
    "audi-rs6": { name: "Audi RS6", type: "Performance Sedan", category: "Performance", image: "image/cars/rs6.jpg", transmission: "Automatic", seats: "5 Seats", fuel: "Petrol", luggage: "Unlimited", price: "€450" },
    "mercedes-g63": { name: "Mercedes G63", type: "Luxury SUV", category: "Luxury", image: "image/cars/g63.jpg", transmission: "Automatic", seats: "5 Seats", fuel: "Petrol", luggage: "Unlimited", price: "€500" }
};

/* ========== PËRMBLEDHJA ========== */
function updateSummary() {
    summaryVehicle.textContent = selectedCar ? selectedCar.name : "Select a vehicle";
    summaryPickup.textContent = pickupLocation.value || "—";
    summaryReturn.textContent = returnLocation.value || "—";

    let days = 0;

    if (pickupDate.value && returnDate.value) {
        const diff = new Date(returnDate.value) - new Date(pickupDate.value);
        if (diff >= 0) {
            // e njëjta ditë = 1 ditë qiraje
            days = Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
        }
    }

    summaryDays.textContent = `${days} ${days === 1 ? "day" : "days"}`;

    if (selectedCar && days > 0) {
        const price = parseInt(selectedCar.price.replace("€", ""), 10);
        summaryTotal.textContent = `€${(price * days).toLocaleString()}`;
    } else {
        summaryTotal.textContent = "€0";
    }
}

/* ========== ZGJEDHJA E MAKINËS ========== */
document.querySelectorAll("[data-car]").forEach(button => {
    button.addEventListener("click", () => {
        const car = cars[button.dataset.car];
        if (!car) return;

        selectedCar = car;

        carDropdownText.textContent = `${car.name} — ${car.price} / day`;
        carDropdownText.classList.remove("text-secondary");

        selectedCarImage.src = "/static/" + car.image;
        selectedCarImage.alt = car.name;
        selectedCarName.textContent = car.name;
        selectedCarType.textContent = car.type;
        selectedCarCategory.textContent = car.category;
        selectedCarTransmission.textContent = car.transmission;
        selectedCarSeats.textContent = car.seats;
        selectedCarFuel.textContent = car.fuel;
        selectedCarLuggage.textContent = car.luggage;
        selectedCarPrice.textContent = car.price;

        selectedCarWrapper.classList.remove("d-none");
        updateSummary();
    });
});

/* ========== LOKACIONET ========== */
document.querySelectorAll("[data-pickup-location]").forEach(item => {
    item.addEventListener("click", function () {
        const location = this.dataset.pickupLocation;
        pickupLocationText.textContent = location;
        pickupLocationText.classList.remove("text-secondary");
        pickupLocation.value = location;
        updateSummary();
    });
});

document.querySelectorAll("[data-return-location]").forEach(item => {
    item.addEventListener("click", function () {
        const location = this.dataset.returnLocation;
        returnLocationText.textContent = location;
        returnLocationText.classList.remove("text-secondary");
        returnLocation.value = location;
        updateSummary();
    });
});

/* ========== DATAT ========== */
const today = new Date().toISOString().split("T")[0];
pickupDate.min = today;
returnDate.min = today;

pickupDate.addEventListener("change", function () {
    returnDate.min = this.value;
    if (returnDate.value && returnDate.value < this.value) {
        returnDate.value = "";
    }
    updateSummary();
});

returnDate.addEventListener("change", updateSummary);

/* ========== KONFIRMIMI ========== */
confirmReservation.addEventListener("click", () => {
    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();

    if (!selectedCar) return alert("Ju lutem zgjidhni një makinë.");
    if (!pickupLocation.value || !returnLocation.value) return alert("Ju lutem zgjidhni vendin e marrjes dhe të kthimit.");
    if (!pickupDate.value || !returnDate.value) return alert("Ju lutem zgjidhni datat.");
    if (!firstName || !lastName || !email || !phone) return alert("Ju lutem plotësoni të dhënat tuaja.");

    document.getElementById("successVehicle").textContent = selectedCar.name;
document.getElementById("successTotal").textContent = summaryTotal.textContent;

new bootstrap.Modal(document.getElementById("successModal")).show();
});

/* ========== ZGJEDHJE AUTOMATIKE NGA URL (në fund!) ========== */
const carFromURL = new URLSearchParams(window.location.search).get("car");
if (carFromURL && cars[carFromURL]) {
    document.querySelector(`[data-car="${carFromURL}"]`)?.click();
}

updateSummary();
/* ========== OK → REFRESH & NË FILLIM ========== */
document.getElementById("successModal").addEventListener("hidden.bs.modal", () => {
    // heq ?car=... nga URL që të mos zgjidhet makina automatikisht
    window.location.href = window.location.pathname;
});

// shfletuesi mos ta rikthejë pozicionin e vjetër të scroll-it
if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
}
window.scrollTo(0, 0);