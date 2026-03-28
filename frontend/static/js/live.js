/**
 * Lightweight live updates: prefers Server-Sent Events, falls back to polling.
 */
(function () {
  function setText(el, value) {
    if (!el) return;
    el.textContent = value;
  }

  function pollSummary(el) {
    fetch('/api/orders/summary', { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        setText(el, data.active_orders);
      })
      .catch(function () { /* ignore */ });
  }

  window.HotelLive = {
    watchSummary: function (el) {
      if (!el) return;
      if (typeof EventSource !== 'undefined') {
        try {
          var es = new EventSource('/api/stream/orders');
          es.onmessage = function (ev) {
            try {
              var data = JSON.parse(ev.data);
              setText(el, data.active_orders);
            } catch (e) {
              pollSummary(el);
            }
          };
          es.onerror = function () {
            es.close();
            pollSummary(el);
            setInterval(function () { pollSummary(el); }, 4000);
          };
          return;
        } catch (e) {
          /* fall through */
        }
      }
      pollSummary(el);
      setInterval(function () { pollSummary(el); }, 4000);
    }
  };
})();
