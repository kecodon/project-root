async function loadFlightSheets() {
  const res = await fetch("/api/flight-sheets");
  const sheets = await res.json();
  const list = document.getElementById("flightList");
  list.innerHTML = "";
  sheets.forEach(s => {
    const li = document.createElement("li");
    li.textContent = `${s.coin} - ${s.pool} (${s.miner}) using wallet ${s.wallet}`;
    list.appendChild(li);
  });
}

async function loadWalletOptions() {
  const res = await fetch("/api/wallets");
  const wallets = await res.json();
  const select = document.getElementById("wallet");
  select.innerHTML = "";
  wallets.forEach(w => {
    const option = document.createElement("option");
    option.value = w.name;
    option.textContent = `${w.name} (${w.coin})`;
    select.appendChild(option);
  });
}

document.getElementById("flightForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const coin = document.getElementById("coin").value;
  const wallet = document.getElementById("wallet").value;
  const pool = document.getElementById("pool").value;
  const miner = document.getElementById("miner").value;
  await fetch("/api/flight-sheets", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({coin, wallet, pool, miner})
  });
  e.target.reset();
  loadFlightSheets();
});

loadWalletOptions();
loadFlightSheets();
