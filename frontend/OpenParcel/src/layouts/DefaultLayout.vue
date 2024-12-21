<template>
    <div class="default-layout">
      <header>Header Navigation</header>
      <main>
        <slot />
      </main>
    </div>
  </template>
  
  <style scoped>
  .default-layout {
    display: flex;
    flex-direction: column;
  }
  main {
    flex: 1;
    padding: 20px;
  }
  </style>
  