(function () {
  'use strict';

  const D = window.EXPLORER_DATA;
  const app = document.getElementById('app');
  const storageKey = 'animalExplorerAreasV1';
  const areaColors = ['#176d8c', '#087d72', '#6457a6', '#b95622', '#a83c61'];
  const views = ['overview', 'focus', 'variations', 'questions', 'work', 'knowledge', 'settings', 'realities', 'careers', 'study', 'glossary', 'sources'];
  const viewMeta = {
    overview: { label: 'Overview', icon: '🧭', color: '#176d8c', intro: 'The scope of the field and routes into its detailed sections.' },
    focus: { label: 'Main focus', icon: '🔎', color: '#087d72', intro: 'The subjects, processes, and problems at the center of this field.' },
    variations: { label: 'How it varies', icon: '↔', color: '#5969a8', intro: 'Ways the emphasis, methods, species, and daily work can differ.' },
    questions: { label: 'Questions investigated', icon: '?', color: '#6b4ca5', intro: 'Questions that guide scientific, clinical, operational, and management work.' },
    work: { label: 'Responsibilities', icon: '✓', color: '#b95622', intro: 'The activities professionals and students carry out.' },
    knowledge: { label: 'Knowledge & skills', icon: '◆', color: '#176d8c', intro: 'Scientific, technical, analytical, and communication preparation used in the field.' },
    settings: { label: 'Work settings', icon: '⌂', color: '#2c765f', intro: 'Places and organizations where this work occurs.' },
    realities: { label: 'Practical realities', icon: '!', color: '#9a5a20', intro: 'Conditions that can shape schedules, workload, training, and early-career experience.' },
    careers: { label: 'Careers', icon: '▣', color: '#a83c61', intro: 'Example roles connected to the field, including their focus and preparation.' },
    study: { label: 'College study', icon: '🎓', color: '#8b6418', intro: 'Undergraduate paths with different combinations of breadth, specialization, and experience.' },
    glossary: { label: 'Glossary', icon: 'Aa', color: '#367187', intro: 'Concepts and technical language encountered in courses and professional work.' },
    sources: { label: 'Sources & connections', icon: '↗', color: '#536677', intro: 'Professional resources and neighboring fields for further exploration.' }
  };
  const overviewGroups = [
    { label: 'Understand the field', views: ['focus', 'variations', 'questions'] },
    { label: 'Experience the work', views: ['work', 'knowledge', 'settings', 'realities'] },
    { label: 'Explore paths', views: ['careers', 'study'] },
    { label: 'Reference', views: ['glossary', 'sources'] }
  ];
  const kindLabels = {
    topics: 'Focus topic',
    variations: 'How the work varies',
    questions: 'Question people investigate',
    activities: 'Responsibility or activity',
    skills: 'Knowledge or skill',
    settings: 'Work setting',
    realities: 'Practical reality',
    terms: 'Term',
    careers: 'Career example',
    programs: 'Undergraduate path',
    references: 'Source',
    related: 'Related area'
  };

  let areas = [];
  let browseSelection = '';

  const photos = {
    field: {
      url: 'https://www.fws.gov/sites/default/files/2023-03/GMT%20veg%20transect%20072810%20LD.jpg',
      alt: 'A wildlife biologist records measurements along a grassland survey transect.',
      credit: 'Lauren Dennhardt / U.S. Fish & Wildlife Service',
      source: 'https://www.fws.gov/media/sara-conducting-belt-transect-survey-grassland-monitoring-team-photo-credit-lauren'
    },
    health: {
      url: 'https://www.fws.gov/sites/default/files/images/2024-03-3/5847.jpg',
      alt: 'Wildlife researchers conduct a veterinary examination of a Florida panther in the field.',
      credit: 'U.S. Fish & Wildlife Service',
      source: 'https://www.fws.gov/media/florida-panther-research'
    },
    people: {
      url: 'https://media.fisheries.noaa.gov/dam-migration/mteapstaff_birchaquarium-swfsc-mmtd-noaa.jpg',
      alt: 'A marine educator speaks with visitors at an aquarium outreach exhibit.',
      credit: 'NOAA Fisheries',
      source: 'https://www.fisheries.noaa.gov/west-coast/science-data/marine-turtle-outreach'
    }
  };

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
  function photoFor(area) {
    if (['zoology', 'ecology', 'wildlife-ecology-management', 'conservation-biology'].includes(area.id)) return photos.field;
    if (['animal-physiology', 'veterinary-science', 'wildlife-health', 'wildlife-rehabilitation', 'animal-science'].includes(area.id)) return photos.health;
    return photos.people;
  }
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

  function setActiveNav(routeName) {
    document.querySelectorAll('[data-route]').forEach(link => link.classList.toggle('active', link.dataset.route === routeName));
    document.getElementById('primaryNav').classList.remove('open');
    document.getElementById('menuButton').setAttribute('aria-expanded', 'false');
  }

  function route() {
    const hash = (location.hash || '#areas').slice(1);
    const parts = hash.split('/');
    if (hash === 'summary') {
      setActiveNav('summary');
      renderSummary();
    } else if (parts[0] === 'area' && parts[1]) {
      setActiveNav('areas');
      renderArea(parts[1], views.includes(parts[2]) ? parts[2] : 'overview');
    } else {
      setActiveNav('areas');
      renderAreas();
    }
    app.focus({ preventScroll: true });
  }

  function renderAreas(filterText) {
    document.title = 'Animal Fields & Work Explorer';
    app.innerHTML = `<div class="page browse-page">
      <header class="browse-heading">
        <div><div class="eyebrow">${areas.length} fields and work areas</div><h1>Explore animal-related fields</h1><p class="lead">Choose an area to see its scope, central questions, work, preparation, and possible paths.</p></div>
        <div class="search-wrap"><label for="areaSearch">Search all area content</label><input id="areaSearch" class="search" type="search" placeholder="Behavior, health, wildlife…" value="${esc(filterText || '')}"></div>
      </header>
      <div id="areaBrowser"></div>
    </div>`;
    renderAreaBrowser(String(filterText || '').trim().toLowerCase());
    document.getElementById('areaSearch').addEventListener('input', event => renderAreaBrowser(event.target.value.trim().toLowerCase()));
  }

  function renderAreaBrowser(q) {
    const root = document.getElementById('areaBrowser');
    const matches = areas.filter(area => {
      const blob = [area.title, area.short, area.bigPicture, ...area.focus.map(itemText), ...area.knowledgeSkills.map(itemText), ...area.terms.map(item => `${item.term} ${item.definition}`)].join(' ').toLowerCase();
      return !q || blob.includes(q);
    });
    if (!matches.length) {
      root.innerHTML = '<div class="empty">No areas match that search.</div>';
      return;
    }
    if (!matches.some(area => area.id === browseSelection)) browseSelection = matches[0].id;
    const selected = areaById(browseSelection);
    const photo = photoFor(selected);
    root.innerHTML = `<label class="mobile-area-picker"><span>Choose a field</span><select id="browseAreaSelect">${matches.map(area => `<option value="${esc(area.id)}" ${area.id === selected.id ? 'selected' : ''}>${esc(area.title)}</option>`).join('')}</select></label>
    <section class="area-browser" aria-label="Area explorer">
      <div class="area-browser-list" role="listbox" aria-label="Animal-related fields">
        ${matches.map(area => `<button type="button" class="area-choice ${area.id === selected.id ? 'selected' : ''}" data-preview-area="${esc(area.id)}" role="option" aria-selected="${area.id === selected.id}"><span>${esc(area.title)}</span><small>${esc(area.short)}</small></button>`).join('')}
      </div>
      <article class="area-preview" style="--group-color:${colorFor(selected)}">
        <figure class="preview-photo"><img src="${esc(photo.url)}" alt="${esc(photo.alt)}"><figcaption>Photo: <a href="${esc(photo.source)}" target="_blank" rel="noopener">${esc(photo.credit)}</a></figcaption></figure>
        <div class="preview-topline"><span>Field overview</span>${state.savedAreas.includes(selected.id) ? '<span class="saved-label">Saved</span>' : ''}</div>
        <h2>${esc(selected.title)}</h2>
        <p class="preview-intro">${esc(selected.short)}</p>
        <div class="preview-stats"><span><strong>${selected.questions.length}</strong> questions</span><span><strong>${selected.careers.length}</strong> careers</span><span><strong>${selected.programs.length}</strong> college paths</span></div>
        <a class="btn primary" href="#area/${selected.id}/overview">Open ${esc(selected.title)}</a>
      </article>
    </section>`;
  }

  function explorerControls(area, activeView, saved) {
    return `<div class="explorer-controls">
      <a class="back" href="#areas" aria-label="Return to all areas">← All areas</a>
      <label><span>Field</span><select id="fieldSelect">${areas.map(item => `<option value="${esc(item.id)}" ${item.id === area.id ? 'selected' : ''}>${esc(item.title)}</option>`).join('')}</select></label>
      <label><span>Section</span><select id="sectionSelect">${views.map(view => `<option value="${view}" ${view === activeView ? 'selected' : ''}>${esc(viewMeta[view].label)}</option>`).join('')}</select></label>
      <button id="saveArea" class="save-control ${saved ? 'saved' : ''}" type="button">${saved ? '★ Saved' : '☆ Save'}</button>
    </div>`;
  }

  function reactionButtons(key) {
    const selected = reactionFor(key);
    return `<div class="micro-reactions" role="group" aria-label="Optional quick reaction"><span>Mark</span>
      <button class="micro-reaction up ${selected === 'up' ? 'selected' : ''}" type="button" data-reaction-key="${esc(key)}" data-reaction-value="up" aria-label="Mark as interesting" title="Mark as interesting" aria-pressed="${selected === 'up'}"><span aria-hidden="true">👍</span></button>
      <button class="micro-reaction down ${selected === 'down' ? 'selected' : ''}" type="button" data-reaction-key="${esc(key)}" data-reaction-value="down" aria-label="Mark as not appealing right now" title="Mark as not appealing right now" aria-pressed="${selected === 'down'}"><span aria-hidden="true">👎</span></button>
    </div>`;
  }

  function itemText(item) {
    if (typeof item === 'string') return item;
    if (Array.isArray(item)) return item.join(': ');
    return item.title || item.question || item.term || item.name || item.text || item.label || '';
  }

  function itemAt(list, index) {
    return Array.isArray(list) && list.length ? list[index % list.length] : '';
  }

  function referenceFor(area, kind, index, preferredSource) {
    if (!area.references.length) return null;
    const offsets = { topics: 0, questions: 1, activities: 0, skills: 2, settings: 1, realities: 1, variations: 0 };
    if (typeof preferredSource === 'string') {
      const matched = area.references.find(reference => reference.title === preferredSource || reference.url === preferredSource);
      if (matched) return matched;
    }
    const selectedIndex = Number.isInteger(preferredSource) ? preferredSource : (index + (offsets[kind] || 0)) % area.references.length;
    return area.references[selectedIndex % area.references.length];
  }

  function detailFor(area, kind, item, index) {
    const responsibility = itemText(itemAt(area.responsibilities, index));
    const question = itemText(itemAt(area.questions, index));
    const skill = itemText(itemAt(area.knowledgeSkills, index));
    const setting = itemText(itemAt(area.settings, index));
    const variation = itemAt(area.variations, index) || {};
    const career = itemAt(area.careers, index);
    const careerName = typeof career === 'object' ? career.name : career;
    const lower = value => String(value || '').replace(/^[A-Z]/, letter => letter.toLowerCase()).replace(/\.$/, '');
    const customExamples = typeof item === 'object' && Array.isArray(item.examples)
      ? item.examples.map(example => [example.label, example.text])
      : null;
    const details = {
      topics: { explanation: item.description, examples: [['A question it can raise', question], ['How it appears in the work', responsibility], ['Useful preparation', skill]] },
      questions: { explanation: item.approach, examples: [['Related activity', responsibility], ['Evidence or expertise', skill], ['Possible work context', setting]] },
      activities: { explanation: (typeof item === 'object' && item.description) || `This work uses ${lower(skill)} to collect information, provide care, or support a decision. It may contribute to questions such as “${question}”`, examples: [['Knowledge that supports it', skill], ['Where it may happen', setting], ['Related career example', careerName]] },
      skills: { explanation: (typeof item === 'object' && item.description) || `In ${area.title}, this preparation supports work such as ${lower(responsibility)}.`, examples: [['Used for', responsibility], ['Question it can help answer', question], ['Place to develop it', setting]] },
      settings: { explanation: (typeof item === 'object' && item.description) || `In ${area.title}, work here may include ${lower(responsibility)}.`, examples: [['Example activity', responsibility], ['Relevant preparation', skill], ['Related career example', careerName]] },
      realities: { explanation: (typeof item === 'object' && item.description) || `This condition can shape daily routines and the ${lower(variation.label)} of the work.`, examples: [['What that range can look like', variation.description], ['Responsibility affected', responsibility], ['Setting to investigate', setting]] }
    };
    const generated = details[kind];
    return {
      title: itemText(item),
      explanation: generated.explanation,
      examples: (customExamples || generated.examples).filter(example => example[1]),
      reference: referenceFor(area, kind, index, typeof item === 'object' ? item.source : null),
      reactionKey: aspectKey(area.id, kind, index)
    };
  }

  function careerDetail(item) {
    const supplied = typeof item === 'object' ? item : null;
    const career = careerByName(supplied ? supplied.name : item);
    const name = career ? career.name : (supplied ? supplied.name : item);
    const focus = career ? career.roleFocus : (supplied ? supplied.focus : 'Related career example; a full profile has not yet been added to the research database.');
    const education = career ? career.educationBand : (supplied ? supplied.educationBand : 'Preparation varies');
    const tags = career ? career.workTags : (supplied ? supplied.workTags : []);
    const competencies = career ? (career.competencies || []).slice(0, 6) : [];
    return {
      title: name,
      explanation: focus,
      examples: [
        ['Typical education', education],
        ['Work patterns', (tags || []).slice(0, 5).join(' · ')],
        ['Selected competencies', competencies.map(entry => entry.name).join(' · ')]
      ].filter(example => example[1]),
      action: '<a class="btn text" href="index.html#careers">Open the complete career research →</a>'
    };
  }

  function programDetail(program) {
    return {
      title: `${program.code} · ${program.title}`,
      kicker: program.school,
      explanation: program.fundamental || 'Review the program curriculum and experiential opportunities to see how it supports this field.',
      examples: [['School', program.school], ['Experience structure', (program.experienceTags || []).slice(0, 6).join(' · ')]].filter(example => example[1]),
      action: '<a class="btn text" href="index.html#programs">Compare all researched college paths →</a>'
    };
  }

  function detailData(area, kind, item, index) {
    if (['topics', 'questions', 'activities', 'skills', 'settings', 'realities'].includes(kind)) return detailFor(area, kind, item, index);
    if (kind === 'variations') return { title: item.label, explanation: item.description, examples: [], reference: referenceFor(area, kind, index, item.source) };
    if (kind === 'terms') return { title: item.term, explanation: item.definition, examples: [] };
    if (kind === 'careers') return careerDetail(item);
    if (kind === 'programs') return programDetail(item);
    if (kind === 'references') return { title: item.title, kicker: item.type, explanation: 'An external resource used to define the field, its work, preparation, or professional context.', examples: [], action: `<a class="btn primary" href="${esc(item.url)}" target="_blank" rel="noopener">Open source ↗</a>` };
    if (kind === 'related') {
      const related = areaById(item);
      return { title: related.title, explanation: related.short, examples: related.focus.slice(0, 3).map(focus => ['Area of focus', focus.title]), action: `<a class="btn primary" href="#area/${related.id}/overview">Explore ${esc(related.title)}</a>` };
    }
    return { title: itemText(item), explanation: '', examples: [] };
  }

  function menuItemTitle(kind, item) {
    if (kind === 'careers') return typeof item === 'object' ? item.name : item;
    if (kind === 'programs') return `${item.school}: ${item.title}`;
    if (kind === 'references') return item.title;
    if (kind === 'related') return areaById(item).title;
    return itemText(item);
  }

  function browserDetailHtml(area, kind, item, index) {
    const detail = detailData(area, kind, item, index);
    const reference = detail.reference;
    return `<div class="browser-detail-inner">
      <div class="detail-heading"><div><span class="detail-kicker">${esc(detail.kicker || kindLabels[kind])}</span><h3>${esc(detail.title)}</h3></div>${detail.reactionKey ? reactionButtons(detail.reactionKey) : ''}</div>
      ${detail.explanation ? `<p class="detail-explanation">${esc(detail.explanation)}</p>` : ''}
      ${detail.examples && detail.examples.length ? `<div class="example-list">${detail.examples.map(example => `<div class="example-item"><strong>${esc(example[0])}</strong><span>${esc(example[1])}</span></div>`).join('')}</div>` : ''}
      <div class="detail-footer">${reference ? `<a class="source-link" href="${esc(reference.url)}" target="_blank" rel="noopener"><span>${esc(reference.type)}</span>${esc(reference.title)} ↗</a>` : '<span></span>'}${detail.action || ''}</div>
    </div>`;
  }

  function contentBrowser(area, groups) {
    const available = groups.filter(group => group.items.length);
    const flattened = available.flatMap(group => group.items.map((item, index) => ({ kind: group.kind, index, item })));
    const first = flattened[0];
    return `<div class="content-browser" data-content-browser>
      <div class="item-toolbar">
        <label><span>${available.length === 1 ? esc(available[0].label) : 'Choose an item'}</span>
          <select data-item-select>${available.map(group => `<optgroup label="${esc(group.label)}">${group.items.map((item, index) => `<option value="${group.kind}:${index}">${esc(menuItemTitle(group.kind, item))}</option>`).join('')}</optgroup>`).join('')}</select>
        </label>
        <div class="item-stepper"><span data-item-counter>1 of ${flattened.length}</span><button type="button" data-item-step="-1" disabled aria-label="Previous item">←</button><button type="button" data-item-step="1" ${flattened.length < 2 ? 'disabled' : ''} aria-label="Next item">→</button></div>
      </div>
      <article class="browser-detail" aria-live="polite">${browserDetailHtml(area, first.kind, first.item, first.index)}</article>
    </div>`;
  }

  function panelContent(area, activeView) {
    const programs = area.programs.map(program => ({ ...(programByCode(program.code) || {}), ...program }));
    const configurations = {
      focus: [{ kind: 'topics', label: 'Areas of focus', items: area.focus }],
      variations: [{ kind: 'variations', label: 'How the work varies', items: area.variations }],
      questions: [{ kind: 'questions', label: 'Questions people investigate', items: area.questions }],
      work: [{ kind: 'activities', label: 'Responsibilities and activities', items: area.responsibilities }],
      knowledge: [{ kind: 'skills', label: 'Knowledge and skills', items: area.knowledgeSkills }],
      settings: [{ kind: 'settings', label: 'Work settings', items: area.settings }],
      realities: [{ kind: 'realities', label: 'Practical realities', items: area.realities }],
      careers: [{ kind: 'careers', label: 'Career examples', items: area.careers }],
      study: [{ kind: 'programs', label: 'Undergraduate paths', items: programs }],
      glossary: [{ kind: 'terms', label: 'Field glossary', items: area.terms }],
      sources: [{ kind: 'references', label: 'External resources', items: area.references }, { kind: 'related', label: 'Related areas', items: area.related }]
    };
    const meta = viewMeta[activeView];
    if (activeView === 'overview') {
      const photo = photoFor(area);
      return `<section class="view-panel overview-panel" style="--section-color:${meta.color}">
        <header class="view-heading"><span class="view-icon" aria-hidden="true">${meta.icon}</span><div><span class="view-label">${esc(area.title)}</span><h1>${esc(meta.label)}</h1></div></header>
        <div class="overview-feature"><figure><img src="${esc(photo.url)}" alt="${esc(photo.alt)}"><figcaption>Photo: <a href="${esc(photo.source)}" target="_blank" rel="noopener">${esc(photo.credit)}</a></figcaption></figure><div><p class="overview-short">${esc(area.short)}</p><p>${esc(area.bigPicture)}</p><div class="overview-stats"><span><strong>${area.focus.length}</strong> focus areas</span><span><strong>${area.questions.length}</strong> questions</span><span><strong>${area.careers.length}</strong> careers</span></div></div></div>
        <nav class="section-menu" aria-label="Sections in ${esc(area.title)}">${overviewGroups.map(group => `<section><h2>${esc(group.label)}</h2>${group.views.map(view => `<a href="#area/${area.id}/${view}" style="--tile-color:${viewMeta[view].color}"><span class="menu-icon" aria-hidden="true">${viewMeta[view].icon}</span><span>${esc(viewMeta[view].label)}</span></a>`).join('')}</section>`).join('')}</nav>
      </section>`;
    }
    return `<section class="view-panel" style="--section-color:${meta.color}"><header class="view-heading"><span class="view-icon" aria-hidden="true">${meta.icon}</span><div><span class="view-label">${esc(area.title)}</span><h1>${esc(meta.label)}</h1><p>${esc(meta.intro)}</p></div></header>${contentBrowser(area, configurations[activeView])}</section>`;
  }

  function renderArea(id, activeView) {
    const area = areaById(id);
    if (!area) { location.hash = 'areas'; return; }
    document.title = `${area.title} — ${viewMeta[activeView].label}`;
    const saved = state.savedAreas.includes(area.id);
    app.innerHTML = `<div class="page detail-page"><div class="detail-main" style="--group-color:${colorFor(area)}">${explorerControls(area, activeView, saved)}${panelContent(area, activeView)}</div></div>`;

    document.getElementById('saveArea').addEventListener('click', () => {
      const index = state.savedAreas.indexOf(area.id);
      if (index >= 0) state.savedAreas.splice(index, 1); else state.savedAreas.push(area.id);
      saveState();
      renderArea(area.id, activeView);
    });
  }

  const aspectLabels = { topics: 'Focus topic', questions: 'Question', activities: 'Responsibility', skills: 'Knowledge or skill', settings: 'Work setting', realities: 'Practical reality' };

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
    return `<section class="reaction-group ${value}"><h3><span class="reaction-dot"></span>${esc(title)}</h3>${entries.map(entry => `<div class="reaction-entry"><div><a href="#area/${entry.area.id}/overview">${esc(entry.area.title)}</a><small>${esc(aspectLabels[entry.kind])}</small></div><div>${esc(entry.text)}</div></div>`).join('')}</section>`;
  }

  function renderSummary() {
    document.title = 'Saved areas and quick marks';
    const entries = allReactionEntries();
    const up = entries.filter(entry => entry.value === 'up');
    const down = entries.filter(entry => entry.value === 'down');
    const saved = state.savedAreas.map(areaById).filter(Boolean);
    app.innerHTML = `<div class="page narrow"><header class="browse-heading"><div><div class="eyebrow">Saved for later</div><h1>Saved areas and quick marks</h1><p class="lead">Areas and details you chose to keep track of.</p></div></header>
      ${saved.length || entries.length ? `${saved.length ? `<section class="summary-section"><h2>Saved areas</h2><div class="pill-row">${saved.map(area => `<a class="btn small" href="#area/${area.id}/overview">${esc(area.title)}</a>`).join('')}</div></section>` : ''}
        <section class="summary-section"><h2>Quick marks</h2><div class="mark-columns"><div>${renderReactionGroup('up', 'Interesting', up) || '<p class="muted">Nothing marked interesting yet.</p>'}</div><div>${renderReactionGroup('down', 'Not appealing right now', down) || '<p class="muted">Nothing marked unappealing.</p>'}</div></div></section><div class="summary-actions"><a class="btn primary" href="#areas">Continue exploring areas</a></div>` : `<div class="empty"><h2>Nothing saved or marked yet</h2><p>Open an area to explore it. Save an area or use the small thumbs in a detail panel when something stands out.</p><a class="btn primary" href="#areas">Explore areas</a></div>`}
    </div>`;
  }

  function collectionsForArea(area) {
    return {
      topics: area.focus,
      variations: area.variations,
      questions: area.questions,
      activities: area.responsibilities,
      skills: area.knowledgeSkills,
      settings: area.settings,
      realities: area.realities,
      terms: area.terms,
      careers: area.careers,
      programs: area.programs.map(program => ({ ...(programByCode(program.code) || {}), ...program })),
      references: area.references,
      related: area.related
    };
  }

  function updateItemBrowser(browser, area) {
    const select = browser.querySelector('[data-item-select]');
    const [kind, rawIndex] = select.value.split(':');
    const index = Number(rawIndex);
    const items = collectionsForArea(area)[kind];
    browser.querySelector('.browser-detail').innerHTML = browserDetailHtml(area, kind, items[index], index);
    browser.querySelector('[data-item-counter]').textContent = `${select.selectedIndex + 1} of ${select.options.length}`;
    const buttons = browser.querySelectorAll('[data-item-step]');
    buttons[0].disabled = select.selectedIndex === 0;
    buttons[1].disabled = select.selectedIndex === select.options.length - 1;
  }

  app.addEventListener('change', event => {
    if (event.target.id === 'browseAreaSelect') {
      browseSelection = event.target.value;
      const q = document.getElementById('areaSearch') ? document.getElementById('areaSearch').value.trim().toLowerCase() : '';
      renderAreaBrowser(q);
      return;
    }
    if (event.target.id === 'fieldSelect') {
      const parts = (location.hash || '#area').slice(1).split('/');
      location.hash = `area/${event.target.value}/${views.includes(parts[2]) ? parts[2] : 'overview'}`;
      return;
    }
    if (event.target.id === 'sectionSelect') {
      const parts = (location.hash || '').slice(1).split('/');
      location.hash = `area/${parts[1]}/${event.target.value}`;
      return;
    }
    if (event.target.matches('[data-item-select]')) {
      const areaId = (location.hash || '').slice(1).split('/')[1];
      updateItemBrowser(event.target.closest('[data-content-browser]'), areaById(areaId));
    }
  });

  app.addEventListener('click', event => {
    const previewButton = event.target.closest('[data-preview-area]');
    if (previewButton) {
      browseSelection = previewButton.dataset.previewArea;
      const q = document.getElementById('areaSearch') ? document.getElementById('areaSearch').value.trim().toLowerCase() : '';
      renderAreaBrowser(q);
      return;
    }

    const stepButton = event.target.closest('[data-item-step]');
    if (stepButton) {
      const browser = stepButton.closest('[data-content-browser]');
      const select = browser.querySelector('[data-item-select]');
      select.selectedIndex += Number(stepButton.dataset.itemStep);
      const areaId = (location.hash || '').slice(1).split('/')[1];
      updateItemBrowser(browser, areaById(areaId));
      return;
    }

    const reactionButton = event.target.closest('[data-reaction-key]');
    if (!reactionButton) return;
    const key = reactionButton.dataset.reactionKey;
    const value = reactionButton.dataset.reactionValue;
    if (state.reactions[key] === value) delete state.reactions[key]; else state.reactions[key] = value;
    saveState();
    reactionButton.closest('.micro-reactions').querySelectorAll('[data-reaction-key]').forEach(control => {
      const selected = state.reactions[key] === control.dataset.reactionValue;
      control.classList.toggle('selected', selected);
      control.setAttribute('aria-pressed', String(selected));
    });
  });

  document.getElementById('menuButton').addEventListener('click', event => {
    const nav = document.getElementById('primaryNav');
    const open = nav.classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });

  initialize();
})();
