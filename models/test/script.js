document.addEventListener('DOMContentLoaded', function() {
    const scheduleDate = document.getElementById('schedule-date');
    const yearElement = document.getElementById('year');
    
    // Get current date
    const currentDate = new Date();
    
    // Format date as: Day, Month Date, Year (e.g., "Monday, August 21, 2024")
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = currentDate.toLocaleDateString(undefined, options);
    
    // Set the header text to the current date
    scheduleDate.textContent = formattedDate;

    // Set the copyright year dynamically
    if (yearElement) {
        yearElement.textContent = currentDate.getFullYear();
    }

    const timeSlots = document.querySelectorAll('.schedule-time');

    timeSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            clearActiveClasses();
            slot.classList.add('active');
            const time = slot.getAttribute('data-time');
            alert(`You clicked on the ${time} slot!`);
            // You can replace the alert with code to open a modal, form, etc.
        });
    });

    function clearActiveClasses() {
        timeSlots.forEach(slot => {
            slot.classList.remove('active');
        });
    }
});

// the hompage slide effect
var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}
function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" w3-white", "");
  }
  x[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " w3-white";
}