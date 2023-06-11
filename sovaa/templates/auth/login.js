document.addEventListener('DOMContentLoaded', function() {
  var loginForm = document.getElementById('login-form');
  loginForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Создаем объект FormData для отправки данных формы
    var formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    // Создаем AJAX запрос
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/auth/login', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        // Обработка успешного ответа от сервера
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
          // Вход успешен
          window.location.href = '/'; // Перенаправляем на главную страницу
        } else {
          // Ошибка входа
          var errorElement = document.getElementById('error-message');
          errorElement.textContent = response.error;
          errorElement.style.display = 'block';
        }
      }
    };

    // Отправляем запрос на сервер
    xhr.send(formData);
  });
});