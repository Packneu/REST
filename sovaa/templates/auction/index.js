$(document).ready(function() {
    // Проверка авторизации пользователя
    $.get('/check_auth', function(data) {
        if (data.authenticated) {
            // Пользователь авторизован
            $('#user-info').text('Welcome, ' + data.username + '!');
            $('#logout-btn').html('<a href="/logout">Logout</a>');
            $('#create-announcement-section').show();
        } else {
            // Пользователь не авторизован
            $('#user-info').text('');
            $('#logout-btn').html('');
            $('#create-announcement-section').hide();
        }
    });
    // Обработка события отправки формы для создания объявления
    $('#announcement-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/create',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Объявление успешно создано
                window.location.href = '/';
                },
            error: function(xhr, status, error) {
                // Возникла ошибка при создании объявления
                var errorMessage = xhr.responseText || 'An error occurred.';
                alert(errorMessage);
            }
        });
    });
});