addEventListener("DOMContentLoaded", async function () {
	const saveButton = document.getElementById("saveButton");

	document.getElementById("comment").value = "";
	document.getElementById("customer").value = "";
	document.getElementById("shipment").value = "";

	document
		.getElementById("addProductButton")
		.addEventListener("click", addProductToList);

	saveButton.addEventListener("click", async function () {
		saveOrder();
	});
});

// From here
async function getProducts(limit = 200, page = 0) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(
		`${baseUrl}/api/products?limit=${limit}&page=${page}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
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
		var sections = await getProducts(200, currentPage);
		sections = sections.items;


		mergedSections = mergedSections.concat(sections);

		if (sections.length < 199) {
			break;
		}

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

async function createOrder() {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const csrf_token = getCookie("csrf_token")

	const response = await fetch(`${baseUrl}/api/orders`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRF-Token": csrf_token,
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

let order = {
	products: [],
	comment: null,
	customer: null,
	shipmentType: null,
	state: null,
};

async function saveOrder() {
	const comment = document.getElementById("comment").value;
	const customer = document.getElementById("customer").value;
	const shipment = document.getElementById("shipment").value;
	const status = document.getElementById("state").value;

	order.comment = comment;
	order.customer = customer;
	order.shipmentType = shipment;
	order.state = status;

	createOrder()
		.then(() => {
			location.reload();
		})
		.catch((error) => {
			console.error("Fehler beim Speichern der Bestellung:", error);
		});
}

function buildProductList() {
	const productListElement = document.getElementById("productList");

	productListElement.innerHTML = "";

	order.products.forEach(async (product, index) => {
		const listItem = document.createElement("li");
		listItem.classList.add("product-item");

		const productInfo = await getProductInfo(product.id);
		const productName = productInfo.name;

		const productLink = document.createElement("a");
		productLink.href = `view-product.html?id=${encodeURIComponent(product.id)}`;
		productLink.textContent = `${productName} (x${product.count})`;

		const deleteButton = document.createElement("button");
		deleteButton.textContent = "❌";
		deleteButton.classList.add("delete-button");
		deleteButton.onclick = () => {
			order.products.splice(index, 1);
			listItem.remove();

			delete order.comment;
			delete order.customer;
			delete order.dateAdd;
			delete order.dateClosed;
			delete order.shipmentType;
			delete order.state;
		};

		listItem.appendChild(deleteButton);
		listItem.appendChild(productLink);

		productListElement.appendChild(listItem);
	});
}

async function addProductToList() {
	const productInput = document.getElementById("productName");
	const productCountInput = document.getElementById("productCount");

	const productName = productInput.value.trim();
	const productCount = parseInt(productCountInput.value, 10);

	if (productName && !isNaN(productCount) && productCount > 0) {
		try {
			const productId = await findBestMatchId(
				await buildJsonBomb(),
				productName
			);

			if (!productId) {
				alert("Produkt konnte nicht gefunden werden.");
				return;
			}

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

			buildProductList();
		} catch (error) {
			console.error("Fehler beim Hinzufügen des Produkts:", error);
		}
	} else {
		alert("Bitte geben Sie einen gültigen Produktnamen und eine Anzahl ein.");
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