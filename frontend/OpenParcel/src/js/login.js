export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      passwordVisible: false,
    }
  },
  methods: {
    async login() {
      // Überprüfen des Benutzernamens vor dem Absenden
      if (!/^[0-9a-zA-Z]{1,15}$/.test(this.username)) {
        alert(
          'Benutzername darf nur Kleinbuchstaben und Zahlen enthalten und maximal 15 Zeichen lang sein.',
        )
        return
      }

      try {
        const response = await fetch('http://localhost:8080/api/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        })

        // Fehlerbehandlung
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Ungültige Anmeldedaten')
          }
          if (response.status === 429) {
            throw new Error('Zu viele Anfragen, bitte versuche es später erneut.')
          }
          throw new Error('Login fehlgeschlagen')
        }

        // Antwort im Erfolgsfall
        const data = await response.json()

        if (data.success) {
          localStorage.setItem('token', data.token)
          this.$router.push('/dashboard')
        } else {
          throw new Error(data.message || 'Unbekannter Fehler')
        }
      } catch (err) {
        alert(err.message)
      }
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible
    },
  },
}
