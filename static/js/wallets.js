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
