// This script is everything but efficient, but it works, so I am happy with it (for now)

addEventListener("DOMContentLoaded", async function () {
	const urlParams = new URLSearchParams(window.location.search);
	const id = urlParams.get("id");
	const order = await getOrderData(id);

	const textCustomer = document.getElementById("customer");
	const textComment = document.getElementById("comment");
	const dateAdd = document.getElementById("addDate");
	const closeDate = document.getElementById("closeDate");
	const textShipment = document.getElementById("shipment");

	const deleteButton = document.getElementById("deleteOrderButton");

	deleteButton.addEventListener("click", () => {
		deleteOrder(id).then(() => {
			window.location.href = "orders.html";
		});
	});

	textCustomer.addEventListener("change", function () {
		textChange();
	});

	textComment.addEventListener("change", function () {
		textChange();
	});

	dateAdd.addEventListener("change", function () {
		textChange();
	});

	closeDate.addEventListener("change", function () {
		textChange();
	});

	textShipment.addEventListener("change", function () {
		textChange();
	});

	document
		.getElementById("addProductButton")
		.addEventListener("click", addProductToList);

	if (order.dateClosed == "-") {
		var dateClosed = "-";
	} else {
		var dateClosed = order.dateClosed;
	}

	document.getElementById("order-id").textContent = id;

	document.getElementById("comment").value = order.comment;
	document.getElementById("customer").value = order.customer;
	document.getElementById("addDate").value = formatDateForInput(order.dateAdd);
	document.getElementById("closeDate").value = formatDateForInput(dateClosed);
	document.getElementById("shipment").value = order.shipmentType;
	document.getElementById("state").value = order.state;

	buildProductList(order);
});

async function getOrderData(id) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(`${baseUrl}/api/orders/info?id=${id}`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json"
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

function formatDateForInput(isoDate) {
	const date = new Date(isoDate);
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, "0");
	const day = String(date.getDate()).padStart(2, "0");
	const hours = String(date.getHours()).padStart(2, "0");
	const minutes = String(date.getMinutes()).padStart(2, "0");

	return `${year}-${month}-${day}T${hours}:${minutes}`;
}

async function getProductInfo(id) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(`${baseUrl}/api/products/info?id=${id}`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json"
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

async function deleteOrder(id) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(`${baseUrl}/api/orders?id=${id}`, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json"
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
	throw new Error("Unbekannter Fehler beim Abrufen der Daten");
}

function buildProductList(order) {
	const productListElement = document.getElementById("productList");

	// Leere die Produktliste
	productListElement.innerHTML = "";

	// Iteriere über die Produkte
	order.products.forEach(async (product, index) => {
		const listItem = document.createElement("li");
		listItem.classList.add("product-item");

		// Hole die Produktinformationen basierend auf der ID
		const productInfo = await getProductInfo(product.id);
		const productName = productInfo.name;

		// Erstelle den Link für das Produkt
		const productLink = document.createElement("a");
		productLink.href = `view-product.html?id=${encodeURIComponent(product.id)}`;
		productLink.textContent = `${productName} (x${product.count})`;

		// Erstelle den Löschen-Button
		const deleteButton = document.createElement("button");
		deleteButton.textContent = "❌";
		deleteButton.classList.add("delete-button");
		deleteButton.onclick = () => {
			// Entferne das Produkt aus der Liste
			order.products.splice(index, 1);
			listItem.remove();

			// Lösche nicht benötigte Eigenschaften, falls erforderlich
			delete order.comment;
			delete order.customer;
			delete order.dateAdd;
			delete order.dateClosed;
			delete order.shipmentType;
			delete order.state;

			// Speichere die geänderte Bestellung
			saveOrder(order);
		};

		// Füge die Elemente zur Liste hinzu
		listItem.appendChild(deleteButton);
		listItem.appendChild(productLink);

		productListElement.appendChild(listItem);
	});
}

// From here
async function getProducts(limit = 200, page = 0) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(
		`${baseUrl}/api/products?limit=${limit}&page=${page}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json"
			},
		}
	);
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

async function buildJsonBomb() {
	let mergedSections = [];
	let currentPage = 0;

	while (true) {
		const sections = await getProducts(200, currentPage);

		// Anhängen der Abschnitte an das Ergebnis
		mergedSections = mergedSections.concat(sections);

		// Wenn weniger als 199 Abschnitte zurückkommen, abbrechen
		if (sections.length < 199) {
			break;
		}

		// Seite erhöhen und erneut anfragen
		currentPage++;
	}

	return mergedSections;
}

function findBestMatchId(jsonData, inputName) {
	let bestMatch = { id: null, similarity: Infinity };

	jsonData.forEach((item) => {
		const similarity = levenshteinDistance(
			item.name.toLowerCase(),
			inputName.toLowerCase()
		);
		if (similarity < bestMatch.similarity) {
			bestMatch = { id: item.id, similarity: similarity };
		}
	});

	return bestMatch.id;
}

function levenshteinDistance(a, b) {
	const matrix = Array.from({ length: a.length + 1 }, (_, i) =>
		Array(b.length + 1).fill(0)
	);

	for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
	for (let j = 0; j <= b.length; j++) matrix[0][j] = j;

	for (let i = 1; i <= a.length; i++) {
		for (let j = 1; j <= b.length; j++) {
			const cost = a[i - 1] === b[j - 1] ? 0 : 1;
			matrix[i][j] = Math.min(
				matrix[i - 1][j] + 1, // Deletion
				matrix[i][j - 1] + 1, // Insertion
				matrix[i - 1][j - 1] + cost // Substitution
			);
		}
	}

	return matrix[a.length][b.length];
}
// To here, the code is a bit shit, and could be a bit more optimized using a special API endpoint, but I am a bit to tired to do this right now, so for now its a bit shitty

async function saveOrder(order) {
	const urlParams = new URLSearchParams(window.location.search);
	const id = urlParams.get("id");

	delete order.id;

	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(`${baseUrl}/api/orders?id=${id}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(order),
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

async function addProductToList() {
	const productInput = document.getElementById("productName");
	const productCountInput = document.getElementById("productCount");

	const productName = productInput.value.trim();
	const productCount = parseInt(productCountInput.value, 10);

	const urlParams = new URLSearchParams(window.location.search);
	const id = urlParams.get("id");

	const order = await getOrderData(id);

	if (productName && productCount > 0) {
		const productId = findBestMatchId(await buildJsonBomb(), productName);

		const existingProduct = order.products.find(
			(product) => product.id === productId
		);

		if (existingProduct) {
			existingProduct.count += productCount;
		} else {
			order.products.push({ id: productId, count: productCount });
		}

		productInput.value = "";
		productCountInput.value = "1";

		buildProductList(order);

		delete order.comment;
		delete order.customer;
		delete order.dateAdd;
		delete order.dateClosed;
		delete order.shipmentType;
		delete order.state;

		saveOrder(order);
	} else {
		alert("Bitte geben Sie einen gültigen Produktnamen und eine Anzahl ein.");
	}
}

async function textChange() {
	const textCustomer = document.getElementById("customer").value;
	const textComment = document.getElementById("comment").value;
	const dateAdd = document.getElementById("addDate").value;
	const closeDate = document.getElementById("closeDate").value;
	const textShipment = document.getElementById("shipment").value;

	const order = {};

	order.customer = textCustomer;
	order.comment = textComment;
	order.dateAdd = dateAdd;
	order.dateClosed = closeDate;
	order.shipmentType = textShipment;

	saveOrder(order);
}

async function handleInputChange(event) {
	const value = document.getElementById("state").value;

	const order = {};
	order.state = value;
	saveOrder(order);
}
