
document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token") || sessionStorage.getItem("token");

    if (token) {
        window.location.href = "/dashboard.html";
    } else {
        window.location.href = "/login.html";
    }
});