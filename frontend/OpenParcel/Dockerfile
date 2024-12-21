# Build-Phase mit einer neueren Node.js-Version
FROM node:18-alpine AS build

# Arbeitsverzeichnis erstellen
WORKDIR /usr/src/app

# Package-Dateien kopieren und Abhängigkeiten installieren
COPY package.json package-lock.json ./
RUN npm install

# Projektdateien kopieren und den Produktions-Build erstellen
COPY . .
RUN npm run build

# Serve-Phase
FROM nginx:stable-alpine

# Build-Ergebnis in das Nginx-Verzeichnis kopieren
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

# Exponiere den Port für Nginx
EXPOSE 80

# Nginx starten
CMD ["nginx", "-g", "daemon off;"]