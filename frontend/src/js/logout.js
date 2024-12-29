addEventListener("DOMContentLoaded", async function () {
  const token =
    localStorage.getItem("token") || sessionStorage.getItem("token");
  const currentUrl = window.location.href;
  const baseUrl = currentUrl.split("/").slice(0, 3).join("/");

  async function logout() {
    try {
      const response = await fetch(`${baseUrl}/api/user/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 400) {
        throw new Error("Ungültige Anfrage");
      }
      if (response.status === 401) {
        throw new Error("Ungültiger Token");
      }
    } catch (error) {
      console.error(error);
    }
  }
  await logout();

  localStorage.removeItem("token");
  sessionStorage.removeItem("token");

  window.location.href = "/";
});
