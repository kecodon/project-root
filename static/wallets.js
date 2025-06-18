document.addEventListener("DOMContentLoaded", () => {
  const walletForm = document.getElementById("walletForm");

  walletForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const coin = document.getElementById("coin").value.trim();
    const source = document.getElementById("source").value.trim();
    const address = document.getElementById("address").value.trim();

    if (!coin || !source || !address) return alert("All fields are required.");

    await fetch("/api/wallet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ coin, source, address }),
    });

    location.reload();
  });
});

function deleteWallet(address) {
  fetch("/api/wallet/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ address }),
  }).then(() => location.reload());
}
