addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("token") || sessionStorage.getItem("token");
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.split('/').slice(0, 3).join('/');

    const orderList = document.querySelector('.order-list');
    const orderLimitSelector = document.getElementById('order-limit');
    

    async function getDashboardData() {
        const response = await fetch(`${baseUrl}/api/dashboard`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${token}`
            },
        });

        if (response.status === 200) {
            return await response.json();
        }
        if (response.status === 400) {
            throw new Error('Ungültige Anfrage');
        }
        if (response.status === 401) {
            throw new Error('Ungültiger Token');
        }
        throw new Error('Unbekannter Fehler beim Abrufen der Daten');
    }

    async function getOrders(limit, page) {
        const response = await fetch(`${baseUrl}/api/orders?limit=${limit}&page=${page}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${token}`
            },
        });

        if (response.status === 200) {
            return await response.json();
        }
        if (response.status === 400) {
            throw new Error('Ungültige Anfrage');
        }
        if (response.status === 401) {
            throw new Error('Ungültiger Token');
        }
        throw new Error('Unbekannter Fehler beim Abrufen der Daten');
    }

    function updateDashboard(data) {
        const statTitles = document.querySelectorAll('.stat-title');
    
        statTitles.forEach(title => {
            const statValue = title.nextElementSibling; // Das entsprechende .stat-value finden
            if (title.textContent.trim() === "Abgeschlossen") {
                statValue.textContent = data.done;
            } else if (title.textContent.trim() === "Wartend") {
                statValue.textContent = data.hold;
            } else if (title.textContent.trim() === "Lichter") {
                statValue.textContent = data.lights;
            } else if (title.textContent.trim() === "Mappers") {
                statValue.textContent = data.mappers;
            } else if (title.textContent.trim() === "Offen") {
                statValue.textContent = data.open;
            } else if (title.textContent.trim() === "Produkte") {
                statValue.textContent = data.products;
            }
        });
    }

    async function updateOrderList(limit, page = 0) {
        const orders = await getOrders(limit, page);

        orderList.innerHTML = "";
        const visibleOrders = orders.slice(0, limit);

        visibleOrders.forEach(order => {
            const orderItem = document.createElement('div');
            
            let stateClass = '';
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

            orderItem.classList.add('order-item', stateClass);

            const dateAdded = new Date(order.dateAdd).toLocaleString();

            orderItem.innerHTML = `
                <h3>Bestellung #${order.id}</h3>
                <p><strong>Kunde:</strong> ${order.customer}</p>
                <p><strong>Datum:</strong> ${dateAdded}</p>
                <p><strong>Produkte:</strong> ${order.products.join(', ')}</p>
            `;

            orderList.appendChild(orderItem);
        });
    }

    orderLimitSelector.addEventListener('change', function () {
        currentLimit = parseInt(this.value, 10);
        updateOrderList(currentLimit);
    });

    data = await getDashboardData();
    updateDashboard(data);

    updateOrderList(parseInt(orderLimitSelector.value, 10));
});