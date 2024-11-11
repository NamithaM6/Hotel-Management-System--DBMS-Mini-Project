document.addEventListener('DOMContentLoaded', function () {
    const messageElement = document.getElementById('django-messages');
    if (messageElement) {
        const message = messageElement.getAttribute('data-message');
        if (message) {
            alert(message);
        }
    }
});
