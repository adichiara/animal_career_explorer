(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { careers: [], programs: [] };
  const app = document.getElementById('articleApp');
  const currentId = document.body.dataset.area;
  let areas = [];
  let photos = {};

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  async function fetchJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }
  function areaById(id) { return areas.find(area => area.id === id); }
  function careerByName(name) { return D.careers.find(career => career.name.toLowerCase() === name.toLowerCase()); }
  function programByCode(code) { return D.programs.find(program => program.code === code); }
  function photoFor(area) { return photos[area.id]; }
  function sourceFor(area, reference) {
    if (!reference) return null;
    return area.references.find(item => item.title === reference || item.url === reference) || null;
  }
  function sourceLink(area, reference) {
    const source = sourceFor(area, reference);
    return source ? `<a class="inline-source" href="${esc(source.url)}" target="_blank" rel="noopener">Source: ${esc(source.title)}</a>` : '';
  }
  function examplesHtml(examples) {
    if (!Array.isArray(examples) || !examples.length) return '';
    return `<div class="examples"><p class="mini-label">Examples</p>${examples.map(example => {
      if (typeof example === 'string') return `<p>${esc(example)}</p>`;
      return `<p>${example.label ? `<strong>${esc(example.label)}:</strong> ` : ''}${esc(example.text || example.description || '')}</p>`;
    }).join('')}</div>`;
  }
  function narrativeItems(items, area) {
    return items.map(item => {
      if (typeof item === 'string') return `<li><p>${esc(item)}</p></li>`;
      const title = item.title || item.label || item.term || '';
      const text = item.description || item.definition || item.text || '';
      return `<li>${title ? `<h3>${esc(title)}</h3>` : ''}<p>${esc(text)}</p>${examplesHtml(item.examples)}${sourceLink(area, item.source)}</li>`;
    }).join('');
  }
  function focusHtml(area) {
    return area.focus.map(item => `<article class="subsection"><h3>${esc(item.title)}</h3><p>${esc(item.description)}</p>${examplesHtml(item.examples)}${sourceLink(area, item.source)}</article>`).join('');
  }
  function questionsHtml(area) {
    return area.questions.map(item => `<article class="question"><h3>${esc(item.question)}</h3><p>${esc(item.approach)}</p>${examplesHtml(item.examples)}${sourceLink(area, item.source)}</article>`).join('');
  }
  function careerHtml(name) {
    const career = careerByName(name);
    if (!career) return `<article class="career-entry"><h3>${esc(name)}</h3><p>This role appears in the field guide, but no separate job-example page is currently available for it.</p></article>`;
    const details = career.details || {};
    const rows = [
      ['Typical settings', details['Typical work settings']],
      ['Useful undergraduate preparation', details['Undergraduate preparation most useful']],
      ['Education and progression', details['Typical education / progression']],
      ['Titles to search', details['Searchable job titles']]
    ].filter(row => row[1]);
    return `<article class="career-entry">
      <h3>${esc(career.name)}</h3><p>${esc(career.roleFocus)}</p>
      <div class="fact-line">${[career.educationBand, career.directContact ? `${career.directContact} direct animal contact` : '', ...(career.workTags || [])].filter(Boolean).map(value => `<span>${esc(value)}</span>`).join('')}</div>
      ${rows.length ? `<dl>${rows.map(([term, value]) => `<div><dt>${esc(term)}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl>` : ''}
      ${career.competencies && career.competencies.length ? `<div class="competencies"><p class="mini-label">Common competencies</p><ul>${career.competencies.map(item => `<li><strong>${esc(item.name)}</strong> — ${esc(item.description)}</li>`).join('')}</ul></div>` : ''}
      ${(career.recentPostings || []).length || (career.observedTitles || []).length ? `<a class="inline-source" href="../job.html?role=${encodeURIComponent(career.slug)}">View dated job examples →</a>` : ''}
    </article>`;
  }
  function programHtml(areaProgram) {
    const detailed = programByCode(areaProgram.code) || {};
    const program = Object.assign({}, detailed, areaProgram);
    const lists = [
      ['Science foundation', program.scienceFoundation],
      ['Animal-focused content', program.animalContent],
      ['Advantages', program.advantages],
      ['Important tradeoffs', program.tradeoffs]
    ].filter(([, values]) => Array.isArray(values) && values.length);
    return `<article class="program-entry">
      <p class="program-school">${esc(program.school || '')}</p><h3>${esc(program.title || program.code)}</h3>
      ${program.fundamental ? `<p>${esc(program.fundamental)}</p>` : ''}
      ${program.experience ? `<h4>Experience structure</h4><p>${esc(program.experience)}</p>` : ''}
      ${lists.map(([label, values]) => `<h4>${esc(label)}</h4><ul>${values.map(value => `<li>${esc(value)}</li>`).join('')}</ul>`).join('')}
      ${program.bestWhen ? `<div class="best-when"><strong>Especially relevant when</strong><p>${esc(program.bestWhen)}</p></div>` : ''}
    </article>`;
  }

  function render(area) {
    const photo = photoFor(area);
    if (!photo) throw new Error(`No photograph is configured for ${area.id}.`);
    const index = areas.findIndex(item => item.id === area.id);
    const previous = areas[(index - 1 + areas.length) % areas.length];
    const next = areas[(index + 1) % areas.length];
    document.title = `${area.title} | Animal Pathways`;
    document.querySelector('meta[name="description"]').setAttribute('content', area.short);
    app.innerHTML = `<article class="field-article">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../areas.html">All field guides</a><span aria-hidden="true">/</span><span>${esc(area.title)}</span></nav>
      <header class="article-hero">
        <div class="hero-copy"><div class="eyebrow">Field guide</div><h1>${esc(area.title)}</h1><p class="standfirst">${esc(area.short)}</p></div>
        <figure><img src="${esc(photo.url)}" alt="${esc(photo.alt)}" width="1200" height="675" decoding="async" fetchpriority="high"><figcaption>Photo: <a href="${esc(photo.source)}" target="_blank" rel="noopener">${esc(photo.credit)}</a>${photo.license ? ` · ${photo.licenseUrl ? `<a href="${esc(photo.licenseUrl)}" target="_blank" rel="noopener">${esc(photo.license)}</a>` : esc(photo.license)}` : ''}</figcaption></figure>
      </header>
      <div class="article-body">
        <aside class="article-toc" aria-labelledby="tocTitle"><p id="tocTitle" class="mini-label">In this guide</p><ol>
          <li><a href="#understanding">Understanding the field</a></li><li><a href="#questions-work">Questions and responsibilities</a></li><li><a href="#preparation">Knowledge and working environment</a></li><li><a href="#careers">Careers</a></li><li><a href="#study">College study</a></li><li><a href="#terms">Key terms</a></li><li><a href="#sources">Sources and related fields</a></li>
        </ol></aside>
        <div class="article-content">
          <p class="big-picture">${esc(area.bigPicture)}</p>
          <section id="understanding" class="article-section">
            <div class="section-heading"><p class="section-number">01</p><h2>Understanding the field</h2></div>
            <h3 class="group-heading">What this area focuses on</h3><div class="prose-grid">${focusHtml(area)}</div>
            <h3 class="group-heading">How work within the area varies</h3><ul class="narrative-list">${narrativeItems(area.variations, area)}</ul>
          </section>
          <section id="questions-work" class="article-section">
            <div class="section-heading"><p class="section-number">02</p><h2>Questions and professional work</h2></div>
            <p class="section-intro">These questions show how people in the field turn broad interests into observation, investigation, care, management, or action.</p>
            <div class="questions-list">${questionsHtml(area)}</div>
            <h3 class="group-heading">Common responsibilities</h3><ul class="narrative-list compact">${narrativeItems(area.responsibilities, area)}</ul>
          </section>
          <section id="preparation" class="article-section">
            <div class="section-heading"><p class="section-number">03</p><h2>Knowledge and working environment</h2></div>
            <div class="article-columns"><div><h3 class="group-heading first">Knowledge and skills</h3><ul class="narrative-list compact">${narrativeItems(area.knowledgeSkills, area)}</ul></div><div><h3 class="group-heading first">Work settings</h3><ul class="narrative-list compact">${narrativeItems(area.settings, area)}</ul></div></div>
            <h3 class="group-heading">Practical realities</h3><ul class="reality-list">${narrativeItems(area.realities, area)}</ul>
          </section>
          <section id="careers" class="article-section">
            <div class="section-heading"><p class="section-number">04</p><h2>Careers connected to this field</h2></div>
            <p class="section-intro">Titles, settings, and qualifications vary by employer. These examples show several ways this field can become professional work.</p>
            <div class="career-list">${area.careers.map(careerHtml).join('')}</div><a class="research-link" href="../jobs.html">Browse all job examples →</a>
          </section>
          <section id="study" class="article-section">
            <div class="section-heading"><p class="section-number">05</p><h2>College study and preparation</h2></div>
            <p class="section-intro">A major is one part of preparation. Course selection, research, fieldwork, internships, volunteering, and technical skills can change what a program makes possible.</p>
            <div class="program-list">${area.programs.map(programHtml).join('')}</div><a class="research-link" href="../programs.html">Browse all college program guides →</a>
          </section>
          <section id="terms" class="article-section">
            <div class="section-heading"><p class="section-number">06</p><h2>Key terms</h2></div>
            <dl class="glossary-list">${area.terms.map(item => `<div><dt>${esc(item.term)}</dt><dd>${esc(item.definition)}</dd></div>`).join('')}</dl>
          </section>
          <section id="sources" class="article-section">
            <div class="section-heading"><p class="section-number">07</p><h2>Sources and related fields</h2></div>
            <h3 class="group-heading first">References and further reading</h3><ul class="source-list">${area.references.map(item => `<li><a href="${esc(item.url)}" target="_blank" rel="noopener">${esc(item.title)}</a><span>${esc(item.type)}</span></li>`).join('')}</ul>
            <h3 class="group-heading">Related field guides</h3><div class="related-links">${area.related.map(id => areaById(id)).filter(Boolean).map(item => `<a href="${esc(item.id)}.html">${esc(item.title)} <span aria-hidden="true">→</span></a>`).join('')}</div>
          </section>
        </div>
      </div>
      <nav class="article-pagination" aria-label="Field guide navigation">
        <a href="${esc(previous.id)}.html"><span>Previous field</span><strong>← ${esc(previous.title)}</strong></a><a class="all-guides" href="../areas.html">All field guides</a><a class="next" href="${esc(next.id)}.html"><span>Next field</span><strong>${esc(next.title)} →</strong></a>
      </nav>
    </article>`;
  }
  async function initialize() {
    try {
      const root = '../content/areas/';
      const [manifest, photoManifest] = await Promise.all([
        fetchJson(`${root}index.json`),
        fetchJson(`${root}photos.json`)
      ]);
      photos = photoManifest.photos || photoManifest;
      areas = await Promise.all(manifest.areas.map(file => fetchJson(`${root}${file}`)));
      const area = areaById(currentId);
      if (!area) throw new Error(`No area content found for ${currentId}.`);
      render(area);
    } catch (error) {
      console.error(error);
      app.innerHTML = `<div class="error-page"><h1>This field guide could not be loaded</h1><p>Check the area JSON file, then reload the page.</p><code>${esc(error.message)}</code><p><a href="../areas.html">Return to all field guides</a></p></div>`;
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
