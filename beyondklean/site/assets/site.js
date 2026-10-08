// Mobile menu, "What needs cleaning?" finder, directory / FAQ / glossary filters, demo forms.
(function () {
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var norm = function (s) { return String(s).toLowerCase().replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim(); };

  // ---- Mobile menu
  var mb = document.querySelector(".menu-btn");
  var nav = document.getElementById("mainnav");
  if (mb && nav) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      mb.setAttribute("aria-expanded", open ? "true" : "false");
      mb.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };
    mb.addEventListener("click", function () { setOpen(!nav.classList.contains("is-open")); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") setOpen(false); });
    document.addEventListener("click", function (ev) { if (!nav.contains(ev.target) && !mb.contains(ev.target)) setOpen(false); });
  }

  // ---- "What needs cleaning?" finder (type-ahead over every service name and the names crews use for it)
  var finder = document.querySelector("[data-finder]");
  if (finder && window.BK_INDEX) {
    var input = finder.querySelector("input");
    var list = finder.querySelector(".finder-list");
    var data = window.BK_INDEX.map(function (r) {
      return { name: r[0], alts: r[1], fam: r[2], url: r[3], w: r[4] || 0, n: norm(r[0]), an: r[1].map(norm), xn: (r[5] || []).map(norm) };
    });
    var STARTERS = ["Final clean of entire building", "Open ceiling deck cleaning", "Grout haze removal",
      "Interior window cleaning", "VCT initial floor finish", "Rough clean of entire building", "Commercial kitchen post-construction clean"];
    var active = -1, shown = [];

    var mark = function (text, q) {
      var i = text.toLowerCase().indexOf(q);
      if (i < 0 || !q) return esc(text);
      return esc(text.slice(0, i)) + "<b>" + esc(text.slice(i, i + q.length)) + "</b>" + esc(text.slice(i + q.length));
    };
    var wordStart = function (hay, q) { return hay.indexOf(q) === 0 || hay.indexOf(" " + q) !== -1; };

    var search = function (raw) {
      var q = norm(raw), words = q.split(" ").filter(Boolean);
      if (q.length < 2) return [];
      var out = [];
      data.forEach(function (d) {
        var best = 0, via = "";
        var test = function (hay, isAlt, label) {
          if (!words.every(function (w) { return hay.indexOf(w) !== -1; })) return;
          var s = hay.indexOf(q) === 0 ? 100 : wordStart(hay, q) ? 85 : hay.indexOf(q) !== -1 ? 60 : 45;
          if (isAlt) s -= 12;
          if (s > best) { best = s; via = isAlt ? label : ""; }
        };
        test(d.n, false);
        d.an.forEach(function (a, i) { test(a, true, d.alts[i]); });
        d.xn.forEach(function (a) { test(a, true, ""); });
        if (best) out.push({ d: d, s: best + d.w - d.name.length / 200, via: via });
      });
      out.sort(function (a, b) { return b.s - a.s; });
      return out.slice(0, 7);
    };

    var render = function () {
      var raw = input.value.trim(), q = norm(raw), html = "";
      if (q.length < 2) {
        shown = STARTERS.map(function (n) { return data.filter(function (d) { return d.name === n; })[0]; })
          .filter(Boolean).map(function (d) { return { d: d, via: "" }; });
        html = '<li class="hint-row" role="presentation">Popular requests</li>';
      } else {
        shown = search(raw);
      }
      shown.forEach(function (r, i) {
        var name = r.via ? esc(r.d.name) : mark(r.d.name, q);
        var aka = r.via ? '<span class="aka">also called ' + mark(r.via, q) + "</span>" : "";
        html += '<li role="option" id="fo-' + i + '" aria-selected="' + (i === active) + '"><a href="' + esc(r.d.url) + '"><span>' + name + aka +
          '</span><span class="fam">' + esc(r.d.fam) + "</span></a></li>";
      });
      if (q.length >= 2 && !shown.length) {
        html = '<li class="none"><a href="quote.html">Can’t find it? Tell us what you need →</a></li>';
      }
      list.innerHTML = html;
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      input.setAttribute("aria-activedescendant", active >= 0 ? "fo-" + active : "");
    };
    var close = function () { list.hidden = true; active = -1; input.setAttribute("aria-expanded", "false"); };

    input.addEventListener("input", function () { active = -1; render(); });
    input.addEventListener("focus", render);
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        ev.preventDefault();
        if (list.hidden) render();
        var n = shown.length; if (!n) return;
        active = ev.key === "ArrowDown" ? (active + 1) % n : (active - 1 + n) % n;
        render();
      } else if (ev.key === "Escape") { close(); }
    });
    finder.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var pick = shown[active >= 0 ? active : 0];
      if (input.value.trim().length >= 2 && pick) { location.href = pick.d.url; return; }
      if (input.value.trim()) { location.href = "quote.html"; return; }
      input.focus(); render();
    });
    document.addEventListener("click", function (ev) { if (!finder.contains(ev.target)) close(); });
  }

  // ---- Directory, FAQ and glossary filters
  var box = document.querySelector(".filter");
  if (box) {
    var flist = document.getElementById(box.getAttribute("data-list"));
    var finput = box.querySelector("input");
    var count = box.querySelector("[data-count]");
    var countline = box.querySelector("[data-countline]");
    var items = flist.querySelectorAll("[data-s]");
    var chip = "";
    var run = function () {
      var words = norm(finput.value).split(" ").filter(function (w) { return w.length > 1; });
      var n = 0;
      items.forEach(function (el) {
        var s = el.getAttribute("data-s");
        var ok = words.every(function (w) { return s.indexOf(w) !== -1; });
        if (ok && chip) ok = (" " + (el.getAttribute("data-f") || "") + " ").indexOf(" " + chip + " ") !== -1;
        el.hidden = !ok;
        if (ok) n++;
        if (ok && words.length && el.tagName === "DETAILS") el.open = n <= 3;
      });
      flist.querySelectorAll(".faqsec").forEach(function (sec) {
        sec.hidden = !sec.querySelector("[data-s]:not([hidden])");
      });
      if (count) count.textContent = n.toLocaleString();
      if (countline) countline.hidden = !(words.length || chip);
    };
    finput.addEventListener("input", run);
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
    try {
      var qp = new URLSearchParams(location.search).get("q");
      if (qp) { finput.value = qp; run(); }
    } catch (e) { /* query string not available */ }
  }

  // ---- Open a linked FAQ answer (task.html#q3)
  var t = location.hash && document.getElementById(location.hash.slice(1));
  if (t && t.tagName === "DETAILS") t.open = true;

  // ---- Quote / application forms: preview build does not transmit anything
  document.querySelectorAll("form[data-demo]").forEach(function (f) {
    try {
      var task = new URLSearchParams(location.search).get("task");
      var sel = f.querySelector("[name=task]");
      if (task && sel) sel.value = task;
    } catch (e) { /* query string not available */ }
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = f.querySelector(".notice");
      msg.hidden = false;
      msg.focus();
    });
  });
})();
