document.addEventListener("DOMContentLoaded", () => {
  loadWallets();

  document.getElementById("walletForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const wallet = {
      coin: document.getElementById("coin").value,
      source: document.getElementById("source").value,
      address: document.getElementById("address").value
    };
    fetch("/api/wallet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(wallet)
    }).then(() => {
      bootstrap.Modal.getInstance(document.getElementById("walletModal")).hide();
      loadWallets();
    });
  });
});

function loadWallets() {
  fetch("/api/wallets")
    .then((res) => res.json())
    .then((data) => {
      const table = document.getElementById("wallets-table");
      table.innerHTML = "";
      data.forEach((w, i) => {
        const row = `
          <tr>
            <td>${w.coin}</td>
            <td>${w.source}</td>
            <td>${w.address}</td>
            <td><button class="btn btn-sm btn-danger" onclick="deleteWallet(${i})">Delete</button></td>
          </tr>`;
        table.innerHTML += row;
      });
    });
}

function deleteWallet(index) {
  fetch("/api/wallet/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index })
  }).then(() => loadWallets());
}

function openWalletModal() {
  const modal = new bootstrap.Modal(document.getElementById("walletModal"));
  document.getElementById("walletForm").reset();
  modal.show();
}
