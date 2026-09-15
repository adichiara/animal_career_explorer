(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { programs: [] };
  const app = document.getElementById('app');

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function searchableText(program) {
    return [program.school, program.title, program.type, program.scale, program.fundamental, ...(program.scienceFoundation || []), ...(program.animalContent || []), ...(program.experienceTags || [])].join(' ').toLowerCase();
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const matches = D.programs.filter(program => !q || searchableText(program).includes(q));
    const schools = [...new Set(matches.map(program => program.school))];
    app.innerHTML = `<div class="index-page">
      <header class="index-hero">
        <div class="eyebrow">${D.programs.length} researched undergraduate pathways</div>
        <h1>Look inside the program, not only at the major name</h1>
        <p>Each guide examines a specific program’s academic foundation, animal-related content, research and experience structure, four-year progression, strengths, and tradeoffs.</p>
        <label class="guide-search" for="programSearch"><span>Find a school, program, or subject</span><input id="programSearch" type="search" placeholder="Try behavior, wildlife, fieldwork, GIS…" value="${esc(query || '')}"></label>
      </header>
      <section class="guide-index" aria-labelledby="programIndexTitle">
        <div class="section-heading"><p class="section-number">College program index</p><h2 id="programIndexTitle">Choose a program to examine</h2></div>
        ${matches.length ? schools.map(school => `<section class="index-group"><h3>${esc(school)}</h3><div class="guide-list">${matches.filter(program => program.school === school).map(program => `<a class="guide-link program-guide-link" href="program.html?code=${encodeURIComponent(program.code)}">
          <span class="guide-count">${String(D.programs.indexOf(program) + 1).padStart(2, '0')}</span><span class="guide-copy"><strong>${esc(program.title)}</strong><span>${esc(program.fundamental)}</span><span class="index-meta">${esc(program.type)} · ${esc(program.scale)}</span></span><span class="guide-arrow" aria-hidden="true">Read guide&nbsp;→</span>
        </a>`).join('')}</div></section>`).join('') : '<p class="empty">No college programs match that search.</p>'}
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
  render('');
})();
