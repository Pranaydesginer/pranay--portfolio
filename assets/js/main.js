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
    if (soundPill) soundPill.textContent = soundOn ? 'Sound on' : 'Sound off';
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

  /* ---------- 6. Page reveal (defined early, used below) ---------- */
  function revealPage() {
    document.body.classList.remove('is-locked');
    // next frame so the transition actually runs
    requestAnimationFrame(function () { root.classList.add('revealed'); });
  }

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
    intro.classList.add('lines-out', 'is-leaving');
    setTimeout(function () {
      intro.className = 'intro';
      intro.setAttribute('aria-hidden', 'true');
    }, 450);
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
  enterBtn.focus({ preventScroll: true });

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
