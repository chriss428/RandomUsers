document.addEventListener('DOMContentLoaded', function() {
    const usersTableBody = document.getElementById('usersTableBody');
    const loadUsersBtn = document.getElementById('loadUsers');
    const clearAllBtn = document.getElementById('clearAll');
    const userCountInput = document.getElementById('userCount');
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');

    let currentPage = 1;
    const usersPerPage = 10;
    let totalUsers = 0;

    loadUsers(currentPage);

    loadUsersBtn.addEventListener('click', async function() {
        const count = parseInt(userCountInput.value);
        if (count > 0 && count < 5001) {
            try {
                const response = await fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({n: count})
                });

                if (!response.ok) {
                    throw new Error('Ошибка при загрузке пользователей');
                }

                await response.json();
                currentPage = 1;
                await loadUsers(currentPage);
                alert(`Успешно добавлено ${count} пользователей`);
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            }
        } else {
            alert('Введите число от 1 до 5000');
        }
    });

    clearAllBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/', {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Ошибка при удалении пользователей');
            }

            currentPage = 1;
            await loadUsers(currentPage);
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
});

    prevPageBtn.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            loadUsers(currentPage);
        }
    });

    nextPageBtn.addEventListener('click', function() {
        currentPage++;
        loadUsers(currentPage);
    });

    async function loadUsers(page) {
        try {
            const skip = (page - 1) * usersPerPage;
            const response = await fetch(`/users/?skip=${skip}&limit=${usersPerPage}`);

            if (!response.ok) {
                throw new Error('Ошибка при загрузке данных');
            }

            const users = await response.json();

            if (users.length > 0) {
                totalUsers = users.length === usersPerPage ? skip + usersPerPage + 1 : skip + users.length;
            } else {
                totalUsers = skip;
            }

            renderUsers(users);
            updatePaginationControls();
        } catch (error) {
            console.error('Error:', error);
            usersTableBody.innerHTML = `<tr><td colspan="8" style="text-align: center;">Ошибка загрузки данных: ${error.message}</td></tr>`;
        }
    }

    function renderUsers(users) {
        usersTableBody.innerHTML = '';

        if (users.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="9" style="text-align: center;">Нет данных о пользователях</td>`;
            usersTableBody.appendChild(row);
            return;
        }

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td><img src="${user.picture}" alt="User Photo" class="user-photo"></td>
                <td>${user.first_name}</td>
                <td>${user.last_name}</td>
                <td>${user.gender === 'male' ? 'Мужской' : 'Женский'}</td>
                <td><a href="mailto:${user.email}">${user.email}</a></td>
                <td><a href="tel:${user.phone_number}">${user.phone_number}</a></td>
                <td>${user.city}, ${user.country}<br><small>${user.street}</small></td>
                <td><a href="/user_id/${user.id}" class="view-btn">Просмотр</a></td>
            `;
            usersTableBody.appendChild(row);
        });
    }

    function updatePaginationControls() {
        pageInfo.textContent = `Страница ${currentPage}`;
        prevPageBtn.disabled = currentPage <= 1;
        nextPageBtn.disabled = usersTableBody.querySelector('tr td[colspan="8"]') !== null ||
                              (usersTableBody.children.length > 0 &&
                               usersTableBody.children.length < usersPerPage);
    }
});