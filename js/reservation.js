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


const cars = {

    bmw5: {
        name: "BMW 5 Series",
        type: "Luxury Sedan",
        category: "Luxury",
        image: "image/cars/bmw5.jpg",
        transmission: "Automatic",
        seats: "5 Seats",
        fuel: "Petrol",
        luggage: "Unlimited",
        price: "€360"
    },

    "audi-rsq8": {
        name: "Audi RS Q8",
        type: "Performance SUV",
        category: "Performance",
        image: "image/cars/rsq8.jpg",
        transmission: "Automatic",
        seats: "5 Seats",
        fuel: "Petrol",
        luggage: "Unlimited",
        price: "€390"
    },

    "mercedes-cclass": {
        name: "Mercedes C-Class",
        type: "Premium Sedan",
        category: "Premium",
        image: "image/cars/mb.jpg",
        transmission: "Automatic",
        seats: "5 Seats",
        fuel: "Petrol",
        luggage: "Unlimited",
        price: "€230"
    },

    "range-rover": {
        name: "Range Rover Sport",
        type: "Luxury SUV",
        category: "Luxury",
        image: "image/cars/range.jpg",
        transmission: "Automatic",
        seats: "5 Seats",
        fuel: "Petrol",
        luggage: "Unlimited",
        price: "€200"
    },
    "audi-rs6": {
    name: "Audi RS6",
    type: "Performance Sedan",
    category: "Performance",
    image: "image/cars/rs6.jpg",
    transmission: "Automatic",
    seats: "5 Seats",
    fuel: "Petrol",
    luggage: "Unlimited",
    price: "€450"
},

"mercedes-g63": {
    name: "Mercedes G63",
    type: "Luxury SUV",
    category: "Luxury",
    image: "image/cars/g63.jpg",
    transmission: "Automatic",
    seats: "5 Seats",
    fuel: "Petrol",
    luggage: "Unlimited",
    price: "€500"
}
};


// SELECT CAR
document.querySelectorAll("[data-car]").forEach(button => {

    button.addEventListener("click", () => {

        const carId = button.dataset.car;
        const car = cars[carId];

        if (!car) return;


        // Update dropdown
        carDropdownText.textContent =
            `${car.name} — ${car.price} / day`;

        carDropdownText.classList.remove("text-secondary");


        // Update image
        selectedCarImage.src = car.image;
        selectedCarImage.alt = car.name;


        // Update car information
        selectedCarName.textContent = car.name;
        selectedCarType.textContent = car.type;
        selectedCarCategory.textContent = car.category;

        selectedCarTransmission.textContent = car.transmission;
        selectedCarSeats.textContent = car.seats;
        selectedCarFuel.textContent = car.fuel;
        selectedCarLuggage.textContent = car.luggage;

        selectedCarPrice.textContent = car.price;


        // Show selected car
        selectedCarWrapper.classList.remove("d-none");

    });

});


// GET CAR FROM URL
const urlParams = new URLSearchParams(window.location.search);
const carFromURL = urlParams.get("car");


// AUTO SELECT CAR
if (carFromURL && cars[carFromURL]) {

    const selectedButton = document.querySelector(
        `[data-car="${carFromURL}"]`
    );

    if (selectedButton) {
        selectedButton.click();
    }

}