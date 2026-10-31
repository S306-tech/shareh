document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("date");

    if (dateInput) {
        const today = new Date().toISOString().split("T")[0];
        dateInput.min = today;
    }

    const bookingForm = document.querySelector("form");

    if (bookingForm && dateInput) {
        bookingForm.addEventListener("submit", function (event) {
            if (dateInput.value < dateInput.min) {
                event.preventDefault();
                alert("Please select today or a future date.");
            }
        });
    }
});