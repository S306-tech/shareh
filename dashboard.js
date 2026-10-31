document.addEventListener("DOMContentLoaded", function () {
    const actionForms = document.querySelectorAll(".booking-action-form");

    actionForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm("Are you sure you want to update this booking?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});