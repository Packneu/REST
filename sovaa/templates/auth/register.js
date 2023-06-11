document.addEventListener('DOMContentLoaded', function() {
  var registerForm = document.getElementById('register-form');
  registerForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Создаем объект FormData для отправки данных формы
    var formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    // Создаем AJAX запрос
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/auth/register', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        // Обработка успешного ответа от сервера
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
          // Регистрация успешна
          window.location.href = '/'; // Перенаправляем на главную страницу
        } else {
          // Ошибка регистрации
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