/* =========================================================
   Pranay Chowdary Puthumbaka — Portfolio scripts
   1. Storage helpers  2. Sound  3. Theme
   4. Welcome screen   5. Intro transition  6. Page reveal
   ========================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Storage helpers (never crash if storage is blocked) ---------- */
  function getItem(store, key) { try { return window[store].getItem(key); } catch (e) { return null; } }
  function setItem(store, key, val) { try { window[store].setItem(key, val); } catch (e) {} }

  /* ---------- 2. Sound (Web Audio, no files; off by default) ---------- */
  var soundOn = getItem('localStorage', 'pp-sound') === 'on';
  var audioCtx = null;
  var soundBtn = document.getElementById('soundBtn');
  var soundPill = document.getElementById('soundPill');

  function click(freq) {
    if (!soundOn) return;
    try {
      audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
      var t = audioCtx.currentTime;
      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.0001, t);
      gain.gain.exponentialRampToValueAtTime(0.08, t + 0.01);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
      osc.connect(gain).connect(audioCtx.destination);
      osc.start(t);
      osc.stop(t + 0.13);
    } catch (e) {}
  }

  function renderSound() {
    [soundBtn, soundPill].forEach(function (el) {
      if (el) el.setAttribute('aria-pressed', soundOn ? 'true' : 'false');
    });
    var pillLabel = document.getElementById('soundPillLabel');
    if (pillLabel) pillLabel.textContent = soundOn ? 'Sound on' : 'Sound off';
  }

  function toggleSound(e) {
    if (e) e.stopPropagation(); // don't trigger the welcome "click to continue"
    soundOn = !soundOn;
    setItem('localStorage', 'pp-sound', soundOn ? 'on' : 'off');
    renderSound();
    click(660);
  }

  if (soundBtn) soundBtn.addEventListener('click', toggleSound);
  if (soundPill) soundPill.addEventListener('click', toggleSound);
  renderSound();

  /* ---------- 3. Theme ---------- */
  var themeBtn = document.getElementById('themeBtn');

  function renderThemeLabel() {
    var dark = root.getAttribute('data-theme') === 'dark';
    if (themeBtn) themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  }

  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      setItem('localStorage', 'pp-theme', next);
      renderThemeLabel();
      click(440);
    });
  }
  renderThemeLabel();

  /* ---------- 7. Contact form (About page) ----------
     No server: builds a mailto: link so the visitor's email app opens
     with the message filled in. */
  var form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.elements.name, email = form.elements.email, msg = form.elements.message;
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
      var fields = [[name, name.value.trim() !== ''], [email, emailOk], [msg, msg.value.trim() !== '']];
      var firstBad = null;
      fields.forEach(function (f) {
        f[0].setAttribute('aria-invalid', f[1] ? 'false' : 'true');
        if (!f[1] && !firstBad) firstBad = f[0];
      });
      document.getElementById('cf-error').hidden = !firstBad;
      if (firstBad) { firstBad.focus(); return; }

      var subject = 'Portfolio enquiry from ' + name.value.trim();
      var body = msg.value.trim() + '\n\n' + name.value.trim() + '\n' + email.value.trim();
      click(520);
      window.location.href = 'mailto:pranaydesigner03@gmail.com?subject=' +
        encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }

  /* ---------- 6. Page reveal + scroll reveal ----------
     Headings fade in word by word; other blocks fade up as they scroll
     into view. Nothing animates until the welcome/intro has finished. */
  var SPLIT_SEL = '.hero__title, .section-title, .about-name';
  var SCROLL_SEL = [
    '.eyebrow', '.a-lead', '.subhead', '.tag-list', '.faq__item',
    '.flow__step', '.flow__arrow', '.step', '.xp__card', '.value', '.hobby', '.polaroid',
    '.note', '.connect-list', '.a-connect .btn', '.a-connect__form'
  ].join(',');

  // Wrap each word of a heading in a span, keeping <strong> etc. intact
  function splitWords(el) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement('span');
            w.className = 'w';
            w.style.setProperty('--i', i++);
            w.textContent = part;
            frag.appendChild(w);
          });
          child.parentNode.replaceChild(frag, child);
        } else if (child.nodeType === 1) {
          walk(child);
        }
      });
    })(el);
    el.classList.add('words');
  }

  function setupScrollReveal() {
    if (reducedMotion || !('IntersectionObserver' in window)) { root.classList.add('no-anim'); return; }
    document.querySelectorAll(SPLIT_SEL).forEach(splitWords);
    // Stagger siblings that appear together (cards, chips, FAQ rows...)
    document.querySelectorAll(SCROLL_SEL).forEach(function (el) {
      if (el.classList.contains('reveal')) return;      // hero items use the load reveal
      var idx = 0, sib = el.previousElementSibling;
      while (sib && idx < 6) { if (sib.matches(SCROLL_SEL)) idx++; sib = sib.previousElementSibling; }
      el.style.setProperty('--sd', (idx * 0.12) + 's');
      el.classList.add('sr');
    });
  }

  function startObserving() {
    var targets = document.querySelectorAll('.sr:not(.note), .words');
    if (!targets.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
          // Handwritten notes are fully clipped before they "write" in, so the
          // observer can't see them: reveal them with the rest of their section.
          var sec = entry.target.closest('section');
          if (sec) sec.querySelectorAll('.note.sr').forEach(function (n) { n.classList.add('is-in'); });
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    targets.forEach(function (t) { io.observe(t); });
  }

  setupScrollReveal();

  /* ---------- 9. Values (About): scroll-linked highlight ----------
     The accent line draws along the wavy path as you scroll; each value
     lights up when the line reaches it (on mobile: when it scrolls into view). */
  function setupValues() {
    var box = document.getElementById('values');
    if (!box) return;
    var items = Array.prototype.slice.call(box.querySelectorAll('.value'));
    var prog = box.querySelector('.values__progress');
    var pathSvg = box.querySelector('.values__path');
    box.querySelectorAll('.icon-tile--value svg *').forEach(function (el) { el.setAttribute('pathLength', '1'); });
    if (reducedMotion) { items.forEach(function (it) { it.classList.add('is-lit'); }); return; }

    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight;
      var pathShown = pathSvg && getComputedStyle(pathSvg).display !== 'none';
      if (pathShown) {
        var top = box.getBoundingClientRect().top;
        var p = Math.max(0, Math.min(1, (vh * 0.85 - top) / (vh * 0.55)));
        prog.style.strokeDashoffset = String(1 - p);
        items.forEach(function (it, i) { it.classList.toggle('is-lit', p >= i * 0.2 + 0.08); });
      } else {
        items.forEach(function (it) { it.classList.toggle('is-lit', it.getBoundingClientRect().top < vh * 0.75); });
      }
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }
  setupValues();


  function revealPage() {
    document.body.classList.remove('is-locked');
    // next frame so the transitions actually run
    requestAnimationFrame(function () {
      root.classList.add('revealed');
      startObserving();
    });
  }

  /* ---------- 8. Page transitions ----------
     Internal links fade the page out, then the next page fades in. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var href = a.getAttribute('href');
    if (a.target === '_blank' || a.hasAttribute('download') || !/^[\w-]+\.html(#.*)?$/.test(href)) return;
    if (a.getAttribute('aria-current') === 'page') { e.preventDefault(); return; }
    e.preventDefault();
    click(480);
    setItem('sessionStorage', 'pp-nav', '1');
    document.body.classList.add('is-leaving');
    setTimeout(function () { window.location.href = href; }, reducedMotion ? 0 : 420);
  });
  // Coming back with the browser's Back button: undo the fade-out
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) document.body.classList.remove('is-leaving');
  });

  /* ---------- 5. Intro transition ---------- */
  var intro = document.getElementById('intro');
  var greetEl = document.getElementById('introGreet');
  var greetings = ['Hello', 'नमस्ते', 'నమస్కారం', 'Hola', 'Bonjour', 'Ciao'];
  var timers = [];
  var introRunning = false;

  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }

  function endIntro() {
    if (!introRunning) return;
    introRunning = false;
    timers.forEach(clearTimeout);
    timers = [];
    document.removeEventListener('keydown', introKeys);
    // Crossfade: the overlay (with its grid lines) fades while the page fades in underneath
    intro.classList.add('is-leaving');
    setTimeout(function () {
      intro.className = 'intro';
      intro.setAttribute('aria-hidden', 'true');
    }, 950);
    revealPage();
  }

  function introKeys(e) {
    if (e.key === 'Escape' || e.key === 'Enter') { e.preventDefault(); endIntro(); }
  }

  function playIntro() {
    if (reducedMotion || !intro || !greetEl) { revealPage(); return; }
    introRunning = true;
    intro.classList.add('is-active');
    document.addEventListener('keydown', introKeys);
    if (skipBtn) skipBtn.focus({ preventScroll: true });

    // 1. lines draw out (+ labels fade in via CSS delay)
    later(function () { intro.classList.add('lines-in'); }, 60);

    // 2. greetings cycle every 380ms from 0.7s
    greetings.forEach(function (word, i) {
      later(function () {
        if (i === 0) { greetEl.textContent = word; click(380); return; }
        greetEl.classList.add('is-swapping');
        later(function () {
          greetEl.textContent = word;
          greetEl.classList.remove('is-swapping');
          click(380 + 40 * i);
        }, 170);
      }, 700 + i * 380);
    });

    // 3. accent block wipes in with "Welcome."
    later(function () { intro.classList.add('block-in'); click(700); }, 3200);
    // 4. block fades out
    later(function () { intro.classList.add('block-out'); greetEl.textContent = ''; }, 4200);
    // 5. lines shrink, overlay fades, page reveals
    later(endIntro, 4500);
  }

  var skipBtn = document.getElementById('introSkip');
  if (skipBtn) skipBtn.addEventListener('click', endIntro);

  /* ---------- 4. Welcome screen ---------- */
  var welcome = document.getElementById('welcome');
  var alreadyWelcomed = root.classList.contains('welcomed');

  if (alreadyWelcomed || !welcome) {
    revealPage();
    return;
  }

  document.body.classList.add('is-locked');
  var textEl = document.getElementById('welcomeText');
  var enterBtn = document.getElementById('welcomeEnter');
  var word = 'Welcome';
  var done = false;

  // Type "Welcome" letter by letter (instant if reduced motion)
  if (reducedMotion) {
    textEl.textContent = word;
  } else {
    var i = 0;
    var typer = setInterval(function () {
      textEl.textContent = word.slice(0, ++i);
      if (i >= word.length) clearInterval(typer);
    }, 140);
  }

  function continueOn() {
    if (done) return;
    done = true;
    click(520);
    setItem('sessionStorage', 'pp-welcomed', '1');
    document.removeEventListener('keydown', welcomeKeys);
    welcome.classList.add('is-leaving');
    setTimeout(function () {
      welcome.style.display = 'none';
      playIntro();
    }, 500);
  }

  function welcomeKeys(e) {
    if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
      e.preventDefault();
      continueOn();
    }
  }

  document.addEventListener('keydown', welcomeKeys);
  welcome.addEventListener('click', continueOn);
})();
