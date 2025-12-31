// Modal Toggle
function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal.classList.contains('active')) {
        modal.classList.remove('active');
    } else {
        modal.classList.add('active');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}

// Delete Email
function deleteEmail(id) {
    if (confirm('Are you sure you want to delete this email ID? All associated websites and submissions will also be deleted.')) {
        fetch(`/delete_email/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Delete Website
function deleteWebsite(id) {
    if (confirm('Are you sure you want to delete this website? All associated submissions will also be deleted.')) {
        fetch(`/delete_website/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Delete Submission
function deleteSubmission(id) {
    if (confirm('Are you sure you want to delete this submission?')) {
        fetch(`/delete_submission/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Update Submission Status
function updateStatus(id, status) {
    fetch(`/update_submission_status/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Check for upcoming deadlines
function checkDeadlines() {
    // This could be expanded to show browser notifications
    console.log('Checking deadlines...');
}

// Run on page load
document.addEventListener('DOMContentLoaded', function() {
    checkDeadlines();
});
