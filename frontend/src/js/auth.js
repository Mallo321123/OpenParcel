document.addEventListener("DOMContentLoaded", async function () {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	try {
		const token = getCookie("access_token");
	} catch (error) {
		window.location.href = "/login.html";
    return;
	}

	const isValid = await valid_token();

	if (!isValid) {
		deleteCookie("access_token");
		window.location.href = "/login.html";
	}

	async function valid_token() {
		try {
			const response = await fetch(`${baseUrl}/api/token`, {
				method: "GET",
				credentials: "include",
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

	function getCookie(name) {
		const value = `; ${document.cookie}`;
		const parts = value.split(`; ${name}=`);
		if (parts.length === 2) {
			return parts.pop().split(";").shift();
		}
		return null;
	}

	function deleteCookie(name) {
		document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
	}
});
