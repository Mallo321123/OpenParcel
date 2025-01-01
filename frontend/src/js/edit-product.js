addEventListener("DOMContentLoaded", async function () {
	const inputName = document.getElementById("name");
	const inputComment = document.getElementById("comment");
	const inputBuildTime = document.getElementById("buildTime");
	const choseDifficulty = document.getElementById("difficulty");

	inputName.addEventListener("input", function () {});
	inputComment.addEventListener("input", function () {});
	inputBuildTime.addEventListener("input", function () {});
	choseDifficulty.addEventListener("input", function () {});

	const product = await getProduct(id);
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

async function saveOrder(product) {
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

			saveOrder(product);
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