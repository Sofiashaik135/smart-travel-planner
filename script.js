const API_URL = "http://127.0.0.1:5000";


const tripForm = document.getElementById("tripForm");

const recommendButton =
    document.getElementById("recommendButton");

const message =
    document.getElementById("message");

const recommendationList =
    document.getElementById("recommendationList");

const tripList =
    document.getElementById("tripList");


// ==========================================
// SAVE TRIP
// ==========================================

tripForm.addEventListener("submit", async function(event) {

    event.preventDefault();


    const tripData = {

        start_location:
            document.getElementById("startLocation").value,

        destination:
            document.getElementById("destination").value,

        start_date:
            document.getElementById("startDate").value,

        end_date:
            document.getElementById("endDate").value,

        currency:
            document.getElementById("currency").value,

        budget:
            document.getElementById("budget").value,

        travelers:
            document.getElementById("travelers").value,

        interests:
            document.getElementById("interests").value
    };


    if (tripData.end_date < tripData.start_date) {

        message.textContent =
            "❌ End date must be after start date.";

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/api/trips`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(tripData)
            }
        );


        const result = await response.json();


        if (response.ok) {

            message.textContent =
                "✅ Trip saved successfully!";

            tripForm.reset();

            document.getElementById("currency").value = "₹";

            loadTrips();

        } else {

            message.textContent =
                "❌ " + result.error;
        }


    } catch (error) {

        message.textContent =
            "❌ Backend server is not running.";

        console.error(error);
    }

});


// ==========================================
// AI / DAY-WISE RECOMMENDATIONS
// ==========================================

recommendButton.addEventListener(
    "click",
    async function() {


        const startLocation =
            document.getElementById("startLocation").value;

        const destination =
            document.getElementById("destination").value;

        const startDate =
            document.getElementById("startDate").value;

        const endDate =
            document.getElementById("endDate").value;

        const currency =
            document.getElementById("currency").value;

        const budget =
            document.getElementById("budget").value;

        const travelers =
            document.getElementById("travelers").value;

        const interests =
            document.getElementById("interests").value;


        if (
            !startLocation ||
            !destination ||
            !startDate ||
            !endDate ||
            !budget ||
            !travelers ||
            !interests
        ) {

            recommendationList.innerHTML =
                "<p>❌ Please fill all trip details first.</p>";

            return;
        }


        if (endDate < startDate) {

            recommendationList.innerHTML =
                "<p>❌ End date must be after start date.</p>";

            return;
        }


        recommendationList.innerHTML =
            "<p>🤖 Creating your personalized day-wise plan...</p>";


        try {

            const response = await fetch(
                `${API_URL}/api/recommend`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        start_location: startLocation,

                        destination: destination,

                        start_date: startDate,

                        end_date: endDate,

                        currency: currency,

                        budget: budget,

                        travelers: travelers,

                        interests: interests
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                recommendationList.innerHTML =
                    `<p>❌ ${data.error}</p>`;

                return;
            }


            recommendationList.innerHTML = "";


            data.day_wise_plan.forEach(function(day) {

                const div =
                    document.createElement("div");

                div.className =
                    "recommendation";


                div.innerHTML = `

                    <h3 class="day-title">
                        📅 ${day.day}
                    </h3>

                    <p>
                        <strong>Date:</strong>
                        ${day.date}
                    </p>

                    <p>
                        <strong>Morning:</strong>
                        ${day.morning}
                    </p>

                    <p>
                        <strong>Afternoon:</strong>
                        ${day.afternoon}
                    </p>

                    <p>
                        <strong>Evening:</strong>
                        ${day.evening}
                    </p>

                    <p>
                        <strong>Plan:</strong>
                        ${day.focus}
                    </p>

                `;


                recommendationList.appendChild(div);

            });


        } catch (error) {

            recommendationList.innerHTML =
                "<p>❌ Could not connect to backend.</p>";

            console.error(error);
        }

    }
);


// ==========================================
// LOAD SAVED TRIPS
// ==========================================

async function loadTrips() {

    try {

        const response = await fetch(
            `${API_URL}/api/trips`
        );


        const trips = await response.json();


        tripList.innerHTML = "";


        if (trips.length === 0) {

            tripList.innerHTML =
                "<p>No saved trips yet.</p>";

            return;
        }


        trips.forEach(function(trip) {

            const card =
                document.createElement("div");

            card.className =
                "trip-card";


            card.innerHTML = `

                <h3>
                    📍 ${trip.start_location}
                    → ${trip.destination}
                </h3>

                <p>
                    <strong>Dates:</strong>
                    ${trip.start_date}
                    to
                    ${trip.end_date}
                </p>

                <p>
                    <strong>Budget:</strong>
                    ${trip.currency || "₹"}${trip.budget}
                </p>

                <p>
                    <strong>Travelers:</strong>
                    ${trip.travelers}
                </p>

                <p>
                    <strong>Requirements:</strong>
                    ${trip.interests}
                </p>

                <button
                    class="delete-button"
                    onclick="deleteTrip(${trip.id})">
                    🗑️ Delete Trip
                </button>

            `;


            tripList.appendChild(card);

        });


    } catch (error) {

        tripList.innerHTML =
            "<p>❌ Backend server is not running.</p>";

        console.error(error);
    }
}


// ==========================================
// DELETE TRIP
// ==========================================

async function deleteTrip(tripId) {

    try {

        const response = await fetch(
            `${API_URL}/api/trips/${tripId}`,
            {
                method: "DELETE"
            }
        );


        const result =
            await response.json();


        if (response.ok) {

            message.textContent =
                "✅ Trip deleted successfully!";

            loadTrips();

        } else {

            message.textContent =
                "❌ " + result.error;

        }


    } catch (error) {

        message.textContent =
            "❌ Could not connect to backend.";

        console.error(error);
    }
}


// ==========================================
// LOAD TRIPS WHEN PAGE OPENS
// ==========================================

loadTrips();