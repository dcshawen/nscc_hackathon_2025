// Function to enable drawing on a canvas
function enableDrawing(canvasId) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext("2d");
    let drawing = false;

    canvas.addEventListener("mousedown", () => (drawing = true));
    canvas.addEventListener("mouseup", () => {
        drawing = false;
        ctx.beginPath(); // Reset path to avoid lines connecting points
    });
    canvas.addEventListener("mousemove", (event) => {
        if (!drawing) return;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        ctx.lineWidth = 2;
        ctx.lineCap = "round";
        ctx.strokeStyle = "#000";
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    });
}

// Function to clear the canvas
function clearCanvas(canvasId) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Enable drawing for both signature canvases
enableDrawing("manager-signature");
enableDrawing("employee-signature");

// Function to calculate the total hours dynamically for each week
function calculateTotalHours(weekNumber) {
    const weekTable = document.querySelector(`.week-table:nth-of-type(${weekNumber})`);
    const hoursInputs = weekTable.querySelectorAll(".hours");
    const totalField = weekTable.querySelector(`#week${weekNumber}-total`);

    // Event listener to update total when hours are entered
    hoursInputs.forEach((input) => {
        input.addEventListener("input", () => {
            let total = 0;
            hoursInputs.forEach((hourInput) => {
                total += parseFloat(hourInput.value) || 0; // Sum all valid inputs
            });
            totalField.value = total.toFixed(2); // Update total field
        });
    });
}

// comment this out to make auto fill work
// Initialize total hours calculation for Week 1 and Week 2
// calculateTotalHours(1);
// calculateTotalHours(2);

// if invalid input is given default to 0
var hoursClass = document.getElementsByClassName("hours");
for (let i = 0; i < 14; i++) {
    hoursClass[i].addEventListener("change", function() {
        var input = Number(hoursClass[i].value)
        if (input == 0) {
            this.value = 0;
            window.alert("Daily hours must be between 0-24")
        }
        else if (input > 24) {
            this.value = 0;
            window.alert("Daily hours must be between 0-24")
        }
    })
}

// -------------------------------------- date managment -----------------------------------------
// Auto fill dates if start date is entered
document.getElementById("startDate").addEventListener("change", function() {
    const startDate = new Date(this.value)

    if (startDate.getDay() == 6) {
        extrapolateDate("startDate", "endDate", 14);
        extrapolateDate("startDate", "day1", 1);
        for (let i = 0; i < 13; i++) {
            var dayID = "day" + (i + 1)
            var nextDayID = "day" + (i + 2)
    
            extrapolateDate(dayID, nextDayID, 2)
        }
    }
    else {
        this.value = ""
        window.alert("Start day must be a sunday")
    }
})

// Auto fill dates if end date is entered
document.getElementById("endDate").addEventListener("change", function() {
    const endDate = new Date(this.value)

    if (endDate.getDay() == 5) {
        extrapolateDate("endDate", "startDate", -12);
        extrapolateDate("startDate", "day1", 1);
        for (let i = 0; i < 13; i++) {
            var dayID = "day" + (i + 1)
            var nextDayID = "day" + (i + 2)
    
            extrapolateDate(dayID, nextDayID, 2)
        }
    }
    else {
        this.value = ""
        window.alert("End date must be a saturday")
    }

})

// Add an amount of days to a date and output it to an input box
// Takes in id of original date, id of where to write the new date, how many days to add/subtract
function extrapolateDate(origDateID, newDateID, days) {
    const endDateBox = document.getElementById(newDateID);
    const startDateBox = document.getElementById(origDateID);
    
    const startDateInput = startDateBox.value;
    const startDate = new Date(startDateInput);
    
    const endDate = new Date(startDateInput);

    endDate.setDate(endDate.getDate() + days);

    const endDay = ("0" + endDate.getDate()).slice(-2);
    const endMonth = ("0" + (endDate.getMonth() + 1)).slice(-2);
    const endDateInput = endDate.getFullYear() + "-" + endMonth + "-" + endDay;

    endDateBox.value = endDateInput;
}