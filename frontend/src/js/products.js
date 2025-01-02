addEventListener("DOMContentLoaded", async function () {
	const currentLimitSelector = document.getElementById("product-limit");
	const searchName = document.getElementById("search-name");
	const searchDifficulty = document.getElementById("search-difficulty");

	searchDifficulty.value = "";
	searchName.value = "";

	currentLimitSelector.value = localStorage.getItem("item-limit") || 10;

	currentLimitSelector.addEventListener("change", async function () {
		currentLimit = currentLimitSelector.value;
		localStorage.setItem("item-limit", currentLimit);

		searchName.value = "";
		searchDifficulty.value = "";

		products = await getProducts(currentLimit, currentPage);
		totalProducts = products.total;
		updateData(products);
		renderPagination();
	});

	document.querySelectorAll(".sort-controls").forEach((button) => {
		button.addEventListener("click", handleSortClick);
	});

	searchDifficulty.addEventListener("change", async function () {
		difficulty = searchDifficulty.value;
		searchName = "";
		currentLimit = localStorage.getItem("item-limit") || 10;
		products = await searchProducts(currentLimit, currentPage, "", difficulty);

		searchName.value = "";
		totalProducts = products.total;

		updateData(products);
		renderPagination();
	});

	searchName.addEventListener("change", async function () {
		searchName = searchName.value;
		difficulty = "";
		currentLimit = localStorage.getItem("item-limit") || 10;
		products = await searchProducts(currentLimit, currentPage, searchName, "");

		searchDifficulty.value = "";
		totalProducts = products.total;
		updateData(products);
		renderPagination();
	});

	currentLimit = localStorage.getItem("item-limit") || 10;
	currentLimitSelector.value = currentLimit;
	products = await getProducts(currentLimit, 0);
	totalProducts = products.total;

	updateData(products);
	renderPagination();
});
const loading = document.getElementById("loading");
let totalProducts = 1;
let currentPage = 0;
let currentLimit = 10;
let difficulty = "";
let searchName = "";

async function getProducts(limit, page) {
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

	if (!response.ok) {
		console.error("Failed to fetch products");
		return [];
	}

	return await response.json();
}

async function getProductsSorted(limit, page, sortField, sortOrder) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const response = await fetch(
		`${baseUrl}/api/products/list?limit=${limit}&page=${page}&sort=${sortField}&order=${sortOrder}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
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

	products.items.forEach((product) => {
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
	document.getElementById("search-name").value = "";

	const button = event.target;

	const sortField = button.getAttribute("data-field");
	const sortOrder = button.getAttribute("data-order");

	localStorage.setItem("productSortField", sortField);
	localStorage.setItem("productSortOrder", sortOrder);

	currentLimit = localStorage.getItem("item-limit") || 10;

	if (sortField === null || sortOrder === null) {
		products = await getProducts(currentLimit, 0);
		updateData(products);
		return;
	}

	products = await getProductsSorted(currentLimit, 0, sortField, sortOrder);
	updateData(products);
}

async function renderPagination() {
	const pagination = document.getElementById("pagination");
	pagination.innerHTML = "";

	var totalPages = Math.ceil(totalProducts / currentLimit);

	const prevButton = document.createElement("button");
	prevButton.textContent = "«";
	prevButton.disabled = currentPage === 0;
	prevButton.addEventListener("click", async () => {
		currentPage--;
		products = await searchProducts(
			currentLimit,
			currentPage,
			searchName,
			difficulty
		);
		updateData(products);
		totalProducts = products.total;
		renderPagination();
	});
	pagination.appendChild(prevButton);

	for (let i = 1; i <= totalPages; i++) {
		const pageButton = document.createElement("button");
		pageButton.textContent = i;
		pageButton.classList.toggle("active", i - 1 === currentPage);
		pageButton.addEventListener("click", async () => {
			currentPage = i - 1;
			products = await searchProducts(
				currentLimit,
				currentPage,
				searchName,
				difficulty
			);
			updateData(products);
			totalProducts = products.total;
			renderPagination();
		});
		pagination.appendChild(pageButton);
	}

	const nextButton = document.createElement("button");
	nextButton.textContent = "»";
	nextButton.disabled = currentPage === totalPages;
	nextButton.addEventListener("click", async () => {
		currentPage++;
		products = await searchProducts(
			currentLimit,
			currentPage,
			searchName,
			difficulty
		);
		updateData(products);
		totalProducts = products.total;
		renderPagination();
	});
	pagination.appendChild(nextButton);
}
