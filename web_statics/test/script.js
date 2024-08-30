const scheduleList = document.getElementById('schedule-list');

// function to generate schedule items
function generateSchedule() {
  const scheduleItems = [];
  for (let hour = 0; hour < 24; hour++) {
    const time = `${String(hour).padStart(2, '0')}:00`;
    const event = `Event at ${time}`;
    scheduleItems.push(`<li class="schedule-item"><span class="time">${time}</span><span class="event">${event}</span></li>`);
  }
  scheduleList.innerHTML = scheduleItems.join('');
}

// update schedule every hour
setInterval(() => {
  generateSchedule();
}, 60 * 60 * 1000); // 1 hour

// initial render
generateSchedule();