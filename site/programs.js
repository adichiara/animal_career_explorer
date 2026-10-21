(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { programs: [] };
  const app = document.getElementById('app');
  let programs = [];
  let loadWarning = '';
  const CURRENT_FOCUS = window.PROGRAM_FOCUS_AREAS || {};

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function searchableText(program) {
    return [program.school, program.title, program.type, program.scale, program.fundamental, ...(program.scienceFoundation || []), ...(program.animalContent || []), ...(program.experienceTags || []), ...(CURRENT_FOCUS[program.code] || [])].join(' ').toLowerCase();
  }
  async function loadPrograms() {
    const focused = (D.programs || []).map(program => ({ ...program, collection: program.collection || 'focused' }));
    try {
      const response = await fetch('content/programs/additional-programs.json');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const additions = await response.json();
      if (!Array.isArray(additions)) throw new Error('Expected an array of programs');
      const codes = new Set(focused.map(program => program.code));
      programs = [...focused, ...additions.filter(program => program && program.code && !codes.has(program.code))];
    } catch (error) {
      programs = focused;
      loadWarning = 'The additional-program file could not be loaded. The focused comparison is still available.';
      console.error('Unable to load additional college programs:', error);
    }
  }
  function renderCollection(collection, matches) {
    const inCollection = matches.filter(collection.test);
    if (!inCollection.length) return '';
    const schools = [...new Set(inCollection.map(program => program.school))];
    return `<section class="program-collection" aria-labelledby="${collection.key}Title">
      <div class="collection-heading"><p class="eyebrow">${esc(collection.eyebrow.replace('{count}', String(inCollection.length)))}</p><h2 id="${collection.key}Title">${esc(collection.title)}</h2><p>${esc(collection.description)}</p></div>
      ${schools.map(school => `<section class="index-group"><h3>${esc(school)}</h3><div class="guide-list">${inCollection.filter(program => program.school === school).map(program => `<a class="guide-link program-guide-link" href="program.html?code=${encodeURIComponent(program.code)}">
        <span class="guide-count">${String(programs.indexOf(program) + 1).padStart(2, '0')}</span><span class="guide-copy"><strong>${esc(program.title)}</strong><span>${esc(program.fundamental)}</span><span class="index-meta">${esc(program.type)} · ${esc(program.scale)}</span>${CURRENT_FOCUS[program.code] ? `<span class="index-meta"><strong>Current-focus match:</strong> ${CURRENT_FOCUS[program.code].map(esc).join(' · ')}</span>` : '<span class="index-meta">Related comparison only; does not independently drive recommendations</span>'}</span><span class="guide-arrow" aria-hidden="true">Read guide&nbsp;→</span>
      </a>`).join('')}</div></section>`).join('')}
    </section>`;
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const matches = programs.filter(program => !q || searchableText(program).includes(q));
    const collections = [
      { key: 'focus', eyebrow: 'Current focus · {count} pathways', title: 'Programs that match the current animal-career focus', description: 'These programs have documented strength in at least one recommendation-driving area: animal biology, zoology, wildlife biology, animal behavior, animal welfare science, non-agricultural animal science, zoo/aquarium managed-animal care, or veterinary technology. This is a relevance filter, not a ranking.', test: program => Boolean(CURRENT_FOCUS[program.code]) },
      { key: 'context', eyebrow: 'Context · {count} pathways', title: 'Related programs kept for comparison', description: 'These are legitimate animal-related pathways, but their center of gravity is in adjacent areas such as conservation/ecology, agriculture/pre-vet, or wildlife rehabilitation. They remain visible for completeness and do not independently drive school recommendations.', test: program => !CURRENT_FOCUS[program.code] }
    ];
    app.innerHTML = `<div class="index-page">
      <header class="index-hero">
        <h1>College Programs</h1>
        <p class="section-intro">School-fit comparisons are now anchored to eight core fields. Marine biology remains available as a species/environment context but is not an emphasized recommendation category.</p>
        <label class="guide-search" for="programSearch"><span>Find a school, program, or subject</span><input id="programSearch" type="search" placeholder="Try behavior, wildlife, fieldwork, GIS…" value="${esc(query || '')}"></label>
        ${loadWarning ? `<p class="load-warning" role="status">${esc(loadWarning)}</p>` : ''}
      </header>
      <section class="guide-index" aria-labelledby="programIndexTitle">
        <div class="section-heading"><p class="section-number">College program index</p><h2 id="programIndexTitle">Choose a program to examine</h2></div>
        ${matches.length ? collections.map(collection => renderCollection(collection, matches)).join('') : '<p class="empty">No college programs match that search.</p>'}
      </section>
    </div>`;
    const search = document.getElementById('programSearch');
    search.addEventListener('input', event => render(event.target.value));
    if (query) {
      search.focus({ preventScroll: true });
      search.setSelectionRange(search.value.length, search.value.length);
    }
  }
  const menuButton = document.getElementById('menuButton');
  const nav = document.getElementById('primaryNav');
  menuButton.addEventListener('click', () => { const open = nav.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); });
  nav.addEventListener('click', () => { nav.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); });
  loadPrograms().then(() => render(''));
})();
