addEventListener("DOMContentLoaded", async function () {
	const currentUrl = window.location.href;
	const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

	const orderList = document.querySelector(".order-list");
	const orderLimitSelector = document.getElementById("order-limit");
	const loading = document.getElementById("loading");

	const links = document.querySelectorAll(".dashboard-card a");

	links.forEach((link) => {
		link.addEventListener("click", (event) => {
			const clickedCard = event.currentTarget;
			const cardTitle = clickedCard.querySelector(".stat-title").textContent;

			if (cardTitle === "Abgeschlossen") {
				key = "closed";
			} else if (cardTitle === "Wartend") {
				key = "hold";
			} else if (cardTitle === "Offen") {
				key = "open";
			} else {
				key = null;
			}

			this.localStorage.setItem("search-state", key);
		});
	});

	async function getDashboardData() {
		const response = await fetch(`${baseUrl}/api/dashboard`, {
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

	async function getOrders(page) {
		limit = localStorage.getItem("item-limit") || 10;
		const response = await fetch(
			`${baseUrl}/api/orders?limit=${limit}&page=${page}`,
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

	function updateDashboard(data) {
		const statTitles = document.querySelectorAll(".stat-title");

		statTitles.forEach((title) => {
			const statValue = title.nextElementSibling; // Das entsprechende .stat-value finden
			if (title.textContent.trim() === "Abgeschlossen") {
				statValue.textContent = data.done;
			} else if (title.textContent.trim() === "Wartend") {
				statValue.textContent = data.hold;
			} else if (title.textContent.trim() === "Lichter") {
				statValue.textContent = data.lights;
			} else if (title.textContent.trim() === "Mapper") {
				statValue.textContent = data.mappers;
			} else if (title.textContent.trim() === "Offen") {
				statValue.textContent = data.open;
			} else if (title.textContent.trim() === "Produkte") {
				statValue.textContent = data.products;
			}
		});
	}

	async function updateOrderList(page = 0) {
		loading.style.display = "flex";
		orderList.style.display = "none";

		const orders = await getOrders(page);

		limit = localStorage.getItem("item-limit") || 10;

		orderList.innerHTML = "";

		orders.items.forEach((order) => {
			const orderItem = document.createElement("div");

			let stateClass = "";
			switch (order.state) {
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

			orderItem.innerHTML = `
                <div class="order-row">
                    <span><strong>#${order.id}</strong> - ${order.customer}</span>
                    <text>${dateAdded}</text>
                    <a href="/edit-order.html?id=${encodeURIComponent(order.id)}" class="edit-link" title="Bearbeiten">
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
		orderList.style.display = "block"; // Bestell-Liste anzeigen
	}

	orderLimitSelector.addEventListener("change", function () {
		currentLimit = parseInt(this.value, 10);
		localStorage.setItem("item-limit", currentLimit);
		updateOrderList();
	});

	data = await getDashboardData();
	updateDashboard(data);

	updateOrderList();
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(";").shift();
    }
    return null;
  }