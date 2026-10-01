/* Bob Miller Flooring — site scripts (mock-up) */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     SETTINGS — edit these when the site goes live
     FORM_ENDPOINT: where the quote form posts (e.g. a Formspree,
       Basin or Netlify Forms URL). Leave '' to show the thank-you
       message without sending anything (mock-up mode).
     TURNSTILE_SITEKEY: Cloudflare Turnstile key. The value below is
       Cloudflare's public TEST key, which always passes. Replace it
       with your real key for the live domain.
  --------------------------------------------------------------- */
  var FORM_ENDPOINT = '';
  var TURNSTILE_SITEKEY = '1x00000000000000000000AA';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* year */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* sticky header shadow */
  var top = $('.top');
  var onScroll = function () { if (top) top.classList.toggle('scrolled', window.scrollY > 30); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mobile menu */
  var mb = $('.menu-btn'), ul = $('#nav-list');
  if (mb && ul) {
    mb.addEventListener('click', function () {
      var open = ul.classList.toggle('open');
      mb.setAttribute('aria-expanded', open);
      mb.textContent = open ? 'Close' : 'Menu';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && ul.classList.contains('open')) { ul.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); mb.textContent = 'Menu'; mb.focus(); }
    });
  }

  /* scroll reveal */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add('in'); }); }

  /* count-up numbers */
  $$('[data-count]').forEach(function (el) {
    var end = +el.dataset.count, suf = el.dataset.suffix || '', done = false;
    var run = function () {
      if (done) return; done = true;
      var t0 = performance.now();
      (function step(t) {
        var p = Math.min((t - t0) / 1600, 1), e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(end * e) + suf;
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en, o) { if (en[0].isIntersecting) { run(); o.disconnect(); } }).observe(el);
    } else run();
  });

  /* before / after sliders */
  $$('.ba').forEach(function (ba) {
    var input = $('input', ba), after = $('.after', ba), line = $('.line', ba), knob = $('.knob', ba);
    var set = function () { var v = input.value; after.style.clipPath = 'inset(0 0 0 ' + v + '%)'; line.style.left = v + '%'; knob.style.left = v + '%'; };
    input.addEventListener('input', set); set();
  });

  /* gallery filter + lightbox */
  var filters = $$('.filters button'), figs = $$('.masonry figure');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      var f = b.dataset.filter;
      figs.forEach(function (fig) { fig.classList.toggle('hide', f !== 'all' && fig.dataset.cat !== f); fig.classList.add('in'); });
    });
  });
  var lb = $('.lightbox');
  if (lb) {
    var lbImg = $('img', lb), lbCap = $('p', lb), idx = 0, lastFocus = null;
    var visible = function () { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return $('button', f); }); };
    var show = function (i) {
      var list = visible(); if (!list.length) return;
      idx = (i + list.length) % list.length;
      var b = list[idx]; lbImg.src = b.dataset.full; lbImg.alt = $('img', b).alt;
      var tmp = document.createElement('div'); tmp.innerHTML = b.dataset.cap; lbCap.textContent = tmp.textContent;
    };
    var close = function () { lb.classList.remove('open'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); };
    figs.forEach(function (f) {
      $('button', f).addEventListener('click', function () {
        lastFocus = this; show(visible().indexOf(this)); lb.classList.add('open'); document.body.style.overflow = 'hidden'; $('.x', lb).focus();
      });
    });
    $('.x', lb).addEventListener('click', close);
    $('.prev', lb).addEventListener('click', function () { show(idx - 1); });
    $('.next', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* material explorer tabs */
  var tabs = $$('[role=tab]');
  var activate = function (t) {
    tabs.forEach(function (x) {
      var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
  };
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { activate(t); });
    t.addEventListener('keydown', function (e) {
      var n = null;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
      if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
      if (n) { e.preventDefault(); activate(n); n.focus(); }
    });
  });

  /* ZIP checker (service areas) */
  var zipForm = $('#zip-form');
  if (zipForm) {
    zipForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var z = $('#zip-in').value.trim(), out = $('#zip-out'), p3 = +z.slice(0, 3);
      out.className = 'zip-out';
      if (!/^\d{5}$/.test(z)) { out.textContent = 'Please enter a 5-digit ZIP code.'; out.classList.add('no'); return; }
      var fl = p3 >= 330 && p3 <= 334, pa = p3 >= 150 && p3 <= 156;
      if (fl) { out.innerHTML = 'Yes! We serve your area in South Florida. Call <a href="tel:+19545550163">(954) 555-0163</a> or <a href="free-quote.html">get a free quote</a>.'; out.classList.add('ok'); }
      else if (pa) { out.innerHTML = 'Yes! We serve your area around Pittsburgh. Call <a href="tel:+14125550187">(412) 555-0187</a> or <a href="free-quote.html">get a free quote</a>.'; out.classList.add('ok'); }
      else { out.innerHTML = 'That ZIP is outside our usual area, but for the right project we travel. <a href="free-quote.html">Ask us anyway</a>.'; out.classList.add('no'); }
    });
  }

  /* ---------------- quote form + CAPTCHA ---------------- */
  var form = $('#quote-form');
  if (!form) return;
  var msg = $('#form-msg'), mathBox = $('#math-box'), mathQ = $('#math-q'), mathAns = $('#math-ans');
  var turnstileId = null, turnstileToken = '', useMath = false, mathSum = 0;

  var newMath = function () {
    var a = 2 + Math.floor(Math.random() * 8), b = 1 + Math.floor(Math.random() * 9);
    mathSum = a + b; mathQ.textContent = a + ' + ' + b; mathAns.value = '';
  };
  var fallbackToMath = function () {
    if (turnstileId !== null || useMath) return;
    useMath = true; newMath(); mathBox.classList.add('on');
  };
  window.bmfTurnstileReady = function () {
    if (useMath || !window.turnstile) return;
    try {
      turnstileId = window.turnstile.render('#turnstile-box', {
        sitekey: TURNSTILE_SITEKEY, theme: 'light',
        callback: function (t) { turnstileToken = t; },
        'expired-callback': function () { turnstileToken = ''; },
        'error-callback': function () { turnstileToken = ''; }
      });
    } catch (err) { fallbackToMath(); }
  };
  if (window.turnstile) window.bmfTurnstileReady();
  /* if Cloudflare can't load (offline / blocked), use a simple math check */
  setTimeout(fallbackToMath, 6000);

  var fail = function (text, el) {
    msg.textContent = text; msg.className = 'form-msg err';
    if (el) el.focus();
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    msg.className = 'form-msg'; msg.textContent = '';
    if ($('#website').value) return; // honeypot: bots fill hidden field

    if (!form.querySelector('input[name=project]:checked')) return fail('Please choose what we’re working on.', form.querySelector('input[name=project]'));
    var req = ['#region', '#name', '#phone', '#email'];
    for (var i = 0; i < req.length; i++) {
      var el = $(req[i]);
      if (!el.value.trim()) return fail('Please fill in: ' + form.querySelector('label[for=' + el.id + ']').textContent.replace('*', '').trim() + '.', el);
    }
    if (!$('#email').checkValidity()) return fail('Please enter a valid email address.', $('#email'));
    if ($('#phone').value.replace(/\D/g, '').length < 10) return fail('Please enter a 10-digit phone number.', $('#phone'));

    if (useMath) {
      if (+mathAns.value !== mathSum) { newMath(); return fail('That security answer wasn’t right. Please try the new sum.', mathAns); }
    } else if (!turnstileToken) {
      return fail('Please complete the security check above the button.');
    }

    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.firstChild.textContent = 'Sending… ';
    var data = new FormData(form);
    if (turnstileToken) data.append('cf-turnstile-response', turnstileToken);

    var done = function () {
      form.hidden = true;
      var th = $('#thanks'); th.classList.add('on'); th.focus();
      th.scrollIntoView({ behavior: 'smooth', block: 'center' });
    };
    if (!FORM_ENDPOINT) { setTimeout(done, 700); return; }
    fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); done(); })
      .catch(function () {
        btn.disabled = false; btn.firstChild.textContent = 'Get my free quote ';
        fail('Sorry, something went wrong sending your request. Please call us instead.');
        if (turnstileId !== null) { window.turnstile.reset(turnstileId); turnstileToken = ''; }
      });
  });
})();
