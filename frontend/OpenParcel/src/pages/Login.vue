<template>
  <div class="login">
    <div class="card">
      <div class="loader">
        <div class="text">Versendet...</div>
        <div class="words">
          <span class="word">LEDs</span>
          <span class="word">Lötkolben</span>
          <span class="word">Einhörner</span>
          <span class="word">Schalter</span>
          <span class="word">Platinen</span>
        </div>
      </div>
    </div>
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
          <svg
            stroke="currentColor"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
              stroke-width="2"
              stroke-linejoin="round"
              stroke-linecap="round"
            ></path>
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
        <span @click="togglePasswordVisibility" style="cursor: pointer">
          <svg
            :stroke="passwordVisible ? '#3498db' : 'currentColor'"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              :d="
                passwordVisible
                  ? 'M12 5C7.23 5 3.27 7.44 2 11a9.02 9.02 0 0 0 0 2c1.27 3.56 5.23 6 10 6 4.77 0 8.73-2.44 10-6a9.02 9.02 0 0 0 0-2c-1.27-3.56-5.23-6-10-6z'
                  : 'M15 12a3 3 0 11-6 0 3 3 0 016 0z'
              "
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

<script src="../js/login.js"></script>
<style scoped src="../styles/login.css"></style>
