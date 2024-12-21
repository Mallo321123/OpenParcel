<template>
  <div class="login">
    <form class="form" @submit.prevent="login">
      <p class="form-title">Login</p>
      <div class="input-container">
        <input 
          placeholder="Nutzername" 
          type="text" 
          v-model="username" 
          :maxlength="15"
          pattern="^[0-9a-zA-Z]{1,15}$" 
          required 
        />
        <span>
          <svg stroke="currentColor" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"></path>
          </svg>
        </span>
      </div>
      <div class="input-container">
        <input 
          placeholder="Passwort" 
          :type="passwordVisible ? 'text' : 'password'" 
          v-model="password" 
          :maxlength="255" 
          required 
        />
        <span @click="togglePasswordVisibility" style="cursor: pointer;">
          <svg 
            :stroke="passwordVisible ? '#3498db' : 'currentColor'" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
          >
            <path 
              :d="passwordVisible 
                ? 'M12 5C7.23 5 3.27 7.44 2 11a9.02 9.02 0 0 0 0 2c1.27 3.56 5.23 6 10 6 4.77 0 8.73-2.44 10-6a9.02 9.02 0 0 0 0-2c-1.27-3.56-5.23-6-10-6z' 
                : 'M15 12a3 3 0 11-6 0 3 3 0 016 0z'" 
              stroke-width="2" 
              stroke-linejoin="round" 
              stroke-linecap="round"
            ></path>
          </svg>
        </span>
      </div>
      <button class="submit" type="submit">Einloggen</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      passwordVisible: false,
    };
  },
  methods: {
    async login() {
      // Überprüfen des Benutzernamens vor dem Absenden
      if (!/^[0-9a-zA-Z]{1,15}$/.test(this.username)) {
        alert("Benutzername darf nur Kleinbuchstaben und Zahlen enthalten und maximal 15 Zeichen lang sein.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8080/api/user/login", {
          method: "POST",
          headers: { 
            "Content-Type": "application/json" 
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        // Fehlerbehandlung
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error("Ungültige Anmeldedaten");
          }
          if (response.status === 429) {
            throw new Error("Zu viele Anfragen, bitte versuche es später erneut.");
          }
          throw new Error("Login fehlgeschlagen");
        }

        // Antwort im Erfolgsfall
        const data = await response.json();

        if (data.success) {
          localStorage.setItem("token", data.token);
          this.$router.push("/dashboard");
        } else {
          throw new Error(data.message || "Unbekannter Fehler");
        }
      } catch (err) {
        alert(err.message);
      }
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
  },
};
</script>
  
<style scoped>
  .login {
    max-width: 400px;
    margin: 0 auto;
    padding: 10%;
    text-align: center;
    border: 0px solid #ddd;
    border-radius: 8px;
  }
.form {
  background-color: #fff;
  display: block;
  padding: 1rem;
  max-width: 365px;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.form-title {
  font-size: 1.8rem;
  line-height: 1.75rem;
  font-weight: 600;
  text-align: center;
  color: #000;
}

.input-container {
  position: relative;
}

.input-container input, .form button {
  outline: none;
  border: 1px solid #e5e7eb;
  margin: 8px 0;
}

.input-container input {
  background-color: #fff;
  padding: 1rem;
  padding-right: 3rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  width: 300px;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.input-container span {
  display: grid;
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  padding-left: 1rem;
  padding-right: 1rem;
  place-content: center;
}

.input-container span svg {
  color: #9CA3AF;
  width: 1rem;
  height: 1rem;
}

.submit {
  display: block;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  padding-left: 1.25rem;
  padding-right: 1.25rem;
  background-color: #4F46E5;
  color: #ffffff;
  font-size: 0.875rem;
  line-height: 1.25rem;
  font-weight: 500;
  width: 100%;
  border-radius: 0.5rem;
  text-transform: uppercase;
}
</style>
  