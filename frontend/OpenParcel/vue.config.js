module.exports = {
    pages: {
      index: {
        entry: 'src/main.js', // Haupt-JavaScript für die Startseite
        template: 'public/index.html',
        filename: 'index.html',
      },
      dashboard: {
        entry: 'src/dashboard.js', // JavaScript für die Dashboard-Seite
        template: 'public/dashboard.html',
        filename: 'dashboard.html',
      },
      login: {
        entry: 'src/login.js', // JavaScript für die About-Seite
        template: 'public/about.html',
        filename: 'about.html',
      },
    },
  };