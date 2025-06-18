document.addEventListener("DOMContentLoaded", () => {
  loadWallets();

  document.getElementById("walletForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      coin: document.getElementById("coin").value,
      source: document.getElementById("source").value,
      address: document.getElementById("address").value,
    };

    await fetch("/api/wallet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    bootstrap.Modal.getInstance(document.getElementById("walletModal")).hide();
    loadWallets();  // <- Load lại sau khi thêm
  });
});

async function loadWallets() {
  const res = await fetch("/api/wallets");
  const wallets = await res.json();
  const tbody = document.getElementById("wallets-table");
  const filters = document.getElementById("coin-filters");
  tbody.innerHTML = "";
  filters.innerHTML = "";

  const coins = [...new Set(wallets.map(w => w.coin))];

  coins.forEach(c => {
    const btn = document.createElement("button");
    btn.className = "btn btn-sm btn-outline-light";
    btn.innerText = c;
    btn.onclick = () => {
      const rows = tbody.querySelectorAll("tr");
      rows.forEach(r => {
        r.style.display = r.dataset.coin === c ? "" : "none";
      });
    };
    filters.appendChild(btn);
  });

  wallets.forEach(w => {
    const tr = document.createElement("tr");
    tr.dataset.coin = w.coin;
    tr.innerHTML = `
      <td>${w.coin}</td>
      <td>${w.source}</td>
      <td>${w.address}</td>
      <td>
        <button class="btn btn-sm btn-danger" onclick="deleteWallet('${w.source}')">Del</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function deleteWallet(source) {
  await fetch("/api/wallet/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source }),
  });
  loadWallets();
}

function openWalletModal() {
  document.getElementById("walletForm").reset();
  const modal = new bootstrap.Modal(document.getElementById("walletModal"));
  modal.show();
}
