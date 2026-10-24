/* Everglades Restorations & Land Clearing Inc. — site scripts (no dependencies) */
(function () {
  "use strict";

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "✕ Close" : "☰ Menu";
      document.documentElement.classList.toggle("nav-open", open);
    });
  }

  // Close dropdowns when clicking elsewhere (desktop)
  var drops = document.querySelectorAll(".nav details");
  document.addEventListener("click", function (e) {
    drops.forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute("open"); });
  });
  drops.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) drops.forEach(function (o) { if (o !== d) o.removeAttribute("open"); });
    });
  });

  // Video slots: <div class="video" data-yt="VIDEO_ID">. Empty id = placeholder.
  document.querySelectorAll(".video[data-yt]").forEach(function (box) {
    var id = (box.getAttribute("data-yt") || "").trim();
    if (!id) return;
    var title = box.getAttribute("data-title") || "Job video";
    box.innerHTML = '<img src="https://i.ytimg.com/vi/' + id + '/hqdefault.jpg" alt="" loading="lazy">' +
      '<button type="button" aria-label="Play: ' + title.replace(/"/g, "&quot;") + '"><span class="play"></span></button>';
    box.querySelector("button").addEventListener("click", function () {
      box.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&rel=0" title="' + title.replace(/"/g, "&quot;") +
        '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
    });
  });

  // Before / after sliders
  document.querySelectorAll(".ba").forEach(function (ba) {
    var r = ba.querySelector("input[type=range]");
    if (!r) return;
    var set = function () { ba.style.setProperty("--pos", r.value + "%"); };
    r.addEventListener("input", set);
    set();
  });

  // Project library filters
  var grid = document.getElementById("project-grid");
  if (grid) {
    var sel = document.querySelectorAll("[data-filter]");
    var apply = function () {
      var want = {};
      sel.forEach(function (s) { want[s.getAttribute("data-filter")] = s.value; });
      var shown = 0;
      grid.querySelectorAll("[data-service]").forEach(function (c) {
        var ok = Object.keys(want).every(function (k) {
          return !want[k] || (c.getAttribute("data-" + k) || "").split(" ").indexOf(want[k]) !== -1;
        });
        c.style.display = ok ? "" : "none";
        if (ok) shown++;
      });
      var none = document.getElementById("no-results");
      if (none) none.style.display = shown ? "none" : "";
    };
    sel.forEach(function (s) { s.addEventListener("change", apply); });
  }

  // Remember how the visitor first arrived (landing page + referrer + utm), for the bid form
  try {
    if (!sessionStorage.getItem("eg_first")) {
      sessionStorage.setItem("eg_first", JSON.stringify({
        landing: location.pathname + location.search,
        referrer: document.referrer || "direct"
      }));
    }
  } catch (e) {}

  // Request-a-bid form: quietly scores the request (visitors never see this)
  var form = document.getElementById("bid-form");
  if (form) {
    var first = {};
    try { first = JSON.parse(sessionStorage.getItem("eg_first") || "{}"); } catch (e) {}
    var setHidden = function (name, val) { var f = form.elements[name]; if (f) f.value = val || ""; };
    setHidden("landing_page", first.landing);
    setHidden("referrer", first.referrer);

    var params = new URLSearchParams(location.search);
    var pre = params.get("service");
    if (pre) {
      var box = form.querySelector('input[name="services"][value="' + pre + '"]');
      if (box) box.checked = true;
    }

    form.addEventListener("submit", function (e) {
      var role = form.elements.role.value;
      var size = form.elements.size.value;
      var bidNo = (form.elements.solicitation.value || "").trim();
      var services = Array.prototype.map.call(form.querySelectorAll('input[name="services"]:checked'), function (c) { return c.value; });
      var bigServices = ["wetland-restoration-mitigation", "exotic-invasive-removal", "hurricane-debris-removal"];
      var lane = "C";
      if (["government", "utility", "engineer"].indexOf(role) !== -1 || bidNo ||
          (["20-100", "100+", "linear"].indexOf(size) !== -1 && services.some(function (s) { return bigServices.indexOf(s) !== -1; }))) {
        lane = "A";
      } else if (["contractor", "developer", "hoa", "commercial"].indexOf(role) !== -1 ||
                 ["5-20", "20-100", "100+", "linear"].indexOf(size) !== -1) {
        lane = "B";
      }
      setHidden("lead_lane", lane);

      // FORM ENDPOINT NOT CONNECTED YET: until it is, go straight to the thank-you page.
      if (!form.getAttribute("action") || form.getAttribute("action") === "#") {
        e.preventDefault();
        location.href = form.getAttribute("data-thanks");
      }
    });
  }

  // QR codes that point at wherever this site is currently hosted
  if (window.qrcode) {
    document.querySelectorAll("[data-qr]").forEach(function (el) {
      var path = el.getAttribute("data-qr") || "/";
      var url = location.protocol === "file:" ? "https://www.example.com/" : location.origin + path;
      var qr = window.qrcode(0, "M");
      qr.addData(url);
      qr.make();
      el.innerHTML = qr.createSvgTag({ cellSize: 6, margin: 2, scalable: true });
      var cap = document.querySelector('[data-qr-url="' + el.id + '"]');
      if (cap) cap.textContent = url.replace(/^https?:\/\//, "").replace(/\/$/, "");
    });
  }

  // Hero background video: pause control + reduced-motion respect (WCAG 2.2.2)
  var vid = document.querySelector(".hero-vid"), pause = document.querySelector(".hero-pause");
  if (vid && pause) {
    var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var setState = function (paused) {
      pause.setAttribute("aria-pressed", paused ? "true" : "false");
      pause.setAttribute("aria-label", paused ? "Play background video" : "Pause background video");
      pause.textContent = paused ? "▶" : "⏸";
    };
    if (still) { vid.pause(); pause.hidden = true; }
    pause.addEventListener("click", function () {
      if (vid.paused) { vid.play(); setState(false); } else { vid.pause(); setState(true); }
    });
  }

  // Footer accordions: open on computers, collapsed on phones (HTML ships open so nothing hides without JS)
  if (window.matchMedia && window.matchMedia("(max-width: 900px)").matches) {
    document.querySelectorAll("details[data-desktop-open]").forEach(function (d) { d.removeAttribute("open"); });
  }

  // Footer year
  document.querySelectorAll("[data-current-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
