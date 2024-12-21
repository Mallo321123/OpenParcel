<template>
  <div id="app">
    <!-- Open Parcel Logo in der oberen linken Ecke -->
    <div class="logo">
      OpenParcel
    </div>
    <!-- Hier wird die aktuelle Route gerendert -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
/* Body mit Margin und Grundschriftart */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

/* Positioniert das OpenParcel-Logo oben links */
.logo {
  position: fixed;
  top: 20px;
  left: 20px;
  padding: 10px 20px;
  background-color: #3498db; /* Open Parcel spezifische Farbe (blau) */
  color: white;
  font-size: 18px;
  font-weight: bold;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000; /* Damit das Logo immer oben bleibt */
}
</style>
