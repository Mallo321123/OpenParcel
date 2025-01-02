addEventListener("DOMContentLoaded", async function () {
	const orderLimitSelector = document.getElementById("order-limit");
	const searchCustomer = document.getElementById("search-customer");
	const searchShipment = document.getElementById("search-shipmentType");

	async function handleSortClick(event) {
		const button = event.target;

		const sortField = button.getAttribute("data-field");
		const sortOrder = button.getAttribute("data-order");

		localStorage.setItem("sortField", sortField);
		localStorage.setItem("sortOrder", sortOrder);
		updateData();
	}

	orderLimitSelector.value = localStorage.getItem("item-limit") || 10;

	orderLimitSelector.addEventListener("change", function () {
		localStorage.setItem("item-limit", this.value);
		updateData();
	});

	searchCustomer.addEventListener("change", function () {
		updateData();
	});

	searchShipment.addEventListener("change", function () {
		updateData();
	});

	document.querySelectorAll(".sort-controls").forEach((button) => {
		button.addEventListener("click", handleSortClick);
	});

	const statusSelect = document.getElementById("search-state");
	if (localStorage.getItem("search-state") !== "null") {
		statusSelect.value = localStorage.getItem("search-state");
		this.localStorage.setItem("search-state", null);
	}

	await updateData();
	renderPagination();
});

const loading = document.getElementById("loading");
let totalOrders = 1;
let currentPage = 0;
let currentLimit = 10;

async function updateData() {
	const searchCustomer = document.getElementById("search-customer").value;
	const searchShipment = document.getElementById("search-shipmentType").value;
	const statusSelect = document.getElementById("search-state").value;

	const currentLimit = localStorage.getItem("item-limit") || 10;

	const sortField = localStorage.getItem("sortField");
	const sortOrder = localStorage.getItem("sortOrder");

	if (searchCustomer == "") {
		var customer = null;
	}
	if (searchShipment == "") {
		var shipment = null;
	}
	if (statusSelect == "") {
		var state = null;
	}

	const orders = await getOrdersSorted(
		currentLimit,
		currentPage,
		statusSelect,
		searchCustomer,
		searchShipment,
		sortField,
		sortOrder
	);

	totalOrders = await orders.totalItems;

	updateOrderList(await orders);
}

async function updateOrderList(orders) {
	const orderList = document.querySelector(".order-list");

	loading.style.display = "flex";
	orderList.style.display = "none";

	orderList.innerHTML = "";

	orders.items.forEach((order) => {
		const orderItem = document.createElement("div");

		let stateClass = "";
		switch (order.state) {
			case "":
				stateClass = "";
				break;
			case "open":
				stateClass = "open";
				break;
			case "closed":
				stateClass = "closed";
				break;
			case "hold":
				stateClass = "hold";
				break;
			case "working":
				stateClass = "working";
				break;
			default:
				stateClass = "";
		}

		orderItem.classList.add("order-item", stateClass);

		const dateAdded = new Date(order.dateAdd).toLocaleString();

		if (order.dateClosed == "-") {
			var dateClose = "-";
		} else {
			var dateClose = new Date(order.dateClosed).toLocaleString();
		}

		orderItem.innerHTML = `
            <div class="order-row">
                <span class="order-id-customer">
                    <strong>#${order.id}</strong> - ${order.customer}
                </span>
                <span class="order-date">${dateAdded}</span>
                <span class="shipment-type">${order.shipmentType}</span>
                <span class="close-date">${dateClose}</span>
                <a href="/edit-order.html?id=${encodeURIComponent(
									order.id
								)}" class="edit-link" title="Bearbeiten">
                    ✏️
                </a>
            </div>
        `;

		orderItem.addEventListener("click", function () {
			window.location.href = `/view-order.html?id=${encodeURIComponent(
				order.id
			)}`;
		});

		const editLink = orderItem.querySelector(".edit-link");
		editLink.addEventListener("click", function (event) {
			event.stopPropagation();
		});

		orderList.appendChild(orderItem);
	});

	loading.style.display = "none";
	orderList.style.display = "block";
}

async function getOrdersSorted(
	limit,
	page,
	state = null,
	customer = null,
	shipment = null,
	sortField = null,
	sortOrder = null
) {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const queryParams = new URLSearchParams({
		limit,
		page,
		state,
		shipment,
		customer,
		sort: sortField,
		order: sortOrder,
	});

	// what is this shit?
	queryParams.forEach((value, key) => {
		if (value === "null" || value === "") {
			queryParams.delete(key);
		}
	});
	queryParams.forEach((value, key) => {
		if (value === "null" || value === "") {
			queryParams.delete(key);
		}
	});
	queryParams.forEach((value, key) => {
		if (value === "null" || value === "") {
			queryParams.delete(key);
		}
	});
	queryParams.forEach((value, key) => {
		if (value === "null" || value === "") {
			queryParams.delete(key);
		}
	});

	const url = `${baseUrl}/api/orders/list?${queryParams.toString()}`;

	const response = await fetch(url, {
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

function handleInputChange() {
	updateData();
}

function renderPagination() {
	const pagination = document.getElementById("pagination");
	pagination.innerHTML = "";

	var totalPages =  Math.ceil(totalOrders / currentLimit);

	console.log("totalPages: ", totalPages, "totalOrders: ", totalOrders, "currentLimit: ", currentLimit);
  
	const prevButton = document.createElement("button");
	prevButton.textContent = "«";
	prevButton.disabled = currentPage === 0;
	prevButton.addEventListener("click", () => {
	  currentPage--;
	  updateData();
	  renderPagination();
	});
	pagination.appendChild(prevButton);
  
	// Seitenzahlen
	for (let i = 1; i <= totalPages; i++) {
	  const pageButton = document.createElement("button");
	  pageButton.textContent = i;
	  pageButton.classList.toggle("active", i-1 === currentPage);
	  pageButton.addEventListener("click", () => {
		currentPage = i-1;
		updateData();
		renderPagination();
	  });
	  pagination.appendChild(pageButton);
	}
  
	// Nächste Seite
	const nextButton = document.createElement("button");
	nextButton.textContent = "»";
	nextButton.disabled = currentPage === totalPages;
	nextButton.addEventListener("click", () => {
	  currentPage++;
	  updateData();
	  renderPagination();
	});
	pagination.appendChild(nextButton);
  }