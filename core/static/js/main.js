document.querySelectorAll('.notification').forEach(item => {
    item.addEventListener('click', () => {
        const id = item.dataset.id;
        fetch(`/notifications/mark-read/${id}/`)
            .then(res => location.reload());
    });
});
