addEventListener("DOMContentLoaded", async function () {
	const product = await getProduct(id);
    
    document.getElementById("name").textContent = product.name;
    document.getElementById("comment").textContent = product.comment;
    document.getElementById("buildTime").textContent = product.buildTime;
    document.getElementById("difficulty").textContent = product.difficulty;

	buildCustomerGroupList(product);
});

const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get("id");
const currentUrl = window.location.href;
const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

async function getProduct(id) {
	const response = await fetch(`${baseUrl}/api/products/info?id=${id}`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
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

function buildCustomerGroupList(product) {
	const customerGroupListElement =
		document.getElementById("customerGroupsList");

	customerGroupListElement.innerHTML = "";

	product.customerGroups.forEach((group, index) => {
		const listItem = document.createElement("li");
		listItem.classList.add("customer-group-item");

		const groupLink = document.createElement("a");
		// Implement Maybe Later
		//groupLink.href = `view-group.html?group=${encodeURIComponent(group.id)}`;
		groupLink.textContent = group;

		listItem.appendChild(groupLink);

		customerGroupListElement.appendChild(listItem);
	});
}