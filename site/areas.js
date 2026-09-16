(function () {
  'use strict';
  const app = document.getElementById('app');
  let areas = [];

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  async function fetchJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }
  function searchableText(area) {
    const itemText = item => typeof item === 'string' ? item : Object.values(item || {}).flat().join(' ');
    return [area.title, area.short, area.bigPicture, ...area.focus.map(itemText), ...area.questions.map(itemText), ...area.knowledgeSkills.map(itemText), ...area.careers].join(' ').toLowerCase();
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const matches = areas.filter(area => !q || searchableText(area).includes(q));
    app.innerHTML = `<div class="index-page">
      <header class="index-hero">
        <h1>Field Guides</h1>
        <label class="guide-search" for="areaSearch"><span>Find a field or topic</span><input id="areaSearch" type="search" placeholder="Try behavior, rehabilitation, ecology…" value="${esc(query || '')}"></label>
      </header>
      <section class="guide-index" aria-labelledby="guideIndexTitle">
        <div class="section-heading"><p class="section-number">Field guide index</p><h2 id="guideIndexTitle">Choose an area to read</h2></div>
        <div class="guide-list">${matches.length ? matches.map((area, index) => `<a class="guide-link" href="areas/${esc(area.id)}.html">
          <span class="guide-count">${String(index + 1).padStart(2, '0')}</span>
          <span class="guide-copy"><strong>${esc(area.title)}</strong><span>${esc(area.short)}</span></span>
          <span class="guide-arrow" aria-hidden="true">Read guide&nbsp;→</span>
        </a>`).join('') : '<p class="empty">No field guides match that search.</p>'}</div>
      </section>
    </div>`;
    const search = document.getElementById('areaSearch');
    search.addEventListener('input', event => render(event.target.value));
    if (query) {
      search.focus({ preventScroll: true });
      search.setSelectionRange(search.value.length, search.value.length);
    }
  }
  async function initialize() {
    const legacy = (location.hash || '').match(/^#area\/([^/]+)/);
    if (legacy) {
      location.replace(`areas/${encodeURIComponent(legacy[1])}.html`);
      return;
    }
    try {
      const root = 'content/areas/';
      const manifest = await fetchJson(`${root}index.json`);
      areas = await Promise.all(manifest.areas.map(file => fetchJson(`${root}${file}`)));
      render('');
    } catch (error) {
      console.error(error);
      app.innerHTML = `<div class="error-page"><h1>Field guides could not be loaded</h1><p>Check the area JSON files, then reload the page.</p><code>${esc(error.message)}</code></div>`;
    }
  }
  const menuButton = document.getElementById('menuButton');
  const nav = document.getElementById('primaryNav');
  menuButton.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', () => {
    nav.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  });
  initialize();
})();
