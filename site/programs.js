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
  function displaySchool(program) {
    const school = String(program && program.school || '');
    if (school === 'UMass Amherst' || school === 'University of Massachusetts Amherst') return 'University of Massachusetts Amherst';
    if (school === 'University of Maine') return 'University of Maine (Orono)';
    if (school === 'University of Maine at Augusta') return 'University of Maine at Augusta (Bangor Campus)';
    if (school === 'SUNY Canton') return 'SUNY Canton (Canton Campus)';
    if (school === 'SUNY Delhi') return 'SUNY Delhi (Delhi Campus)';
    return school;
  }
  const newEnglandSchools = new Set([
    'University of Maine',
    'University of Maine at Augusta',
    'UMass Amherst',
    'University of Massachusetts Amherst',
    'University of New England',
    'University of Rhode Island',
    'University of New Hampshire',
    'Unity Environmental University'
  ]);
  function regionFor(program) {
    return newEnglandSchools.has(String(program && program.school || '')) ? 'New England' : 'Outside New England';
  }
  function searchableText(program) {
    return [
      displaySchool(program), program.school, program.title, program.type, program.scale, program.fundamental,
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
        <span>${esc(program.fundamental || '')}</span>
        ${tags}
        <span class="index-meta">${esc(program.type)} · ${esc(program.scale)}</span>
      </span>
      <span class="guide-arrow" aria-hidden="true">Read guide&nbsp;→</span>
    </a>`;
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const matches = programs
      .filter(program => !q || searchableText(program).includes(q))
      .sort((a, b) => displaySchool(a).localeCompare(displaySchool(b)) || a.title.localeCompare(b.title));

    const renderRegion = (title, items) => {
      if (!items.length) return '';
      const schools = [...new Set(items.map(displaySchool))].sort((a, b) => a.localeCompare(b));
      return `<section class="program-region"><div class="section-heading"><h2>${esc(title)}</h2></div>${schools.map(school => `<section class="index-group">
        <h3>${esc(school)}</h3>
        <div class="guide-list">${items.filter(program => displaySchool(program) === school).map(renderProgram).join('')}</div>
      </section>`).join('')}</section>`;
    };

    const newEngland = matches.filter(program => regionFor(program) === 'New England');
    const outside = matches.filter(program => regionFor(program) === 'Outside New England');

    app.innerHTML = `<div class="index-page">
      <header class="index-hero">
        <h1>School &amp; Program Library</h1>
        <label class="guide-search" for="programSearch"><span>Find a school, program, or interest</span><input id="programSearch" type="search" placeholder="Try behavior, welfare, vet tech, zoo…" value="${esc(query || '')}"></label>
        ${loadWarning ? `<p class="load-warning" role="status">${esc(loadWarning)}</p>` : ''}
      </header>
      <section class="guide-index" aria-label="School and program library">
        ${matches.length ? renderRegion('New England', newEngland) + renderRegion('Outside New England', outside) : '<p class="empty">No college programs match that search.</p>'}
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
