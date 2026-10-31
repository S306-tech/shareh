from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "sharehub-demo-secret-key"

# Demo data (resets when the server restarts)
users = []
bookings = []

resources = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "Borrow a laptop for learning, projects and academic work.",
        "location": "Computer Lab",
        "availability": "Available",
        "image": "images/laptop.jpg"
    },
    {
        "id": 2,
        "name": "DSLR Camera",
        "description": "Use a DSLR camera for photography and creative projects.",
        "location": "Media Room",
        "availability": "Available",
        "image": "images/dslr-camera.jpg"
    },
    {
        "id": 3,
        "name": "Lab Equipment",
        "description": "Access shared laboratory equipment for experiments and research.",
        "location": "Science Laboratory",
        "availability": "Available",
        "image": "images/lab-equipment.jpg"
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email", "").lower()
        password = request.form.get("password")
        role = request.form.get("role")

        if any(user["email"] == email for user in users):
            flash("An account with this email already exists.")
            return redirect(url_for("register"))

        users.append({
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "role": role
        })

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").lower()
        password = request.form.get("password")

        user = next(
            (u for u in users if u["email"] == email),
            None
        )

        if user and check_password_hash(user["password"], password):
            session["email"] = user["email"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "owner":
                return redirect(url_for("owner_dashboard"))

            return redirect(url_for("student_dashboard"))

        flash("Incorrect email or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/explore")
def explore():
    return render_template("explore.html", resources=resources)


@app.route("/resource/<int:resource_id>")
def resource_details(resource_id):
    resource = next(
        (r for r in resources if r["id"] == resource_id),
        None
    )

    if resource is None:
        return "Resource not found", 404

    return render_template("resource_details.html", resource=resource)


@app.route("/request-booking", methods=["GET", "POST"])
def request_booking():
    if request.method == "POST":
        resource = request.form.get("resource")
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        purpose = request.form.get("purpose")

        if not all([resource, name, email, date, purpose]):
            flash("Please complete all booking fields.")
            return redirect(url_for("explore"))

        bookings.append({
            "id": len(bookings) + 1,
            "name": name,
            "email": email.lower(),
            "resource": resource,
            "date": date,
            "purpose": purpose,
            "status": "Pending"
        })

        return render_template(
            "booking_success.html",
            name=name,
            resource=resource
        )

    resource = request.args.get("resource", "Laptop")
    return render_template("booking.html", resource=resource)


@app.route("/student-dashboard")
def student_dashboard():
    if "email" not in session or session.get("role") != "student":
        flash("Please log in as a student.")
        return redirect(url_for("login"))

    student_bookings = [
        b for b in bookings if b["email"] == session["email"]
    ]

    user = {
        "name": session["name"]
    }

    return render_template(
        "student_dashboard.html",
        user=user,
        bookings=student_bookings
    )


@app.route("/owner-dashboard")
def owner_dashboard():
    if "email" not in session or session.get("role") != "owner":
        flash("Please log in as a resource owner.")
        return redirect(url_for("login"))

    return render_template(
        "owner_dashboard.html",
        bookings=bookings
    )


@app.route("/update-booking/<int:booking_id>", methods=["POST"])
def update_booking(booking_id):
    if "email" not in session or session.get("role") != "owner":
        return redirect(url_for("login"))

    new_status = request.form.get("status")

    if new_status not in ["Approved", "Rejected"]:
        return redirect(url_for("owner_dashboard"))

    booking = next(
        (b for b in bookings if b["id"] == booking_id),
        None
    )

    if booking:
        booking["status"] = new_status
        flash("Booking status updated.")

    return redirect(url_for("owner_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)