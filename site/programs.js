(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { programs: [] };
  const app = document.getElementById('app');
  let programs = [];
  let library = null;
  let loadWarning = '';

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function searchableText(program) {
    return [
      program.school, program.title, program.type, program.scale, program.fundamental,
      program.whyExplore, program.lookFirst,
      ...(program.tags || []), ...(program.scienceFoundation || []),
      ...(program.animalContent || []), ...(program.experienceTags || [])
    ].join(' ').toLowerCase();
  }
  async function fetchJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }
  async function loadPrograms() {
    const focused = (D.programs || []).map(program => ({ ...program, collection: program.collection || 'focused' }));
    let additions = [];
    try {
      [additions, library] = await Promise.all([
        fetchJson('content/programs/additional-programs.json'),
        fetchJson('content/programs/school-library.json')
      ]);
      if (!Array.isArray(additions)) throw new Error('Expected an array of additional programs');
      if (!library || !Array.isArray(library.programs)) throw new Error('Expected school-library programs');
    } catch (error) {
      console.error('Unable to load the current school library:', error);
      loadWarning = 'The current school-library file could not be loaded. Showing the researched program set instead.';
      programs = [...focused, ...(Array.isArray(additions) ? additions : [])];
      return;
    }
    const detailed = new Map();
    [...focused, ...additions].forEach(program => {
      if (program && program.code && !detailed.has(program.code)) detailed.set(program.code, program);
    });
    const missing = [];
    programs = library.programs.map(item => {
      const detail = detailed.get(item.code);
      if (!detail) {
        missing.push(item.code);
        return null;
      }
      return { ...detail, ...item, libraryCurrent: true };
    }).filter(Boolean);
    if (missing.length) {
      loadWarning = `Some library records are missing detailed program data: ${missing.join(', ')}.`;
    }
  }
  function renderProgram(program) {
    const tags = (program.tags || []).length
      ? `<span class="program-tags">${program.tags.map(tag => esc(tag)).join(' · ')}</span>`
      : '';
    return `<a class="guide-link program-guide-link" href="program.html?code=${encodeURIComponent(program.code)}">
      <span class="guide-count">${String(programs.indexOf(program) + 1).padStart(2, '0')}</span>
      <span class="guide-copy">
        <strong>${esc(program.title)}</strong>
        <span>${esc(program.whyExplore || program.fundamental)}</span>
        ${tags}
        <span class="index-meta">${esc(program.type)} · ${esc(program.scale)}</span>
      </span>
      <span class="guide-arrow" aria-hidden="true">Read guide&nbsp;→</span>
    </a>`;
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const matches = programs.filter(program => !q || searchableText(program).includes(q));
    const schools = [...new Set(matches.map(program => program.school))];
    app.innerHTML = `<div class="index-page">
      <header class="index-hero">
        <p class="eyebrow">Browse, don't rank</p>
        <h1>School &amp; Program Library</h1>
        <p>These are programs worth examining because they connect directly to the current animal-focused fields. A school can appear through more than one pathway, and no single field or program is treated as the winner.</p>
        <label class="guide-search" for="programSearch"><span>Find a school, program, or interest</span><input id="programSearch" type="search" placeholder="Try behavior, welfare, vet tech, zoo…" value="${esc(query || '')}"></label>
        ${loadWarning ? `<p class="load-warning" role="status">${esc(loadWarning)}</p>` : ''}
      </header>
      <section class="guide-index" aria-labelledby="programIndexTitle">
        <div class="section-heading"><p class="section-number">Current exploration set</p><h2 id="programIndexTitle">Choose a school or pathway to examine</h2></div>
        ${matches.length ? `<div class="collection-heading library-note"><p class="eyebrow">How inclusion works</p><p>Programs enter this library through evidence of strength in the current school-fit fields: animal biology, zoology, wildlife biology, animal behavior, animal welfare science, non-agricultural animal science, zoo/aquarium science or managed animal care, and veterinary technology. Other field guides remain useful context but do not qualify a school by themselves.</p></div>` : ''}
        ${matches.length ? schools.map((school, schoolIndex) => `<section class="index-group">
          <h3>${esc(school)}</h3>
          <div class="guide-list">${matches.filter(program => program.school === school).map(renderProgram).join('')}</div>
        </section>`).join('') : '<p class="empty">No college programs match that search.</p>'}
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
  menuButton.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', () => {
    nav.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  });
  loadPrograms().then(() => render(''));
})();
