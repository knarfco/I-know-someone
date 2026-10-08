// Search + chip filters for the directory, FAQ library and glossary; quote form handling.
(function () {
  var box = document.querySelector(".filter");
  if (box) {
    var list = document.getElementById(box.getAttribute("data-list"));
    var input = box.querySelector("input");
    var count = box.querySelector("[data-count]");
    var items = list.querySelectorAll("[data-s]");
    var chip = "";
    var run = function () {
      var words = input.value.toLowerCase().replace(/[^a-z0-9 ]+/g, " ").split(/\s+/).filter(function (w) { return w.length > 1; });
      var n = 0;
      items.forEach(function (el) {
        var s = el.getAttribute("data-s");
        var ok = words.every(function (w) { return s.indexOf(w) !== -1; });
        if (ok && chip) ok = (" " + (el.getAttribute("data-f") || "") + " ").indexOf(" " + chip + " ") !== -1;
        el.hidden = !ok;
        if (ok) n++;
        if (ok && words.length && el.tagName === "DETAILS") el.open = n <= 3;
      });
      list.querySelectorAll(".faqsec").forEach(function (sec) {
        sec.hidden = !sec.querySelector("[data-s]:not([hidden])");
      });
      if (count) count.textContent = n.toLocaleString();
    };
    input.addEventListener("input", run);
    box.querySelectorAll("[data-filter]").forEach(function (b) {
      b.addEventListener("click", function () {
        chip = b.getAttribute("data-filter");
        box.querySelectorAll("[data-filter]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
        run();
      });
    });
    var h = (location.hash || "").slice(1);
    var pre = h && box.querySelector('[data-filter="' + h + '"]');
    if (pre) pre.click();
  }

  // Open a linked FAQ answer (task.html#q3)
  var t = location.hash && document.getElementById(location.hash.slice(1));
  if (t && t.tagName === "DETAILS") t.open = true;

  // Quote / application forms: preview build does not transmit anything
  document.querySelectorAll("form[data-demo]").forEach(function (f) {
    var params = new URLSearchParams(location.search);
    var task = params.get("task");
    var sel = f.querySelector("[name=task]");
    if (task && sel) sel.value = task;
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = f.querySelector(".notice");
      msg.hidden = false;
      msg.focus();
    });
  });
})();
