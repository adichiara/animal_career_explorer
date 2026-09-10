(function () {
  'use strict';

  const D = window.EXPLORER_DATA;
  const app = document.getElementById('app');
  const storageKey = 'animalExplorerAreasV1';

  let areas = [];
  const areaColors = ['#176d8c', '#087d72', '#6457a6', '#b95622', '#a83c61'];

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
  }

  function loadState() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      const reactions = {};
      Object.entries(saved.reactions || {}).forEach(([key, value]) => {
        if (value === 'appealing' || value === 'up') reactions[key] = 'up';
        if (value === 'unappealing' || value === 'down') reactions[key] = 'down';
      });
      return { reactions, savedAreas: saved.savedAreas || [] };
    } catch (_) {
      return { reactions: {}, savedAreas: [] };
    }
  }

  let state = loadState();

  function saveState() {
    localStorage.setItem(storageKey, JSON.stringify(state));
  }

  function areaById(id) { return areas.find(area => area.id === id); }
  function colorFor(area) { return area.color || areaColors[Math.max(0, areas.indexOf(area)) % areaColors.length]; }
  function programByCode(code) { return D.programs.find(program => program.code === code); }
  function careerByName(name) { return D.careers.find(career => career.name === name); }
  function aspectKey(areaId, kind, index) { return `${areaId}::${kind}::${index}`; }
  function reactionFor(key) { return state.reactions[key] || ''; }

  async function fetchJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    try {
      return await response.json();
    } catch (error) {
      throw new Error(`${path}: ${error.message}`);
    }
  }

  function validateContent() {
    if (!Array.isArray(areas) || !areas.length) throw new Error('The area manifest does not contain any area files.');
    const areaIds = new Set();
    const requiredLists = ['focus', 'questions', 'responsibilities', 'knowledgeSkills', 'variations', 'settings', 'realities', 'careers', 'programCodes', 'programs', 'related', 'references', 'terms'];
    areas.forEach(area => {
      if (!area.id || !area.title) throw new Error(`Invalid identity in ${area.id || 'an area file'}.`);
      if (areaIds.has(area.id)) throw new Error(`Duplicate area id: ${area.id}.`);
      areaIds.add(area.id);
      requiredLists.forEach(field => {
        if (!Array.isArray(area[field])) throw new Error(`${area.id}: ${field} must be a list.`);
      });
      area.focus.forEach((topic, index) => {
        if (!topic.title || !topic.description) throw new Error(`${area.id}: focus item ${index + 1} needs a title and description.`);
      });
      area.questions.forEach((question, index) => {
        if (!question.question || !question.approach) throw new Error(`${area.id}: question ${index + 1} needs a question and approach.`);
      });
      area.references.forEach((reference, index) => {
        if (!reference.title || !reference.type || !reference.url) throw new Error(`${area.id}: reference ${index + 1} is incomplete.`);
      });
    });
    const programCodes = new Set(D.programs.map(program => program.code));
    areas.forEach(area => {
      area.related.forEach(relatedId => {
        if (!areaIds.has(relatedId)) throw new Error(`${area.id}: related area ${relatedId} does not exist.`);
      });
      area.programCodes.forEach(code => {
        if (!programCodes.has(code)) throw new Error(`${area.id}: program code ${code} does not exist in site/data.js.`);
      });
    });
  }

  async function loadContent() {
    const root = 'content/areas/';
    const manifest = await fetchJson(`${root}index.json`);
    areas = await Promise.all(manifest.areas.map(file => fetchJson(`${root}${file}`)));
    validateContent();
  }

  async function initialize() {
    try {
      await loadContent();
      window.addEventListener('hashchange', route);
      route();
    } catch (error) {
      console.error('Unable to load area content', error);
      app.innerHTML = `<div class="page narrow"><div class="empty content-error"><h1>Area content could not be loaded</h1><p>Check the edited JSON file for a missing comma, quote, or required field, then reload the page.</p><code>${esc(error.message)}</code></div></div>`;
    }
  }

  function setActiveNav(route) {
    document.querySelectorAll('[data-route]').forEach(link => link.classList.toggle('active', link.dataset.route === route));
    document.getElementById('primaryNav').classList.remove('open');
    document.getElementById('menuButton').setAttribute('aria-expanded', 'false');
  }

  function route() {
    const hash = (location.hash || '#areas').slice(1);
    if (hash === 'summary') {
      setActiveNav('summary');
      renderSummary();
    } else if (hash.startsWith('area/')) {
      setActiveNav('areas');
      renderArea(hash.slice(5));
    } else {
      setActiveNav('areas');
      renderAreas();
    }
    app.focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: 'auto' });
  }

  function renderAreas(filterText) {
    const q = String(filterText || '').trim().toLowerCase();
    app.innerHTML = `
      <div class="page">
        <div class="page-heading">
          <div>
            <div class="eyebrow">${areas.length} overlapping fields and work areas</div>
            <h1>Explore the different ways people study, care for, and work with animals</h1>
            <p class="lead">Open an area to learn what it covers, how the work varies, which responsibilities and skills it may involve, and where it can lead.</p>
          </div>
          <div class="search-wrap">
            <label for="areaSearch">Find an area</label>
            <input id="areaSearch" class="search" type="search" placeholder="Try behavior, wildlife, health…" value="${esc(filterText || '')}">
          </div>
        </div>
        <div id="areaGroups"></div>
      </div>`;
    renderAreaList(q);
    document.getElementById('areaSearch').addEventListener('input', event => renderAreaList(event.target.value.trim().toLowerCase()));
  }

  function renderAreaList(q) {
    const root = document.getElementById('areaGroups');
    const matches = areas.filter(area => {
      const blob = [area.title, area.short, area.bigPicture, ...area.focus.map(itemText), ...area.knowledgeSkills.map(itemText), ...area.terms.map(item => `${item.term} ${item.definition}`)].join(' ').toLowerCase();
      return !q || blob.includes(q);
    });
    root.innerHTML = matches.length ? `<section class="group"><div class="area-grid">${matches.map(area => areaCard(area, areas.indexOf(area))).join('')}</div></section>` : '<div class="empty">No areas match that search.</div>';
  }

  function areaCard(area, index) {
    const saved = state.savedAreas.includes(area.id);
    return `<article class="area-card" style="--group-color:${colorFor(area)}">
      <span class="area-number">Area ${String(index + 1).padStart(2, '0')}</span>
      <h3>${esc(area.title)}</h3><p>${esc(area.short)}</p>
      <div class="card-footer"><span class="stat">${saved ? 'Saved area' : `${area.careers.length} career examples`}</span><a class="btn small" href="#area/${area.id}">Explore area</a></div>
    </article>`;
  }

  function areaNavigation(currentId) {
    return `<aside class="area-nav" aria-label="Field navigation">
      <strong>Areas</strong>
      ${areas.map(area => `<a class="${area.id === currentId ? 'current' : ''}" href="#area/${area.id}">${esc(area.title)}</a>`).join('')}
      <a class="summary-link" href="#summary">Saved &amp; marked</a>
    </aside>`;
  }

  function reactionButtons(key) {
    const selected = reactionFor(key);
    return `<div class="micro-reactions" role="group" aria-label="Optional quick reaction"><span>Optional</span>
      <button class="micro-reaction up ${selected === 'up' ? 'selected' : ''}" type="button" data-reaction-key="${esc(key)}" data-reaction-value="up" aria-label="Mark as interesting" title="Mark as interesting" aria-pressed="${selected === 'up'}"><span aria-hidden="true">👍</span></button>
      <button class="micro-reaction down ${selected === 'down' ? 'selected' : ''}" type="button" data-reaction-key="${esc(key)}" data-reaction-value="down" aria-label="Mark as not appealing right now" title="Mark as not appealing right now" aria-pressed="${selected === 'down'}"><span aria-hidden="true">👎</span></button>
    </div>`;
  }

  function itemText(item) {
    if (typeof item === 'string') return item;
    if (Array.isArray(item)) return item.join(': ');
    return item.title || item.question || item.text || item.label || '';
  }

  function referenceFor(area, kind, index, preferredSource) {
    if (!area.references.length) return null;
    const offsets = { topics: 0, questions: 1, activities: 0, skills: 2, settings: 1, realities: 1 };
    if (typeof preferredSource === 'string') {
      const matched = area.references.find(reference => reference.title === preferredSource || reference.url === preferredSource);
      if (matched) return matched;
    }
    const selectedIndex = Number.isInteger(preferredSource) ? preferredSource : (index + (offsets[kind] || 0)) % area.references.length;
    return area.references[selectedIndex % area.references.length];
  }

  function detailFor(area, kind, item, index) {
    const responsibility = itemText(area.responsibilities[index % area.responsibilities.length]);
    const question = itemText(area.questions[index % area.questions.length]);
    const skill = itemText(area.knowledgeSkills[index % area.knowledgeSkills.length]);
    const setting = itemText(area.settings[index % area.settings.length]);
    const variation = area.variations[index % area.variations.length];
    const career = area.careers[index % area.careers.length];
    const careerName = typeof career === 'object' ? career.name : career;
    const lower = value => String(value).replace(/^[A-Z]/, letter => letter.toLowerCase()).replace(/\.$/, '');
    const customExamples = typeof item === 'object' && Array.isArray(item.examples)
      ? item.examples.map(example => [example.label, example.text])
      : null;
    const details = {
      topics: { explanation: item.description, examples: [['A question it can raise', question], ['How it appears in the work', responsibility], ['Useful preparation', skill]] },
      questions: { explanation: `Investigating this question draws on ${lower(skill)}. Evidence may come from experiments, direct observation, care records, field monitoring, or existing datasets.`, examples: [['Related activity', responsibility], ['Evidence or expertise', skill], ['Possible work context', setting]] },
      activities: { explanation: `This work uses ${lower(skill)} to collect information, provide care, or support a decision. It may contribute to questions such as “${question}”`, examples: [['Knowledge that supports it', skill], ['Where it may happen', setting], ['Related career example', careerName]] },
      skills: { explanation: `In ${area.title}, this preparation supports work such as ${lower(responsibility)}.`, examples: [['Used for', responsibility], ['Question it can help answer', question], ['Place to develop it', setting]] },
      settings: { explanation: `In ${area.title}, work here may include ${lower(responsibility)}.`, examples: [['Example activity', responsibility], ['Relevant preparation', skill], ['Related career example', careerName]] },
      realities: { explanation: `This condition can shape daily routines and the ${lower(variation.label)} of the work.`, examples: [['What that range can look like', variation.description], ['Responsibility affected', responsibility], ['Setting to investigate', setting]] }
    };
    const generated = details[kind];
    return {
      explanation: (typeof item === 'object' && (item.description || item.approach)) || generated.explanation,
      examples: customExamples || generated.examples,
      reference: referenceFor(area, kind, index, typeof item === 'object' ? item.source : null)
    };
  }
  function drillCard(area, kind, item, index) {
    const text = itemText(item);
    const key = aspectKey(area.id, kind, index);
    const detail = detailFor(area, kind, item, index);
    const reference = detail.reference;
    return `<details class="drill-card"><summary><span class="drill-number">${String(index + 1).padStart(2, '0')}</span><span class="drill-title">${esc(text)}</span><span class="drill-cue">Details &amp; examples</span></summary>
      <div class="drill-content"><p class="drill-explanation">${esc(detail.explanation)}</p>
        <div class="example-list">${detail.examples.map(example => `<div class="example-item"><strong>${esc(example[0])}</strong><span>${esc(example[1])}</span></div>`).join('')}</div>
        <div class="drill-footer">${reference ? `<a class="source-link" href="${esc(reference.url)}" target="_blank" rel="noopener"><span>${esc(reference.type)}</span>${esc(reference.title)} ↗</a>` : '<span></span>'}${reactionButtons(key)}</div>
      </div></details>`;
  }
  function aspectSection(area, kind, title, intro, items, tag) {
    return `<section class="content-section" id="${kind}"><div class="section-head"><div><h2>${esc(title)}</h2><p>${esc(intro)}</p></div><span class="section-tag">${esc(tag)}</span></div>
      <div class="drill-list">${items.map((item, index) => drillCard(area, kind, item, index)).join('')}</div></section>`;
  }

  function careerCard(item) {
    const supplied = typeof item === 'object' ? item : null;
    const career = careerByName(supplied ? supplied.name : item);
    const name = career ? career.name : (supplied ? supplied.name : item);
    const focus = career ? career.roleFocus : (supplied ? supplied.focus : 'Related career example; a full profile has not yet been added to the research database.');
    const education = career ? career.educationBand : (supplied ? supplied.educationBand : 'Preparation varies');
    const tags = career ? career.workTags : (supplied ? supplied.workTags : []);
    const competencies = career ? (career.competencies || []).slice(0, 6) : [];
    return `<article class="career-card">
      <h3>${esc(name)}</h3>
      <p>${esc(focus)}</p>
      <div class="pill-row"><span class="pill">${esc(education)}</span>${(tags || []).slice(0, 4).map(tag => `<span class="pill">${esc(tag)}</span>`).join('')}</div>
      ${competencies.length ? `<details><summary>Knowledge and skills in the career profile</summary><ul>${competencies.map(item => `<li><strong>${esc(item.name)}:</strong> ${esc(item.description)}</li>`).join('')}</ul></details>` : ''}
    </article>`;
  }

  function renderArea(id) {
    const area = areaById(id);
    if (!area) { location.hash = 'areas'; return; }
    const saved = state.savedAreas.includes(area.id);
    const programs = area.programs.map(program => ({ ...(programByCode(program.code) || {}), ...program }));
    app.innerHTML = `<div class="page">
      <div class="detail-shell">
        ${areaNavigation(area.id)}
        <div class="detail-main" style="--group-color:${colorFor(area)}">
          <a class="back" href="#areas">← All areas</a>
          <section class="detail-hero">
            <div class="eyebrow">Animal field &amp; work area</div>
            <h1>${esc(area.title)}</h1>
            <p class="lead">${esc(area.bigPicture)}</p>
            <div class="hero-actions"><button id="saveArea" class="btn ${saved ? 'saved' : ''}" type="button">${saved ? 'Saved area' : 'Save area'}</button></div>
          </section>
          <nav class="section-jump" aria-label="On this page"><strong>On this page</strong><a href="#topics">Focus</a><a href="#questions">Questions</a><a href="#activities">Work</a><a href="#skills">Skills</a><a href="#settings">Settings</a><a href="#realities">Realities</a><a href="#terms">Terms</a><a href="#careers">Careers</a><a href="#programs">College paths</a><a href="#references">Sources</a></nav>

          ${aspectSection(area, 'topics', 'What this area commonly focuses on', 'Major subjects, processes, and problems studied or managed in this field.', area.focus, 'Topics')}
          ${aspectSection(area, 'questions', 'Questions people investigate', 'Scientific, clinical, operational, and management questions that guide the work.', area.questions, 'Questions')}
          ${aspectSection(area, 'activities', 'Responsibilities and activities', 'How professionals and students carry out the work.', area.responsibilities, 'Work')}

          <section class="content-section" id="variety">
            <div class="section-head"><div><h2>How work within this area varies</h2><p>The same field can produce very different workdays, settings, and relationships with animals.</p></div><span class="section-tag">Range</span></div>
            <div class="variation-grid">${area.variations.map(item => `<div class="info-box variation"><h3>${esc(item.label)}</h3><p>${esc(item.description)}</p></div>`).join('')}</div>
          </section>

          ${aspectSection(area, 'skills', 'Knowledge and skills', 'Scientific, technical, analytical, and communication preparation used in the field.', area.knowledgeSkills, 'Preparation')}
          ${aspectSection(area, 'settings', 'Work settings', 'Places and organizations where this work occurs.', area.settings, 'Environment')}
          ${aspectSection(area, 'realities', 'Practical realities', 'Conditions that can shape training, schedules, workload, and early-career experience.', area.realities, 'Conditions')}

          <section class="content-section" id="terms">
            <div class="section-head"><div><h2>Terms used in this area</h2><p>Concepts and technical language that appear in courses, research, and professional work.</p></div><span class="section-tag">Glossary</span></div>
            <div class="term-grid">${area.terms.map(item => `<article class="term-card"><h3>${esc(item.term)}</h3><p>${esc(item.definition)}</p></article>`).join('')}</div>
          </section>

          <section class="content-section" id="careers">
            <div class="section-head"><div><h2>Related careers</h2><p>Career examples from the research database, with role focus, education level, work type, and selected competencies.</p></div><span class="section-tag">${area.careers.length} examples</span></div>
            <div class="career-grid">${area.careers.map(careerCard).join('')}</div>
            <p><a class="btn text" href="index.html#careers">Browse all 93 researched roles →</a></p>
          </section>

          <section class="content-section" id="programs">
            <div class="section-head"><div><h2>Undergraduate paths to examine</h2><p>Researched programs with different combinations of scientific breadth, specialization, and hands-on experience.</p></div><span class="section-tag">College</span></div>
            <div class="program-grid">${programs.map(program => `<article class="program-card"><span class="school">${esc(program.school)}</span><h3>${esc(program.code)} · ${esc(program.title)}</h3><p>${esc(program.fundamental)}</p><div class="pill-row">${(program.experienceTags || []).slice(0, 5).map(tag => `<span class="pill">${esc(tag)}</span>`).join('')}</div></article>`).join('')}</div>
            <p><a class="btn text" href="index.html#programs">Compare all researched college paths →</a></p>
          </section>

          <section class="content-section" id="related">
            <div class="section-head"><div><h2>Related and overlapping areas</h2><p>Many careers combine more than one field.</p></div><span class="section-tag">Connections</span></div>
            <div class="pill-row">${area.related.map(relatedId => { const related = areaById(relatedId); return `<a class="btn small" href="#area/${related.id}">${esc(related.title)}</a>`; }).join('')}</div>
          </section>

          <section class="content-section" id="references">
            <div class="section-head"><div><h2>Learn more from field and program sources</h2><p>Professional organizations, occupational references, qualification standards, job boards, and official university pages from the project research.</p></div><span class="section-tag">Sources</span></div>
            <div class="reference-grid">${area.references.map(reference => `<article class="reference-card"><span class="source-type">${esc(reference.type)}</span><h3>${esc(reference.title)}</h3><a href="${esc(reference.url)}" target="_blank" rel="noopener">Open source ↗</a></article>`).join('')}</div>
          </section>
        </div>
      </div>
    </div>`;

    document.getElementById('saveArea').addEventListener('click', () => {
      const index = state.savedAreas.indexOf(area.id);
      if (index >= 0) state.savedAreas.splice(index, 1); else state.savedAreas.push(area.id);
      saveState();
      renderArea(area.id);
    });
  }

  const aspectLabels = { topics: 'Topic', questions: 'Question', activities: 'Responsibility', skills: 'Knowledge or skill', settings: 'Work setting', realities: 'Practical reality' };

  function allReactionEntries() {
    const entries = [];
    areas.forEach(area => {
      const collections = { topics: area.focus, questions: area.questions, activities: area.responsibilities, skills: area.knowledgeSkills, settings: area.settings, realities: area.realities };
      Object.entries(collections).forEach(([kind, items]) => {
        items.forEach((item, index) => {
          const key = aspectKey(area.id, kind, index);
          const value = reactionFor(key);
          if (value) entries.push({ area, kind, text: itemText(item), value });
        });
      });
    });
    return entries;
  }

  function renderReactionGroup(value, title, entries) {
    if (!entries.length) return '';
    return `<section class="reaction-group ${value}"><h3><span class="reaction-dot"></span>${esc(title)}</h3>
      ${entries.map(entry => `<div class="reaction-entry"><div><a href="#area/${entry.area.id}">${esc(entry.area.title)}</a><small>${esc(aspectLabels[entry.kind])}</small></div><div>${esc(entry.text)}</div></div>`).join('')}
    </section>`;
  }

  function renderSummary() {
    const entries = allReactionEntries();
    const up = entries.filter(entry => entry.value === 'up');
    const down = entries.filter(entry => entry.value === 'down');
    const saved = state.savedAreas.map(areaById).filter(Boolean);
    app.innerHTML = `<div class="page narrow"><div class="page-heading"><div><div class="eyebrow">Saved for later</div><h1>Saved areas and quick marks</h1><p class="lead">A compact record of the areas and individual details you chose to keep track of.</p></div></div>
      ${saved.length || entries.length ? `${saved.length ? `<section class="summary-section"><h2>Saved areas</h2><p class="muted">Return directly to any field guide.</p><div class="pill-row">${saved.map(area => `<a class="btn small" href="#area/${area.id}">${esc(area.title)}</a>`).join('')}</div></section>` : ''}
        <section class="summary-section"><h2>Quick marks</h2><p class="muted">These are optional reminders, not a fit score or recommendation.</p><div class="mark-columns">
          <div>${renderReactionGroup('up', 'Interesting', up) || '<p class="muted">Nothing marked interesting yet.</p>'}</div><div>${renderReactionGroup('down', 'Not appealing right now', down) || '<p class="muted">Nothing marked unappealing.</p>'}</div>
        </div></section><div class="summary-actions"><a class="btn primary" href="#areas">Continue exploring areas</a></div>
      ` : `<div class="empty"><h2>Nothing saved or marked yet</h2><p>Open an area to read the field guide. Save an area or use the small thumbs inside any expanded item only when something stands out.</p><a class="btn primary" href="#areas">Explore areas</a></div>`}
    </div>`;
  }

  app.addEventListener('click', event => {
    const button = event.target.closest('[data-reaction-key]');
    if (!button) return;
    const key = button.dataset.reactionKey;
    const value = button.dataset.reactionValue;
    if (state.reactions[key] === value) delete state.reactions[key]; else state.reactions[key] = value;
    saveState();
    button.closest('.micro-reactions').querySelectorAll('[data-reaction-key]').forEach(control => {
      const isSelected = state.reactions[key] === control.dataset.reactionValue;
      control.classList.toggle('selected', isSelected);
      control.setAttribute('aria-pressed', String(isSelected));
    });
  });

  document.getElementById('menuButton').addEventListener('click', event => {
    const nav = document.getElementById('primaryNav');
    const open = nav.classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });

  initialize();
})();
