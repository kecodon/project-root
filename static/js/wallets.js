async function loadWallets() {
  const res = await fetch("/api/wallets");
  const wallets = await res.json();
  const tbody = document.getElementById("wallets-table");
  tbody.innerHTML = "";
  wallets.forEach(w => {
    const row = `<tr><td>${w.coin}</td><td>${w.source}</td><td>${w.address}</td>
      <td><button class='btn btn-sm btn-danger' onclick="deleteWallet('${w.source}')">Delete</button></td></tr>`;
    tbody.innerHTML += row;
  });
}
async function deleteWallet(source) {
  await fetch("/api/wallet/delete", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source })
  });
  loadWallets();
}
function openWalletModal() {
  new bootstrap.Modal(document.getElementById("walletModal")).show();
}
async function addWallet() {
    const name = document.getElementById("wallet-name").value;
    const address = document.getElementById("wallet-address").value;
    const coin = document.getElementById("wallet-coin").value;

    const response = await fetch("/api/wallets/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, address, coin }),
    });

    if (response.ok) {
        await loadWallets();
        document.getElementById("wallet-name").value = "";
        document.getElementById("wallet-address").value = "";
        document.getElementById("wallet-coin").value = "";
    } else {
        alert("Failed to add wallet");
    }
}
document.getElementById("walletForm").onsubmit = async function(e) {
  e.preventDefault();
  const coin = document.getElementById("coin").value;
  const source = document.getElementById("source").value;
  const address = document.getElementById("address").value;
  await fetch("/api/wallet", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ coin, source, address })
  });
  bootstrap.Modal.getInstance(document.getElementById("walletModal")).hide();
  loadWallets();
}
window.onload = loadWallets;
