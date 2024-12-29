addEventListener("DOMContentLoaded", async function () {
	const token =
		localStorage.getItem("token") || sessionStorage.getItem("token");
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const minPasswordInput = document.getElementById("min-password-length");

	async function getSettings() {
		const response = await fetch(`${baseUrl}/api/settings`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
		});

		if (response.status === 200) {
			return await response.json();
		}
		if (response.status === 400) {
			throw new Error("Ungültige Anfrage");
		}
		if (response.status === 401) {
			throw new Error("Ungültiger Token");
		}
		throw new Error("Unbekannter Fehler beim Abrufen der Daten");
	}

	async function putSettings(data) {
		const response = await fetch(`${baseUrl}/api/settings`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify(data),
		});
		if (response.status === 200) {
			return true;
		}
		if (response.status === 400) {
			throw new Error("Ungültige Anfrage");
		}
		if (response.status === 401) {
			throw new Error("Ungültiger Token");
		}
	}

	async function updateSettings(data) {
		try {
			minPasswordInput.value = data.minPasswordLength;
		} catch (error) {
			console.error(error);
		}
	}

	minPasswordInput.addEventListener("change", async function () {
		const newValue = parseInt(minPasswordInput.value);
		try {
			await putSettings({ minPasswordLength: newValue });
		} catch (error) {
			console.error("Fehler beim Senden des Werts ans Backend: ", error);
		}
	});

	const backend_settings = await getSettings();
	updateSettings(backend_settings);
});
