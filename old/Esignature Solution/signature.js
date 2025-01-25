// Elements
const canvas = document.getElementById('signatureCanvas');
const ctx = canvas.getContext('2d');
const clearBtn = document.getElementById('clearBtn');
const saveBtn = document.getElementById('saveBtn');
const checkbox = document.getElementById('certifyCheckbox');
const replayCanvas = document.createElement('canvas');
replayCanvas.width = canvas.width;
replayCanvas.height = canvas.height;
replayCanvas.id = 'replayCanvas';
const replayCtx = replayCanvas.getContext('2d');
const replayLabel = document.createElement('p');
replayLabel.textContent = 'Load Signature Pad';
replayLabel.id = 'replayLabel';
replayLabel.style.display = 'none';
replayCanvas.style.display = 'none';
document.body.appendChild(replayLabel);
document.body.appendChild(replayCanvas);

let drawing = false;
let pixelData = []; // To store pixel data

// Functions for drawing
const startDrawing = (event) => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(getX(event), getY(event));
    pixelData.push({ x: getX(event), y: getY(event), newStroke: true });
};

const draw = (event) => {
    if (!drawing) return;
    const x = getX(event);
    const y = getY(event);

    ctx.lineTo(x, y);
    ctx.stroke();

    // Store the pixel data (x, y)
    pixelData.push({ x, y, newStroke: false });
};

const stopDrawing = () => {
    drawing = false;
    ctx.closePath();
};

const getX = (event) => {
    const rect = canvas.getBoundingClientRect();
    return (event.clientX || event.touches[0].clientX) - rect.left;
};

const getY = (event) => {
    const rect = canvas.getBoundingClientRect();
    return (event.clientY || event.touches[0].clientY) - rect.top;
};

// Event listeners for drawing
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseleave', stopDrawing);

canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    startDrawing(e);
});

canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    draw(e);
});

canvas.addEventListener('touchend', (e) => {
    e.preventDefault();
    stopDrawing(e);
});

// Clear canvas
clearBtn.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pixelData = []; // Clear stored pixel data
});

// Save canvas
saveBtn.addEventListener('click', () => {
    // Convert pixelData to JSON for SQL storage
    const jsonData = JSON.stringify(pixelData);

    // Display JSON data for demonstration purposes
    console.log('Pixel Data JSON:', jsonData);

    // Replay signature on the replayCanvas
    replayCtx.clearRect(0, 0, replayCanvas.width, replayCanvas.height); // Clear previous replay
    replayCtx.beginPath();

    pixelData.forEach((point) => {
        if (point.newStroke) {
            replayCtx.moveTo(point.x, point.y);
        } else {
            replayCtx.lineTo(point.x, point.y);
        }
    });

    replayCtx.stroke();
});

// Checkbox interaction
checkbox.addEventListener('change', () => {
    if (checkbox.checked) {
        // Simulate checking for saved signature
        const savedExists = Math.random() > 0.5; // Randomly simulate a saved signature existing
        if (savedExists) {
            // Simulate loading a saved signature
            const savedData = JSON.parse('[{"x":50,"y":60,"newStroke":true},{"x":60,"y":70,"newStroke":false},{"x":70,"y":80,"newStroke":false}]'); // Replace with backend-provided JSON

            // Clear the canvas for a new signature
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Replay the saved data onto the canvas
            ctx.beginPath();
            savedData.forEach((point) => {
                if (point.newStroke) {
                    ctx.moveTo(point.x, point.y);
                } else {
                    ctx.lineTo(point.x, point.y);
                }
            });
            ctx.stroke();

            // Store the loaded data in pixelData
            pixelData = savedData;
        } else {
            // No saved signature; clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            pixelData = [];
        }

        // Show the signature pad, replay canvas, and buttons
        canvas.style.display = 'block';
        clearBtn.style.display = 'inline';
        saveBtn.style.display = 'inline';
        replayCanvas.style.display = 'block';
        replayLabel.style.display = 'block';
    } else {
        // Hide the signature pad, replay canvas, and buttons
        canvas.style.display = 'none';
        clearBtn.style.display = 'none';
        saveBtn.style.display = 'none';
        replayCanvas.style.display = 'none';
        replayLabel.style.display = 'none';
    }
});
