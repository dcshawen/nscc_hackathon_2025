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

// Initialize total hours calculation for Week 1 and Week 2
calculateTotalHours(1);
calculateTotalHours(2);
