addEventListener("DOMContentLoaded", async function () {
	const urlParams = new URLSearchParams(window.location.search);
	const id = urlParams.get("id");
	const order = await getOrderData(id);

	const dateAdded = new Date(order.dateAdd).toLocaleString();

	if (order.dateClosed == "-") {
		var dateClosed = "-";
	} else {
		var dateClosed = new Date(order.dateClosed).toLocaleString();
	}

	let stateClass = "";
	let text = "";
	switch (order.state) {
		case "open":
			stateClass = "open";
			text = "Offen";
			break;
		case "closed":
			stateClass = "closed";
			text = "Abgeschlossen";
			break;
		case "hold":
			stateClass = "hold";
			text = "Wartend";
			break;
		case "working":
			stateClass = "working";
			text = "In Bearbeitung";
			break;
		default:
			stateClass = "";
	}

	displayProducts(order);

	document.getElementById("order-id").textContent = order.id;
	document.getElementById("comment").textContent = order.comment;
	document.getElementById("customer").textContent = order.customer;
	document.getElementById("addDate").textContent = dateAdded;
	document.getElementById("closeDate").textContent = dateClosed;
	document.getElementById("shipment").textContent = order.shipmentType;
	document.getElementById("state").textContent = text;
	document.getElementById("state").className = "status " + stateClass;
});

async function getOrderData(id) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(`${baseUrl}/api/orders/info?id=${id}`, {
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

async function getProductInfo(id) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

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

async function displayProducts(order) {
	const productListElement = document.getElementById("productList");

	productListElement.innerHTML = "";

	order.products.forEach(async (product) => {
		const listItem = document.createElement("li");
		listItem.classList.add("product-item");

		const productInfo = await getProductInfo(product.id);
		const productName = productInfo.name;

		const productLink = document.createElement("a");
		productLink.href = `view-product.html?id=${encodeURIComponent(product.id)}`;
		productLink.textContent = `${productName} (x${product.count})`;

		listItem.appendChild(productLink);
		productListElement.appendChild(listItem);
	});
}
