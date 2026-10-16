// Estimator: line-item quotes from the price book, CSV export, print-to-PDF, editable rates.
// Everything stays in this browser (localStorage); nothing is sent anywhere.
(function () {
  var root = document.querySelector("[data-estimator]");
  if (!root || !window.BK_PRICEBOOK) return;

  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var norm = function (s) { return String(s).toLowerCase().replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim(); };
  var num = function (v) { var n = parseFloat(String(v == null ? "" : v).replace(/[^0-9.\-]/g, "")); return isFinite(n) ? n : 0; };
  var money = function (n) { return (n < 0 ? "-$" : "$") + Math.abs(n).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var rateFmt = function (n) { return n >= 10 ? n.toFixed(2) : String(Math.round(n * 1000) / 1000); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
  };
  var today = function (plus) { var d = new Date(); d.setDate(d.getDate() + (plus || 0)); return d.toISOString().slice(0, 10); };
  var download = function (name, text, type) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: type }));
    a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  };

  // ---------------------------------------------------------------- price book
  var PB = window.BK_PRICEBOOK, UNITS = PB.units;
  var base = {};
  PB.items.forEach(function (r) {
    base[r[0]] = { task: r[0], fam: r[1], unit: r[2], low: r[3], mid: r[4], high: r[5], min: r[6], basis: r[7], conf: r[8], alts: r[9] || [], phase: r[10] };
  });
  var overrides = store.get("bk-est-pb", {});
  var book = function (task) {
    var b = base[task]; if (!b) return null;
    var o = overrides[task] || {};
    return { task: task, fam: b.fam, unit: o.unit || b.unit, low: o.low != null ? o.low : b.low, mid: o.mid != null ? o.mid : b.mid,
      high: o.high != null ? o.high : b.high, min: o.min != null ? o.min : b.min, basis: b.basis, conf: b.conf, edited: !!overrides[task] };
  };
  var unitOpts = function (sel) {
    return Object.keys(UNITS).map(function (u) { return '<option value="' + u + '"' + (u === sel ? " selected" : "") + ">" + esc(UNITS[u]) + "</option>"; }).join("");
  };

  // ---------------------------------------------------------------- company settings
  var DEFAULT_TERMS = "Pricing is based on the scope, quantities and schedule listed above. Work outside this scope is billed as a change order at the rates shown.\n" +
    "Owner or GC provides water, power, dumpster and site access. Lifts provided by the GC unless listed above.\n" +
    "One re-clean of punch items is included. Additional re-cleans caused by other trades are billed at the hourly rate.\n" +
    "Net 30 from invoice. This quote is valid until the date shown.";
  var co = store.get("bk-est-co", { name: "", license: "", phone: "", email: "", address: "", web: "", op: "10", tax: "0", terms: DEFAULT_TERMS });

  // ---------------------------------------------------------------- quote state
  var newQuote = function () {
    var d = new Date();
    var no = "BK-Q" + String(d.getFullYear()).slice(2) + ("0" + (d.getMonth() + 1)).slice(-2) + ("0" + d.getDate()).slice(-2) + "-" + String(Math.floor(Math.random() * 900) + 100);
    return { no: no, date: today(0), valid: today(30), tier: "mid",
      client: { name: "", company: "", phone: "", email: "", project: "", type: "", needed: "", address: "", city: "", zip: "", sqft: "" },
      lines: [], adj: { mob: "", travel: "", height: "", night: "", rush: "", op: co.op || "", disc: "", tax: co.tax || "" }, terms: co.terms || DEFAULT_TERMS };
  };
  var Q = store.get("bk-est-quote", null) || newQuote();
  var save = function () { store.set("bk-est-quote", Q); };

  var getPath = function (obj, path) { return path.split(".").reduce(function (o, k) { return o ? o[k] : ""; }, obj); };
  var setPath = function (obj, path, v) { var ks = path.split("."), last = ks.pop(); ks.reduce(function (o, k) { return o[k]; }, obj)[last] = v; };

  // ---------------------------------------------------------------- tabs
  root.querySelectorAll("[data-tab]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-tab");
      root.querySelectorAll("[data-tab]").forEach(function (x) { var on = x === b; x.classList.toggle("is-on", on); x.setAttribute("aria-selected", on); });
      root.querySelectorAll("[data-pane]").forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== t; });
      if (t === "book") renderBook();
      if (t === "quote") { renderCo(); renderLines(); }
    });
  });

  // ---------------------------------------------------------------- company block
  var renderCo = function () {
    var el = root.querySelector("[data-co]");
    var lines = [co.address, [co.phone, co.email].filter(Boolean).join(" · "), co.web, co.license ? "License " + co.license : ""].filter(Boolean);
    el.innerHTML = '<p class="qco-name">' + esc(co.name || "Your company name") + "</p>" + lines.map(function (l) { return "<p>" + esc(l) + "</p>"; }).join("") +
      (co.name ? "" : '<p class="small muted noprint">Set this on the Company tab.</p>');
  };
  root.querySelectorAll("[data-co-f]").forEach(function (inp) {
    var k = inp.getAttribute("data-co-f");
    inp.value = co[k] || "";
    inp.addEventListener("input", function () { co[k] = inp.value; store.set("bk-est-co", co); });
  });

  // ---------------------------------------------------------------- header / client fields
  var bindFields = function () {
    root.querySelectorAll("[data-q]").forEach(function (inp) {
      var k = inp.getAttribute("data-q");
      inp.value = getPath(Q, k) || "";
    });
    root.querySelectorAll("[data-adj]").forEach(function (inp) { inp.value = Q.adj[inp.getAttribute("data-adj")] || ""; });
    root.querySelector("[data-tier]").value = Q.tier || "mid";
  };
  root.querySelectorAll("[data-q]").forEach(function (inp) {
    inp.addEventListener("input", function () { setPath(Q, inp.getAttribute("data-q"), inp.value); save(); });
  });
  root.querySelectorAll("[data-adj]").forEach(function (inp) {
    inp.addEventListener("input", function () { Q.adj[inp.getAttribute("data-adj")] = inp.value; save(); renderSum(); });
  });
  root.querySelector("[data-tier]").addEventListener("change", function (ev) {
    Q.tier = ev.target.value;
    Q.lines.forEach(function (l) { var b = book(l.task); if (b && !l.rateEdited) { l.rate = b[Q.tier]; l.min = b.min; } });
    save(); renderLines();
  });

  // ---------------------------------------------------------------- line items
  var lineAmount = function (l) {
    var a = num(l.qty) * num(l.rate);
    var useMin = num(l.qty) > 0 && num(l.min) > 0 && a < num(l.min);
    return { amt: useMin ? num(l.min) : a, min: useMin };
  };
  var addLine = function (task) {
    var b = book(task);
    var l = b ? { task: task, notes: "", qty: "", unit: b.unit, rate: b[Q.tier || "mid"], min: b.min, rateEdited: false }
              : { task: task || "Custom item", notes: "", qty: "1", unit: "lot", rate: "", min: 0, rateEdited: true, custom: true };
    if (b && b.unit === "sqft" && num(Q.client.sqft)) l.qty = String(num(Q.client.sqft));
    Q.lines.push(l); save(); renderLines();
    var rows = root.querySelectorAll("[data-lines] tr");
    var last = rows[rows.length - 1];
    var f = last && last.querySelector(l.custom ? '[data-l="task"]' : '[data-l="qty"]');
    if (f) f.focus();
  };
  var renderLines = function () {
    var tb = root.querySelector("[data-lines]");
    if (!Q.lines.length) {
      tb.innerHTML = '<tr class="emptyrow"><td colspan="7">No lines yet. Add a service below.</td></tr>';
      renderSum(); return;
    }
    tb.innerHTML = Q.lines.map(function (l, i) {
      var r = lineAmount(l);
      return '<tr data-i="' + i + '">' +
        '<td class="mono">' + (i + 1) + "</td>" +
        '<td class="svc"><input data-l="task" value="' + esc(l.task) + '"' + (l.custom ? "" : " readonly") + ' aria-label="Service">' +
        '<input class="notes" data-l="notes" value="' + esc(l.notes) + '" placeholder="Notes: areas, floors, phase" aria-label="Notes"></td>' +
        '<td class="num"><input data-l="qty" inputmode="decimal" value="' + esc(l.qty) + '" aria-label="Quantity"></td>' +
        '<td><select data-l="unit" aria-label="Unit">' + unitOpts(l.unit) + "</select></td>" +
        '<td class="num"><input data-l="rate" inputmode="decimal" value="' + esc(l.rate === "" ? "" : rateFmt(num(l.rate))) + '" aria-label="Rate"></td>' +
        '<td class="num amt" data-amt>' + money(r.amt) + (r.min ? '<span class="minflag">minimum</span>' : "") + "</td>" +
        '<td class="noprint"><button type="button" class="x" data-del aria-label="Remove line">×</button></td></tr>';
    }).join("");
    renderSum();
  };
  var tbody = root.querySelector("[data-lines]");
  tbody.addEventListener("input", function (ev) {
    var tr = ev.target.closest("tr[data-i]"); if (!tr) return;
    var l = Q.lines[+tr.getAttribute("data-i")], k = ev.target.getAttribute("data-l");
    if (!k) return;
    l[k] = ev.target.value;
    if (k === "rate") l.rateEdited = true;
    save();
    var r = lineAmount(l);
    tr.querySelector("[data-amt]").innerHTML = money(r.amt) + (r.min ? '<span class="minflag">minimum</span>' : "");
    renderSum();
  });
  tbody.addEventListener("change", function (ev) {
    if (ev.target.getAttribute("data-l") === "unit") { var tr = ev.target.closest("tr[data-i]"); Q.lines[+tr.getAttribute("data-i")].unit = ev.target.value; save(); }
  });
  tbody.addEventListener("click", function (ev) {
    if (!ev.target.hasAttribute("data-del")) return;
    Q.lines.splice(+ev.target.closest("tr").getAttribute("data-i"), 1); save(); renderLines();
  });

  // ---------------------------------------------------------------- totals
  var totals = function () {
    var sub = Q.lines.reduce(function (s, l) { return s + lineAmount(l).amt; }, 0);
    var a = Q.adj, rows = [["Subtotal", sub]];
    var prem = 0;
    [["height", "Height / lift premium"], ["night", "Night or weekend premium"], ["rush", "Rush premium"]].forEach(function (p) {
      var pct = num(a[p[0]]); if (pct) { var v = sub * pct / 100; prem += v; rows.push([p[1] + " (" + pct + "%)", v]); }
    });
    if (num(a.mob)) rows.push(["Mobilization", num(a.mob)]);
    if (num(a.travel)) rows.push(["Travel crew: lodging and per diem", num(a.travel)]);
    var costs = sub + prem + num(a.mob) + num(a.travel);
    var op = costs * num(a.op) / 100; if (op) rows.push(["Overhead and profit (" + num(a.op) + "%)", op]);
    var afterOp = costs + op;
    var disc = afterOp * num(a.disc) / 100; if (disc) rows.push(["Discount (" + num(a.disc) + "%)", -disc]);
    var pre = afterOp - disc;
    var tax = pre * num(a.tax) / 100; if (tax) rows.push(["Sales tax (" + num(a.tax) + "%)", tax]);
    var total = pre + tax;
    return { rows: rows, total: total, sub: sub };
  };
  var renderSum = function () {
    var t = totals();
    var sf = num(Q.client.sqft);
    root.querySelector("[data-sum]").innerHTML = t.rows.map(function (r) { return "<tr><th>" + esc(r[0]) + "</th><td>" + money(r[1]) + "</td></tr>"; }).join("") +
      '<tr class="grand"><th>Total</th><td>' + money(t.total) + "</td></tr>" +
      (sf && t.total ? '<tr class="persf"><th>Per square foot</th><td>' + money(t.total / sf) + "</td></tr>" : "");
  };

  // ---------------------------------------------------------------- add-a-service finder
  var data = PB.items.map(function (r) { return { name: r[0], fam: r[1], n: norm(r[0]), an: (r[9] || []).map(norm), alts: r[9] || [] }; });
  var finder = root.querySelector("[data-estfinder]");
  var fin = finder.querySelector("input"), flist = finder.querySelector(".finder-list"), shown = [], active = -1;
  var search = function (raw) {
    var q = norm(raw), words = q.split(" ").filter(Boolean); if (q.length < 2) return [];
    var out = [];
    data.forEach(function (d) {
      var best = 0, via = "";
      var test = function (hay, alt, label) {
        if (!words.every(function (w) { return hay.indexOf(w) !== -1; })) return;
        var s = hay.indexOf(q) === 0 ? 100 : hay.indexOf(" " + q) !== -1 ? 85 : hay.indexOf(q) !== -1 ? 60 : 45;
        if (alt) s -= 12; if (s > best) { best = s; via = alt ? label : ""; }
      };
      test(d.n, false); d.an.forEach(function (a, i) { test(a, true, d.alts[i]); });
      if (best) out.push({ d: d, s: best - d.name.length / 200, via: via });
    });
    return out.sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
  };
  var renderFind = function () {
    shown = search(fin.value);
    if (!shown.length) { flist.hidden = true; fin.setAttribute("aria-expanded", "false"); return; }
    flist.innerHTML = shown.map(function (r, i) {
      var b = book(r.d.name);
      var price = b ? money(num(b[Q.tier || "mid"])).replace(/\.00$/, "") + " / " + (UNITS[b.unit] || b.unit).toLowerCase() : "";
      return '<li role="option" id="eo-' + i + '" aria-selected="' + (i === active) + '"><a href="#" data-pick="' + i + '"><span>' + esc(r.d.name) +
        (r.via ? '<span class="aka">also called ' + esc(r.via) + "</span>" : "") + '</span><span class="fam">' + esc(price) + "</span></a></li>";
    }).join("");
    flist.hidden = false; fin.setAttribute("aria-expanded", "true");
  };
  var pick = function (i) { var r = shown[i]; if (!r) return; addLine(r.d.name); fin.value = ""; flist.hidden = true; active = -1; };
  fin.addEventListener("input", function () { active = -1; renderFind(); });
  fin.addEventListener("keydown", function (ev) {
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      ev.preventDefault(); var n = shown.length; if (!n) return;
      active = ev.key === "ArrowDown" ? (active + 1) % n : (active - 1 + n) % n; renderFind();
    } else if (ev.key === "Enter") { ev.preventDefault(); pick(active >= 0 ? active : 0); }
    else if (ev.key === "Escape") { flist.hidden = true; }
  });
  flist.addEventListener("mousedown", function (ev) { var a = ev.target.closest("[data-pick]"); if (a) { ev.preventDefault(); pick(+a.getAttribute("data-pick")); } });
  document.addEventListener("click", function (ev) { if (!finder.contains(ev.target)) flist.hidden = true; });

  // ---------------------------------------------------------------- actions
  var csvCell = function (v) { v = String(v == null ? "" : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
  var quoteCsv = function () {
    var c = Q.client, rows = [];
    rows.push(["Quote", Q.no], ["Date", Q.date], ["Valid until", Q.valid], ["Company", co.name], ["License", co.license],
      ["Client", c.name], ["Client company", c.company], ["Project", c.project], ["Project type", c.type],
      ["Location", [c.address, c.city, c.zip].filter(Boolean).join(", ")], ["Square feet", c.sqft], ["Needed by", c.needed], []);
    rows.push(["#", "Service", "Notes", "Qty", "Unit", "Rate", "Amount", "Minimum applied"]);
    Q.lines.forEach(function (l, i) {
      var r = lineAmount(l);
      rows.push([i + 1, l.task, l.notes, num(l.qty), UNITS[l.unit] || l.unit, num(l.rate), r.amt.toFixed(2), r.min ? "yes" : ""]);
    });
    rows.push([]);
    var t = totals();
    t.rows.forEach(function (r) { rows.push(["", r[0], "", "", "", "", r[1].toFixed(2)]); });
    rows.push(["", "Total", "", "", "", "", t.total.toFixed(2)]);
    return rows.map(function (r) { return r.map(csvCell).join(","); }).join("\r\n");
  };
  var fileName = function (ext) { return (Q.no || "quote") + (Q.client.project ? "-" + norm(Q.client.project).replace(/ /g, "-") : "") + "." + ext; };

  root.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-act]"); if (!b || b.tagName === "INPUT") return;
    var act = b.getAttribute("data-act");
    if (act === "print") window.print();
    else if (act === "csv") download(fileName("csv"), quoteCsv(), "text/csv");
    else if (act === "save") download(fileName("json"), JSON.stringify({ quote: Q, company: co }, null, 2), "application/json");
    else if (act === "new") { if (!Q.lines.length || confirm("Start a new quote? The current one is cleared (save it first if you need it).")) { Q = newQuote(); save(); bindFields(); renderLines(); } }
    else if (act === "custom") addLine(fin.value.trim() || "");
    else if (act === "book-json") download("beyond-klean-price-book.json", JSON.stringify(exportBook(), null, 2), "application/json");
    else if (act === "book-csv") {
      var rows = [["Service", "Family", "Unit", "Low", "Typical", "High", "Minimum", "Basis"]];
      Object.keys(base).sort().forEach(function (k) { var x = book(k); rows.push([x.task, x.fam, UNITS[x.unit] || x.unit, x.low, x.mid, x.high, x.min, x.basis]); });
      download("beyond-klean-price-book.csv", rows.map(function (r) { return r.map(csvCell).join(","); }).join("\r\n"), "text/csv");
    }
    else if (act === "book-reset") { if (confirm("Reset every rate to the defaults? Your edits are removed.")) { overrides = {}; store.set("bk-est-pb", overrides); renderBook(); } }
  });
  var readFile = function (inp, fn) {
    var f = inp.files && inp.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () { try { fn(JSON.parse(r.result)); } catch (e) { alert("That file couldn't be read."); } inp.value = ""; };
    r.readAsText(f);
  };
  root.querySelector('[data-act="open"]').addEventListener("change", function (ev) {
    readFile(ev.target, function (d) { if (!d.quote || !Array.isArray(d.quote.lines)) throw new Error("bad"); Q = d.quote; save(); bindFields(); renderLines(); });
  });
  var exportBook = function () {
    var out = {}; Object.keys(base).forEach(function (k) { var x = book(k); out[k] = { unit: x.unit, low: x.low, mid: x.mid, high: x.high, min: x.min }; }); return { items: out };
  };
  root.querySelector('[data-act="book-import"]').addEventListener("change", function (ev) {
    readFile(ev.target, function (d) {
      var items = d.items || d, n = 0;
      Object.keys(items).forEach(function (k) { if (base[k]) { overrides[k] = items[k]; n++; } });
      store.set("bk-est-pb", overrides); renderBook(); alert(n + " rates imported.");
    });
  });

  // ---------------------------------------------------------------- price book table
  var pbq = root.querySelector("[data-pbq]");
  var renderBook = function () {
    var words = norm(pbq.value).split(" ").filter(Boolean), n = 0;
    var html = Object.keys(base).sort().map(function (k) {
      var x = book(k), b = base[k];
      var hay = norm(k + " " + b.fam + " " + b.alts.join(" "));
      if (!words.every(function (w) { return hay.indexOf(w) !== -1; })) return "";
      n++;
      var cell = function (f) { return '<td class="num"><input data-pb="' + f + '" inputmode="decimal" value="' + esc(x[f]) + '" aria-label="' + f + '"></td>'; };
      return '<tr data-k="' + esc(k) + '"' + (x.edited ? ' class="edited"' : "") + "><td>" + esc(k) + '<span class="small muted block">' + esc(b.fam) + "</span></td>" +
        '<td><select data-pb="unit" aria-label="Unit">' + unitOpts(x.unit) + "</select></td>" + cell("low") + cell("mid") + cell("high") + cell("min") +
        '<td class="small muted">' + esc(b.basis) + (b.conf ? " <em>(" + esc(b.conf) + ")</em>" : "") + "</td></tr>";
    }).join("");
    root.querySelector("[data-pb]").innerHTML = html;
    root.querySelector("[data-pbcount]").textContent = n + " services";
    var m = PB.meta || {};
    root.querySelector("[data-pbmeta]").textContent = [m.as_of ? "Rates as of " + m.as_of : "", m.region || "", m.notes || ""].filter(Boolean).join(" · ");
  };
  pbq.addEventListener("input", renderBook);
  var pbt = root.querySelector("[data-pb]");
  var pbEdit = function (ev) {
    var f = ev.target.getAttribute("data-pb"); if (!f) return;
    var k = ev.target.closest("tr").getAttribute("data-k");
    var o = overrides[k] || {}; o[f] = f === "unit" ? ev.target.value : num(ev.target.value);
    overrides[k] = o; store.set("bk-est-pb", overrides);
    ev.target.closest("tr").classList.add("edited");
  };
  pbt.addEventListener("input", pbEdit); pbt.addEventListener("change", pbEdit);

  // hide empty fields on the printed quote
  window.addEventListener("beforeprint", function () {
    root.querySelectorAll(".qdoc label").forEach(function (l) {
      var c = l.querySelector("input, select, textarea");
      l.classList.toggle("pempty", !!c && !String(c.value).trim());
    });
  });

  // ---------------------------------------------------------------- start
  renderCo(); bindFields(); renderLines();
})();
