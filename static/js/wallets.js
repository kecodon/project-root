document.addEventListener("DOMContentLoaded", () => {
  loadWallets();
  document.getElementById("walletForm").addEventListener("submit", saveWallet);
});

function loadWallets() {
  fetch("/api/wallets")
    .then((res) => res.json())
    .then((data) => {
      const table = document.getElementById("wallets-table");
      table.innerHTML = "";
      data.forEach((wallet, i) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${wallet.coin}</td>
          <td>${wallet.source}</td>
          <td>${wallet.address}</td>
          <td>
            <button class="btn btn-sm btn-danger" onclick="deleteWallet(${i})">Delete</button>
          </td>
        `;
        table.appendChild(row);
      });
    });
}

function saveWallet(e) {
  e.preventDefault();
  const wallet = {
    coin: document.getElementById("coin").value,
    source: document.getElementById("source").value,
    address: document.getElementById("address").value,
  };

  fetch("/api/wallets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(wallet),
  }).then(() => {
    const modal = bootstrap.Modal.getInstance(document.getElementById("walletModal"));
    modal.hide();
    loadWallets();
  });
}

function deleteWallet(index) {
  fetch("/api/wallets/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index }),
  }).then(() => loadWallets());
}

function openWalletModal() {
  document.getElementById("walletForm").reset();
  const modal = new bootstrap.Modal(document.getElementById("walletModal"));
  modal.show();
}
