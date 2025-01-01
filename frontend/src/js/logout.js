addEventListener("DOMContentLoaded", async function () {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	async function logout() {
		try {
			const response = await fetch(`${baseUrl}/api/user/logout`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
			});

			if (response.status === 400) {
				throw new Error("Ungültige Anfrage");
			}
			if (response.status === 401) {
				throw new Error("Ungültiger Token");
			}
		} catch (error) {
			console.error(error);
		}
	}
	await logout();

  deleteCookie("access_token");
  deleteCookie("csrf_token");

	window.location.href = "/";
});

function deleteCookie(cookieName) {
  document.cookie = `${cookieName}=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT;`;
}