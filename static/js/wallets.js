document.addEventListener("DOMContentLoaded", function () {
  loadWallets();
});

function loadWallets() {
  fetch("/api/wallets")
    .then((res) => res.json())
    .then((wallets) => {
      const table = document.getElementById("wallets-table");
      table.innerHTML = "";
      wallets.forEach((w, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${w.coin}</td>
          <td>${w.source}</td>
          <td>${w.address}</td>
          <td><button class="btn btn-danger btn-sm" onclick="deleteWallet(${index})">Delete</button></td>
        `;
        table.appendChild(row);
      });
    });
}

function openWalletModal() {
  new bootstrap.Modal(document.getElementById("walletModal")).show();
}

document.getElementById("walletForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const data = {
    coin: document.getElementById("coin").value,
    source: document.getElementById("source").value,
    address: document.getElementById("address").value
  };
  fetch("/api/wallets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  }).then(() => {
    document.getElementById("walletForm").reset();
    bootstrap.Modal.getInstance(document.getElementById("walletModal")).hide();
    loadWallets();  // <== QUAN TRỌNG: GỌI LẠI
  });
});

function deleteWallet(index) {
  fetch("/api/wallets/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index })
  }).then(() => loadWallets());
}
