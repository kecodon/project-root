async function loadWallets() {
  const res = await fetch("/api/wallets");
  const wallets = await res.json();
  const list = document.getElementById("walletList");
  list.innerHTML = "";
  wallets.forEach(w => {
    const li = document.createElement("li");
    li.textContent = `${w.name} (${w.coin}) - ${w.address}`;
    list.appendChild(li);
  });
}

document.getElementById("walletForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const address = document.getElementById("address").value;
  const coin = document.getElementById("coin").value;
  await fetch("/api/wallets", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, address, coin})
  });
  e.target.reset();
  loadWallets();
});

loadWallets();
