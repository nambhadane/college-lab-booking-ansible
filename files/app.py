
from flask import Flask, jsonify, request
from datetime import datetime
from threading import Lock

app = Flask(__name__)

labs = [
    {"id": 1, "name": "Computer Lab 1", "capacity": 30},
    {"id": 2, "name": "Computer Lab 2", "capacity": 25},
    {"id": 3, "name": "AI and ML Lab", "capacity": 20}
]

bookings = []
next_booking_id = 1
booking_lock = Lock()


@app.route("/")
def home():
    return jsonify({
        "application": "College Lab Resource Booking API",
        "message": "API is running",
        "endpoints": {
            "health": "/health",
            "labs": "/labs",
            "create_booking": "POST /bookings",
            "view_bookings": "GET /bookings"
        }
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/labs", methods=["GET"])
def get_labs():
    return jsonify(labs), 200


@app.route("/bookings", methods=["POST"])
def create_booking():
    global next_booking_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a valid JSON object"}), 400

    student_name = data.get("student_name")
    lab_id = data.get("lab_id")
    booking_date = data.get("booking_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([student_name, lab_id, booking_date, start_time, end_time]):
        return jsonify({
            "error": "Required fields: student_name, lab_id, "
                     "booking_date, start_time, end_time"
        }), 400

    if not isinstance(student_name, str) or not student_name.strip():
        return jsonify({"error": "Student name must not be empty"}), 400

    if isinstance(lab_id, bool) or not isinstance(lab_id, int):
        return jsonify({"error": "lab_id must be an integer"}), 400

    selected_lab = next((lab for lab in labs if lab["id"] == lab_id), None)
    if selected_lab is None:
        return jsonify({"error": "Lab not found"}), 404

    try:
        date_value = datetime.strptime(booking_date, "%Y-%m-%d").date()
        start_value = datetime.strptime(start_time, "%H:%M").time()
        end_value = datetime.strptime(end_time, "%H:%M").time()
    except (TypeError, ValueError):
        return jsonify({
            "error": "Use booking_date YYYY-MM-DD and times HH:MM"
        }), 400

    if date_value < datetime.now().date():
        return jsonify({"error": "Booking date cannot be in the past"}), 400

    if start_value >= end_value:
        return jsonify({"error": "End time must be after start time"}), 400

    with booking_lock:
        for booking in bookings:
            if (
                booking["lab_id"] == lab_id
                and booking["booking_date"] == booking_date
                and start_time < booking["end_time"]
                and end_time > booking["start_time"]
            ):
                return jsonify({
                    "error": "This lab already has a booking "
                             "during the selected time"
                }), 409

        booking = {
            "booking_id": next_booking_id,
            "student_name": student_name.strip(),
            "lab_id": lab_id,
            "lab_name": selected_lab["name"],
            "booking_date": booking_date,
            "start_time": start_time,
            "end_time": end_time,
            "status": "confirmed"
        }

        bookings.append(booking)
        next_booking_id += 1

    return jsonify({
        "message": "Lab booked successfully",
        "booking": booking
    }), 201


@app.route("/bookings", methods=["GET"])
def get_bookings():
    return jsonify(bookings), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

