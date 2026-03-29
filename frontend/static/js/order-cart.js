/**
 * Builds hidden JSON payload for waiter / parcel order forms.
 */
(function () {
  var state = new Map();

  function renderSummary(container, totalEl, items) {
    if (!container) return;
    var subtotal = 0;
    var html = '';
    items.forEach(function (item) {
      var line = item.price * item.qty;
      subtotal += line;
      html += '<div class="menu-item">';
      html += '<div><strong>' + item.name + '</strong><div class="muted small">' + item.category + '</div></div>';
      html += '<div>Qty ' + item.qty + ' × ₹' + item.price.toFixed(2) + '</div>';
      html += '<div><strong>₹' + line.toFixed(2) + '</strong></div>';
      html += '</div>';
    });
    container.innerHTML = html || '<p class="muted">No dishes selected yet.</p>';
    if (totalEl) totalEl.textContent = '₹ ' + subtotal.toFixed(2);
    return subtotal;
  }

  window.OrderCart = {
    bind: function (options) {
      var menuList = document.getElementById(options.menuListId);
      var hiddenInput = document.getElementById(options.hiddenInputId);
      var summary = document.getElementById(options.summaryId);
      var total = document.getElementById(options.totalId);
      var search = document.getElementById(options.searchId);

      function syncHidden() {
        var payload = [];
        state.forEach(function (qty, id) {
          if (qty > 0) payload.push({ item_id: Number(id), quantity: qty });
        });
        hiddenInput.value = JSON.stringify(payload);
      }

      function refresh() {
        var items = [];
        state.forEach(function (qty, id) {
          if (qty <= 0) return;
          var node = menuList.querySelector('[data-item-id="' + id + '"]');
          if (!node) return;
          items.push({
            id: id,
            name: node.dataset.name,
            category: node.dataset.category,
            price: Number(node.dataset.price),
            qty: qty
          });
        });
        renderSummary(summary, total, items);
        syncHidden();
      }

      if (search) {
        search.addEventListener('input', function () {
          var q = search.value.toLowerCase();
          menuList.querySelectorAll('.menu-row').forEach(function (row) {
            var hay = (row.dataset.search || '').toLowerCase();
            row.style.display = hay.indexOf(q) >= 0 ? '' : 'none';
          });
        });
      }

      menuList.addEventListener('input', function (e) {
        var t = e.target;
        if (t && t.classList.contains('qty-input')) {
          var id = t.getAttribute('data-item-id');
          var qty = parseInt(t.value, 10) || 0;
          if (qty <= 0) state.delete(id); else state.set(id, qty);
          refresh();
        }
      });

      refresh();
    }
  };
})();
