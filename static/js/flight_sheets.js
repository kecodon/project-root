document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("create-btn").addEventListener("click", createSheet);
});

function createSheet() {
  fetch("/api/flight_sheet", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      coin: document.getElementById("coin").value,
      wallet: document.getElementById("wallet").value,
      pool: document.getElementById("pool").value,
      miner: document.getElementById("miner").value,
      name: document.getElementById("name").value
    })
  }).then(() => location.reload());
}

function deleteSheet(name) {
  fetch("/api/flight_sheet/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  }).then(() => location.reload());
}
