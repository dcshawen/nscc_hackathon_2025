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

// -------------------------------- Data validation --------------------------------
// Validate employee name input
document.getElementById("empNameID").addEventListener("change", function() {
    if (this.value.length > 50) {
        this.value = '';
        window.alert("Employee name must be less than 40 characters")
    }
    else if (!/^[A-Za-z]+ [A-Za-z]+$/.test(this.value)) {
        this.value = '';
        window.alert("Name must be in the format 'First Last' (no extra spaces)")
    }
})

// Validate W number input
document.getElementById("wNumberID").addEventListener("change", function() {
    if (this.value.length != 8) {
        this.value = '';
        window.alert("W Number must be 8 characters long")
    }
    else if (!/^[Ww]\d{7}$/.test(this.value)) {
        this.value = '';
        window.alert("W Number must be in the format 'W########'")
    }
})

// Validate fund input
document.getElementById("fundID").addEventListener("change", function() {
    if (this.value.length > 40) {
        this.value = '';
        window.alert("Fund must be less than 40 characters")
    }
    else if (!/^[A-Za-z0-9 ]+$/.test(this.value)) {
        this.value = '';
        window.alert("Fund must be alphanumeric and can contain spaces")
    }
})

// Validate department input
document.getElementById("deptID").addEventListener("change", function() {
    if (this.value.length > 40) {
        this.value = '';
        window.alert("Dept must be less than 40 characters")
    }
    else if (!/^[A-Za-z0-9 ]+$/.test(this.value)) {
        this.value = '';
        window.alert("Dept must be alphanumeric and can contain spaces")
    }
})

// Validate program input
document.getElementById("programID").addEventListener("change", function() {
    if (this.value.length > 40) {
        this.value = '';
        window.alert("Program must be less than 40 characters")
    }
    else if (!/^[A-Za-z0-9 ]+$/.test(this.value)) {
        this.value = '';
        window.alert("Program must be alphanumeric and can contain spaces")
    }
})

// Validate account input
document.getElementById("acctID").addEventListener("change", function() {
    if (this.value.length > 40) {
        this.value = '';
        window.alert("Acct must be less than 40 characters")
    }
    else if (!/^[A-Za-z0-9 ]+$/.test(this.value)) {
        this.value = '';
        window.alert("Acct must be alphanumeric and can contain spaces")
    }
})

// Validate project input
document.getElementById("projectID").addEventListener("change", function() {
    if (this.value.length > 40) {
        this.value = '';
        window.alert("Project must be less than 40 characters")
    }
    else if (!/^[A-Za-z0-9 ]+$/.test(this.value)) {
        this.value = '';
        window.alert("Project must be alphanumeric and can contain spaces")
    }
})

// Validate daily hours input
var hoursClass = document.getElementsByClassName("hours");
for (let i = 0; i < hoursClass.length; i++) {
    hoursClass[i].addEventListener("change", function() {
        var input = parseFloat(this.value);
        if (isNaN(input)) {
            this.value = 0;
            window.alert("Daily hours must be a numeric value");
        }
        else if (input < 0 || input > 24) {
            this.value = 0;
            window.alert("Daily hours must be between 0-24");
        }
        else if (input % 0.5 !== 0) {
            this.value = 0;
            window.alert("Daily hours must be in increments of 0.5");
        }
    });
    hoursClass[i].addEventListener("input", function() {
        var input = parseFloat(this.value);
        if (isNaN(input)) {
            this.value = 0;
            window.alert("Daily hours must be a numeric value");
        }
    });
}

// Validate notes/comments input
document.getElementById("noteID").addEventListener("change", function() {
    if (this.value.length > 255) {
        window.alert("Notes/comments must be less than 255 characters");
    }
    else if (/;/.test(this.value)) {
        this.value = this.value.replace(/;/g, '');
        window.alert("Notes/comments cannot contain semicolons");
    }
});
document.getElementById("noteID").addEventListener("input", function() {
    if (this.value.length > 255) {
        window.alert("Notes/comments must be less than 255 characters");
    }
    else if (/;/.test(this.value)) {
        this.value = this.value.replace(/;/g, '');
        window.alert("Notes/comments cannot contain semicolons");
    }
});

// Validate optional information input
var optionalInformationClass = document.getElementsByClassName("optionalInformation");
for (let i = 0; i < optionalInformationClass.length; i++) {
    optionalInformationClass[i].addEventListener("change", function() {
        if (this.value.length > 255) {
            window.alert("Notes/comments must be less than 255 characters");
        }
        else if (/;/.test(this.value)) {
            this.value = this.value.replace(/;/g, '');
            window.alert("Notes/comments cannot contain semicolons");
        }
    });
    optionalInformationClass[i].addEventListener("input", function() {
        if (this.value.length > 255) {
            window.alert("Notes/comments must be less than 255 characters");
        }
        else if (/;/.test(this.value)) {
            this.value = this.value.replace(/;/g, '');
            window.alert("Notes/comments cannot contain semicolons");
        }
    });
}

// -------------------------------------- AUTO POPULATION -----------------------------------------
// define variables to change fields
var empNameID = document.getElementById("empNameID");
var wNumberID = document.getElementById("wNumberID");
var fundID = document.getElementById("fundID");
var deptID = document.getElementById("deptID");
var programID = document.getElementById("programID");
var acctID = document.getElementById("acctID");
var projectID = document.getElementById("projectID");
var startDate = document.getElementById("startDate");

// fill in data when page loads
document.body.onload = function() {
    empNameID.value = "John Doe";
    wNumberID.value = "w0000001";
    fundID.value = "Fund A";
    deptID.value = "Dept A";
    programID.value = "Program A";
    acctID.value = "Acct A";
    projectID.value = "Project A";
    startDate.value = "2024-01-28";
    
    extrapolateDate("startDate", "day1", 1);
    extrapolateDate("startDate", "endDate", 14);
    for (let i = 0; i < 13; i++) {
        var dayID = "day" + (i + 1)
        var nextDayID = "day" + (i + 2)
    
        extrapolateDate(dayID, nextDayID, 2)
    }
}



// -------------------------------------- database stuff for auto population -----------------------------------------
// function fetchDatabaseInfo() {
//     console.log("Fetching data from the database...");
//     var xhr = new XMLHttpRequest();
//     xhr.open("GET", "side-script.php", true);
    
//     xhr.onreadystatechange = function () {
//         console.log("Ready state: " + xhr.readyState + ", Status: " + xhr.status);
//         if (xhr.readyState == 4) {
//             if (xhr.status == 200) {
//                 var data = JSON.parse(xhr.responseText);
//                 console.log(data); // Handle the data as needed
//             } else {
//                 console.error("Error fetching data: " + xhr.status + " " + xhr.statusText);
//                 window.alert("An error occurred while fetching data. Please try again later.");
//             }
//         }
//     };
    
//     xhr.onerror = function () {
//         console.error("Request failed");
//         window.alert("An error occurred while fetching data. Please check your network connection and try again.");
//     };
    
//     xhr.send();
// }

// // Call the function to fetch and populate data
// fetchDatabaseInfo();
