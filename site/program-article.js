(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { programs: [] };
  const app = document.getElementById('articleApp');
  const code = new URLSearchParams(location.search).get('code');
  let programs = [];
  let libraryPrograms = [];
  let programPhotos = {};
  let schoolProfiles = { programSchools: {}, schools: {}, programOverrides: {} };
  let fields = [];

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
  function list(items, className) {
    return `<ul class="${className || 'narrative-list'}">${(items || []).map(item => `<li><p>${esc(item)}</p></li>`).join('')}</ul>`;
  }
  function sourceUrl(value) { return /^https?:\/\//i.test(value) ? value : `https://${value}`; }
  function sourceLabel(value) { return value.replace(/^https?:\/\//i, '').replace(/\/$/, ''); }
  function preparationSummary(program) {
    const competencies = (program.competencies || []).filter(item => item && item.name && item.description);
    const strong = competencies.filter(item => Number(item.strength) >= 2.4);
    if (!strong.length) return '<p>No specific undergraduate preparation strengths are documented for this program.</p>';
    return `<div class="preparation-summary"><h3 class="group-heading first">Skills developed</h3><ul class="narrative-list compact">${strong.map(item => `<li><p><strong>${esc(item.name)}:</strong> ${esc(item.description)}</p></li>`).join('')}</ul></div>`;
  }
  async function fetchJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }
  async function loadPrograms() {
    const focused = (D.programs || []).map(program => ({ ...program, collection: program.collection || 'focused' }));
    let additions = [];
    let library = { programs: [] };
    let photoManifest = { photos: {} };
    try {
      [additions, library, photoManifest] = await Promise.all([
        fetchJson('content/programs/additional-programs.json'),
        fetchJson('content/programs/school-library.json'),
        fetchJson('content/programs/photos.json')
      ]);
    } catch (error) {
      console.error('Unable to load one or more college-program support files:', error);
    }
    if (!Array.isArray(additions)) additions = [];
    if (!library || !Array.isArray(library.programs)) library = { programs: [] };
    programPhotos = photoManifest && photoManifest.photos ? photoManifest.photos : {};
    // Keep school context separate from program research and shared across degrees.
    schoolProfiles = await fetchJson('content/programs/schools.json');
    try {
      const manifest = await fetchJson('content/areas/index.json');
      fields = await Promise.all(manifest.areas.map(file => fetchJson(`content/areas/${file}`)));
    } catch (error) {
      console.error('Unable to load field guides:', error);
    }

    const detailMap = new Map();
    [...focused, ...additions].forEach(program => {
      if (program && program.code && !detailMap.has(program.code)) detailMap.set(program.code, program);
    });
    const libraryMap = new Map(library.programs.map(item => [item.code, item]));
    programs = [...detailMap.values()].map(program => {
      const libraryInfo = libraryMap.get(program.code);
      return { ...program, ...(libraryInfo || {}), libraryCurrent: Boolean(libraryInfo) };
    });
    libraryPrograms = library.programs.map(item => {
      const detail = detailMap.get(item.code);
      return detail ? { ...detail, ...item, libraryCurrent: true } : null;
    }).filter(Boolean);
  }
  function schoolOverview(program) {
    const school = schoolProfiles.schools[schoolProfiles.programSchools[program.code]];
    if (!school) throw new Error(`Missing school overview for ${program.code}`);
    const override = schoolProfiles.programOverrides?.[program.code] || {};
    const facts = { ...school.facts, ...override.facts };
    const campuses = override.campuses || school.campuses;
    const topics = [
      ['type', 'School type'], ['size', 'Student population'], ['campus', 'Location and campus'],
      ['housing', 'Housing and dining'], ['studentLife', 'Student life'], ['recreation', 'Athletics and recreation']
    ];
    const usedSources = [...new Set(topics.flatMap(([key]) => facts[key].sources))];
    const references = keys => keys.map(key => `<sup><a href="#school-source-${esc(key)}" aria-label="Source: ${esc(school.sources[key].label)}">[${usedSources.indexOf(key) + 1}]</a></sup>`).join(' ');
    const photos = override.photos || school.photos;
    return `<section id="school" class="article-section school-overview"><div class="section-heading"><p class="section-number">02</p><h2>School overview</h2></div>
      <p class="school-overview-name">${esc(school.name)}</p>
      <p class="school-overview-campus">${campuses.map(esc).join(" · ")}</p>
      ${photos.map(photo => `<figure class="school-photo"><img src="${esc(photo.url)}" alt="${esc(photo.alt)}" loading="lazy" decoding="async" width="1200" height="750" referrerpolicy="no-referrer"><figcaption>${esc(photo.caption)}. Photo: <a href="${esc(photo.source)}" target="_blank" rel="noopener">${esc(photo.credit)}</a></figcaption></figure>`).join('')}
      <dl class="school-facts">${topics.map(([key, label]) => `<div><dt>${label}</dt><dd>${esc(facts[key].text)} ${references(facts[key].sources)}</dd></div>`).join('')}</dl>
      <div class="school-sources"><h3>School information sources</h3><ol>${usedSources.map(key => `<li id="school-source-${esc(key)}"><a href="${esc(school.sources[key].url)}" target="_blank" rel="noopener">${esc(school.sources[key].label)}</a></li>`).join('')}</ol></div>
    </section>`;
  }
  function render(program) {
    const schoolName = displaySchool(program);
    const currentIndex = libraryPrograms.findIndex(item => item.code === program.code);
    const navSet = currentIndex >= 0 ? libraryPrograms : programs;
    const index = navSet.findIndex(item => item.code === program.code);
    const previous = navSet[(index - 1 + navSet.length) % navSet.length];
    const next = navSet[(index + 1) % navSet.length];
    const tags = (program.tags || []).length
      ? `<div class="program-tag-list" aria-label="Program topics">${program.tags.map(tag => `<span>${esc(tag)}</span>`).join('')}</div>`
      : '';
    const relatedFields = (program.primaryFields || []).map(id => fields.find(field => field.id === id)).filter(Boolean);
    const connections = relatedFields.length ? `<h3 class="group-heading">Explore the connected fields and careers</h3><div class="related-links">${relatedFields.map(field => `<a href="areas/${esc(field.id)}.html">${esc(field.title)} <span aria-hidden="true">→</span></a>`).join('')}</div><p>Each field guide explains the work, preparation, and related careers.</p>` : '<p>Browse the <a href="areas.html">field guides</a> for career and study context.</p>';
    const photo = programPhotos[program.code];
    const photoHtml = photo ? `<figure><img src="${esc(photo.url)}" alt="${esc(photo.alt || '')}" width="1200" height="675" decoding="async" fetchpriority="high" referrerpolicy="no-referrer"><figcaption>Photo: <a href="${esc(photo.source)}" target="_blank" rel="noopener">${esc(photo.credit || schoolName)}</a></figcaption></figure>` : '';
    document.title = `${program.title} | Animal Education Pathways`;
    document.querySelector('meta[name="description"]').setAttribute('content', program.fundamental || program.overview);
    app.innerHTML = `<article class="field-article program-article">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="programs.html">School &amp; Program Library</a><span aria-hidden="true">/</span><span>${esc(schoolName)}</span></nav>
      <header class="article-hero program-photo-hero">
        <div class="program-hero-copy-wrap">
          <div class="hero-copy"><div class="eyebrow">College program guide</div><p class="program-school-hero">${esc(schoolName)}</p><h1>${esc(program.title)}</h1><p class="standfirst">${esc(program.fundamental)}</p></div>
          <aside class="hero-facts" aria-label="Program facts"><p class="mini-label">Program at a glance</p><dl>
            <div><dt>School</dt><dd>${esc(schoolName)}</dd></div>
            <div><dt>Program type</dt><dd>${esc(program.type)}</dd></div>
            <div><dt>Setting</dt><dd>${esc(program.scale)}</dd></div>
            <div><dt>Research verified</dt><dd>${esc(program.lastVerified || 'See sources')}</dd></div>
          </dl></aside>
        </div>
        ${photoHtml}
      </header>
      <div class="article-body">
        <aside class="article-toc" aria-labelledby="tocTitle"><p id="tocTitle" class="mini-label">In this guide</p><ol>
          <li><a href="#overview">Program overview</a></li><li><a href="#school">School overview</a></li><li><a href="#academics">Academic foundation</a></li><li><a href="#experience">Experience and research</a></li><li><a href="#progression">Program progression</a></li><li><a href="#fit">Strengths and tradeoffs</a></li><li><a href="#skills">Skills and preparation</a></li><li><a href="#sources">Official sources</a></li>
        </ol></aside>
        <div class="article-content">
          <section id="overview" class="article-section first-section"><div class="section-heading"><p class="section-number">01</p><h2>Program overview</h2></div><p class="big-picture program-overview">${esc(program.overview)}</p>${tags}${connections}<p><a class="research-link" href="compare.html#${encodeURIComponent(program.code)}">Compare this program with the library →</a></p></section>
          ${schoolOverview(program)}
          <section id="academics" class="article-section"><div class="section-heading"><p class="section-number">03</p><h2>Academic foundation</h2></div>
            <div class="article-columns"><div><h3 class="group-heading first">Science foundation</h3>${list(program.scienceFoundation)}</div><div><h3 class="group-heading first">Animal-related content</h3>${list(program.animalContent)}</div></div>
          </section>
          <section id="experience" class="article-section"><div class="section-heading"><p class="section-number">04</p><h2>Experience and research</h2></div>
            <div class="prose-blocks"><article><h3>Hands-on experience</h3><p>${esc(program.experience)}</p></article><article><h3>Research environment</h3><p>${esc(program.research)}</p></article></div>
          </section>
          <section id="progression" class="article-section"><div class="section-heading"><p class="section-number">05</p><h2>One way to progress through the program</h2></div>${list(program.progression, 'reality-list')}</section>
          <section id="fit" class="article-section"><div class="section-heading"><p class="section-number">06</p><h2>Strengths and tradeoffs</h2></div>
            <div class="article-columns"><div><h3 class="group-heading first">Distinctive advantages</h3>${list(program.advantages)}</div><div><h3 class="group-heading first">Important tradeoffs</h3>${list(program.tradeoffs)}</div></div>
            ${program.bestWhen ? `<div class="best-when"><strong>Program emphasis</strong><p>${esc(program.bestWhen)}</p></div>` : ''}
          </section>
          <section id="skills" class="article-section"><div class="section-heading"><p class="section-number">07</p><h2>Skills and preparation</h2></div>
            <h3 class="group-heading first">What a student could build</h3><p class="resume-outcome">${esc(program.resume)}</p>
            ${preparationSummary(program)}
          </section>
          <section id="sources" class="article-section"><div class="section-heading"><p class="section-number">08</p><h2>Official sources</h2></div><p class="section-intro">Use these institutional pages to confirm current curriculum, faculty, concentrations, accreditation where relevant, and requirements.</p>
            <ul class="source-list">${(program.sources || []).map(source => `<li><a href="${esc(sourceUrl(source))}" target="_blank" rel="noopener">${esc(sourceLabel(source))}</a><span>Official program or university page</span></li>`).join('')}</ul>
          </section>
        </div>
      </div>
      <nav class="article-pagination" aria-label="College program navigation"><a href="program.html?code=${encodeURIComponent(previous.code)}"><span>Previous program</span><strong>← ${esc(previous.title)}</strong></a><a class="all-guides" href="programs.html">School &amp; Program Library</a><a class="next" href="program.html?code=${encodeURIComponent(next.code)}"><span>Next program</span><strong>${esc(next.title)} →</strong></a></nav>
    </article>`;
  }
  function fail(message) { app.innerHTML = `<div class="error-page"><h1>This college program could not be loaded</h1><p>${esc(message)}</p><p><a href="programs.html">Return to the school and program library</a></p></div>`; }
  const menuButton = document.getElementById('menuButton');
  const nav = document.getElementById('primaryNav');
  menuButton.addEventListener('click', () => { const open = nav.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); });
  nav.addEventListener('click', () => { nav.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); });
  loadPrograms().then(() => {
    const program = libraryPrograms.find(item => item.code === code);
    if (program) {
      render(program);
      if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
    } else fail(code ? 'That program is not in the School & Program Library.' : 'Choose a program from the school and program library.');
  }).catch(error => { console.error(error); fail('Program information is temporarily unavailable. Please try again.'); });
})();
