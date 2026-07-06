// ── Particles ─────────────────────────────────────────────
function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 4 + 2;
    p.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}%;
      animation-duration:${Math.random() * 15 + 10}s;
      animation-delay:-${Math.random() * 20}s;
    `;
    container.appendChild(p);
  }
}
createParticles();

// ── Animate dial on load ───────────────────────────────────
window.addEventListener('load', () => {
  const arc = document.getElementById('dialArc');
  if (!arc) return;
  const target = parseInt(arc.dataset.target);
  arc.style.strokeDashoffset = '565';
  setTimeout(() => {
    arc.style.strokeDashoffset = target;
  }, 400);
});

// ── Animate metric bars ────────────────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.mc-fill, .prob-fill').forEach(el => {
        const w = el.style.width;
        el.style.width = '0';
        setTimeout(() => { el.style.transition = 'width 0.8s ease'; el.style.width = w; }, 100);
      });
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll('.metrics-grid, .prob-bars').forEach(el => observer.observe(el));
