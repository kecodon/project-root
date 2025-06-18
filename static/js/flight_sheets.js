document.addEventListener("DOMContentLoaded", () => {
  loadFlightSheets();
  loadWallets();
  loadMinerTools();
});

function loadFlightSheets() {
  fetch("/api/flight_sheets")
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("sheets-container");
      container.innerHTML = "";

      if (data.length === 0) {
        container.innerHTML = "<p>No flight sheets yet.</p>";
        return;
      }

      data.forEach(fs => {
        const div = document.createElement("div");
        div.className = "border-bottom py-2 d-flex justify-content-between";
        div.innerHTML = `
          <div>
            <span class="highlight">${fs.coin}</span> - ${fs.wallet} / ${fs.pool} / ${fs.miner}
            <div><small>${fs.name}</small></div>
          </div>
          <button class="btn btn-sm btn-danger" onclick="deleteSheet('${fs.name}')">Delete</button>
        `;
        container.appendChild(div);
      });
    });
}

function loadWallets() {
  fetch("/api/wallets")
    .then(res => res.json())
    .then(data => {
      const select = document.getElementById("wallet");
      select.innerHTML = '<option value="">Select wallet</option>';
      data.forEach(w => {
        const opt = document.createElement("option");
        opt.value = w.source;
        opt.textContent = w.source;
        select.appendChild(opt);
      });
    });
}

function loadMinerTools() {
  const tools = ["xmrig", "cpuminer", "other-tool"]; // bạn có thể sửa danh sách tool ở đây
  const select = document.getElementById("miner");
  select.innerHTML = '<option value="">Select miner</option>';
  tools.forEach(tool => {
    const opt = document.createElement("option");
    opt.value = tool;
    opt.textContent = tool;
    select.appendChild(opt);
  });
}

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
  }).then(() => loadFlightSheets());
}

function deleteSheet(name) {
  fetch("/api/flight_sheet/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  }).then(() => loadFlightSheets());
}
