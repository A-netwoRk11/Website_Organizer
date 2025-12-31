function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal.classList.contains('active')) {
        modal.classList.remove('active');
    } else {
        modal.classList.add('active');
    }
}
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}
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
function checkDeadlines() {
    
    console.log('Checking deadlines...');
}
document.addEventListener('DOMContentLoaded', function() {
    checkDeadlines();
});