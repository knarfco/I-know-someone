// Beyond Klean in-house estimator.
// Top: your costs (labor, travel, equipment, overhead, margin). Middle: the job, line by line.
// Bottom: hours, schedule, cost, price and profit, checked against market rates.
// Everything stays in this browser (localStorage); nothing is sent anywhere.
// The price book arrives encrypted (pricebook.enc.js) and is decrypted with the password on unlock.
(function () {
  var root = document.querySelector("[data-estimator]");
  var lock = document.querySelector("[data-lock]");
  if (!root || !lock || !window.BK_PB_ENC) return;

  // ================================================================ lock
  var b64 = function (s) { var bin = atob(s), u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u; };
  var unlock = function (pw) {
    var E = window.BK_PB_ENC, enc = new TextEncoder();
    return crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveKey"])
      .then(function (k) {
        return crypto.subtle.deriveKey({ name: "PBKDF2", salt: b64(E.salt), iterations: E.iter, hash: "SHA-256" },
          k, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
      })
      .then(function (key) { return crypto.subtle.decrypt({ name: "AES-GCM", iv: b64(E.iv) }, key, b64(E.ct)); })
      .then(function (buf) { return JSON.parse(new TextDecoder().decode(buf)); });
  };
  var SKEY = "bk-est-pw";
  var form = lock.querySelector("[data-lockform]"), pwIn = form.querySelector("input"), err = lock.querySelector("[data-lockerr]");
  var fail = function (msg) { err.textContent = msg; err.hidden = false; pwIn.select(); };
  var opened = function (data) { lock.hidden = true; root.hidden = false; start(data); };
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (!window.crypto || !crypto.subtle) { fail("This page needs a secure (https) connection to unlock."); return; }
    var pw = pwIn.value;
    unlock(pw).then(function (d) {
      try { sessionStorage.setItem(SKEY, pw); } catch (e) { /* storage unavailable */ }
      opened(d);
    }, function () { fail("That password didn't work. Try again."); });
  });
  root.querySelector("[data-lockout]").addEventListener("click", function () {
    try { sessionStorage.removeItem(SKEY); } catch (e) { /* storage unavailable */ }
    location.reload();
  });
  var remembered = null;
  try { remembered = sessionStorage.getItem(SKEY); } catch (e) { /* storage unavailable */ }
  if (remembered && window.crypto && crypto.subtle) unlock(remembered).then(opened, function () { pwIn.focus(); });
  else pwIn.focus();

  // ================================================================ helpers
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var norm = function (s) { return String(s).toLowerCase().replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim(); };
  var num = function (v) { var n = parseFloat(String(v == null ? "" : v).replace(/[^0-9.\-]/g, "")); return isFinite(n) ? n : 0; };
  var money = function (n, dp) { dp = dp == null ? 2 : dp; return (n < 0 ? "-$" : "$") + Math.abs(n).toLocaleString("en-US", { minimumFractionDigits: dp, maximumFractionDigits: dp }); };
  var money0 = function (n) { return money(n, 0); };
  var hrs = function (n) { return (Math.round(n * 10) / 10).toLocaleString("en-US") + " hr"; };
  var pct = function (n) { return isFinite(n) ? (Math.round(n * 10) / 10) + "%" : "–"; };
  var rateFmt = function (n) { n = num(n); return n >= 10 ? n.toFixed(2) : String(Math.round(n * 10000) / 10000); };
  var uid = function () { return Math.random().toString(36).slice(2, 10); };
  var today = function (plus) { var d = new Date(); d.setDate(d.getDate() + (plus || 0)); return d.toISOString().slice(0, 10); };
  var clone = function (o) { return JSON.parse(JSON.stringify(o)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
  };
  var download = function (name, text, type) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: type }));
    a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  };
  var csvCell = function (v) { v = String(v == null ? "" : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
  var csv = function (rows) { return rows.map(function (r) { return r.map(csvCell).join(","); }).join("\r\n"); };
  var getPath = function (o, p) { return p.split(".").reduce(function (x, k) { return x == null ? x : x[k]; }, o); };
  var setPath = function (o, p, v) { var ks = p.split("."), last = ks.pop(); ks.reduce(function (x, k) { if (x[k] == null) x[k] = {}; return x[k]; }, o)[last] = v; };

  var started = false;
  function start(D) {
    if (started) return;
    started = true;

    var UNITS = D.units, FREQ = D.freq;
    var SHORT = { sqft: "sq ft", lf: "lin ft", each: "ea", pane: "panes", fixture: "fixtures", room: "rooms", hour: "hrs", unit: "units", floor: "floors",
      opening: "openings", load: "loads", cy: "cu yd", ton: "tons", lot: "lot", day: "days", flight: "flights", month: "months" };
    var uShort = function (u) { return SHORT[u] || (UNITS[u] || u).toLowerCase(); };
    var ROLES = D.roles.map(function (r) { return { key: r[0], label: r[1], wage: r[2] }; });
    var ROLE_LABEL = {}; ROLES.forEach(function (r) { ROLE_LABEL[r.key] = r.label; });
    var HEIGHT = { floor: ["Floor level", 1], ladder: ["Ladder", 1.25], lift: ["Lift", 1.6] };
    var SOIL = { light: ["Light", .85], normal: ["Normal", 1], heavy: ["Heavy", 1.35] };
    var FREQ_KEYS = Object.keys(FREQ);

    // ------------------------------------------------------------ libraries (+ local overrides)
    var LIB = { project: {}, routine: {} };
    D.items.forEach(function (r) {
      LIB.project[r[0]] = { task: r[0], group: r[1], unit: r[2], low: r[3], mid: r[4], high: r[5], min: r[6], basis: r[7], conf: r[8],
        alts: r[9] || [], phase: r[10], rate: r[11], mat: r[12], role: r[13], scope: r[14] || [] };
    });
    D.routine.forEach(function (r) {
      LIB.routine[r[0]] = { task: r[0], group: r[1], unit: r[2], rate: r[3], mat: r[4], freq: r[5], desc: r[6], role: r[2] === "hour" && /Supervisor/.test(r[0]) ? "lead" : "general", alts: [], scope: [r[6]] };
    });
    var OV = store.get("bk-e2-pb", { project: {}, routine: {} });
    var book = function (src, task) {
      var b = LIB[src] && LIB[src][task]; if (!b) return null;
      var o = (OV[src] || {})[task] || {}, out = {};
      Object.keys(b).forEach(function (k) { out[k] = o[k] != null ? o[k] : b[k]; });
      out.edited = !!(OV[src] || {})[task];
      return out;
    };

    // ------------------------------------------------------------ company and defaults
    var DEFAULT_TERMS = "Pricing is based on the scope, quantities and schedule listed above. Work outside this scope is billed as a change order.\n" +
      "Owner or GC provides water, power and site access. Lifts and dumpsters are included only where listed.\n" +
      "One re-clean of punch items is included. Re-cleans caused by other trades are billed at our hourly rate.\n" +
      "Net 30 from invoice. This quote is valid for the number of days shown.";
    var wages = {}; ROLES.forEach(function (r) { wages[r.key] = r.wage; });
    var DEFAULT_COSTS = { wages: wages, burden: 30, supPct: 10, crew: 4, shift: 8, night: false, nightPct: 15,
      travel: "local", vehicles: 1, perMile: 0.70, dailyMiles: 40, oneWay: 300, lodging: 110, perRoom: 2, perDiem: 60, travelOther: 0,
      equip: [], disposal: 0, other: 0, monthlyTravel: 0, overhead: 12, margin: 25, method: "market", level: "mid",
      billExtras: true, discount: 0, tax: 0, adjust: 0 };
    var CO = store.get("bk-e2-co", null) || { name: "", license: "", phone: "", email: "", address: "", web: "", terms: DEFAULT_TERMS, defaults: clone(DEFAULT_COSTS) };
    var saveCo = function () { store.set("bk-e2-co", CO); };
    var costsDefaults = function () { var c = clone(DEFAULT_COSTS); var d = CO.defaults || {}; Object.keys(d).forEach(function (k) { c[k] = clone(d[k]); }); c.wages = Object.assign({}, DEFAULT_COSTS.wages, d.wages || {}); return c; };

    var nextNo = function () {
      var n = store.get("bk-e2-seq", 1000) + 1; store.set("bk-e2-seq", n);
      return "BK-E" + String(new Date().getFullYear()).slice(2) + "-" + n;
    };
    var newEstimate = function (mode) {
      return { id: uid(), no: nextNo(), created: today(0), updated: today(0), mode: mode || "project", status: "Draft",
        project: { name: "", type: "", sqft: "", city: "", zip: "", start: "", due: "" },
        client: { name: "", company: "", phone: "", email: "" },
        costs: costsDefaults(), lines: [],
        review: { preparedBy: "", reviewedBy: "", approvedOn: "", validDays: 30, notes: "" },
        terms: CO.terms || DEFAULT_TERMS, ui: { area: "", itemized: true, scopeOnQuote: false } };
    };
    var E = store.get("bk-e2-cur", null) || newEstimate("project");
    var saveCur = function () { E.updated = today(0); store.set("bk-e2-cur", E); };

    // ================================================================ calculation
    var loaded = function (c, role) {
      var w = num((c.wages || {})[role]);
      return w * (1 + num(c.burden) / 100) * (c.night ? 1 + num(c.nightPct) / 100 : 1);
    };
    var lineBase = function (l) { return l.src === "custom" ? null : book(l.src, l.task); };

    function calc(est) {
      var c = est.costs, rec = est.mode === "recurring";
      var OH = num(c.overhead) / 100, M = Math.min(num(c.margin), 95) / 100, ADJ = 1 + num(c.adjust) / 100;
      var out = { lines: [], rec: rec };
      var totH = 0, totHOnce = 0;
      // pass 1: hours, labor, materials
      est.lines.forEach(function (l) {
        var b = lineBase(l) || {};
        var q = num(l.qty), rate = l.rate !== "" && l.rate != null ? num(l.rate) : num(b.rate);
        var hf = (HEIGHT[l.height] || HEIGHT.floor)[1], sf = (SOIL[l.soil] || SOIL.normal)[1];
        var once = rec && l.freq === "once";
        var fm = rec && !once ? (FREQ[l.freq] || FREQ.monthly)[1] : 1;
        var h = rate > 0 ? q / rate * hf * sf * fm : 0;
        var matU = l.mat !== "" && l.mat != null ? num(l.mat) : num(b.mat);
        var mat = q * matU * (l.soil === "heavy" ? 1.2 : l.soil === "light" ? .9 : 1) * fm;
        var lab = h * loaded(c, l.role || b.role || "general");
        var r = { l: l, b: b, q: q, rate: rate, hours: h, labor: lab, mat: mat, once: once, fm: fm };
        out.lines.push(r);
        if (once) totHOnce += h; else totH += h;
      });
      // supervision, allocated by hours
      var supRate = loaded(c, "lead"), supPct = num(c.supPct) / 100;
      out.lines.forEach(function (r) { r.sup = r.hours * supPct * supRate; r.supH = r.hours * supPct; });
      var crewHours = totH * (1 + supPct), onceHours = totHOnce * (1 + supPct);
      // schedule
      var crew = Math.max(1, num(c.crew)), shift = Math.max(1, num(c.shift));
      var days = rec ? 0 : (crewHours > 0 ? Math.ceil(crewHours / (crew * shift)) : 0);
      // extras
      var travel = 0, tParts = [];
      if (!rec) {
        if (c.travel === "travel") {
          var miles = num(c.vehicles) * num(c.oneWay) * 2 * num(c.perMile);
          var rooms = Math.ceil(crew / Math.max(1, num(c.perRoom)));
          var lodging = days ? rooms * days * num(c.lodging) : 0;
          var diem = days ? crew * (days + 1) * num(c.perDiem) : 0;
          travel = miles + lodging + diem + num(c.travelOther);
          tParts = [["Mileage", miles], ["Lodging (" + rooms + " rooms × " + days + " nights)", lodging], ["Per diem", diem], ["Other travel", num(c.travelOther)]];
        } else {
          travel = num(c.vehicles) * num(c.dailyMiles) * num(c.perMile) * days;
          tParts = [["Mileage (" + days + " days)", travel]];
        }
      } else {
        travel = num(c.monthlyTravel);
        tParts = [["Monthly travel", travel]];
      }
      var equip = 0, eParts = [];
      (c.equip || []).forEach(function (q) {
        var d = rec ? 1 : (q.days === "" || q.days == null ? days : num(q.days));
        var v = num(q.qty) * d * num(q.rate); equip += v; eParts.push([q.name + (rec ? "" : " (" + num(q.qty) + " × " + d + " days)"), v]);
      });
      var site = num(c.disposal) + num(c.other);
      var extras = travel + equip + site, extrasLoaded = extras * (1 + OH);
      // pass 2: cost and price per line
      var marketOn = !rec && c.method === "market";
      var level = c.level || "mid";
      var sumP = 0, mLow = 0, mMid = 0, mHigh = 0;
      out.lines.forEach(function (r) {
        var direct = r.labor + r.sup + r.mat;
        r.cost = direct * (1 + OH);
        var unitP = r.l.price !== "" && r.l.price != null ? num(r.l.price) : null;
        var b = r.b, min = r.l.min !== "" && r.l.min != null ? num(r.l.min) : num(b.min);
        var p;
        if (unitP != null) p = r.q * unitP * r.fm;
        else if (marketOn && b && b.mid) p = r.q * num(b[level]);
        else p = M < 1 ? r.cost / (1 - M) : r.cost;
        if (!rec && min > 0 && r.q > 0 && p < min) { p = min; r.minApplied = true; }
        r.unitAuto = r.q ? (marketOn && b && b.mid ? num(b[level]) : (M < 1 ? r.cost / (1 - M) : r.cost) / (r.q * r.fm || 1)) : 0;
        r.priceRaw = p;
        if (!rec && b && b.mid) {
          var mm = function (v) { var x = r.q * num(v); return min > 0 && r.q > 0 && x < min ? min : x; };
          mLow += mm(b.low); mMid += mm(b.mid); mHigh += mm(b.high); r.inMarket = true;
        }
        sumP += p;
      });
      // extras: billed as lines, or folded into line prices (cost-plus) / absorbed (market)
      var extraLines = [];
      if (c.billExtras) {
        var ep = function (v) { return M < 1 ? v * (1 + OH) / (1 - M) * ADJ : v * (1 + OH) * ADJ; };
        if (travel > 0) extraLines.push({ name: rec ? "Travel" : "Mobilization and travel", cost: travel * (1 + OH), price: ep(travel) });
        if (equip > 0) extraLines.push({ name: "Equipment and lifts", cost: equip * (1 + OH), price: ep(equip) });
        if (site > 0) extraLines.push({ name: "Disposal and site costs", cost: site * (1 + OH), price: ep(site) });
      }
      var fold = !c.billExtras && !marketOn && extras > 0 ? (M < 1 ? extrasLoaded / (1 - M) : extrasLoaded) : 0;
      var recurringP = 0, onceP = 0, recurringC = 0, onceC = 0;
      out.lines.forEach(function (r) {
        var share = sumP > 0 ? r.priceRaw / sumP : (out.lines.length ? 1 / out.lines.length : 0);
        r.price = (r.priceRaw + fold * share) * ADJ;
        r.profit = r.price - r.cost;
        r.margin = r.price ? r.profit / r.price * 100 : 0;
        if (r.once) { onceP += r.price; onceC += r.cost; } else { recurringP += r.price; recurringC += r.cost; }
      });
      var mYours = out.lines.reduce(function (s, r) { return s + (r.inMarket ? r.price * (1 - num(c.discount) / 100) : 0); }, 0);
      var extrasP = extraLines.reduce(function (s, x) { return s + x.price; }, 0);
      var disc = num(c.discount) / 100, tax = num(c.tax) / 100;
      // project: one total. recurring: monthly (recurring lines + extras) and one-time.
      var basePrice = rec ? recurringP + extrasP : recurringP + onceP + extrasP;
      var baseCost = (rec ? recurringC : recurringC + onceC) + extrasLoaded;
      var discount = basePrice * disc, net = basePrice - discount, taxAmt = net * tax;
      var profit = net - baseCost;
      var labor = 0, supC = 0, matC = 0;
      out.lines.forEach(function (r) { if (rec && r.once) return; labor += r.labor; supC += r.sup; matC += r.mat; });
      var overheadAmt = (labor + supC + matC + extras) * OH;
      var sqft = num(est.project.sqft);
      out.t = {
        crewHours: crewHours, baseHours: totH, supHours: totH * supPct, onceHours: onceHours, crew: crew, shift: shift, days: days,
        travel: travel, tParts: tParts, equip: equip, eParts: eParts, site: site, extras: extras, extraLines: extraLines,
        labor: labor, sup: supC, mat: matC, overhead: overheadAmt, cost: baseCost,
        subtotal: basePrice, discount: discount, net: net, tax: taxAmt, total: net + taxAmt, profit: profit,
        margin: net ? profit / net * 100 : 0, target: M * 100,
        perHour: crewHours ? profit / crewHours : 0, perSqft: sqft ? net / sqft : 0, sqft: sqft,
        mLow: mLow, mMid: mMid, mHigh: mHigh, mYours: mYours, marketOn: marketOn,
        onceP: onceP * (1 - disc), onceC: onceC, onceProfit: onceP * (1 - disc) - onceC,
        nightlyHours: rec ? crewHours / 21.67 : 0, perNight: rec ? crewHours / 21.67 / shift : 0, fte: rec ? crewHours / 173.3 : 0
      };
      return out;
    }

    // ================================================================ rendering: estimate
    var $ = function (sel) { return root.querySelector(sel); };
    var $$ = function (sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); };

    var bindFields = function () {
      $$("[data-k]").forEach(function (inp) {
        var v = getPath(E, inp.getAttribute("data-k"));
        if (inp.type === "checkbox") inp.checked = !!v; else inp.value = v == null ? "" : v;
      });
      $("[data-show=no]").textContent = E.no;
      $$("[data-mode]").forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-mode") === E.mode); });
      $$("[data-only]").forEach(function (el) { el.hidden = el.getAttribute("data-only") !== E.mode; });
      $$("[data-travel]").forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-travel") === E.costs.travel); });
      $$("[data-travel-only]").forEach(function (el) { el.hidden = el.getAttribute("data-travel-only") !== E.costs.travel; });
      $("[data-adjv]").textContent = (num(E.costs.adjust) > 0 ? "+" : "") + num(E.costs.adjust) + "%";
      renderRoles(); renderEquip(); renderTemplates(); renderAreas();
    };
    root.addEventListener("input", function (ev) {
      var k = ev.target.getAttribute && ev.target.getAttribute("data-k");
      if (!k || !ev.target.closest("[data-pane=est]")) return;
      var v = ev.target.type === "checkbox" ? ev.target.checked : ev.target.value;
      setPath(E, k, v);
      if (k === "status" && v === "Approved" && !E.review.approvedOn) { E.review.approvedOn = today(0); var a = $('[data-k="review.approvedOn"]'); if (a) a.value = E.review.approvedOn; }
      if (k === "costs.adjust") $("[data-adjv]").textContent = (num(v) > 0 ? "+" : "") + num(v) + "%";
      if (k === "review.preparedBy") $$('[data-k="review.preparedBy"]').forEach(function (x) { if (x !== ev.target) x.value = v; });
      saveCur(); refresh();
    });
    root.addEventListener("change", function (ev) {
      if (ev.target.type === "checkbox" && ev.target.getAttribute("data-k")) { setPath(E, ev.target.getAttribute("data-k"), ev.target.checked); saveCur(); refresh(); }
    });
    $$("[data-mode]").forEach(function (b) {
      b.addEventListener("click", function () {
        var m = b.getAttribute("data-mode"); if (m === E.mode) return;
        if (E.lines.length && !confirm("Switch estimate type? Lines stay, but recurring estimates price by month.")) return;
        E.mode = m;
        E.lines.forEach(function (l) { if (m === "recurring" && !l.freq) l.freq = (lineBase(l) || {}).freq || "monthly"; });
        saveCur(); bindFields(); renderLines(); refresh();
      });
    });
    $$("[data-travel]").forEach(function (b) {
      b.addEventListener("click", function () { E.costs.travel = b.getAttribute("data-travel"); saveCur(); bindFields(); refresh(); });
    });

    // roles table
    var renderRoles = function () {
      $("[data-roles]").innerHTML = ROLES.map(function (r) {
        return "<tr><td>" + esc(r.label) + '</td><td class="num"><input data-wage="' + r.key + '" inputmode="decimal" value="' + esc(E.costs.wages[r.key]) + '" aria-label="' + esc(r.label) + ' wage"></td>' +
          '<td class="num" data-loaded="' + r.key + '"></td></tr>';
      }).join("");
    };
    root.addEventListener("input", function (ev) {
      var k = ev.target.getAttribute && ev.target.getAttribute("data-wage"); if (!k) return;
      E.costs.wages[k] = ev.target.value; saveCur(); refresh();
    });

    // equipment
    var EQ = D.equipment;
    $("[data-eq-pick]").innerHTML = '<option value="">+ Add equipment…</option>' + EQ.map(function (q, i) { return '<option value="' + i + '">' + esc(q[0]) + "</option>"; }).join("") + '<option value="custom">Other equipment…</option>';
    $("[data-eq-pick]").addEventListener("change", function (ev) {
      var v = ev.target.value; if (!v) return;
      var q = v === "custom" ? ["Other equipment", 0] : EQ[+v];
      (E.costs.equip = E.costs.equip || []).push({ name: q[0], qty: 1, days: "", rate: q[1] });
      ev.target.value = ""; saveCur(); renderEquip(); refresh();
    });
    var renderEquip = function () {
      var rec = E.mode === "recurring";
      var list = E.costs.equip || [];
      $("[data-equip]").innerHTML = list.length ? '<table class="e-mini"><thead><tr><th>Item</th><th class="num">Qty</th>' + (rec ? "" : '<th class="num">Days</th>') +
        '<th class="num">' + (rec ? "$ / month" : "$ / day") + "</th><th></th></tr></thead><tbody>" + list.map(function (q, i) {
          return '<tr data-eq="' + i + '"><td><input data-eqf="name" value="' + esc(q.name) + '" aria-label="Equipment"></td>' +
            '<td class="num"><input data-eqf="qty" inputmode="decimal" value="' + esc(q.qty) + '" aria-label="Quantity"></td>' +
            (rec ? "" : '<td class="num"><input data-eqf="days" inputmode="decimal" value="' + esc(q.days) + '" placeholder="auto" aria-label="Days"></td>') +
            '<td class="num"><input data-eqf="rate" inputmode="decimal" value="' + esc(q.rate) + '" aria-label="Rate"></td>' +
            '<td><button type="button" class="x" data-eqx="' + i + '" aria-label="Remove">×</button></td></tr>';
        }).join("") + "</tbody></table>" + (rec ? "" : '<p class="small muted">Days left blank use the scheduled days on site.</p>') : '<p class="small muted">No equipment yet.</p>';
    };
    root.addEventListener("input", function (ev) {
      var f = ev.target.getAttribute && ev.target.getAttribute("data-eqf"); if (!f) return;
      E.costs.equip[+ev.target.closest("[data-eq]").getAttribute("data-eq")][f] = ev.target.value; saveCur(); refresh();
    });
    root.addEventListener("click", function (ev) {
      var x = ev.target.closest && ev.target.closest("[data-eqx]"); if (!x) return;
      E.costs.equip.splice(+x.getAttribute("data-eqx"), 1); saveCur(); renderEquip(); refresh();
    });

    // templates
    var userTpl = store.get("bk-e2-tpl", []);
    var renderTemplates = function () {
      var all = D.templates.map(function (t, i) { return { key: "b" + i, name: t[0], mode: t[1] }; })
        .concat(userTpl.map(function (t, i) { return { key: "u" + i, name: t.name, mode: t.mode, user: true }; }));
      $("[data-tpls]").innerHTML = '<span class="small muted">Start from a template:</span>' + all.filter(function (t) { return t.mode === E.mode; }).map(function (t) {
        return '<button type="button" class="chip" data-tpl="' + t.key + '">' + esc(t.name) + (t.user ? " ★" : "") + "</button>";
      }).join("");
    };
    root.addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest("[data-tpl]"); if (!b) return;
      var key = b.getAttribute("data-tpl"), sqft = num(E.project.sqft);
      if (key[0] === "b") {
        if (!sqft) { alert("Enter the building square feet first (section 1). The template sizes every line from it."); $('[data-k="project.sqft"]').focus(); return; }
        var t = D.templates[+key.slice(1)];
        t[2].forEach(function (x) {
          var q = x[2] === "sqft" ? sqft * x[1] : x[1];
          q = q >= 10 ? Math.round(q) : Math.max(1, Math.round(q * 10) / 10);
          addLine(x[0], LIB.project[x[0]] ? "project" : "routine", { qty: String(q), area: x[3] }, true);
        });
      } else {
        clone(userTpl[+key.slice(1)].lines).forEach(function (l) { l.id = uid(); E.lines.push(l); });
      }
      saveCur(); renderLines(); refresh();
    });

    var renderAreas = function () {
      var seen = {}; E.lines.forEach(function (l) { if (l.area) seen[l.area] = 1; });
      ["Rough", "Light clean", "Final", "Punch", "Overhead", "Exterior", "Nightly", "Weekly", "Periodic"].forEach(function (a) { seen[a] = 1; });
      $("#e-areas").innerHTML = Object.keys(seen).map(function (a) { return '<option value="' + esc(a) + '">'; }).join("");
    };

    // ------------------------------------------------------------ lines
    var addLine = function (task, src, extra, silent) {
      var b = src === "custom" ? null : book(src, task);
      var l = { id: uid(), task: task || "Custom item", src: src, area: E.ui.area || "", qty: "", unit: b ? b.unit : "each",
        freq: E.mode === "recurring" ? (b && b.freq) || "monthly" : "", height: "floor", soil: "normal",
        role: b ? b.role : "general", rate: "", mat: "", price: "", min: "", notes: "" };
      if (src === "custom") { l.rate = 1; l.unit = "hour"; }
      if (b && b.unit === "sqft" && num(E.project.sqft) && E.mode === "project") l.qty = String(num(E.project.sqft));
      if (/overhead|ceiling|high-bay|deck|joist|high dust/i.test(task) && src !== "custom") l.height = "lift";
      Object.assign(l, extra || {});
      E.lines.push(l);
      if (!silent) {
        saveCur(); renderLines(); refresh();
        var cards = $$("[data-lines] .ln"); var last = cards[cards.length - 1];
        var f = last && last.querySelector(src === "custom" ? '[data-f="task"]' : '[data-f="qty"]'); if (f) f.focus();
      }
    };
    var opt = function (pairs, sel) { return pairs.map(function (p) { return '<option value="' + esc(p[0]) + '"' + (String(p[0]) === String(sel) ? " selected" : "") + ">" + esc(p[1]) + "</option>"; }).join(""); };
    var unitPairs = function () { return Object.keys(UNITS).map(function (u) { return [u, UNITS[u]]; }); };
    var renderLines = function () {
      var rec = E.mode === "recurring";
      var box = $("[data-lines]");
      if (!E.lines.length) { box.innerHTML = '<p class="e-empty">No tasks yet. Add one above or start from a template.</p>'; renderAreas(); return; }
      box.innerHTML = E.lines.map(function (l, i) {
        var b = lineBase(l) || {};
        var scope = (b.scope || []).length ? '<div class="ln-scope"><strong>What this task covers</strong><ul>' + b.scope.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul></div>" : "";
        return '<div class="ln" data-i="' + i + '">' +
          '<div class="ln-h"><span class="ln-n">' + (i + 1) + "</span>" +
          '<input class="ln-task" data-f="task" value="' + esc(l.task) + '"' + (l.src === "custom" ? "" : " readonly") + ' aria-label="Task">' +
          '<input class="ln-area" data-f="area" value="' + esc(l.area) + '" list="e-areas" placeholder="Area / phase" aria-label="Area or phase">' +
          '<button type="button" class="ln-more" data-more aria-expanded="' + (l.open ? "true" : "false") + '">Details</button>' +
          '<button type="button" class="x" data-del aria-label="Remove line">×</button></div>' +
          '<div class="ln-in">' +
          '<label>Qty<input data-f="qty" inputmode="decimal" value="' + esc(l.qty) + '"></label>' +
          '<label>Unit<select data-f="unit">' + opt(unitPairs(), l.unit) + "</select></label>" +
          (rec ? '<label>How often<select data-f="freq">' + opt(FREQ_KEYS.map(function (k) { return [k, FREQ[k][0]]; }), l.freq) + "</select></label>" : "") +
          '<label>Height<select data-f="height">' + opt(Object.keys(HEIGHT).map(function (k) { return [k, HEIGHT[k][0]]; }), l.height) + "</select></label>" +
          '<label>Soil<select data-f="soil">' + opt(Object.keys(SOIL).map(function (k) { return [k, SOIL[k][0]]; }), l.soil) + "</select></label>" +
          '<label>Crew<select data-f="role">' + opt(ROLES.map(function (r) { return [r.key, r.label]; }), l.role) + "</select></label>" +
          "</div>" +
          '<div class="ln-out" data-out></div>' +
          '<div class="ln-det"' + (l.open ? "" : " hidden") + ">" +
          '<div class="ln-in">' +
          '<label>Production (' + esc((UNITS[l.unit] || l.unit).toLowerCase()) + ' per worker-hour)<input data-f="rate" inputmode="decimal" value="' + esc(l.rate) + '" placeholder="' + esc(rateFmt(b.rate || 0)) + '"></label>' +
          '<label>Chemicals and supplies ($ per unit)<input data-f="mat" inputmode="decimal" value="' + esc(l.mat) + '" placeholder="' + esc(rateFmt(b.mat || 0)) + '"></label>' +
          '<label>Price per unit ($)<input data-f="price" inputmode="decimal" value="' + esc(l.price) + '" data-autoprice placeholder=""></label>' +
          (rec ? "" : '<label>Minimum charge ($)<input data-f="min" inputmode="decimal" value="' + esc(l.min) + '" placeholder="' + esc(b.min || 0) + '"></label>') +
          "</div>" +
          '<label class="e-block">Notes<input data-f="notes" value="' + esc(l.notes) + '" placeholder="Areas, floors, access, assumptions"></label>' +
          (b.basis ? '<p class="small muted">Market basis: ' + esc(b.basis) + (b.conf ? " (" + esc(b.conf) + ")" : "") + "</p>" : "") +
          scope + "</div></div>";
      }).join("");
      renderAreas();
    };
    var box = $("[data-lines]");
    box.addEventListener("input", function (ev) {
      var card = ev.target.closest(".ln"), f = ev.target.getAttribute("data-f"); if (!card || !f) return;
      E.lines[+card.getAttribute("data-i")][f] = ev.target.value; saveCur(); refresh();
    });
    box.addEventListener("change", function (ev) {
      var card = ev.target.closest(".ln"), f = ev.target.getAttribute("data-f"); if (!card || !f) return;
      E.lines[+card.getAttribute("data-i")][f] = ev.target.value; saveCur();
      if (f === "unit") renderLines();
      refresh();
    });
    box.addEventListener("click", function (ev) {
      var card = ev.target.closest(".ln"); if (!card) return;
      var i = +card.getAttribute("data-i");
      if (ev.target.closest("[data-del]")) { E.lines.splice(i, 1); saveCur(); renderLines(); refresh(); }
      else if (ev.target.closest("[data-more]")) {
        E.lines[i].open = !E.lines[i].open; saveCur();
        card.querySelector(".ln-det").hidden = !E.lines[i].open;
        ev.target.closest("[data-more]").setAttribute("aria-expanded", E.lines[i].open);
      }
    });

    // ------------------------------------------------------------ outputs + summary
    var bar = function (t) {
      var segs = [["Labor", t.labor, "lab"], ["Supervision", t.sup, "sup"], ["Materials", t.mat, "mat"], ["Equipment", t.equip, "eq"],
        ["Travel", t.travel, "tr"], ["Site", t.site, "site"], ["Overhead", t.overhead, "oh"], ["Profit", Math.max(0, t.profit), "pr"]];
      var tot = segs.reduce(function (s, x) { return s + Math.max(0, x[1]); }, 0) || 1;
      return '<div class="e-bar-h" role="img" aria-label="Where each dollar goes">' + segs.filter(function (x) { return x[1] > 0; }).map(function (x) {
        return '<span class="seg-' + x[2] + '" style="width:' + (x[1] / tot * 100).toFixed(2) + '%" title="' + x[0] + " " + money0(x[1]) + '"></span>';
      }).join("") + '</div><ul class="e-legend">' + segs.filter(function (x) { return x[1] > 0; }).map(function (x) {
        return '<li><i class="seg-' + x[2] + '"></i>' + x[0] + " <b>" + money0(x[1]) + "</b> <span>" + pct(x[1] / tot * 100) + "</span></li>";
      }).join("") + "</ul>";
    };
    var refresh = function () {
      var R = calc(E), t = R.t, rec = R.rec;
      // loaded rates
      ROLES.forEach(function (r) { var el = $('[data-loaded="' + r.key + '"]'); if (el) el.textContent = money(loaded(E.costs, r.key)); });
      // per-line outputs
      $$("[data-lines] .ln").forEach(function (card, i) {
        var r = R.lines[i]; if (!r) return;
        var low = r.margin < t.target - 0.5;
        card.querySelector("[data-out]").innerHTML =
          "<div><span>Hours" + (rec && !r.once ? " / mo" : "") + "</span><b>" + hrs(r.hours) + "</b></div>" +
          "<div><span>Labor</span><b>" + money0(r.labor + r.sup) + "</b></div>" +
          "<div><span>Materials</span><b>" + money0(r.mat) + "</b></div>" +
          "<div><span>Cost w/ overhead</span><b>" + money0(r.cost) + "</b></div>" +
          "<div><span>Price" + (rec && !r.once ? " / mo" : r.once ? " (one time)" : "") + "</span><b>" + money0(r.price) + (r.minApplied ? ' <em class="minflag">min</em>' : "") + "</b></div>" +
          '<div class="' + (low ? "warnv" : "okv") + '"><span>Margin</span><b>' + pct(r.margin) + "</b></div>";
        var ap = card.querySelector("[data-autoprice]"); if (ap) ap.placeholder = rateFmt(r.unitAuto) + " auto";
      });
      // summary
      var S = [];
      var row = function (k, v, cls) { return '<tr class="' + (cls || "") + '"><th>' + k + "</th><td>" + v + "</td></tr>"; };
      var sched = rec
        ? row("Crew-hours per month", hrs(t.crewHours)) + row("Hours per night (21.7 work nights)", hrs(t.nightlyHours)) +
          row("Cleaners per night at " + t.shift + " hr shifts", (Math.round(t.perNight * 10) / 10)) + row("Full-time equivalents", (Math.round(t.fte * 100) / 100)) +
          (t.onceHours ? row("One-time service hours", hrs(t.onceHours)) : "")
        : row("Crew-hours (incl. supervision)", hrs(t.crewHours)) + row("Crew", t.crew + " people × " + t.shift + " hr shifts") +
          row("Days on site", t.days || "–");
      var costs = row("Labor", money(t.labor)) + row("Supervision", money(t.sup)) + row("Chemicals and supplies", money(t.mat)) +
        row("Equipment", money(t.equip)) + row(rec ? "Travel" : "Travel and mobilization", money(t.travel)) + row("Disposal and site", money(t.site)) +
        row("Overhead (" + num(E.costs.overhead) + "%)", money(t.overhead)) + row(rec ? "Total monthly cost" : "Total cost", money(t.cost), "strong");
      var price = row(rec ? "Monthly price before discount" : "Price before discount", money(t.subtotal)) +
        (t.discount ? row("Discount", "-" + money(t.discount)) : "") + row(rec ? "Monthly price" : "Price", money(t.net), "strong") +
        (t.tax ? row("Sales tax", money(t.tax)) : "") + row(rec ? "Monthly total to customer" : "Total to customer", money(t.total), "grand");
      var low = t.margin < t.target - 0.5;
      var prof = row(rec ? "Monthly gross profit" : "Gross profit", money(t.profit), low ? "warnv" : "okv") +
        row("Margin", pct(t.margin) + " <span class='muted small'>target " + pct(t.target) + "</span>", low ? "warnv" : "okv") +
        row("Profit per crew-hour", money(t.perHour)) +
        (t.sqft ? row(rec ? "Price per sq ft per month" : "Price per sq ft", money(t.perSqft, 3)) : "") +
        (rec ? row("Annual contract value", money0(t.net * 12)) + (t.onceP ? row("One-time services price", money(t.onceP)) + row("One-time services profit", money(t.onceProfit)) : "") : "");
      var market = "";
      if (!rec && t.mMid) {
        var pos = t.mYours / t.mMid * 100;
        market = '<div class="e-market"><h3>Market check</h3><p>For the price-book tasks in this scope (before travel, equipment and site costs), typical market pricing runs <b>' + money0(t.mLow) + "</b> (low) · <b>" + money0(t.mMid) + "</b> (typical) · <b>" + money0(t.mHigh) +
          "</b> (high). Your price for those tasks is <b>" + money0(t.mYours) + "</b>, " + pct(pos) + " of typical.</p>" +
          '<div class="e-scale"><span class="lo"></span><span class="hi"></span><i style="left:' + Math.max(0, Math.min(100, (t.mYours - t.mLow) / Math.max(1, t.mHigh - t.mLow) * 100)).toFixed(1) + '%"></i></div>' +
          '<p class="small muted e-scale-l"><span>Low</span><span>Typical</span><span>High</span></p></div>';
      }
      var warn = low ? '<p class="e-warn">Margin is below your ' + pct(t.target) + " target. Raise prices, trim hours or check the lines marked in amber.</p>" : "";
      S.push('<div class="e-sum-grid"><div><h3>Schedule</h3><table class="e-st">' + sched + '</table><h3>Costs</h3><table class="e-st">' + costs + "</table></div>" +
        '<div><h3>Price</h3><table class="e-st">' + price + '</table><h3>Profit</h3><table class="e-st">' + prof + "</table>" + warn + "</div></div>");
      S.push('<h3>Where each dollar goes</h3>' + bar(t));
      if (t.tParts.length && t.travel) S.push('<p class="small muted">Travel: ' + t.tParts.filter(function (x) { return x[1]; }).map(function (x) { return esc(x[0]) + " " + money0(x[1]); }).join(" · ") + "</p>");
      S.push(market);
      $("[data-summary]").innerHTML = S.join("");
      lastR = R;
    };
    var lastR = null;

    // ------------------------------------------------------------ add-a-task finder
    var data = [];
    Object.keys(LIB.project).forEach(function (k) { var b = LIB.project[k]; data.push({ name: k, src: "project", grp: b.group, n: norm(k), an: b.alts.map(norm), alts: b.alts }); });
    Object.keys(LIB.routine).forEach(function (k) { var b = LIB.routine[k]; data.push({ name: k, src: "routine", grp: b.group, n: norm(k + " " + b.group), an: [], alts: [] }); });
    var fbox = $("[data-efinder]"), fin = fbox.querySelector("input"), flist = fbox.querySelector(".finder-list"), shown = [], active = -1;
    var search = function (raw) {
      var q = norm(raw), words = q.split(" ").filter(Boolean); if (q.length < 2) return [];
      var out = [], rec = E.mode === "recurring";
      data.forEach(function (d) {
        var best = 0, via = "";
        var test = function (hay, alt, label) {
          if (!words.every(function (w) { return hay.indexOf(w) !== -1; })) return;
          var s = hay.indexOf(q) === 0 ? 100 : hay.indexOf(" " + q) !== -1 ? 85 : hay.indexOf(q) !== -1 ? 60 : 45;
          if (alt) s -= 12; if (s > best) { best = s; via = alt ? label : ""; }
        };
        test(d.n, false); d.an.forEach(function (a, i) { test(a, true, d.alts[i]); });
        if (best) out.push({ d: d, s: best + ((rec ? d.src === "routine" : d.src === "project") ? 15 : 0) - d.name.length / 200, via: via });
      });
      return out.sort(function (a, b) { return b.s - a.s; }).slice(0, 9);
    };
    var renderFind = function () {
      shown = search(fin.value);
      if (!shown.length) { flist.hidden = true; fin.setAttribute("aria-expanded", "false"); return; }
      flist.innerHTML = shown.map(function (r, i) {
        var b = book(r.d.src, r.d.name);
        var tag = r.d.src === "routine" ? "Routine · " + FREQ[b.freq][0] : b.mid ? money(num(b.mid)).replace(/\.00$/, "") + " / " + (UNITS[b.unit] || b.unit).toLowerCase() : "";
        return '<li role="option" id="ef-' + i + '" aria-selected="' + (i === active) + '"><a href="#" data-pick="' + i + '"><span>' + esc(r.d.name) +
          (r.via ? '<span class="aka">also called ' + esc(r.via) + "</span>" : '<span class="aka">' + esc(r.d.grp) + "</span>") + '</span><span class="fam">' + esc(tag) + "</span></a></li>";
      }).join("");
      flist.hidden = false; fin.setAttribute("aria-expanded", "true");
    };
    var pick = function (i) { var r = shown[i]; if (!r) return; addLine(r.d.name, r.d.src); fin.value = ""; flist.hidden = true; active = -1; };
    fin.addEventListener("input", function () { active = -1; renderFind(); });
    fin.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        ev.preventDefault(); var n = shown.length; if (!n) return;
        active = ev.key === "ArrowDown" ? (active + 1) % n : (active - 1 + n) % n; renderFind();
      } else if (ev.key === "Enter") { ev.preventDefault(); pick(active >= 0 ? active : 0); }
      else if (ev.key === "Escape") flist.hidden = true;
    });
    flist.addEventListener("mousedown", function (ev) { var a = ev.target.closest("[data-pick]"); if (a) { ev.preventDefault(); pick(+a.getAttribute("data-pick")); } });
    document.addEventListener("click", function (ev) { if (!fbox.contains(ev.target)) flist.hidden = true; });

    // ================================================================ printed documents
    var groupByArea = function (lines) {
      var g = [], idx = {};
      lines.forEach(function (r) { var a = r.l.area || "Other work"; if (idx[a] == null) { idx[a] = g.length; g.push([a, []]); } g[idx[a]][1].push(r); });
      return g;
    };
    var coBlock = function () {
      var lines = [CO.address, [CO.phone, CO.email].filter(Boolean).join(" · "), CO.web, CO.license ? "License " + CO.license : ""].filter(Boolean);
      return '<div class="pd-co"><p class="pd-co-name">' + esc(CO.name || "Your company name") + "</p>" + lines.map(function (l) { return "<p>" + esc(l) + "</p>"; }).join("") + "</div>";
    };
    var projBlock = function () {
      var p = E.project, c = E.client;
      var items = [["Client", [c.name, c.company].filter(Boolean).join(", ")], ["Phone", c.phone], ["Email", c.email], ["Project", p.name], ["Building type", p.type],
        ["Location", [p.city, p.zip].filter(Boolean).join(" ")], ["Square feet", p.sqft ? num(p.sqft).toLocaleString() : ""], ["Start", p.start], ["Needed by", p.due]];
      return '<dl class="pd-facts">' + items.filter(function (x) { return x[1]; }).map(function (x) { return "<div><dt>" + x[0] + "</dt><dd>" + esc(x[1]) + "</dd></div>"; }).join("") + "</dl>";
    };
    var validUntil = function () { var d = new Date(); d.setDate(d.getDate() + (num(E.review.validDays) || 30)); return d.toISOString().slice(0, 10); };
    var printDoc = function (kind) {
      var R = calc(E), t = R.t, rec = R.rec, html;
      var head = '<header class="pd-head">' + coBlock() + '<div class="pd-meta"><p class="pd-title">' + (kind === "internal" ? "Internal estimate" : rec ? "Service proposal" : "Quote") + "</p>" +
        "<p><b>No.</b> " + esc(E.no) + "</p><p><b>Date</b> " + esc(today(0)) + "</p>" + (kind === "internal" ? "<p><b>Status</b> " + esc(E.status) + "</p>" : "<p><b>Valid until</b> " + validUntil() + "</p>") + "</div></header>";
      if (kind === "internal") {
        var rows = groupByArea(R.lines).map(function (g) {
          return '<tr class="pd-area"><td colspan="' + (rec ? 11 : 10) + '">' + esc(g[0]) + "</td></tr>" + g[1].map(function (r) {
            return "<tr><td>" + esc(r.l.task) + (r.l.notes ? '<span class="pd-note">' + esc(r.l.notes) + "</span>" : "") + '</td><td class="n">' + r.q.toLocaleString() + " " + esc(uShort(r.l.unit)) + "</td>" +
              (rec ? "<td>" + esc(FREQ[r.l.freq] ? FREQ[r.l.freq][0] : "") + "</td>" : "") +
              "<td>" + esc(HEIGHT[r.l.height][0]) + " / " + esc(SOIL[r.l.soil][0]) + "</td><td>" + esc(ROLE_LABEL[r.l.role] || "") + '</td><td class="n">' + hrs(r.hours) + '</td><td class="n">' + money0(r.labor + r.sup) +
              '</td><td class="n">' + money0(r.mat) + '</td><td class="n">' + money0(r.cost) + '</td><td class="n">' + money0(r.price) + '</td><td class="n">' + pct(r.margin) + "</td></tr>";
          }).join("");
        }).join("");
        var c = E.costs;
        var assumptions = ROLES.map(function (r) { return esc(r.label) + " " + money(num(c.wages[r.key])) + " → " + money(loaded(c, r.key)); }).join(" · ") +
          "<br>Burden " + num(c.burden) + "% · supervision " + num(c.supPct) + "% · " + (c.night ? "night premium " + num(c.nightPct) + "% · " : "") + "overhead " + num(c.overhead) + "% · target margin " + num(c.margin) + "%" +
          (rec ? "" : " · lines priced by " + (c.method === "market" ? "market rates (" + c.level + ")" : "cost + margin") + " · " + (c.travel === "travel" ? "travel crew" : "local crew"));
        html = head + projBlock() +
          '<h2>Assumptions</h2><p class="pd-small">' + assumptions + "</p>" +
          '<h2>Line items</h2><table class="pd-t"><thead><tr><th>Task</th><th class="n">Qty</th>' + (rec ? "<th>Frequency</th>" : "") + '<th>Height / soil</th><th>Crew</th><th class="n">Hours' + (rec ? "/mo" : "") + '</th><th class="n">Labor</th><th class="n">Materials</th><th class="n">Cost</th><th class="n">Price</th><th class="n">Margin</th></tr></thead><tbody>' + rows + "</tbody></table>" +
          '<div class="pd-cols"><div><h2>Schedule</h2>' + $("[data-summary] .e-sum-grid > div:first-child").innerHTML + "</div><div>" + $("[data-summary] .e-sum-grid > div:last-child").innerHTML + "</div></div>" +
          (t.eParts.length ? '<p class="pd-small"><b>Equipment:</b> ' + t.eParts.map(function (x) { return esc(x[0]) + " " + money0(x[1]); }).join(" · ") + "</p>" : "") +
          (t.travel ? '<p class="pd-small"><b>Travel:</b> ' + t.tParts.filter(function (x) { return x[1]; }).map(function (x) { return esc(x[0]) + " " + money0(x[1]); }).join(" · ") + "</p>" : "") +
          (E.review.notes ? '<h2>Internal notes</h2><p class="pd-pre">' + esc(E.review.notes) + "</p>" : "") +
          '<div class="pd-sign"><div><span></span>Prepared by ' + esc(E.review.preparedBy) + '</div><div><span></span>Reviewed by ' + esc(E.review.reviewedBy) + '</div><div><span></span>Approved ' + esc(E.review.approvedOn) + "</div></div>";
      } else {
        var showScope = E.ui.scopeOnQuote, itemized = E.ui.itemized;
        var body = groupByArea(R.lines).map(function (g) {
          var sub = g[1].reduce(function (s, r) { return s + r.price * (1 - num(E.costs.discount) / 100); }, 0);
          return '<tr class="pd-area"><td colspan="' + (itemized ? 3 : 2) + '">' + esc(g[0]) + "</td>" + (itemized ? "" : '<td class="n">' + money(sub) + "</td>") + "</tr>" + g[1].map(function (r) {
            var b = r.b || {};
            var sc = showScope && (b.scope || []).length ? '<ul class="pd-scope">' + b.scope.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul>" : "";
            return "<tr><td>" + esc(r.l.task) + (r.once ? " <em>(one time)</em>" : "") + sc + '</td><td class="n">' + r.q.toLocaleString() + " " + esc(uShort(r.l.unit)) +
              (rec && !r.once ? ", " + esc(FREQ[r.l.freq][0].toLowerCase()) : "") + "</td>" + (itemized ? '<td class="n">' + money(r.price * (1 - num(E.costs.discount) / 100)) + "</td>" : "<td></td>") + "</tr>";
          }).join("");
        }).join("");
        var extras = t.extraLines.map(function (x) { return "<tr><td>" + esc(x.name) + '</td><td></td><td class="n">' + money(x.price * (1 - num(E.costs.discount) / 100)) + "</td></tr>"; }).join("");
        var tots = (t.discount ? '<tr><th>Includes discount</th><td>-' + money(t.discount) + "</td></tr>" : "") +
          "<tr><th>" + (rec ? "Monthly service" : "Subtotal") + "</th><td>" + money(t.net) + "</td></tr>" +
          (t.tax ? "<tr><th>Sales tax</th><td>" + money(t.tax) + "</td></tr>" : "") +
          '<tr class="pd-grand"><th>' + (rec ? "Monthly total" : "Total") + "</th><td>" + money(t.total) + "</td></tr>" +
          (rec ? "<tr><th>Annual contract value</th><td>" + money0(t.total * 12) + "</td></tr>" + (t.onceP ? "<tr><th>One-time services (billed once)</th><td>" + money(t.onceP) + "</td></tr>" : "") : "");
        html = head + '<h2>Prepared for</h2>' + projBlock() +
          '<h2>Scope and pricing</h2><table class="pd-t pd-q"><thead><tr><th>Service</th><th class="n">Quantity</th><th class="n">' + (itemized ? "Price" : "") + "</th></tr></thead><tbody>" + body + extras + "</tbody></table>" +
          '<table class="pd-tot"><tbody>' + tots + "</tbody></table>" +
          '<h2>Terms</h2><p class="pd-pre">' + esc(E.terms) + "</p>" +
          '<div class="pd-sign"><div><span></span>Accepted by</div><div><span></span>Title</div><div><span></span>Date</div></div>';
      }
      var pd = $("[data-printdoc]");
      pd.innerHTML = html;
      document.body.classList.add("print-" + kind);
      var done = function () { document.body.classList.remove("print-internal", "print-customer"); window.removeEventListener("afterprint", done); };
      window.addEventListener("afterprint", done);
      window.print();
      setTimeout(done, 1500);
    };

    // ================================================================ CSV
    var estimateCsv = function () {
      var R = calc(E), t = R.t, rec = R.rec, p = E.project, c = E.client, rows = [];
      rows.push(["Estimate", E.no], ["Type", rec ? "Recurring contract" : "Construction project"], ["Status", E.status], ["Date", today(0)],
        ["Client", c.name], ["Company", c.company], ["Phone", c.phone], ["Email", c.email], ["Project", p.name], ["Building type", p.type],
        ["City", p.city], ["ZIP", p.zip], ["Square feet", p.sqft], ["Prepared by", E.review.preparedBy], ["Reviewed by", E.review.reviewedBy], []);
      rows.push(["#", "Area", "Task", "Qty", "Unit"].concat(rec ? ["Frequency"] : []).concat(["Height", "Soil", "Crew", "Production per worker-hr", "Hours", "Labor $", "Supervision $", "Materials $", "Cost w/ overhead $", "Price $", "Margin %", "Notes"]));
      R.lines.forEach(function (r, i) {
        rows.push([i + 1, r.l.area, r.l.task, r.q, UNITS[r.l.unit] || r.l.unit].concat(rec ? [FREQ[r.l.freq] ? FREQ[r.l.freq][0] : ""] : [])
          .concat([HEIGHT[r.l.height][0], SOIL[r.l.soil][0], ROLE_LABEL[r.l.role] || "", r.rate, r.hours.toFixed(2), r.labor.toFixed(2), r.sup.toFixed(2), r.mat.toFixed(2), r.cost.toFixed(2), r.price.toFixed(2), r.margin.toFixed(1), r.l.notes]));
      });
      t.extraLines.forEach(function (x) { rows.push(["", "", x.name, "", "", "", "", "", "", "", "", "", "", x.cost.toFixed(2), x.price.toFixed(2)]); });
      rows.push([]);
      [["Crew-hours", t.crewHours.toFixed(1)], ["Days on site", t.days], ["Labor", t.labor.toFixed(2)], ["Supervision", t.sup.toFixed(2)], ["Materials", t.mat.toFixed(2)],
        ["Equipment", t.equip.toFixed(2)], ["Travel", t.travel.toFixed(2)], ["Disposal and site", t.site.toFixed(2)], ["Overhead", t.overhead.toFixed(2)], ["Total cost", t.cost.toFixed(2)],
        ["Price before discount", t.subtotal.toFixed(2)], ["Discount", t.discount.toFixed(2)], ["Price", t.net.toFixed(2)], ["Sales tax", t.tax.toFixed(2)], ["Total to customer", t.total.toFixed(2)],
        ["Gross profit", t.profit.toFixed(2)], ["Margin %", t.margin.toFixed(1)], ["Profit per crew-hour", t.perHour.toFixed(2)]].forEach(function (x) { rows.push(["", "", x[0], x[1]]); });
      if (rec) rows.push(["", "", "Annual contract value", (t.net * 12).toFixed(2)], ["", "", "One-time services", t.onceP.toFixed(2)]);
      return csv(rows);
    };
    var fileBase = function () { return (E.no + (E.project.name ? "-" + norm(E.project.name).replace(/ /g, "-") : "")).slice(0, 80); };

    // ================================================================ bids
    var BIDS = store.get("bk-e2-bids", []);
    var saveBids = function () { store.set("bk-e2-bids", BIDS); };
    var snapshot = function () {
      var R = calc(E);
      return { id: E.id, no: E.no, date: E.created, updated: today(0), mode: E.mode, status: E.status, client: E.client.name, company: E.client.company,
        email: E.client.email, phone: E.client.phone, project: E.project.name, city: E.project.city, zip: E.project.zip, sqft: E.project.sqft,
        value: R.t.net, profit: R.t.profit, margin: R.t.margin, prepared: E.review.preparedBy, reviewed: E.review.reviewedBy, est: clone(E) };
    };
    var saveToBids = function () {
      var s = snapshot(), i = BIDS.findIndex(function (b) { return b.id === s.id; });
      if (i >= 0) BIDS[i] = s; else BIDS.unshift(s);
      saveBids(); renderBids(); flash("Saved " + E.no + " to bids");
    };
    var flash = function (msg) {
      var f = document.createElement("div"); f.className = "e-flash"; f.textContent = msg; document.body.appendChild(f);
      setTimeout(function () { f.remove(); }, 2200);
    };
    var STAT = ["Draft", "In review", "Approved", "Sent", "Won", "Lost"];
    var renderBids = function () {
      var won = BIDS.filter(function (b) { return b.status === "Won"; }), lost = BIDS.filter(function (b) { return b.status === "Lost"; });
      var open = BIDS.filter(function (b) { return ["Won", "Lost"].indexOf(b.status) === -1; });
      var sum = function (a) { return a.reduce(function (s, b) { return s + num(b.value) * (b.mode === "recurring" ? 12 : 1); }, 0); };
      var avgM = BIDS.length ? BIDS.reduce(function (s, b) { return s + num(b.margin); }, 0) / BIDS.length : 0;
      var k = function (l, v) { return '<div class="kpi"><span>' + l + "</span><b>" + v + "</b></div>"; };
      $("[data-kpis]").innerHTML = k("Estimates", BIDS.length) + k("Open pipeline", money0(sum(open))) + k("Won", money0(sum(won))) +
        k("Win rate", won.length + lost.length ? pct(won.length / (won.length + lost.length) * 100) : "–") + k("Average margin", pct(avgM));
      $("[data-bids]").innerHTML = BIDS.length ? BIDS.map(function (b, i) {
        return '<tr data-b="' + i + '"><td class="mono">' + esc(b.no) + "</td><td>" + esc(b.date) + "</td><td><b>" + esc(b.client || b.company || "—") + "</b><br><span class='small muted'>" + esc(b.project || "") + " " + esc(b.city || "") + "</span></td>" +
          "<td>" + (b.mode === "recurring" ? "Recurring" : "Project") + '</td><td class="num">' + money0(num(b.value)) + (b.mode === "recurring" ? "/mo" : "") + '</td><td class="num">' + pct(num(b.margin)) + "</td>" +
          '<td><select data-bstat aria-label="Status">' + STAT.map(function (s) { return "<option" + (s === b.status ? " selected" : "") + ">" + s + "</option>"; }).join("") + "</select></td>" +
          '<td class="e-bact"><button type="button" class="chip" data-bopen>Open</button><button type="button" class="chip" data-bdup>Copy</button><button type="button" class="x" data-bdel aria-label="Delete">×</button></td></tr>';
      }).join("") : '<tr><td colspan="8" class="muted">No saved bids yet. Use "Save to bids" on an estimate.</td></tr>';
    };
    $("[data-bids]").addEventListener("change", function (ev) {
      if (!ev.target.hasAttribute("data-bstat")) return;
      var b = BIDS[+ev.target.closest("tr").getAttribute("data-b")]; b.status = ev.target.value; b.est.status = b.status;
      if (b.id === E.id) { E.status = b.status; saveCur(); bindFields(); }
      saveBids(); renderBids();
    });
    $("[data-bids]").addEventListener("click", function (ev) {
      var tr = ev.target.closest("tr[data-b]"); if (!tr) return;
      var i = +tr.getAttribute("data-b"), b = BIDS[i];
      if (ev.target.closest("[data-bopen]")) { E = clone(b.est); saveCur(); showTab("est"); bindFields(); renderLines(); refresh(); }
      else if (ev.target.closest("[data-bdup]")) { E = clone(b.est); E.id = uid(); E.no = nextNo(); E.status = "Draft"; E.created = today(0); E.review.approvedOn = ""; saveCur(); showTab("est"); bindFields(); renderLines(); refresh(); flash("Copied as " + E.no); }
      else if (ev.target.closest("[data-bdel]") && confirm("Delete " + b.no + " from bids?")) { BIDS.splice(i, 1); saveBids(); renderBids(); }
    });
    var bidsCsv = function () {
      var rows = [["Estimate No", "Date", "Updated", "Status", "Type", "Client", "Company", "Email", "Phone", "Project", "City", "ZIP", "Square feet", "Price", "Monthly", "Annual value", "Gross profit", "Margin %", "Prepared by", "Reviewed by"]];
      BIDS.forEach(function (b) {
        var rec = b.mode === "recurring";
        rows.push([b.no, b.date, b.updated, b.status, rec ? "Recurring contract" : "Construction project", b.client, b.company, b.email, b.phone, b.project, b.city, b.zip, b.sqft,
          rec ? "" : num(b.value).toFixed(2), rec ? num(b.value).toFixed(2) : "", (num(b.value) * (rec ? 12 : 1)).toFixed(2), num(b.profit).toFixed(2), num(b.margin).toFixed(1), b.prepared, b.reviewed]);
      });
      return csv(rows);
    };

    // ================================================================ price book tab
    var lib = "project";
    var pbq = $("[data-pbq]");
    var renderBook = function () {
      var words = norm(pbq.value).split(" ").filter(Boolean), n = 0;
      var cell = function (f, v) { return '<td class="num"><input data-pbf="' + f + '" inputmode="decimal" value="' + esc(v) + '" aria-label="' + f + '"></td>'; };
      var roleSel = function (v) { return '<td><select data-pbf="role" aria-label="Crew">' + opt(ROLES.map(function (r) { return [r.key, r.label]; }), v) + "</select></td>"; };
      var unitSel = function (v) { return '<td><select data-pbf="unit" aria-label="Unit">' + opt(unitPairs(), v) + "</select></td>"; };
      if (lib === "project") {
        $("[data-pbhead]").innerHTML = '<tr><th>Task</th><th>Unit</th><th class="num">Low</th><th class="num">Typical</th><th class="num">High</th><th class="num">Min</th><th class="num">Per worker-hr</th><th class="num">Materials / unit</th><th>Crew</th><th>Basis</th></tr>';
      } else {
        $("[data-pbhead]").innerHTML = '<tr><th>Task</th><th>Unit</th><th class="num">Per worker-hr</th><th class="num">Materials / unit</th><th>Default frequency</th><th>Crew</th><th>Includes</th></tr>';
      }
      var html = Object.keys(LIB[lib]).sort().map(function (k) {
        var x = book(lib, k), b = LIB[lib][k];
        if (!words.every(function (w) { return norm(k + " " + b.group + " " + (b.alts || []).join(" ")).indexOf(w) !== -1; })) return "";
        n++;
        var first = "<td>" + esc(k) + '<span class="small muted block">' + esc(b.group) + "</span></td>";
        if (lib === "project") return '<tr data-k="' + esc(k) + '"' + (x.edited ? ' class="edited"' : "") + ">" + first + unitSel(x.unit) + cell("low", x.low) + cell("mid", x.mid) + cell("high", x.high) + cell("min", x.min) +
          cell("rate", rateFmt(x.rate)) + cell("mat", rateFmt(x.mat)) + roleSel(x.role) + '<td class="small muted">' + esc(b.basis) + (b.conf ? " <em>(" + esc(b.conf) + ")</em>" : "") + "</td></tr>";
        return '<tr data-k="' + esc(k) + '"' + (x.edited ? ' class="edited"' : "") + ">" + first + unitSel(x.unit) + cell("rate", rateFmt(x.rate)) + cell("mat", rateFmt(x.mat)) +
          '<td><select data-pbf="freq" aria-label="Frequency">' + opt(FREQ_KEYS.map(function (f) { return [f, FREQ[f][0]]; }), x.freq) + "</select></td>" + roleSel(x.role) + '<td class="small muted">' + esc(b.desc) + "</td></tr>";
      }).join("");
      $("[data-pb]").innerHTML = html;
      $("[data-pbcount]").textContent = n + " tasks";
      var m = D.meta || {};
      $("[data-pbmeta]").textContent = lib === "project" ? [m.as_of ? "Market rates as of " + m.as_of : "", m.region || "", "Production rates and materials are starting estimates; replace them with your own timed rates."].filter(Boolean).join(" · ")
        : "Routine production rates are starting points from common published janitorial ranges. Time your own crews and replace them.";
    };
    pbq.addEventListener("input", renderBook);
    $$("[data-lib]").forEach(function (b) { b.addEventListener("click", function () { lib = b.getAttribute("data-lib"); $$("[data-lib]").forEach(function (x) { x.classList.toggle("is-on", x === b); }); renderBook(); }); });
    var pbEdit = function (ev) {
      var f = ev.target.getAttribute("data-pbf"); if (!f) return;
      var k = ev.target.closest("tr").getAttribute("data-k");
      OV[lib] = OV[lib] || {}; var o = OV[lib][k] || {};
      o[f] = ["unit", "role", "freq"].indexOf(f) !== -1 ? ev.target.value : num(ev.target.value);
      OV[lib][k] = o; store.set("bk-e2-pb", OV); ev.target.closest("tr").classList.add("edited");
    };
    $("[data-pb]").addEventListener("input", pbEdit); $("[data-pb]").addEventListener("change", pbEdit);

    // ================================================================ company tab
    $$("[data-co]").forEach(function (inp) {
      var k = inp.getAttribute("data-co"); inp.value = CO[k] || "";
      inp.addEventListener("input", function () { CO[k] = inp.value; saveCo(); });
    });
    var renderDefaults = function () {
      var d = costsDefaults();
      $("[data-defsum]").textContent = "Current defaults: " + ROLES.map(function (r) { return r.label + " $" + num(d.wages[r.key]) + "/hr"; }).join(", ") +
        "; burden " + d.burden + "%; overhead " + d.overhead + "%; target margin " + d.margin + "%; crew " + d.crew + " × " + d.shift + " hr; $" + d.perMile + "/mile.";
    };

    // ================================================================ actions and tabs
    var showTab = function (t) {
      $$("[data-tab]").forEach(function (x) { var on = x.getAttribute("data-tab") === t; x.classList.toggle("is-on", on); x.setAttribute("aria-selected", on); });
      $$("[data-pane]").forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== t; });
      if (t === "bids") renderBids(); if (t === "book") renderBook(); if (t === "company") renderDefaults();
    };
    $$("[data-tab]").forEach(function (b) { b.addEventListener("click", function () { showTab(b.getAttribute("data-tab")); }); });
    var readFile = function (inp, fn) {
      var f = inp.files && inp.files[0]; if (!f) return;
      var r = new FileReader();
      r.onload = function () { try { fn(JSON.parse(r.result)); } catch (e) { alert("That file couldn't be read."); } inp.value = ""; };
      r.readAsText(f);
    };
    root.addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest("[data-act]"); if (!b || b.tagName === "INPUT") return;
      var act = b.getAttribute("data-act"), more = b.closest("details"); if (more) more.open = false;
      if (act === "save") saveToBids();
      else if (act === "print-internal") printDoc("internal");
      else if (act === "print-customer") printDoc("customer");
      else if (act === "csv") download(fileBase() + ".csv", estimateCsv(), "text/csv");
      else if (act === "new") { if (!E.lines.length || confirm("Start a new estimate? Save this one to bids first if you need it.")) { E = newEstimate(E.mode); saveCur(); bindFields(); renderLines(); refresh(); } }
      else if (act === "dup") { E = clone(E); E.id = uid(); E.no = nextNo(); E.status = "Draft"; E.created = today(0); E.review.approvedOn = ""; saveCur(); bindFields(); refresh(); flash("Copied as " + E.no); }
      else if (act === "save-file") download(fileBase() + ".json", JSON.stringify({ estimate: E }, null, 2), "application/json");
      else if (act === "save-tpl") {
        var name = prompt("Template name", E.project.name || "My template"); if (!name) return;
        userTpl.push({ name: name, mode: E.mode, lines: clone(E.lines) }); store.set("bk-e2-tpl", userTpl); renderTemplates(); flash("Template saved");
      }
      else if (act === "reset-costs") { if (confirm("Replace this estimate's costs with your company defaults?")) { E.costs = costsDefaults(); saveCur(); bindFields(); refresh(); } }
      else if (act === "save-defaults") { CO.defaults = clone(E.costs); CO.defaults.adjust = 0; CO.defaults.discount = 0; saveCo(); renderDefaults(); flash("Defaults saved"); }
      else if (act === "custom") { addLine(fin.value.trim() || "Custom item", "custom"); fin.value = ""; }
      else if (act === "bids-csv") download("beyond-klean-bids.csv", bidsCsv(), "text/csv");
      else if (act === "book-json") download("beyond-klean-price-book.json", JSON.stringify(OV, null, 2), "application/json");
      else if (act === "book-reset") { if (confirm("Reset every rate to the defaults? Your edits are removed.")) { OV = { project: {}, routine: {} }; store.set("bk-e2-pb", OV); renderBook(); } }
    });
    root.querySelector('[data-act="open-file"]').addEventListener("change", function (ev) {
      readFile(ev.target, function (d) { var e = d.estimate || d; if (!e || !Array.isArray(e.lines)) throw new Error("bad"); E = e; saveCur(); showTab("est"); bindFields(); renderLines(); refresh(); });
    });
    root.querySelector('[data-act="book-import"]').addEventListener("change", function (ev) {
      readFile(ev.target, function (d) { OV = { project: d.project || {}, routine: d.routine || {} }; store.set("bk-e2-pb", OV); renderBook(); flash("Price book imported"); });
    });

    // ================================================================ go
    bindFields(); renderLines(); refresh();
  }
})();
