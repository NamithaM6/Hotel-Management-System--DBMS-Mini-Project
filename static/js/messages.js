document.addEventListener('DOMContentLoaded', function () {
    const messageElement = document.getElementById('django-messages');
    if (messageElement) {
        const message = messageElement.dataset.message;
        if (message) {
            alert(message);
        }
    }
});