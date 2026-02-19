document.querySelectorAll('.notification').forEach(item => {
    item.addEventListener('click', () => {
        const id = item.dataset.id;
        fetch(`/notifications/mark-read/${id}/`)
            .then(res => location.reload());
    });
});



function sendMessage() {
    const msg = document.getElementById('user_message').value;
    if(msg.trim() === "") return;

    const messages = document.getElementById('messages');
    messages.innerHTML += `<div class="user-msg"><b>You:</b> ${msg}</div>`;

    fetch('/chatbot/', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': csrftoken},
        body: `message=${encodeURIComponent(msg)}`
    })
    .then(res => res.json())
    .then(data => {
        messages.innerHTML += `<div class="bot-msg"><b>Bot:</b> ${data.reply}</div>`;
        messages.scrollTop = messages.scrollHeight;
    });

    document.getElementById('user_message').value = '';
}
