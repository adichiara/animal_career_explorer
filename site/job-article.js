(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { careers: [], programs: [] };
  const app = document.getElementById('articleApp');
  const slug = new URLSearchParams(location.search).get('role');
  const careers = D.careers.filter(career => (career.recentPostings || []).length || (career.observedTitles || []).length);

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function prettyDate(value) {
    if (!value) return 'Date not recorded';
    const date = new Date(`${value}T00:00:00`);
    return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'long', day: 'numeric' }).format(date);
  }
  function money(value, currency) {
    if (value == null) return '';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: currency || 'USD', maximumFractionDigits: Number(value) % 1 ? 2 : 0 }).format(value);
  }
  function salary(item) {
    if (item.salary_min == null && item.salary_max == null) return '';
    const low = money(item.salary_min, item.currency); const high = money(item.salary_max, item.currency);
    const range = low && high && low !== high ? `${low}–${high}` : low || high;
    return `${range} ${item.salary_unit || ''}`.trim();
  }
  function examples(career) {
    const combined = [
      ...(career.recentPostings || []).map(item => Object.assign({ employer: item.employer, date: item.posted_date }, item)),
      ...(career.observedTitles || []).map(item => ({ title: item.title, employer: item.organization, location: item.location, date: item.observed_date, retrieved_date: item.observed_date, notes: item.notes, url: item.source && item.source.url, source: item.source }))
    ];
    const seen = new Set();
    return combined.filter(item => {
      const key = [item.title, item.employer, item.location].map(value => String(value || '').toLowerCase().trim()).join('|');
      if (seen.has(key)) return false;
      seen.add(key); return true;
    });
  }
  function detailRows(career) {
    const d = career.details || {};
    return [['Typical work settings', d['Typical work settings']], ['Titles used in searches', d['Searchable job titles']], ['Alternate terms', d['Alternate names / terms']], ['Education and progression', d['Typical education / progression']], ['Job outlook context', d['Job outlook']], ['Salary context', d['Salary context']]].filter(([, value]) => value);
  }
  function programLinks(career) {
    const supportOrder = { S: 0, C: 1, G: 2 };
    return Object.entries(career.support || {}).filter(([, level]) => level && level !== 'N').sort((a, b) => (supportOrder[a[1]] ?? 9) - (supportOrder[b[1]] ?? 9)).map(([code, level]) => {
      const program = D.programs.find(item => item.code === code); if (!program) return '';
      const label = level === 'S' ? 'Strong/direct preparation' : level === 'C' ? 'Credible with planning' : 'Graduate-oriented foundation';
      return `<a href="program.html?code=${encodeURIComponent(code)}"><span><strong>${esc(program.title)}</strong><small>${esc(program.school)}</small></span><em>${esc(label)}</em></a>`;
    }).join('');
  }
  function sourceItems(career, items) {
    const map = new Map();
    [...items.map(item => item.source).filter(Boolean), ...(career.evidence || []).map(item => item.source).filter(Boolean)].forEach(source => {
      if (source.url && !map.has(source.url)) map.set(source.url, source);
    });
    return [...map.values()];
  }
  function render(career) {
    const items = examples(career);
    const index = careers.indexOf(career); const previous = careers[(index - 1 + careers.length) % careers.length]; const next = careers[(index + 1) % careers.length];
    const details = detailRows(career); const sources = sourceItems(career, items);
    document.title = `${career.name} | Job Examples`;
    document.querySelector('meta[name="description"]').setAttribute('content', career.roleFocus);
    app.innerHTML = `<article class="field-article job-article">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="jobs.html">All job examples</a><span aria-hidden="true">/</span><span>${esc(career.name)}</span></nav>
      <header class="article-hero text-hero job-hero"><div class="hero-copy"><div class="eyebrow">Job example guide</div><h1>${esc(career.name)}</h1><p class="standfirst">${esc(career.roleFocus)}</p></div>
        <aside class="hero-facts" aria-label="Role facts"><p class="mini-label">Role at a glance</p><dl><div><dt>Observed examples</dt><dd>${items.length}</dd></div><div><dt>Role family</dt><dd>${esc(career.roleFamily && career.roleFamily.name || career.category)}</dd></div><div><dt>Typical education</dt><dd>${esc(career.educationBand || 'Varies')}</dd></div><div><dt>Direct animal contact</dt><dd>${esc(career.directContact || 'Varies')}</dd></div></dl></aside>
      </header>
      <div class="article-body"><aside class="article-toc" aria-labelledby="tocTitle"><p id="tocTitle" class="mini-label">On this page</p><ol><li><a href="#examples">Observed examples</a></li><li><a href="#role">Understanding the role</a></li><li><a href="#preparation">Preparation and skills</a></li><li><a href="#requirements">Requirements and evidence</a></li><li><a href="#college">College connections</a></li><li><a href="#sources">Sources</a></li></ol></aside>
        <div class="article-content">
          <section id="examples" class="article-section first-section"><div class="section-heading"><p class="section-number">01</p><h2>Observed job examples</h2></div><p class="section-intro">These postings were recorded as examples of titles and requirements. They may no longer be open.</p>
            <div class="posting-list">${items.map(item => `<article class="posting"><div class="posting-date"><span>Observed</span><strong>${esc(prettyDate(item.date || item.posted_date))}</strong></div><div class="posting-main"><h3>${esc(item.title)}</h3><p class="posting-employer">${esc(item.employer || 'Employer not recorded')}${item.location ? ` · ${esc(item.location)}` : ''}</p><dl>${[['Employment', item.employment_type], ['Minimum education', item.education_min], ['Minimum experience', item.experience_min], ['Compensation', salary(item)]].filter(([, value]) => value).map(([term, value]) => `<div><dt>${esc(term)}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl>${item.notes ? `<p class="posting-note">${esc(item.notes)}</p>` : ''}${item.url || item.source && item.source.url ? `<a class="inline-source" href="${esc(item.url || item.source.url)}" target="_blank" rel="noopener">Original or source record →</a>` : ''}</div></article>`).join('')}</div>
          </section>
          <section id="role" class="article-section"><div class="section-heading"><p class="section-number">02</p><h2>Understanding the role</h2></div><div class="role-details"><dl>${details.map(([term, value]) => `<div><dt>${esc(term)}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl></div><div class="fact-line">${(career.workTags || []).map(value => `<span>${esc(value)}</span>`).join('')}</div></section>
          <section id="preparation" class="article-section"><div class="section-heading"><p class="section-number">03</p><h2>Preparation and skills</h2></div><h3 class="group-heading first">Useful undergraduate preparation</h3><p class="resume-outcome">${esc((career.details || {})['Undergraduate preparation most useful'] || 'Preparation depends on the work setting and employer.')}</p>
            <h3 class="group-heading">Common competencies</h3><div class="competency-grid">${(career.competencies || []).map(item => `<article><span class="importance-mark">${item.importance === 'essential' ? 'Core' : 'Useful'}</span><div><h3>${esc(item.name)}</h3><p>${esc(item.description)}</p><span>${esc(item.category)}</span></div></article>`).join('')}</div>
          </section>
          <section id="requirements" class="article-section"><div class="section-heading"><p class="section-number">04</p><h2>Requirements and supporting evidence</h2></div>
            ${(career.credentials || []).length ? `<h3 class="group-heading first">Credentials or permits</h3><div class="prose-blocks">${career.credentials.map(item => `<article><h3>${esc(item.name)}</h3><p>${esc(item.description)}</p>${item.notes ? `<p>${esc(item.notes)}</p>` : ''}${item.source_url ? `<a class="inline-source" href="${esc(item.source_url)}" target="_blank" rel="noopener">Credential source →</a>` : ''}</article>`).join('')}</div>` : '<p class="section-intro">No role-specific credential or permit was recorded in this research set.</p>'}
            ${(career.evidence || []).length ? `<h3 class="group-heading">Verified findings</h3><ul class="narrative-list">${career.evidence.map(item => `<li><h3>${esc(String(item.claim_type || 'Evidence').replace(/_/g, ' '))}</h3><p>${esc(item.claim_value)}</p>${item.source && item.source.url ? `<a class="inline-source" href="${esc(item.source.url)}" target="_blank" rel="noopener">${esc(item.source.title)} →</a>` : ''}</li>`).join('')}</ul>` : ''}
          </section>
          <section id="college" class="article-section"><div class="section-heading"><p class="section-number">05</p><h2>College program connections</h2></div><p class="section-intro">These links describe how the researched programs support preparation for the broader role. They are not admissions recommendations.</p><div class="program-connection-list">${programLinks(career) || '<p>No program connection is recorded for this role.</p>'}</div></section>
          <section id="sources" class="article-section"><div class="section-heading"><p class="section-number">06</p><h2>Sources and dates</h2></div><ul class="source-list">${sources.map(source => `<li><a href="${esc(source.url)}" target="_blank" rel="noopener">${esc(source.title || source.organization || source.url)}</a><span>${esc(source.organization || '')}${source.retrieved_date ? ` · Retrieved ${esc(prettyDate(source.retrieved_date))}` : ''}</span></li>`).join('')}</ul><p class="source-date">Role research last verified: ${esc(prettyDate(career.lastVerified))}</p></section>
        </div>
      </div>
      <nav class="article-pagination" aria-label="Job example navigation"><a href="job.html?role=${encodeURIComponent(previous.slug)}"><span>Previous role</span><strong>← ${esc(previous.name)}</strong></a><a class="all-guides" href="jobs.html">All job examples</a><a class="next" href="job.html?role=${encodeURIComponent(next.slug)}"><span>Next role</span><strong>${esc(next.name)} →</strong></a></nav>
    </article>`;
  }
  function fail(message) { app.innerHTML = `<div class="error-page"><h1>This job example guide could not be loaded</h1><p>${esc(message)}</p><p><a href="jobs.html">Return to all job examples</a></p></div>`; }
  const career = careers.find(item => item.slug === slug); if (career) render(career); else fail(slug ? `No job examples were found for ${slug}.` : 'Choose a role from the job example index.');
  const menuButton = document.getElementById('menuButton'); const nav = document.getElementById('primaryNav');
  menuButton.addEventListener('click', () => { const open = nav.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); });
  nav.addEventListener('click', () => { nav.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); });
})();
