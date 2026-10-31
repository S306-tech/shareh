document.addEventListener("DOMContentLoaded", function () {
    console.log("ShareHub is ready!");

    const currentYear = document.querySelectorAll(".current-year");

    currentYear.forEach(function (element) {
        element.textContent = new Date().getFullYear();
    });
});