/* Home v2 interactions: before/during/after stage, floor layers, video slot */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* before / during / after — auto-advances until the visitor takes over */
  var figs = document.querySelectorAll('.stage figure'), tabs = document.querySelectorAll('.stage-tabs [role=tab]');
  var timer = document.querySelector('.stage-tabs .timer'), cur = 0, auto = !reduce, handle = null;
  function go(i) {
    cur = i;
    figs.forEach(function (f, n) { f.classList.toggle('on', n === i); });
    tabs.forEach(function (t, n) { t.setAttribute('aria-selected', n === i); });
    if (timer) {
      timer.style.transition = 'none'; timer.style.width = (i * 33.33) + '%';
      if (auto) { void timer.offsetWidth; timer.style.transition = 'width 4.5s linear'; timer.style.width = ((i + 1) * 33.33) + '%'; }
    }
  }
  function loop() { handle = setTimeout(function () { if (!auto) return; go((cur + 1) % 3); loop(); }, 4500); }
  if (figs.length) {
    tabs.forEach(function (t) {
      t.addEventListener('click', function () { auto = false; clearTimeout(handle); go(+t.dataset.go); });
    });
    var stage = document.querySelector('.stage');
    if ('IntersectionObserver' in window && auto) {
      new IntersectionObserver(function (en, o) { if (en[0].isIntersecting) { go(0); loop(); o.disconnect(); } }, { threshold: .4 }).observe(stage);
    }
  }

  /* what's under the floor */
  var svg = document.querySelector('.layers-svg'), btns = document.querySelectorAll('.layer-list button');
  function pick(k) {
    var same = false;
    btns.forEach(function (b) {
      var on = b.dataset.layer === k && b.getAttribute('aria-expanded') !== 'true';
      if (b.dataset.layer === k && !on) same = true;
      b.setAttribute('aria-expanded', on);
    });
    if (!svg) return;
    svg.classList.toggle('focus', !same);
    svg.querySelectorAll('.layer').forEach(function (g) { g.classList.toggle('on', !same && g.dataset.layer === k); });
  }
  btns.forEach(function (b) { b.addEventListener('click', function () { pick(b.dataset.layer); }); });
  if (svg) svg.querySelectorAll('.layer').forEach(function (g) { g.addEventListener('click', function () { pick(g.dataset.layer); }); });

  /* video slot (until Bob's clip exists) */
  var vb = document.querySelector('.video button'), soon = document.getElementById('soon');
  if (vb && soon) vb.addEventListener('click', function () { soon.classList.toggle('on'); });
})();
