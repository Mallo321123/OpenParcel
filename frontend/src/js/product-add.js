addEventListener("DOMContentLoaded", async function () {
    document.getElementById("name").value = "";
    document.getElementById("comment").value = "";
    document.getElementById("buildTime").value = "";

	const buttonSave = document.getElementById("saveButton");
	const buttonAddGroup = document.getElementById("addGroupButton");

	buttonAddGroup.addEventListener("click", async function () {
		const inputElement = document.getElementById("GroupName");
		const group = inputElement.value;

        inputElement.value = "";

        product.customerGroups.push(group);
        buildCustomerGroupList(product);
	});

	buttonSave.addEventListener("click", async function () {
		product.name = document.getElementById("name").value;
		product.comment = document.getElementById("comment").value;
		product.buildTime = document.getElementById("buildTime").value;
		product.difficulty = parseInt(document.getElementById("difficulty").value);

        const response = await saveProduct(product);

        if (response) {
            window.location.href = "product-add.html";
        }
	});
});

product = {
	name: "",
	comment: "",
	buildTime: "",
	difficulty: "",
    customerGroups: [],
};

async function saveProduct(product) {
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.split("/").slice(0, 3).join("/");
    const csrfToken = getCookie("csrf_token");

    const response = await fetch(`${baseUrl}/api/products`, {
        method: "POST",
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
    throw new Error("Unbekannter Fehler beim Speichern der Daten");
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
