document.querySelector('form').addEventListener('submit', (event) => {
    event.preventDefault(); // Предотвращаем отправку формы по умолчанию

    const form = event.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: form.method,
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error creating announcement');
        }
    })
    .then(data => {
        // Обработка успешного ответа от сервера
        console.log('Announcement created:', data);
        // Перенаправление на страницу с объявлениями
        window.location.href = '{{ url_for("auction.index") }}';
    })
    .catch(error => {
        // Обработка ошибки
        console.error(error);
        // Отображение ошибки на странице, например, через flash сообщение
        alert('Error creating announcement. Please try again.');
    });
});