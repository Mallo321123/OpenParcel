document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById('loginForm');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const passwordVisibilityToggle = document.getElementById('passwordVisibilityToggle');
  const alertMessage = document.getElementById('alertMessage');

  // Dynamische API-URL basierend auf der aktuellen URL
  const currentUrl = window.location.href; // Aktuelle URL der Seite
  const baseUrl = currentUrl.split('/').slice(0, 3).join('/'); // Basis-URL (Protokoll + Domain)
  const apiUrl = `${baseUrl}/api/user/login`; // API-URL dynamisch zusammenbauen

  // Login-Logik
  async function login(username, password) {
    // Überprüfen des Benutzernamens
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

      // Fehlerbehandlung
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Ungültige Anmeldedaten');
        }
        if (response.status === 429) {
          throw new Error('Zu viele Anfragen, bitte versuche es später erneut.');
        }
        throw new Error('Login fehlgeschlagen');
      }

      // Antwort im Erfolgsfall
      const data = await response.json();

      if (data.success) {
        localStorage.setItem('token', data.token);
        window.location.href = '/dashboard'; // Weiterleitung nach dem erfolgreichen Login
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

  // Passwortsichtbarkeit umschalten
  function togglePasswordVisibility() {
    const inputType = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = inputType;
    // Ändern des Icons je nach Sichtbarkeit
    const icon = passwordInput.type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    passwordVisibilityToggle.innerHTML = `<i class="${icon}"></i>`;
  }

  // Formular-Submit und Login ausführen
  loginForm.addEventListener('submit', function (event) {
    event.preventDefault();
    login(usernameInput.value, passwordInput.value);
  });

  // Passwort-Sichtbarkeit umschalten, wenn auf das Icon geklickt wird
  if (passwordVisibilityToggle) {
    passwordVisibilityToggle.addEventListener('click', togglePasswordVisibility);
  }
});
