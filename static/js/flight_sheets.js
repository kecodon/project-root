function createSheet() {
  fetch("/api/flight_sheet", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      coin: document.getElementById("coin").value,
      wallet: document.getElementById("wallet").value,
      pool: document.getElementById("pool").value,
      miner: document.getElementById("miner").value,
      name: document.getElementById("name").value
    })
  }).then(() => location.reload());
}

window.onload = async function () {
  const res = await fetch("/api/flight_sheets");
  const sheets = await res.json();
  const list = document.getElementById("sheet-list");
  if (sheets.length === 0) {
    list.innerHTML = "<p>No flight sheets available.</p>";
    return;
  }
  list.innerHTML = "";
  sheets.forEach(fs => {
    list.innerHTML += `<div class="d-flex justify-content-between border-bottom py-2">
      <div><strong>${fs.coin}</strong> - ${fs.wallet} / ${fs.pool} / ${fs.miner} <br><small>${fs.name}</small></div>
      <button class="btn btn-sm btn-danger" onclick="deleteSheet('${fs.name}')">Delete</button>
    </div>`;
  });
};
function deleteSheet(name) {
  fetch("/api/flight_sheet/delete", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  }).then(() => location.reload());
}
