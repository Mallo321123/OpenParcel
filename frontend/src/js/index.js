document.addEventListener("DOMContentLoaded", async function () {
	try {
		const token = getCookie("access_token");
	} catch (error) {
		window.location.href = "/login.html";
    return;
	}

	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");
  const token = getCookie("access_token");

	const isValid = await valid_token(token);

	if (isValid) {
		window.location.href = "/dashboard.html";
	} else {
		localStorage.removeItem("token");
		sessionStorage.removeItem("token");
		window.location.href = "/login.html";
	}

	async function valid_token(token) {
		try {
			const response = await fetch(`${baseUrl}/api/token`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			});

			if (response.status === 200) {
				return true;
			}
			if (response.status === 400) {
				throw new Error("Ungültige Anfrage");
			}
			if (response.status === 204) {
				return false;
			}
			throw new Error("Unerwarteter Statuscode");
		} catch (error) {
			console.error(error);
			return false;
		}
	}
});
