// ========================================
// DRIVEON - RESERVATION
// ========================================

// Get selected car from URL
const params = new URLSearchParams(window.location.search);
const selectedCar = params.get("car");

// ========================================
// CAR DATA
// ========================================

const cars = {
    bmw5: {
        name: "BMW 5 Series",
        price: 120,
        image: "image/cars/bmw5.jpg"
    },

    audiRsq8: {
        name: "Audi RS Q8",
        price: 180,
        image: "image/cars/rsq8.jpg"
    },

    mercedesC: {
        name: "Mercedes C-Class",
        price: 110,
        image: "image/cars/mb.jpg"
    },

    rangeRover: {
        name: "Range Rover Sport",
        price: 160,
        image: "image/cars/range.jpg"
    },

    premiumSedan: {
        name: "Premium Sedan",
        price: 100,
        image: "image/cars/rs6.jpg"
    },

    luxurySuv: {
        name: "Luxury SUV",
        price: 150,
        image: "image/cars/g63.jpg"
    }
};


// If no car is selected, use BMW as default
const car = cars[selectedCar] || cars.bmw5;


// ========================================
// HTML ELEMENTS
// ========================================

const carImage = document.getElementById("carImage");
const carName = document.getElementById("carName");
const carPrice = document.getElementById("carPrice");
const summaryCar = document.getElementById("summaryCar");

const calendarDays = document.querySelectorAll(".calendar-days button");

const pickupDate = document.getElementById("pickupDate");
const returnDate = document.getElementById("returnDate");

const totalPrice = document.getElementById("totalPrice");


// ========================================
// DISPLAY SELECTED CAR
// ========================================

if (carImage) {
    carImage.src = car.image;
    carImage.alt = car.name;
}

if (carName) {
    carName.textContent = car.name;
}

if (carPrice) {
    carPrice.textContent = `€${car.price}`;
}

if (summaryCar) {
    summaryCar.textContent = car.name;
}


// ========================================
// DATE SELECTION
// ========================================

let selectedDates = [];

calendarDays.forEach(day => {

    day.addEventListener("click", () => {

        // Do not allow unavailable dates
        if (day.classList.contains("unavailable")) {
            return;
        }

        const date = day.textContent.trim();

        // If two dates are already selected,
        // start a new selection
        if (selectedDates.length === 2) {

            selectedDates = [];

            calendarDays.forEach(item => {
                item.classList.remove("selected");
            });

            pickupDate.textContent = "Select a date";
            returnDate.textContent = "Select a date";
            totalPrice.textContent = "0";
        }

        // Add selected date
        selectedDates.push(date);

        day.classList.add("selected");


        // ========================================
        // PICK-UP DATE
        // ========================================

        if (selectedDates.length === 1) {

            pickupDate.textContent = date;

            returnDate.textContent = "Select a date";

            totalPrice.textContent = "0";
        }


        // ========================================
        // RETURN DATE
        // ========================================

        if (selectedDates.length === 2) {

            returnDate.textContent = date;

            totalPrice.textContent = car.price;
        }

    });

});