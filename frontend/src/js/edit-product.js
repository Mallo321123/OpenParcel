addEventListener("DOMContentLoaded", async function () {
	const inputName = document.getElementById("name");
	const inputComment = document.getElementById("comment");
	const inputBuildTime = document.getElementById("buildTime");
	const choseDifficulty = document.getElementById("difficulty");
	const buttonAddGroup = document.getElementById("addGroupButton");
	const buttonDeleteProduct = document.getElementById("deleteProductButton");

	const product = await getProduct(id);

	buttonDeleteProduct.addEventListener("click", async function () {
		const success = await deleteProduct(id);
		if (success) {
			window.location.href = "products.html";
		} else {
			throw new Error("Produkt konnte nicht gelöscht werden");
		}
	});

	inputName.addEventListener("change", function () {
		product.name = inputName.value;

		delete product.buildTime;
		delete product.comment;
		delete product.customerGroups;
		delete product.difficulty;

		saveProduct(product);
	});

	inputComment.addEventListener("change", function () {
		product.comment = inputComment.value;

		delete product.buildTime;
		delete product.name;
		delete product.customerGroups;
		delete product.difficulty;

		saveProduct(product);
	});

	inputBuildTime.addEventListener("change", function () {
		product.buildTime = inputBuildTime.value;

		delete product.comment;
		delete product.name;
		delete product.customerGroups;
		delete product.difficulty;

		saveProduct(product);
	});

	choseDifficulty.addEventListener("change", function () {
		product.difficulty = parseInt(choseDifficulty.value);

		delete product.buildTime;
		delete product.comment;
		delete product.name;
		delete product.customerGroups;

		saveProduct(product);
	});

	buttonAddGroup.addEventListener("click", async function () {
		const inputElement = document.getElementById("GroupName");
		const group = inputElement.value;

		const product = await getProduct(id);
		product.customerGroups.push(group);

		delete product.buildTime;
		delete product.comment;
		delete product.difficulty;
		delete product.name;

		const success = await saveProduct(product);
		if (success) {
			buildCustomerGroupList(product);
			inputElement.value = "";
		}
	});

	buildCustomerGroupList(product);
	inputName.value = product.name;
	inputComment.value = product.comment;
	inputBuildTime.value = product.buildTime;
	choseDifficulty.value = product.difficulty;
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

async function deleteProduct(id) {
	const csrfToken = getCookie("csrf_token");

	const response = await fetch(`${baseUrl}/api/products?id=${id}`, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json",
			"X-CSRF-Token": csrfToken,
		},
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

async function saveProduct(product) {
	delete product.id;
	const csrfToken = getCookie("csrf_token");

	const response = await fetch(`${baseUrl}/api/products?id=${id}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
			"X-CSRF-Token": csrfToken,
		},
		body: JSON.stringify(product),
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

function buildCustomerGroupList(product) {
	const customerGroupListElement =
		document.getElementById("customerGroupsList");

	customerGroupListElement.innerHTML = "";

	product.customerGroups.forEach((group, index) => {
		const listItem = document.createElement("li");
		listItem.classList.add("customer-group-item");

		const groupLink = document.createElement("a");
		// Implement Maybe Later
		//groupLink.href = `view-group.html?group=${encodeURIComponent(group)}`;
		groupLink.textContent = group;

		const deleteButton = document.createElement("button");
		deleteButton.textContent = "❌";
		deleteButton.classList.add("delete-button");
		deleteButton.onclick = () => {
			product.customerGroups.splice(index, 1);
			listItem.remove();

			delete product.buildTime;
			delete product.comment;
			delete product.difficulty;
			delete product.name;

			saveProduct(product);
		};

		listItem.appendChild(deleteButton);
		listItem.appendChild(groupLink);

		customerGroupListElement.appendChild(listItem);
	});
}

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) {
		return parts.pop().split(";").shift();
	}
	return null;
}
