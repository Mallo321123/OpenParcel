document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById('loginForm');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const passwordVisibilityToggle = document.getElementById('passwordVisibilityToggle');
  const alertMessage = document.getElementById('alertMessage');

  const currentUrl = window.location.href;
  const baseUrl = currentUrl.split('/').slice(0, 3).join('/');
  const apiUrl = `${baseUrl}/api/user/login`;

  const token = localStorage.getItem("token") || sessionStorage.getItem("token");
  // check for existing token
  if (token) {
    window.location.href = "/dashboard.html";
  }

  // Login-Logic
  async function login(username, password) {
    if (!/^[0-9a-zA-Z]{1,15}$/.test(username)) {
      if (alertMessage) {
        alertMessage.textContent = 'Benutzername darf nur Kleinbuchstaben und Zahlen enthalten und maximal 15 Zeichen lang sein.';
        alertMessage.style.display = 'block';
      }
      return;
    }

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      // Error Handling
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Ungültige Anmeldedaten');
        }
        if (response.status === 400) {
          throw new Error('Ungültige Anfrage');
        }
        if (response.status === 429) {
          throw new Error('Zu viele Anfragen, bitte versuche es später erneut.');
        }
        throw new Error('Sonstiger Fehler beim Login');
      }

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('token', data.token);
        window.location.href = '/dashboard.html'; // Redirect to dashboard
      } else {
        throw new Error(data.message || 'Unbekannter Fehler');
      }
    } catch (err) {
      if (alertMessage) {
        alertMessage.textContent = err.message;
        alertMessage.style.display = 'block';
      }
    }
  }

  function togglePasswordVisibility() {
    const inputType = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = inputType;
    // Ändern des Icons je nach Sichtbarkeit
    const icon = passwordInput.type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    passwordVisibilityToggle.innerHTML = `<i class="${icon}"></i>`;
  }

  loginForm.addEventListener('submit', function (event) {
    event.preventDefault();
    login(usernameInput.value, passwordInput.value);
  });

  if (passwordVisibilityToggle) {
    passwordVisibilityToggle.addEventListener('click', togglePasswordVisibility);
  }
});
