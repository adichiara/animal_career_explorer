(function () {
  'use strict';
  const D = window.EXPLORER_DATA || { programs: [] };
  const app = document.getElementById('articleApp');
  const code = new URLSearchParams(location.search).get('code');
  let programs = [];

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }
  function list(items, className) {
    return `<ul class="${className || 'narrative-list'}">${(items || []).map(item => `<li><p>${esc(item)}</p></li>`).join('')}</ul>`;
  }
  function sourceUrl(value) { return /^https?:\/\//i.test(value) ? value : `https://${value}`; }
  function sourceLabel(value) { return value.replace(/^https?:\/\//i, '').replace(/\/$/, ''); }
  function preparationScore(strength) {
    const value = Math.max(0, Math.min(3, Number(strength) || 0));
    return Math.round((value / 3) * 10);
  }
  function scoreBand(score) { return score <= 3 ? 'low' : score <= 6 ? 'medium' : 'high'; }
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
      console.error('Unable to load additional college programs:', error);
    }
  }
  function render(program) {
    const index = programs.indexOf(program);
    const previous = programs[(index - 1 + programs.length) % programs.length];
    const next = programs[(index + 1) % programs.length];
    document.title = `${program.title} | College Programs`;
    document.querySelector('meta[name="description"]').setAttribute('content', program.fundamental || program.overview);
    app.innerHTML = `<article class="field-article program-article">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="programs.html">All college programs</a><span aria-hidden="true">/</span><span>${esc(program.school)}</span></nav>
      <header class="article-hero text-hero">
        <div class="hero-copy"><div class="eyebrow">College program guide</div><p class="program-school-hero">${esc(program.school)}</p><h1>${esc(program.title)}</h1><p class="standfirst">${esc(program.fundamental)}</p></div>
        <aside class="hero-facts" aria-label="Program facts"><p class="mini-label">Program at a glance</p><dl>
          <div><dt>School</dt><dd>${esc(program.school)}</dd></div><div><dt>Program type</dt><dd>${esc(program.type)}</dd></div><div><dt>Setting</dt><dd>${esc(program.scale)}</dd></div><div><dt>Research set</dt><dd>${program.collection === 'additional' ? 'Additional researched option' : 'Focused comparison'}</dd></div><div><dt>Research verified</dt><dd>${esc(program.lastVerified || 'See sources')}</dd></div>
        </dl></aside>
      </header>
      <div class="article-body">
        <aside class="article-toc" aria-labelledby="tocTitle"><p id="tocTitle" class="mini-label">In this guide</p><ol>
          <li><a href="#overview">Program overview</a></li><li><a href="#academics">Academic foundation</a></li><li><a href="#experience">Experience and research</a></li><li><a href="#progression">Four-year progression</a></li><li><a href="#fit">Strengths and tradeoffs</a></li><li><a href="#skills">Skills and outcomes</a></li><li><a href="#sources">Official sources</a></li>
        </ol></aside>
        <div class="article-content">
          <section id="overview" class="article-section first-section"><div class="section-heading"><p class="section-number">01</p><h2>Program overview</h2></div><p class="big-picture program-overview">${esc(program.overview)}</p></section>
          <section id="academics" class="article-section"><div class="section-heading"><p class="section-number">02</p><h2>Academic foundation</h2></div>
            <div class="article-columns"><div><h3 class="group-heading first">Science foundation</h3>${list(program.scienceFoundation)}</div><div><h3 class="group-heading first">Animal-related content</h3>${list(program.animalContent)}</div></div>
          </section>
          <section id="experience" class="article-section"><div class="section-heading"><p class="section-number">03</p><h2>Experience and research</h2></div>
            <div class="prose-blocks"><article><h3>Hands-on experience</h3><p>${esc(program.experience)}</p></article><article><h3>Research environment</h3><p>${esc(program.research)}</p></article></div>
          </section>
          <section id="progression" class="article-section"><div class="section-heading"><p class="section-number">04</p><h2>One way to build through four years</h2></div>${list(program.progression, 'reality-list')}</section>
          <section id="fit" class="article-section"><div class="section-heading"><p class="section-number">05</p><h2>Strengths, tradeoffs, and fit</h2></div>
            <div class="article-columns"><div><h3 class="group-heading first">Distinctive advantages</h3>${list(program.advantages)}</div><div><h3 class="group-heading first">Important tradeoffs</h3>${list(program.tradeoffs)}</div></div>
            <div class="best-when"><strong>Especially relevant when</strong><p>${esc(program.bestWhen)}</p></div>
          </section>
          <section id="skills" class="article-section"><div class="section-heading"><p class="section-number">06</p><h2>Skills and possible outcomes</h2></div>
            <h3 class="group-heading first">What a student could build</h3><p class="resume-outcome">${esc(program.resume)}</p>
            <h3 class="group-heading">Areas of preparation</h3><p class="section-intro score-intro">Scores summarize the relative strength of preparation documented in this program, not the overall quality of the program.</p><div class="score-legend" aria-label="Preparation score color scale"><span><i class="score-low"></i>0–3 lower</span><span><i class="score-medium"></i>4–6 moderate</span><span><i class="score-high"></i>7–10 stronger</span></div><div class="competency-grid">${(program.competencies || []).map(item => { const score = preparationScore(item.strength); return `<article><span class="strength-mark score-${scoreBand(score)}" aria-label="${score} out of 10">${score}</span><div><h3>${esc(item.name)}</h3><p>${esc(item.description)}</p><span>${esc(item.category)}</span></div></article>`; }).join('')}</div>
          </section>
          <section id="sources" class="article-section"><div class="section-heading"><p class="section-number">07</p><h2>Official sources</h2></div><p class="section-intro">Use these institutional pages to confirm current curriculum, faculty, concentrations, and requirements.</p>
            <ul class="source-list">${(program.sources || []).map(source => `<li><a href="${esc(sourceUrl(source))}" target="_blank" rel="noopener">${esc(sourceLabel(source))}</a><span>Official program or university page</span></li>`).join('')}</ul>
          </section>
        </div>
      </div>
      <nav class="article-pagination" aria-label="College program navigation"><a href="program.html?code=${encodeURIComponent(previous.code)}"><span>Previous program</span><strong>← ${esc(previous.title)}</strong></a><a class="all-guides" href="programs.html">All college programs</a><a class="next" href="program.html?code=${encodeURIComponent(next.code)}"><span>Next program</span><strong>${esc(next.title)} →</strong></a></nav>
    </article>`;
  }
  function fail(message) { app.innerHTML = `<div class="error-page"><h1>This college program could not be loaded</h1><p>${esc(message)}</p><p><a href="programs.html">Return to all college programs</a></p></div>`; }
  const menuButton = document.getElementById('menuButton');
  const nav = document.getElementById('primaryNav');
  menuButton.addEventListener('click', () => { const open = nav.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); });
  nav.addEventListener('click', () => { nav.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); });
  loadPrograms().then(() => {
    const program = programs.find(item => item.code === code);
    if (program) render(program); else fail(code ? `No program was found for ${code}.` : 'Choose a program from the college program index.');
  });
})();
