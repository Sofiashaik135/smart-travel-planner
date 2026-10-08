from flask import Flask, request, jsonify
from flask_cors import CORS

from database import (
    create_table,
    save_trip,
    get_trips,
    delete_trip
)

from datetime import datetime, timedelta


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

CORS(app)


# Create database table
create_table()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message": "Smart Travel Planner API is running!"
    })


# ==========================================
# SAVE TRIP
# ==========================================

@app.route(
    "/api/trips",
    methods=["POST"]
)
def create_trip():

    data = request.get_json()


    start_location = data.get(
        "start_location"
    )

    destination = data.get(
        "destination"
    )

    start_date = data.get(
        "start_date"
    )

    end_date = data.get(
        "end_date"
    )

    currency = data.get(
        "currency",
        "₹"
    )

    budget = data.get(
        "budget"
    )

    travelers = data.get(
        "travelers"
    )

    interests = data.get(
        "interests"
    )


    # Validation

    if not start_location:

        return jsonify({
            "error":
            "Starting location is required"
        }), 400


    if not destination:

        return jsonify({
            "error":
            "Destination is required"
        }), 400


    if not start_date:

        return jsonify({
            "error":
            "Start date is required"
        }), 400


    if not end_date:

        return jsonify({
            "error":
            "End date is required"
        }), 400


    if not budget:

        return jsonify({
            "error":
            "Budget is required"
        }), 400


    if not travelers:

        return jsonify({
            "error":
            "Number of travelers is required"
        }), 400


    if not interests:

        return jsonify({
            "error":
            "Interests are required"
        }), 400


    if end_date < start_date:

        return jsonify({
            "error":
            "End date must be after start date"
        }), 400


    # Save trip

    trip_id = save_trip(

        start_location,

        destination,

        start_date,

        end_date,

        currency,

        budget,

        travelers,

        interests

    )


    return jsonify({

        "message":
        "Trip saved successfully!",

        "trip_id":
        trip_id

    }), 201


# ==========================================
# GET SAVED TRIPS
# ==========================================

@app.route(
    "/api/trips",
    methods=["GET"]
)
def trips():

    all_trips = get_trips()


    return jsonify(
        all_trips
    )


# ==========================================
# DELETE TRIP
# ==========================================

@app.route(
    "/api/trips/<int:trip_id>",
    methods=["DELETE"]
)
def remove_trip(trip_id):

    deleted = delete_trip(
        trip_id
    )


    if deleted == 0:

        return jsonify({
            "error":
            "Trip not found"
        }), 404


    return jsonify({

        "message":
        "Trip deleted successfully!"

    })


# ==========================================
# DAY-WISE RECOMMENDATION
# ==========================================

@app.route(
    "/api/recommend",
    methods=["POST"]
)
def recommend():

    data = request.get_json()


    start_location = data.get(
        "start_location",
        ""
    )

    destination = data.get(
        "destination",
        ""
    )

    start_date = data.get(
        "start_date",
        ""
    )

    end_date = data.get(
        "end_date",
        ""
    )

    currency = data.get(
        "currency",
        "₹"
    )

    budget = data.get(
        "budget",
        ""
    )

    travelers = data.get(
        "travelers",
        ""
    )

    interests = data.get(
        "interests",
        ""
    )


    # Validation

    if not start_date or not end_date:

        return jsonify({
            "error":
            "Start date and end date are required"
        }), 400


    if end_date < start_date:

        return jsonify({
            "error":
            "End date must be after start date"
        }), 400


    try:

        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        )

    except ValueError:

        return jsonify({
            "error":
            "Invalid date format"
        }), 400


    total_days = (
        end - start
    ).days + 1


    # ======================================
    # INTEREST DETECTION
    # ======================================

    interest_text = interests.lower()


    wants_beach = (
        "beach" in interest_text
        or "sea" in interest_text
        or "nature" in interest_text
    )


    wants_food = (
        "food" in interest_text
        or "restaurant" in interest_text
        or "cafe" in interest_text
    )


    wants_history = (
        "history" in interest_text
        or "historical" in interest_text
        or "temple" in interest_text
        or "museum" in interest_text
    )


    wants_shopping = (
        "shopping" in interest_text
        or "market" in interest_text
    )


    # ======================================
    # DIFFERENT ACTIVITIES
    # ======================================

    morning_activities = []

    afternoon_activities = []

    evening_activities = []

    focus_activities = []


    if wants_beach:

        morning_activities.append(
            f"Explore a scenic natural area near {destination}."
        )

        afternoon_activities.append(
            f"Visit a popular beach or nature spot around {destination}."
        )

        evening_activities.append(
            f"Enjoy a relaxing sunset experience in {destination}."
        )

        focus_activities.append(
            "Nature and relaxation"
        )


    if wants_history:

        morning_activities.append(
            f"Visit a historical place or famous landmark in {destination}."
        )

        afternoon_activities.append(
            f"Explore a museum, temple or heritage location in {destination}."
        )

        evening_activities.append(
            f"Walk around an old or culturally important area of {destination}."
        )

        focus_activities.append(
            "History and culture"
        )


    if wants_food:

        morning_activities.append(
            f"Try a popular breakfast or local food in {destination}."
        )

        afternoon_activities.append(
            f"Explore local restaurants and try regional dishes."
        )

        evening_activities.append(
            f"Enjoy a local dinner or food experience in {destination}."
        )

        focus_activities.append(
            "Local food"
        )


    if wants_shopping:

        morning_activities.append(
            f"Explore a local market in {destination}."
        )

        afternoon_activities.append(
            f"Visit a popular shopping area in {destination}."
        )

        evening_activities.append(
            f"Explore local shops and markets."
        )

        focus_activities.append(
            "Shopping"
        )


    # ======================================
    # DEFAULT ACTIVITIES
    # ======================================

    if not morning_activities:

        morning_activities = [

            f"Explore the main attractions of {destination}.",

            f"Visit a popular sightseeing location in {destination}.",

            f"Discover a local cultural area of {destination}."

        ]


    if not afternoon_activities:

        afternoon_activities = [

            f"Visit another important attraction in {destination}.",

            f"Explore local streets and interesting places.",

            f"Spend time discovering the surroundings of {destination}."

        ]


    if not evening_activities:

        evening_activities = [

            f"Enjoy the evening atmosphere in {destination}.",

            f"Visit a popular evening spot in {destination}.",

            f"Relax and explore the city at night."

        ]


    if not focus_activities:

        focus_activities = [

            "Sightseeing",

            "Local exploration",

            "Relaxation"

        ]


    # ======================================
    # CREATE DAY-WISE PLAN
    # ======================================

    day_wise_plan = []


    for i in range(total_days):

        current_date = (
            start + timedelta(days=i)
        )


        # Use different activities
        morning = morning_activities[
            i % len(morning_activities)
        ]

        afternoon = afternoon_activities[
            i % len(afternoon_activities)
        ]

        evening = evening_activities[
            i % len(evening_activities)
        ]

        focus = focus_activities[
            i % len(focus_activities)
        ]


        # Special first day

        if i == 0:

            morning = (
                f"Start your journey from "
                f"{start_location} and travel towards "
                f"{destination}. "
                + morning
            )


        # Special last day

        if i == total_days - 1:

            evening = (
                evening
                + " Prepare for your return journey."
            )


        day_wise_plan.append({

            "day":
            f"Day {i + 1}",

            "date":
            current_date.strftime(
                "%d-%m-%Y"
            ),

            "morning":
            morning,

            "afternoon":
            afternoon,

            "evening":
            evening,

            "focus":
            focus

        })


    # ======================================
    # RESPONSE
    # ======================================

    return jsonify({

        "start_location":
        start_location,

        "destination":
        destination,

        "currency":
        currency,

        "budget":
        budget,

        "travelers":
        travelers,

        "requirements":
        interests,

        "total_days":
        total_days,

        "day_wise_plan":
        day_wise_plan

    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )