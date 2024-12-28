addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("token") || sessionStorage.getItem("token");
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.split('/').slice(0, 3).join('/');

    const orderList = document.querySelector('.order-list');
    const orderLimitSelector = document.getElementById('order-limit');
    const loading = document.getElementById('loading');

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

    async function getSortedOrders(limit, page, field, direction) {
        const response = await fetch(`${baseUrl}/api/orders/list?limit=${limit}&page=${page}&sort=${field}&order=${direction}`, {
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

    async function updateOrderList(orders, limit) {
        loading.style.display = 'flex';
        orderList.style.display = 'none';

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
                    <a href="/edit-order?id=${encodeURIComponent(order.id)}" class="edit-link" title="Bearbeiten">
                        ✏️
                    </a>
                </div>
            `;

            orderItem.addEventListener('click', function () {
                window.location.href = `/view-order?id=${encodeURIComponent(order.id)}`;
            });

            const editLink = orderItem.querySelector('.edit-link');
            editLink.addEventListener('click', function (event) {
                event.stopPropagation();
            });

            orderList.appendChild(orderItem);
        });

        loading.style.display = 'none';
        orderList.style.display = 'block'; // Bestell-Liste anzeigen
    }

    async function handleSortClick(event) {
        const button = event.target;
    
        const sortField = button.getAttribute('data-field');
        const sortOrder = button.getAttribute('data-order');

        currentLimit = parseInt(orderLimitSelector.value, 10);
        const orders = await getSortedOrders(currentLimit, 0, sortField, sortOrder);
        updateOrderList(orders, currentLimit);
    }

    async function updateOnEvent(limit) {
        const orders = await getOrders(limit, 0);
        updateOrderList(orders, limit);
    }


    orderLimitSelector.addEventListener('change', function () {
        currentLimit = parseInt(this.value, 10);
        updateOnEvent(currentLimit);
    });

    document.querySelectorAll('.sort-controls').forEach(button => {
        button.addEventListener('click', handleSortClick);
    });

    updateOnEvent(parseInt(orderLimitSelector.value, 10));
});