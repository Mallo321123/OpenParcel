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

	orderLimitSelector.addEventListener("change", function () {
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

	updateData();
});

const loading = document.getElementById("loading");

async function updateData() {
	const searchCustomer = document.getElementById("search-customer").value;
	const searchShipment = document.getElementById("search-shipmentType").value;
	const statusSelect = document.getElementById("search-state").value;
	const currentLimit = parseInt(
		document.getElementById("order-limit").value,
		10
	);
	const currentPage = 0;

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

	updateOrderList(orders, currentLimit);
}

async function updateOrderList(orders, limit) {
	const orderList = document.querySelector(".order-list");

	loading.style.display = "flex";
	orderList.style.display = "none";

	orderList.innerHTML = "";
	const visibleOrders = orders.slice(0, limit);

	visibleOrders.forEach((order) => {
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
