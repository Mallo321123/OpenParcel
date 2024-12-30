addEventListener("DOMContentLoaded", async function () {
	const productLimitSelector = document.getElementById("product-limit");
	const searchName = document.getElementById("search-name");
	const searchDifficulty = document.getElementById("search-difficulty");

	searchDifficulty.value = "";
	searchName.value = "";

	productLimitSelector.addEventListener("change", async function () {
		productLimit = productLimitSelector.value;
		localStorage.setItem("itemLimit", productLimit);

		searchName.value = "";
		searchDifficulty.value = "";

		products = await getProducts(productLimit, 0);
		updateData(products);
	});

	document.querySelectorAll(".sort-controls").forEach((button) => {
		button.addEventListener("click", handleSortClick);
	});

	searchDifficulty.addEventListener("change", async function () {
		const difficulty = searchDifficulty.value;
		productLimit = localStorage.getItem("itemLimit") || 10;
		products = await searchProducts(productLimit, 0, "", difficulty);

		searchName.value = "";

		updateData(products);
	});

	searchName.addEventListener("change", async function () {
		const name = searchName.value;
		productLimit = localStorage.getItem("itemLimit") || 10;
		products = await searchProducts(productLimit, 0, name, "");

		searchDifficulty.value = "";
		updateData(products);
	});

	productLimit = localStorage.getItem("itemLimit") || 10;
	productLimitSelector.value = productLimit;
	products = await getProducts(productLimit, 0);
	updateData(products);
});
const loading = document.getElementById("loading");

async function getProducts(limit, page) {
	const token =
		localStorage.getItem("token") || sessionStorage.getItem("token");
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(
		`${baseUrl}/api/products?limit=${limit}&page=${page}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
		}
	);

	if (!response.ok) {
		console.error("Failed to fetch products");
		return [];
	}

	return await response.json();
}

async function getProductsSorted(limit, page, sortField, sortOrder) {
	const token =
		localStorage.getItem("token") || sessionStorage.getItem("token");
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(
		`${baseUrl}/api/products/list?limit=${limit}&page=${page}&sort=${sortField}&order=${sortOrder}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
		}
	);

	if (!response.ok) {
		console.error("Failed to fetch products");
		return [];
	}

	return await response.json();
}

async function searchProducts(limit, page, name, difficulty) {
	const token =
		localStorage.getItem("token") || sessionStorage.getItem("token");
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	let url = "";

	if (name === "" && difficulty !== "") {
		url = `${baseUrl}/api/products/list?limit=${limit}&page=${page}&difficulty=${difficulty}`;
	} else if (difficulty === "" && name !== "") {
		url = `${baseUrl}/api/products/list?limit=${limit}&page=${page}&name=${name}`;
	} else if (name === "" && difficulty === "") {
		return await getProducts(limit, page);
	} else {
		throw new Error("Invalid search parameters");
	}

	const response = await fetch(url, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});

	if (!response.ok) {
		console.error("Failed to fetch products");
		return [];
	}

	return await response.json();
}

async function updateData(products) {
	const productList = document.querySelector(".product-list");

	loading.style.display = "flex";
	productList.style.display = "none";

	productList.innerHTML = "";

	products.forEach((product) => {
		const productItem = document.createElement("div");
		productItem.classList.add("product-item");

		productItem.innerHTML = `
            <div class="product-row">
                <span class="product-name">${product.name}</span>
                <span class="product-difficulty">${product.difficulty}</span>
                <a href="/edit-product.html?id=${encodeURIComponent(
									product.id
								)}" class="edit-link" title="Bearbeiten">
                    ✏️
                </a>
            </div>
        `;

		productItem.addEventListener("click", function () {
			window.location.href = `/view-product.html?id=${encodeURIComponent(
				product.id
			)}`;
		});

		const editLink = productItem.querySelector(".edit-link");
		editLink.addEventListener("click", function (event) {
			event.stopPropagation();
		});

		productList.appendChild(productItem);
	});

	loading.style.display = "none";
	productList.style.display = "block";
}

async function handleSortClick(event) {
	const button = event.target;

	const sortField = button.getAttribute("data-field");
	const sortOrder = button.getAttribute("data-order");

	localStorage.setItem("productSortField", sortField);
	localStorage.setItem("productSortOrder", sortOrder);

	productLimit = localStorage.getItem("itemLimit") || 10;

	if (sortField === null || sortOrder === null) {
		products = await getProducts(productLimit, 0);
		updateData(products);
		return;
	}

	products = await getProductsSorted(productLimit, 0, sortField, sortOrder);
	updateData(products);
}
