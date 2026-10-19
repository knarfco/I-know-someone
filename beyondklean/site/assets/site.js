// Mobile menu, bid list, "What needs cleaning?" finder, directory / FAQ / glossary filters, bid form.
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

  // ---- Bid list: services collected across pages, kept in this browser
  var BL_KEY = "bk-bidlist";
  var getList = function () { try { return JSON.parse(localStorage.getItem(BL_KEY)) || []; } catch (e) { return []; } };
  var setList = function (l) { try { localStorage.setItem(BL_KEY, JSON.stringify(l)); } catch (e) { /* storage unavailable */ } paintList(); };
  var addToList = function (name) {
    name = String(name || "").trim(); if (!name) return;
    var l = getList(); if (l.indexOf(name) === -1) l.push(name); setList(l);
  };
  var paintList = function () {
    var l = getList();
    document.querySelectorAll("[data-bidcount]").forEach(function (a) { a.hidden = !l.length; a.querySelector(".badge").textContent = l.length; });
    document.querySelectorAll("[data-bidbadge]").forEach(function (b) { b.hidden = !l.length; b.textContent = l.length; });
    document.querySelectorAll("[data-add]").forEach(function (b) {
      var on = l.indexOf(b.getAttribute("data-add")) !== -1;
      b.textContent = on ? "On your bid list ✓" : "Add to bid list";
      b.classList.toggle("is-added", on);
    });
    document.querySelectorAll("[data-bidlist]").forEach(function (ul) {
      ul.innerHTML = l.length ? l.map(function (n, i) {
        return '<li><span>' + esc(n) + '</span><button type="button" class="x" data-rm="' + i + '" aria-label="Remove ' + esc(n) + '">×</button></li>';
      }).join("") : '<li class="empty">Nothing on your list yet. Add services below or from any service page.</li>';
    });
    document.querySelectorAll("[data-bidfield]").forEach(function (f) { f.value = l.join("; "); });
  };
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-add]");
    if (b) {
      var name = b.getAttribute("data-add"), l = getList(), i = l.indexOf(name);
      if (i === -1) l.push(name); else l.splice(i, 1);
      setList(l); return;
    }
    var rm = ev.target.closest("[data-rm]");
    if (rm) { var l2 = getList(); l2.splice(+rm.getAttribute("data-rm"), 1); setList(l2); }
  });
  try {
    var addp = new URLSearchParams(location.search).get("add");
    if (addp) addToList(addp);
  } catch (e) { /* query string not available */ }
  paintList();

  // ---- "What needs cleaning?" finder (type-ahead over every service name and the names crews use for it).
  // data-mode="add" (bid form) adds the pick to the bid list instead of opening the page.
  var data = (window.BK_INDEX || []).map(function (r) {
    return { name: r[0], alts: r[1], fam: r[2], url: r[3], w: r[4] || 0, n: norm(r[0]), an: r[1].map(norm), xn: (r[5] || []).map(norm) };
  });
  var STARTERS = ["Final clean of entire building", "Open ceiling deck cleaning", "Grout haze removal",
    "Interior window cleaning", "VCT initial floor finish", "Rough clean of entire building", "Commercial kitchen post-construction clean"];
  var mark = function (text, q) {
    var i = text.toLowerCase().indexOf(q);
    if (i < 0 || !q) return esc(text);
    return esc(text.slice(0, i)) + "<b>" + esc(text.slice(i, i + q.length)) + "</b>" + esc(text.slice(i + q.length));
  };
  var wordStart = function (hay, q) { return hay.indexOf(q) === 0 || hay.indexOf(" " + q) !== -1; };
  var search = function (raw, tasksOnly, scope) {
    var q = norm(raw), words = q.split(" ").filter(Boolean);
    if (q.length < 2) return [];
    var out = [];
    data.forEach(function (d) {
      if (tasksOnly && (d.fam === "Service family" || d.fam.indexOf("Specialty") === 0)) return;
      if (scope && d.fam.indexOf(scope) !== 0) return;
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

  document.querySelectorAll("[data-finder]").forEach(function (finder) {
    if (!data.length) return;
    var addMode = finder.getAttribute("data-mode") === "add";
    var up = finder.getAttribute("data-up") || "", scope = finder.getAttribute("data-scope") || "";
    var starters = finder.getAttribute("data-starters") ? finder.getAttribute("data-starters").split("|") : STARTERS;
    var input = finder.querySelector("input");
    var list = finder.querySelector(".finder-list");
    var lid = list.id;
    var active = -1, shown = [];

    var render = function () {
      var raw = input.value.trim(), q = norm(raw), html = "";
      if (q.length < 2) {
        shown = starters.map(function (n) { return data.filter(function (d) { return d.name === n; })[0]; })
          .filter(Boolean).map(function (d) { return { d: d, via: "" }; });
        html = '<li class="hint-row" role="presentation">Popular requests</li>';
      } else {
        shown = search(raw, addMode, scope);
      }
      shown.forEach(function (r, i) {
        var name = r.via ? esc(r.d.name) : mark(r.d.name, q);
        var aka = r.via ? '<span class="aka">also called ' + mark(r.via, q) + "</span>" : "";
        html += '<li role="option" id="' + lid + "-" + i + '" aria-selected="' + (i === active) + '"><a href="' + esc(up + r.d.url) + '" data-pick="' + i + '"><span>' + name + aka +
          '</span><span class="fam">' + (addMode ? "+ Add" : esc(r.d.fam)) + "</span></a></li>";
      });
      if (q.length >= 2 && !shown.length) {
        html = addMode ? '<li class="none"><a href="#" data-typed>Add “' + esc(raw) + '” to your list →</a></li>'
                       : scope ? '<li class="none"><a href="#groups">Can’t find it? Browse every specialty group →</a></li>'
                       : '<li class="none"><a href="' + up + 'quote.html">Can’t find it? Tell us what you need →</a></li>';
      }
      list.innerHTML = html;
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      input.setAttribute("aria-activedescendant", active >= 0 ? lid + "-" + active : "");
    };
    var close = function () { list.hidden = true; active = -1; input.setAttribute("aria-expanded", "false"); };
    var take = function (r) {
      if (addMode) { addToList(r ? r.d.name : input.value); input.value = ""; close(); input.focus(); }
      else if (r) location.href = up + r.d.url;
    };

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
      else if (ev.key === "Enter" && addMode) {
        ev.preventDefault();  // never submit the surrounding bid form from here
        if (input.value.trim().length >= 2) take(shown[active >= 0 ? active : 0] || null);
      }
    });
    list.addEventListener("click", function (ev) {
      if (!addMode) return;
      var a = ev.target.closest("a"); if (!a) return;
      ev.preventDefault();
      take(a.hasAttribute("data-typed") ? null : shown[+a.getAttribute("data-pick")]);
    });
    var typed = finder.querySelector("[data-add-typed]");
    if (typed) typed.addEventListener("click", function () {
      var raw = input.value.trim(); if (raw.length < 2) { input.focus(); render(); return; }
      var r = search(raw, true)[0];
      take(r && norm(r.d.name) === norm(raw) ? r : null);
    });
    if (finder.tagName === "FORM") finder.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var pick = shown[active >= 0 ? active : 0];
      if (input.value.trim().length >= 2 && pick) { location.href = pick.d.url; return; }
      if (input.value.trim()) { location.href = "quote.html"; return; }
      input.focus(); render();
    });
    document.addEventListener("click", function (ev) { if (!finder.contains(ev.target)) close(); });
  });

  // ---- Directory, FAQ and glossary filters
  var box = document.querySelector(".filter[data-list]");
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

  // ---- Before / after sliders on project cards
  document.querySelectorAll("[data-ba]").forEach(function (ba) {
    var stage = ba.querySelector(".ba-stage"), range = ba.querySelector(".ba-range"), during = ba.querySelector(".ba-during");
    range.addEventListener("input", function () { stage.style.setProperty("--pos", range.value + "%"); });
    ba.querySelectorAll("[data-ba-view]").forEach(function (b) {
      b.addEventListener("click", function () {
        var d = b.getAttribute("data-ba-view") === "during";
        stage.hidden = d; if (during) during.hidden = !d;
        ba.querySelectorAll("[data-ba-view]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      });
    });
  });

  // ---- "Read more" on long paragraphs: clamped by CSS, the full text stays in the page
  document.querySelectorAll("[data-more]").forEach(function (box) {
    var p = box.querySelector("p");
    if (p.scrollHeight <= p.clientHeight + 4) { box.classList.add("open"); return; }
    var b = document.createElement("button");
    b.type = "button"; b.className = "more-btn"; b.textContent = "Read more";
    b.addEventListener("click", function () { var o = box.classList.toggle("open"); b.textContent = o ? "Show less" : "Read more"; });
    box.appendChild(b);
  });

  // ---- "Send your specs" opens the optional details on the bid form
  var specs = document.getElementById("specs");
  if (specs && specs.tagName === "DETAILS" && location.hash === "#specs") specs.open = true;

  // ---- Print buttons (capability statement)
  document.querySelectorAll("[data-print]").forEach(function (b) { b.addEventListener("click", function () { window.print(); }); });

  // ---- Open a linked FAQ answer (task.html#q3)
  var t = location.hash && document.getElementById(location.hash.slice(1));
  if (t && t.tagName === "DETAILS") t.open = true;

  // ---- Bid request form: preview build does not transmit anything yet
  document.querySelectorAll("form[data-demo]").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      paintList();
      var d = new Date();
      var ref = "BK-" + String(d.getFullYear()).slice(2) + ("0" + (d.getMonth() + 1)).slice(-2) + ("0" + d.getDate()).slice(-2) +
        "-" + String(Math.floor(Math.random() * 9000) + 1000);
      var slot = f.querySelector("[data-ref]");
      if (slot) slot.textContent = ref;
      var msg = f.querySelector(".notice");
      msg.hidden = false;
      msg.focus();
    });
  });
})();

// I-4 corridor: filter the ZIP table by ZIP or city
(function () {
  var q = document.querySelector('[data-zipfilter]');
  if (!q) return;
  var rows = Array.prototype.slice.call(document.querySelectorAll('.ziptable tbody tr'));
  q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase();
    rows.forEach(function (r) { r.hidden = v && r.textContent.toLowerCase().indexOf(v) < 0; });
  });
})();
