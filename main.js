/* ============================================================
   HARISH RAGHAVENDAR G — PORTFOLIO JAVASCRIPT
   main.js | All Interactions, Animations & Logic
   ============================================================ */

'use strict';

/* ===== PRELOADER ===== */
window.addEventListener('load', () => {
  const preloader = document.getElementById('preloader');
  const texts = [
    'INITIALIZING PORTFOLIO...',
    'LOADING ASSETS...',
    'CALIBRATING SYSTEMS...',
    'READY.'
  ];
  let i = 0;
  const textEl = document.getElementById('preloaderText');
  const interval = setInterval(() => {
    i++;
    if (i < texts.length && textEl) textEl.textContent = texts[i];
    if (i >= texts.length - 1) clearInterval(interval);
  }, 550);

  setTimeout(() => {
    if (preloader) preloader.classList.add('hidden');
    initCounters();
    initTerminalTyping();
  }, 2400);
});

/* ===== CUSTOM CURSOR ===== */
const cursor     = document.getElementById('cursor');
const cursorRing = document.getElementById('cursorRing');
let cx = window.innerWidth / 2;
let cy = window.innerHeight / 2;
let rx = cx, ry = cy;
let cursorVisible = false;

document.addEventListener('mousemove', e => {
  cx = e.clientX; cy = e.clientY;
  if (cursor) {
    cursor.style.left = cx - 5 + 'px';
    cursor.style.top  = cy - 5 + 'px';
  }
  if (!cursorVisible) {
    if (cursor) cursor.style.opacity = '1';
    if (cursorRing) cursorRing.style.opacity = '1';
    cursorVisible = true;
  }
});

document.addEventListener('mouseleave', () => {
  if (cursor) cursor.style.opacity = '0';
  if (cursorRing) cursorRing.style.opacity = '0';
  cursorVisible = false;
});

document.addEventListener('mousedown', () => {
  if (cursor) cursor.classList.add('clicking');
});
document.addEventListener('mouseup', () => {
  if (cursor) cursor.classList.remove('clicking');
});

function animateRing() {
  rx += (cx - rx) * 0.13;
  ry += (cy - ry) * 0.13;
  if (cursorRing) {
    cursorRing.style.left = rx - 18 + 'px';
    cursorRing.style.top  = ry - 18 + 'px';
  }
  requestAnimationFrame(animateRing);
}
animateRing();

// Cursor scale on interactive elements
const interactiveEls = 'a, button, .persona-card, .project-card, .cert-card, .skill-chip, .about-tag, .filter-btn';
document.querySelectorAll(interactiveEls).forEach(el => {
  el.addEventListener('mouseenter', () => {
    if (cursor) cursor.style.transform = 'scale(2.2)';
    if (cursorRing) { cursorRing.style.width = '52px'; cursorRing.style.height = '52px'; }
  });
  el.addEventListener('mouseleave', () => {
    if (cursor) cursor.style.transform = 'scale(1)';
    if (cursorRing) { cursorRing.style.width = '36px'; cursorRing.style.height = '36px'; }
  });
});

/* ===== BACKGROUND PARTICLES ===== */
(function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 35; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 3 + 1;
    const hue  = 190 + Math.random() * 50;
    p.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${Math.random() * 100}%;
      bottom: ${Math.random() * 15}%;
      background: hsl(${hue}deg, 80%, 60%);
      animation-duration: ${9 + Math.random() * 14}s;
      animation-delay: ${Math.random() * 12}s;
    `;
    container.appendChild(p);
  }
})();

/* ===== HERO CANVAS — NETWORK LINES ===== */
(function initHeroCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, nodes = [];

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class Node {
    constructor() { this.reset(); }
    reset() {
      this.x  = Math.random() * W;
      this.y  = Math.random() * H;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.r  = Math.random() * 2 + 1;
    }
    update() {
      this.x += this.vx; this.y += this.vy;
      if (this.x < 0 || this.x > W) this.vx *= -1;
      if (this.y < 0 || this.y > H) this.vy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,245,255,0.6)';
      ctx.fill();
    }
  }

  for (let i = 0; i < 40; i++) nodes.push(new Node());

  function drawLines() {
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = `rgba(33,150,243,${(1 - dist / 130) * 0.25})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);
    nodes.forEach(n => { n.update(); n.draw(); });
    drawLines();
    requestAnimationFrame(loop);
  }
  loop();
})();

/* ===== NAVIGATION ===== */
const nav       = document.getElementById('nav');
const backTop   = document.getElementById('backTop');
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');

window.addEventListener('scroll', () => {
  if (nav)     nav.classList.toggle('scrolled', window.scrollY > 60);
  if (backTop) backTop.classList.toggle('visible', window.scrollY > 450);
  updateActiveNav();
});

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');
  });
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    });
  });
}

function updateActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navAs    = document.querySelectorAll('.nav-links a');
  let current    = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 180) current = sec.id;
  });
  navAs.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
}

/* ===== SCROLL REVEAL ===== */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 90);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ===== SKILL BARS ===== */
const barObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.skill-bar-fill').forEach((bar, i) => {
        setTimeout(() => {
          bar.style.width = bar.dataset.width + '%';
        }, i * 120);
      });
      barObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.25 });

document.querySelectorAll('.skills-container').forEach(el => barObserver.observe(el));

/* ===== COUNTER ANIMATION ===== */
function initCounters() {
  const statNums = document.querySelectorAll('.stat-num[data-count]');
  statNums.forEach(el => {
    const target  = parseInt(el.dataset.count);
    const suffix  = el.dataset.suffix || '';
    const isDecimal = target === 787; // CGPA special case
    const duration = 2000;
    const step     = 16;
    const steps    = duration / step;
    let current    = 0;
    const increment = target / steps;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      if (isDecimal) {
        el.textContent = (current / 100).toFixed(2) + suffix;
      } else {
        el.textContent = Math.floor(current) + suffix;
      }
    }, step);
  });
}

/* ===== HERO GREETING ROTATOR ===== */
const greetings = [
  'Hello, World! 👾',
  'Namaste! 🙏',
  'Hey there! 🎮',
  'Hi, Data World! 📊',
  'Level Up! 🚀'
];
let greetIdx = 0;
const greetEl = document.getElementById('heroGreeting');
if (greetEl) {
  setInterval(() => {
    greetIdx = (greetIdx + 1) % greetings.length;
    greetEl.style.opacity = '0';
    setTimeout(() => {
      greetEl.textContent = greetings[greetIdx];
      greetEl.style.transition = 'opacity 0.4s';
      greetEl.style.opacity = '1';
    }, 350);
  }, 3800);
}

/* ===== TERMINAL TYPING EFFECT ===== */
function initTerminalTyping() {
  const terminalEl = document.getElementById('terminalText');
  if (!terminalEl) return;
  const lines = [
    'QA_MODE: active | bugs_found: 42',
    'model.fit(X_train, y_train) → 85% accuracy',
    'aws s3 sync pipeline → ETL complete ✓',
    'git commit -m "level up achieved 🚀"',
    'target: rockstar_games → applying...',
    'passion: ON | coffee: LOW | drive: MAX'
  ];
  let lineIdx = 0;
  let charIdx = 0;
  let typing  = true;
  let pauseFrames = 0;

  function tick() {
    const line = lines[lineIdx];
    if (typing) {
      if (charIdx < line.length) {
        terminalEl.textContent = line.slice(0, ++charIdx);
      } else {
        typing = false;
        pauseFrames = 80;
      }
    } else {
      if (pauseFrames > 0) {
        pauseFrames--;
      } else {
        if (charIdx > 0) {
          terminalEl.textContent = line.slice(0, --charIdx);
        } else {
          lineIdx = (lineIdx + 1) % lines.length;
          typing  = true;
        }
      }
    }
    setTimeout(tick, typing ? 45 : 18);
  }
  tick();
}

/* ===== PROJECT FILTER ===== */
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;

    projectCards.forEach(card => {
      const cat = card.dataset.category;
      const show = filter === 'all' || cat === filter;
      if (show) {
        card.classList.remove('hidden');
        card.style.animation = 'none';
        card.offsetHeight; // reflow
        card.style.animation = 'fadeSlideUp 0.4s ease both';
      } else {
        card.classList.add('hidden');
      }
    });

    // Re-span featured card only when showing all or qa
    const featured = document.querySelector('.project-card.featured');
    if (featured) {
      featured.style.gridColumn = (filter === 'all' || filter === 'qa') ? 'span 2' : 'span 1';
    }
  });
});

/* ===== CONTACT FORM ===== */
const sendBtn    = document.getElementById('sendBtn');
const formStatus = document.getElementById('formStatus');

if (sendBtn) {
  sendBtn.addEventListener('click', () => {
    const name    = document.getElementById('cName')?.value.trim();
    const email   = document.getElementById('cEmail')?.value.trim();
    const subject = document.getElementById('cSubject')?.value.trim();
    const message = document.getElementById('cMessage')?.value.trim();

    if (!name || !email || !message) {
      showStatus('⚠ Please fill in Name, Email & Message.', 'error');
      return;
    }
    if (!isValidEmail(email)) {
      showStatus('⚠ Please enter a valid email address.', 'error');
      return;
    }

    sendBtn.textContent = 'SENDING...';
    sendBtn.disabled = true;

    setTimeout(() => {
      const mailBody = `From: ${name}\nEmail: ${email}\n\n${message}`;
      const mailto   = `mailto:harishraghav906@gmail.com?subject=${encodeURIComponent(subject || 'Portfolio Contact: ' + name)}&body=${encodeURIComponent(mailBody)}`;
      window.open(mailto);
      showStatus('✓ Message drafted! Your mail client has opened.', 'success');
      sendBtn.textContent = 'SEND MESSAGE ➤';
      sendBtn.disabled = false;
      document.getElementById('cName').value    = '';
      document.getElementById('cEmail').value   = '';
      document.getElementById('cSubject').value = '';
      document.getElementById('cMessage').value = '';
    }, 900);
  });
}

function showStatus(msg, type) {
  if (!formStatus) return;
  formStatus.textContent = msg;
  formStatus.className   = 'form-status ' + type;
  setTimeout(() => { formStatus.textContent = ''; formStatus.className = 'form-status'; }, 5000);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/* ===== SMOOTH SCROLL FOR NAV LINKS ===== */
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top    = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

/* ===== CARD TILT EFFECT (subtle 3D) ===== */
document.querySelectorAll('.project-card, .cert-card, .persona-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect   = card.getBoundingClientRect();
    const x      = e.clientX - rect.left;
    const y      = e.clientY - rect.top;
    const cx2    = rect.width  / 2;
    const cy2    = rect.height / 2;
    const rotateX = ((y - cy2) / cy2) * -5;
    const rotateY = ((x - cx2) / cx2) *  5;
    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.style.transition = 'transform 0.5s ease';
  });
  card.addEventListener('mouseenter', () => {
    card.style.transition = 'transform 0.1s ease, border-color 0.3s, box-shadow 0.3s';
  });
});

/* ===== SKILL CHIP RIPPLE ===== */
document.querySelectorAll('.skill-chip').forEach(chip => {
  chip.addEventListener('click', function(e) {
    const ripple = document.createElement('div');
    const rect   = this.getBoundingClientRect();
    ripple.style.cssText = `
      position: absolute;
      width: 10px; height: 10px;
      background: rgba(0,245,255,0.4);
      border-radius: 50%;
      top: ${e.clientY - rect.top - 5}px;
      left: ${e.clientX - rect.left - 5}px;
      transform: scale(0);
      animation: rippleAnim 0.5s ease-out forwards;
      pointer-events: none;
    `;
    if (getComputedStyle(this).position === 'static') this.style.position = 'relative';
    this.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove());
  });
});

/* ===== INJECT RIPPLE KEYFRAME ===== */
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
  @keyframes rippleAnim {
    to { transform: scale(14); opacity: 0; }
  }
  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(rippleStyle);

/* ===== ABOUT AVATAR MOUSE PARALLAX ===== */
const avatar = document.getElementById('aboutAvatar');
if (avatar) {
  document.addEventListener('mousemove', e => {
    const rect = avatar.getBoundingClientRect();
    const dx   = (e.clientX - (rect.left + rect.width  / 2)) / window.innerWidth;
    const dy   = (e.clientY - (rect.top  + rect.height / 2)) / window.innerHeight;
    avatar.style.transform = `perspective(600px) rotateY(${dx * 8}deg) rotateX(${-dy * 8}deg)`;
  });
}

/* ===== SECTION GLOW ON HOVER ===== */
document.querySelectorAll('.timeline-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.background = 'rgba(13,31,60,0.85)';
  });
  card.addEventListener('mouseleave', () => {
    card.style.background = '';
  });
});

/* ===== KEYBOARD SHORTCUTS ===== */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (hamburger) hamburger.classList.remove('open');
    if (navLinks)  navLinks.classList.remove('open');
  }
  // Press '1'-'6' to jump sections
  const sectionMap = {
    '1': '#home', '2': '#about', '3': '#skills',
    '4': '#experience', '5': '#projects', '6': '#contact'
  };
  if (sectionMap[e.key] && !e.ctrlKey && !e.metaKey && !e.altKey) {
    const el = document.querySelector(sectionMap[e.key]);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }
});

/* ===== PAGE VISIBILITY — pause animations when tab hidden ===== */
document.addEventListener('visibilitychange', () => {
  const canvas = document.getElementById('heroCanvas');
  if (canvas) canvas.style.animationPlayState = document.hidden ? 'paused' : 'running';
});

/* ===== CONSOLE EASTER EGG ===== */
console.log('%c HRG PORTFOLIO ', 'background:#00f5ff;color:#020b18;font-size:18px;font-weight:900;padding:6px 16px;border-radius:2px;');
console.log('%c Built by Harish Raghavendar G ', 'color:#2196f3;font-size:12px;');
console.log('%c QA Tester × Data Scientist | harishraghav906@gmail.com ', 'color:#48cae4;font-size:11px;');
console.log('%c Press keys 1-6 to jump between sections! ', 'color:#90e0ef;font-size:11px;');
