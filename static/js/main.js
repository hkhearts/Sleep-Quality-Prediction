// ── Particles ──────────────────────────────────────────────────────
function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 25; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 4 + 2;
    const colors = [
      'rgba(124,58,237,0.5)', 'rgba(6,182,212,0.5)',
      'rgba(16,185,129,0.4)', 'rgba(192,132,252,0.4)'
    ];
    p.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}%;
      animation-duration:${Math.random() * 15 + 10}s;
      animation-delay:-${Math.random() * 20}s;
      background:radial-gradient(circle,${colors[Math.floor(Math.random()*colors.length)]} 0%,transparent 70%);
    `;
    container.appendChild(p);
  }
}
createParticles();

// ── Watch clock ────────────────────────────────────────────────────
function updateWatch() {
  const el = document.getElementById('watch-time');
  if (!el) return;
  const now = new Date();
  const h = String(now.getHours()).padStart(2,'0');
  const m = String(now.getMinutes()).padStart(2,'0');
  el.textContent = `${h}:${m}`;
}
updateWatch();
setInterval(updateWatch, 1000);

// ── Animate watch metrics ──────────────────────────────────────────
function animateWatchMetrics() {
  const hr  = document.getElementById('w-hr');
  const spo = document.getElementById('w-spo2');
  const eff = document.getElementById('w-eff');
  if (!hr) return;
  setInterval(() => {
    const hrVal  = Math.round(60 + Math.random() * 20);
    const spoVal = (95 + Math.random() * 4).toFixed(1);
    const effVal = Math.round(72 + Math.random() * 20);
    hr.textContent  = hrVal;
    spo.textContent = spoVal;
    eff.textContent = effVal + '%';
    // Update ring
    const ring = document.getElementById('ring-progress');
    if (ring) {
      const dashOffset = 213.6 - (effVal / 100 * 213.6);
      ring.style.strokeDashoffset = dashOffset;
    }
  }, 3000);
}
animateWatchMetrics();

// ── Wearable Simulator ─────────────────────────────────────────────
const SIM_URL = '/simulate/';

function simulate(bias) {
  const status = document.getElementById('sim-status');
  status.textContent = '⌚ Syncing wearable data...';

  const formData = new FormData();
  formData.append('quality_bias', bias);
  formData.append('csrfmiddlewaretoken', getCsrf());

  fetch(SIM_URL, { method: 'POST', body: formData })
    .then(r => r.json())
    .then(data => {
      // Fill all form fields with animation
      const fieldMap = {
        heart_rate: data.heart_rate,
        spo2: data.spo2,
        skin_temperature: data.skin_temperature,
        eda: data.eda,
        active_zone_min: data.active_zone_min,
        screen_time: data.screen_time,
        screen_brightness: data.screen_brightness,
        stress_score: data.stress_score,
        sleep_efficiency: data.sleep_efficiency,
        sleep_latency: data.sleep_latency,
        waso: data.waso,
        rem_pct: data.rem_pct,
        deep_pct: data.deep_pct
      };

      Object.entries(fieldMap).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) {
          el.value = '';
          el.style.transition = 'color 0.3s';
          el.style.color = '#7C3AED';
          setTimeout(() => {
            el.value = val;
            el.style.color = '';
            el.dispatchEvent(new Event('input'));
          }, 200 + Math.random() * 300);
        }
      });

      const labels = { poor:'😴 Poor night simulated', fair:'😐 Average night simulated', good:'😊 Great night simulated', random:'🎲 Random night simulated' };
      status.textContent = `✓ ${labels[bias] || 'Data loaded'} — All 13 fields updated from wearable`;
      status.style.color = '#4ECDC4';
    })
    .catch(() => {
      status.textContent = '⚠️ Simulation failed. Please try again.';
      status.style.color = '#FF6B6B';
    });
}

function getCsrf() {
  const el = document.querySelector('[name=csrfmiddlewaretoken]');
  return el ? el.value : '';
}

// ── Form submit loader ─────────────────────────────────────────────
const form = document.getElementById('mainForm');
if (form) {
  form.addEventListener('submit', () => {
    const btn = document.getElementById('submitBtn');
    if (btn) btn.classList.add('loading');
  });
}

// ── Smooth scroll for nav links ────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── Input highlight on focus ───────────────────────────────────────
document.querySelectorAll('.input-group input').forEach(input => {
  input.addEventListener('focus', () => {
    input.closest('.input-group').style.background = 'rgba(124,58,237,0.06)';
  });
  input.addEventListener('blur', () => {
    input.closest('.input-group').style.background = '';
  });
});
