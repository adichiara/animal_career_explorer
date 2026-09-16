(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { careers: [] };
  const app = document.getElementById('app');
  const careers = D.careers.filter(career => (career.recentPostings || []).length || (career.observedTitles || []).length);

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function examples(career) {
    const combined = [
      ...(career.recentPostings || []).map(item => ({ title: item.title, employer: item.employer, location: item.location, date: item.posted_date })),
      ...(career.observedTitles || []).map(item => ({ title: item.title, employer: item.organization, location: item.location, date: item.observed_date }))
    ];
    const seen = new Set();
    return combined.filter(item => {
      const key = [item.title, item.employer, item.location].map(value => String(value || '').toLowerCase().trim()).join('|');
      if (seen.has(key)) return false;
      seen.add(key); return true;
    });
  }
  function searchableText(career) {
    return [career.name, career.category, career.roleFocus, career.roleFamily && career.roleFamily.name, ...examples(career).flatMap(item => [item.title, item.employer, item.location])].join(' ').toLowerCase();
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const matches = careers.filter(career => !q || searchableText(career).includes(q));
    const categories = [...new Set(matches.map(career => career.category))].sort();
    app.innerHTML = `<div class="index-page jobs-index-page">
      <header class="index-hero">
        <h1>Job Examples</h1>
        <label class="guide-search" for="jobSearch"><span>Find a role, employer, title, or location</span><input id="jobSearch" type="search" placeholder="Try rehabilitation, keeper, research, GIS…" value="${esc(query || '')}"></label>
      </header>
      <section class="guide-index" aria-labelledby="jobIndexTitle"><div class="section-heading"><p class="section-number">Job example index</p><h2 id="jobIndexTitle">Choose a role to examine</h2></div>
        ${matches.length ? categories.map(category => `<section class="index-group"><h3>${esc(category)}</h3><div class="guide-list">${matches.filter(career => career.category === category).map(career => {
          const items = examples(career); const sample = items.slice(0, 2).map(item => item.title).join(' · ');
          return `<a class="guide-link job-guide-link" href="job.html?role=${encodeURIComponent(career.slug)}"><span class="guide-count">${items.length}</span><span class="guide-copy"><strong>${esc(career.name)}</strong><span>${esc(sample)}</span><span class="index-meta">${items.length} observed ${items.length === 1 ? 'example' : 'examples'} · ${esc(career.roleFamily && career.roleFamily.name || career.category)}</span></span><span class="guide-arrow" aria-hidden="true">View examples&nbsp;→</span></a>`;
        }).join('')}</div></section>`).join('') : '<p class="empty">No job examples match that search.</p>'}
      </section>
    </div>`;
    const search = document.getElementById('jobSearch');
    search.addEventListener('input', event => render(event.target.value));
    if (query) { search.focus({ preventScroll: true }); search.setSelectionRange(search.value.length, search.value.length); }
  }
  const menuButton = document.getElementById('menuButton'); const nav = document.getElementById('primaryNav');
  menuButton.addEventListener('click', () => { const open = nav.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); });
  nav.addEventListener('click', () => { nav.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); });
  render('');
})();
