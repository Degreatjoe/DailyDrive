// script.js

// Initialize currentDate to today's date
let currentDate = new Date();
const dateDisplay = document.getElementById('dateDisplay');
const plannerElement = document.getElementById('planner');

// Update date display
function updateDateDisplay() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateDisplay.textContent = currentDate.toLocaleDateString(undefined, options);
}

// Load the previous day's plans
function loadPreviousDay() {
    currentDate.setDate(currentDate.getDate() - 1);
    updateDateDisplay();
    fetchPlansForDate(currentDate);
}

// Load the next day's planner
function loadNextDay() {
    currentDate.setDate(currentDate.getDate() + 1);
    updateDateDisplay();
    fetchPlansForDate(currentDate);
}

// Fetch plans for a specific date
function fetchPlansForDate(date) {
    const formattedDate = date.toISOString().split('T')[0]; // Format date as YYYY-MM-DD
    // Example AJAX request (use Fetch API or Axios if you prefer)
    fetch(`/plans?date=${formattedDate}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                displayPlans(data);
            } else {
                displayEmptyPlanner();
            }
        })
        .catch(error => {
            console.error('Error fetching plans:', error);
            displayEmptyPlanner();
        });
}

// Display the plans for a specific date
function displayPlans(plans) {
    plannerElement.innerHTML = plans.map(plan => `
        <div class="timeSlot">${plan.time}: ${plan.task}</div>
    `).join('');
}

// Display an empty planner (no plans for the date)
function displayEmptyPlanner() {
    plannerElement.innerHTML = `
        <div id="dateDisplay">${dateDisplay.textContent}</div>
        <div class="timeSlot">05:00</div>
        <div class="timeSlot">06:00</div>
        <div class="timeSlot">07:00</div>
        <div class="timeSlot">08:00</div>
        <div class="timeSlot">09:00</div>
        <div class="timeSlot">10:00</div>
        <div class="timeSlot">11:00</div>
        <div class="timeSlot">12:00</div>
        <div class="timeSlot">13:00</div>
        <div class="timeSlot">14:00</div>
        <div class="timeSlot">15:00</div>
        <div class="timeSlot">16:00</div>
        <div class="timeSlot">17:00</div>
        <div class="timeSlot">18:00</div>
        <!-- Add more time slots as needed -->
        <div class="timeSlot">19:00</div>
        <div class="timeSlot">20:00</div>
        <div class="timeSlot">21:00</div>
        <div class="timeSlot">22:00</div>
        <div class="timeSlot">23:00</div>
    `;
}

// Event delegation for handling clicks on time slots
plannerElement.addEventListener('click', function (event) {
    if (event.target.classList.contains('timeSlot')) {
        clearActiveClasses();
        event.target.classList.add('active');
        const time = event.target.getAttribute('data-time');
        alert(`You clicked on the ${time} slot!`);
        // You can replace the alert with code to open a modal, form, etc.
    }
});

function clearActiveClasses() {
    const timeSlots = document.querySelectorAll('.timeSlot');
    timeSlots.forEach(slot => {
        slot.classList.remove('active');
    });
}

// Initialize Hammer.js for swipe handling
const hammer = new Hammer(plannerElement);

hammer.on('swiperight', function() {
    loadPreviousDay();
});

hammer.on('swipeleft', function() {
    loadNextDay();
});

// Initial load for today's date
updateDateDisplay();
fetchPlansForDate(currentDate);
