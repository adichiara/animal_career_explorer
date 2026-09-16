(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { careers: [] };
  const app = document.getElementById('app');
  const careerRoles = D.careers.filter(career => career.roleKind === 'career');
  const specialties = D.careers.filter(career => career.roleKind === 'scientific_specialty');
  const supplementalRoles = D.careers.filter(career => career.roleKind === 'later_career' || career.roleKind === 'professional_assignment');

  const specialtyParent = {
    'animal-communication-researcher': 'animal-behavior-research-assistant-technician',
    'animal-learning-researcher': 'animal-behavior-research-assistant-technician',
    'comparative-cognition-researcher': 'animal-behavior-research-assistant-technician',
    'companion-animal-behavior-researcher': 'shelter-behavior-specialist-coordinator',
    'behavioral-ecologist': 'wildlife-biologist',
    'herpetologist': 'wildlife-biologist',
    'mammalogist': 'wildlife-biologist',
    'ornithologist': 'wildlife-biologist',
    'animal-physiologist': 'zoologist',
    'neuroethologist-neural-behavior-researcher': 'zoologist',
    'conservation-geneticist-wildlife-genomicist': 'evolutionary-biologist-studying-animals',
    'research-ecologist': 'field-ecologist',
    'conservation-breeding-scientist': 'conservation-breeding-technician',
    'population-biologist-zoo-population-management-scientist': 'conservation-breeding-technician',
    'ecological-data-scientist': 'quantitative-ecologist-biometrician',
    'research-statistician-ecology-biology': 'quantitative-ecologist-biometrician',
    'human-dimensions-conservation-social-scientist': 'human-wildlife-conflict-specialist',
    'remote-sensing-geospatial-ecologist': 'gis-wildlife-spatial-analyst'
  };

  const specialtiesByParent = new Map();
  specialties.forEach(specialty => {
    const parent = specialtyParent[specialty.slug];
    if (!parent) {
      console.warn('Scientific specialty has no job-index parent:', specialty.name);
      return;
    }
    if (!specialtiesByParent.has(parent)) specialtiesByParent.set(parent, []);
    specialtiesByParent.get(parent).push(specialty);
  });
  specialtiesByParent.forEach(items => items.sort((a, b) => a.name.localeCompare(b.name)));

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function roleKindLabel(career) {
    return (D.roleKindLabels && D.roleKindLabels[career.roleKind]) || String(career.roleKind || 'career').replaceAll('_', ' ');
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
      seen.add(key);
      return true;
    });
  }
  function ownSearchableText(career) {
    return [career.name, career.category, career.roleFocus, career.roleFamily && career.roleFamily.name, ...examples(career).flatMap(item => [item.title, item.employer, item.location])].join(' ').toLowerCase();
  }
  function searchableText(career) {
    const related = specialtiesByParent.get(career.slug) || [];
    return [ownSearchableText(career), ...related.map(ownSearchableText)].join(' ');
  }
  function specialtyLinks(career) {
    const related = specialtiesByParent.get(career.slug) || [];
    if (!related.length) return '';
    return `<div class="job-specialties"><span class="job-specialties-label">Related scientific specialties</span><div class="job-specialty-links">${related.map(specialty => {
      const count = examples(specialty).length;
      return `<a class="job-specialty-link" href="job.html?role=${encodeURIComponent(specialty.slug)}"><strong>${esc(specialty.name)}</strong><span>${esc(roleKindLabel(specialty))}${count ? ` · ${count} observed ${count === 1 ? 'example' : 'examples'}` : ''}</span></a>`;
    }).join('')}</div></div>`;
  }
  function roleEntry(career, showKind) {
    const items = examples(career);
    const sample = items.slice(0, 2).map(item => item.title).join(' · ') || 'No observed job example in this research snapshot.';
    const related = specialtiesByParent.get(career.slug) || [];
    const kind = showKind ? ` · ${esc(roleKindLabel(career))}` : '';
    return `<div class="job-index-entry${related.length ? ' has-specialties' : ''}">
      <a class="guide-link job-guide-link" href="job.html?role=${encodeURIComponent(career.slug)}"><span class="guide-count">${items.length}</span><span class="guide-copy"><strong>${esc(career.name)}</strong><span>${esc(sample)}</span><span class="index-meta">${items.length} observed ${items.length === 1 ? 'example' : 'examples'} · ${esc(career.roleFamily && career.roleFamily.name || career.category)}${kind}</span></span><span class="guide-arrow" aria-hidden="true">View examples&nbsp;→</span></a>
      ${specialtyLinks(career)}
    </div>`;
  }
  function render(query) {
    const q = String(query || '').trim().toLowerCase();
    const careerMatches = careerRoles.filter(career => !q || searchableText(career).includes(q));
    const supplementalMatches = supplementalRoles.filter(career => !q || ownSearchableText(career).includes(q));
    const categories = [...new Set(careerMatches.map(career => career.category))].sort();

    const careerMarkup = careerMatches.length
      ? categories.map(category => `<section class="index-group"><h3>${esc(category)}</h3><div class="guide-list">${careerMatches.filter(career => career.category === category).map(career => roleEntry(career, false)).join('')}</div></section>`).join('')
      : '<p class="empty">No career roles match that search.</p>';

    const supplementalKinds = ['later_career', 'professional_assignment'];
    const supplementalMarkup = supplementalMatches.length
      ? `<section class="job-supplemental" aria-labelledby="supplementalTitle"><div class="collection-heading"><p class="section-number">Beyond entry roles</p><h2 id="supplementalTitle">Later-career roles and professional assignments</h2><p>These are kept separate from the primary career-role index so they are not mistaken for typical entry points.</p></div>
          ${supplementalKinds.map(kind => {
            const items = supplementalMatches.filter(career => career.roleKind === kind);
            if (!items.length) return '';
            const heading = kind === 'later_career' ? 'Later-career roles' : 'Professional assignments';
            return `<section class="index-group"><h3>${heading}</h3><div class="guide-list">${items.map(career => roleEntry(career, true)).join('')}</div></section>`;
          }).join('')}
        </section>`
      : '';

    app.innerHTML = `<div class="index-page jobs-index-page">
      <header class="index-hero">
        <h1>Job Examples</h1>
        <label class="guide-search" for="jobSearch"><span>Find a role, specialty, employer, title, or location</span><input id="jobSearch" type="search" placeholder="Try rehabilitation, keeper, cognition, GIS…" value="${esc(query || '')}"></label>
      </header>
      <section class="guide-index" aria-labelledby="jobIndexTitle"><div class="section-heading"><p class="section-number">Career role index</p><h2 id="jobIndexTitle">Career roles</h2></div>
        ${careerMarkup}
      </section>
      ${supplementalMarkup}
    </div>`;
    const search = document.getElementById('jobSearch');
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
  render('');
})();
