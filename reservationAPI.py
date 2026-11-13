from flask import Flask, jsonify, request 
from datetime import datetime

app = Flask(__name__)

reservations = [
    {
        "reservation_id": 1,
        "requester_name": "Juan Dela Cruz",
        "comlab_name": "Lab 1",
        "reservation_date": "2026-11-20",
        "start_time": "08:00",
        "end_time": "10:00",
        "purpose": "Programming class",
        "status": "reserved",
    },
    {
        "reservation_id": 2,
        "requester_name": "Maria Santos",
        "comlab_name": "Lab 2",
        "reservation_date": "2026-11-21",
        "start_time": "10:00",
        "end_time": "12:00",
        "purpose": "Thesis defense rehearsal",
        "status": "reserved",
    },
    {
        "reservation_id": 3,
        "requester_name": "Sir Rodney Pogi",
        "comlab_name": "Lab 3",
        "reservation_date": "2026-11-22",
        "start_time": "12:00",
        "end_time": "13:00",
        "purpose": "Programming Python",
        "status": "reserved",
    },
    {
        "reservation_id": 4,
        "requester_name": "Princess Bayhag",
        "comlab_name": "Lab 4",
        "reservation_date": "2026-11-20",
        "start_time": "13:00",
        "end_time": "14:00",
        "purpose": "Thesis defense rehearsal",
        "status": "reserved",
    },
    {
        "reservation_id": 5,
        "requester_name": "Kyla Lacanlale",
        "comlab_name": "Lab 5",
        "reservation_date": "2026-11-24",
        "start_time": "10:00",
        "end_time": "12:00",
        "purpose": "Internet of Things sesh",
        "status": "reserved",
    },
    {
        "reservation_id": 6,
        "requester_name": "Chanel Fernandez",
        "comlab_name": "Lab 6",
        "reservation_date": "2026-11-22",
        "start_time": "10:00",
        "end_time": "12:00",
        "purpose": "Thesis defense rehearsal",
        "status": "reserved",
    },
    {
        "reservation_id": 7,
        "requester_name": "Joy Nisperos",
        "comlab_name": "Lab 7",
        "reservation_date": "2026-11-25",
        "start_time": "10:00",
        "end_time": "12:00",
        "purpose": "WebDeb sesh",
        "status": "reserved",
    },
    {
        "reservation_id": 8,
        "requester_name": "JD Bayani",
        "comlab_name": "Lab 8",
        "reservation_date": "2026-11-25",
        "start_time": "13:00",
        "end_time": "14:00",
        "purpose": "Thesis Defense",
        "status": "reserved",
    },
]

# GET all reservations -> 200 OK (500 on unexpected error)
@app.route("/reservations", methods=["GET"])
def get_all_reservations():
    try:
        return jsonify(reservations), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


# GET one reservation -> 200 OK (404 if not found)
@app.route("/reservations/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    for r in reservations:
        if r["reservation_id"] == reservation_id:
            return jsonify(r), 200
    return jsonify({"error": "Reservation not found"}), 404

# POST a new reservation -> 201 Created
@app.route("/reservations", methods=["POST"])
def create_reservation():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        required_fields = [
            "requester_name",
            "comlab_name",
            "reservation_date",
            "start_time",
            "end_time",
            "purpose"
        ]

        # Check required fields
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        # Check if end time is later than start time
        try:
            start = datetime.strptime(
                data["start_time"], "%H:%M"
            )
            end = datetime.strptime(
                data["end_time"], "%H:%M"
            )
            datetime.strptime(
                data["reservation_date"], "%Y-%m-%d"
            )
        except ValueError:
            return jsonify({
                "error": "Invalid date or time format"
            }), 400

        if end <= start:
            return jsonify({
                "error": "End time must be later than start time"
            }), 400

    except Exception:
        return jsonify({
            "error": "Internal Server Error"
        }), 500
        
    def validate_time(time_value):
    #Validate time format: HH:MM (24-hour format).

        if not isinstance(time_value, str):
            return False

        try:
            datetime.strptime(time_value, "%H:%M")
            return len(time_value) == 5

        except ValueError:
            return False

        # Generate a new reservation ID
    new_id = max(
        [r["reservation_id"] for r in reservations],
        default=0
    ) + 1

    new_reservation = {
        "reservation_id": new_id,
        "requester_name": data["requester_name"],
        "comlab_name": data["comlab_name"],
        "reservation_date": data["reservation_date"],
        "start_time": data["start_time"],
        "end_time": data["end_time"],
        "purpose": data["purpose"],
        "status": "reserved"
    }

    reservations.append(new_reservation)

    return jsonify({
        "message": "Reservation created successfully",
        "reservation": new_reservation
    }), 201  


# PUT update an existing reservation -> 200 OK (400, 404, 409)
@app.route("/reservations/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        # Find existing reservation
        target_reservation = None
        for r in reservations:
            if r["reservation_id"] == reservation_id:
                target_reservation = r
                break

        if not target_reservation:
            return jsonify({
                "error": "Reservation not found."
            }), 404

        # Extract fields to update or keep existing values
        new_comlab = data.get("comlab_name", target_reservation["comlab_name"])
        new_date = data.get("reservation_date", target_reservation["reservation_date"])
        new_start = data.get("start_time", target_reservation["start_time"])
        new_end = data.get("end_time", target_reservation["end_time"])

        # Validate date and time formats if updated
        try:
            start = datetime.strptime(new_start, "%H:%M")
            end = datetime.strptime(new_end, "%H:%M")
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "error": "Invalid date or time format"
            }), 400

        if end <= start:
            return jsonify({
                "error": "End time must be later than start time"
            }), 400

        # Check for scheduling conflicts with other records (excluding current id)
        for r in reservations:
            if r["reservation_id"] != reservation_id:
                if (r["comlab_name"] == new_comlab and 
                    r["reservation_date"] == new_date and 
                    r["start_time"] == new_start):
                    return jsonify({
                        "error": "Conflict: Laboratory is already reserved for this date and time slot."
                    }), 409

        # Perform the update
        target_reservation["requester_name"] = data.get("requester_name", target_reservation["requester_name"])
        target_reservation["comlab_name"] = new_comlab
        target_reservation["reservation_date"] = new_date
        target_reservation["start_time"] = new_start
        target_reservation["end_time"] = new_end
        target_reservation["purpose"] = data.get("purpose", target_reservation["purpose"])
        target_reservation["status"] = data.get("status", target_reservation["status"])

        return jsonify({
            "message": "Reservation updated successfully",
            "reservation": target_reservation
        }), 200

    except Exception:
        return jsonify({
            "error": "Internal Server Error"
        }), 500

#DELETE a reservation -> 200 OK (400 Not Found)
@app.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    for reservation in reservations:
        if reservation['reservation_id'] == reservation_id:
            reservations.remove(reservation)
            return jsonify(message="Reservation is deleted.")
        return jsonify(error="Reservation not found."), 400

if __name__ == "__main__":
    app.run(debug=True)