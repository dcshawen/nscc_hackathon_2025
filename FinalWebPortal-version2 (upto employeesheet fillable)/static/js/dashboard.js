function updateDashboard(role) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => section.classList.add('hidden'));

    // Show the appropriate section based on role
    if (role === 'Employee') {
        document.querySelector('.employee-section').classList.remove('hidden');
    }
    if (role === 'Supervisor') {
        document.querySelector('.supervisor-section').classList.remove('hidden');
    }
    if (role === 'Admin') {
        document.querySelector('.admin-section').classList.remove('hidden');
    }

    // Store role in localStorage
    localStorage.setItem('userRole', role);
}

// Set up the page on load
document.addEventListener('DOMContentLoaded', function () {
    const storedRole = localStorage.getItem('userRole') || 'Employee';
    document.getElementById('user-role').value = storedRole;
    updateDashboard(storedRole);
});

function toggleTimesheetForm(show) {
    const dashboardContainer = document.getElementById('dashboard-container');
    const timesheetContainer = document.getElementById('timesheet-container');
    if (show) {
        dashboardContainer.classList.add('hidden');
        timesheetContainer.classList.remove('hidden');
    } else {
        dashboardContainer.classList.remove('hidden');
        timesheetContainer.classList.add('hidden');
    }
}

function togglePendingTimesheets(show) {
    const dashboardContainer = document.getElementById('dashboard-container');
    const timesheetContainer = document.getElementById('pending-container');
    if (show) {
        dashboardContainer.classList.add('hidden');
        timesheetContainer.classList.remove('hidden');
    } else {
        dashboardContainer.classList.remove('hidden');
        timesheetContainer.classList.add('hidden');
    }
}

function validateForm() {
    const checkbox = document.getElementById('certify-checkbox');
    const submitButton = document.getElementById('submit-button');
    submitButton.disabled = !checkbox.checked;
}
