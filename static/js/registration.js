document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращает стандартное поведение формы, то есть перезагрузку страницы при отправке формы.

        const firstName = document.getElementById('first-name').value;
        const lastName = document.getElementById('last-name').value;
        const middleName = document.getElementById('middle-name').value;
        const birthDate = document.getElementById('birth-date').value;
        const userPassword = document.getElementById('user-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (userPassword !== confirmPassword) {
            alert('Пароли не совпадают');
            return;
        }

        const authorData = {
            first_name: firstName,
            last_name: lastName,
            middle_name: middleName,
            birth_date: birthDate,
            author_password: userPassword
        };

        fetch('/addUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(authorData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Регистрация успешна');
            // Перенаправление на другую страницу или другие действия после успешной регистрации
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Ошибка при регистрации');
        });
    });
});
