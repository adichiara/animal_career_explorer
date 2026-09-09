(function () {
  'use strict';

  const D = window.EXPLORER_DATA;
  const root = document.getElementById('experience');
  const storageKey = 'animalExplorerDiscoveryV1';

  const worlds = [
    {
      id: 'care', icon: '♡', title: 'Care for animals day to day',
      description: 'Feeding, husbandry, enrichment, health observation, and habitat upkeep.',
      careers: [
        'Ambassador animal specialist / animal programs keeper',
        'Aquarist / aquarium animal-care specialist',
        'Sanctuary animal caregiver',
        'Wildlife rehabilitator',
        'Conservation-breeding technician',
        'Service-dog / assistance-animal trainer'
      ]
    },
    {
      id: 'behavior', icon: '◎', title: 'Understand behavior and welfare',
      description: 'Observe learning and behavior, improve wellbeing, and solve behavior problems.',
      careers: [
        'Behavioral husbandry specialist',
        'Animal welfare / behavior coordinator',
        'Animal behavior research assistant / technician',
        'Shelter behavior specialist / coordinator',
        'Science-based animal trainer',
        'Comparative cognition researcher'
      ]
    },
    {
      id: 'wildlife', icon: '⌖', title: 'Study wildlife outdoors',
      description: 'Survey animals, collect field data, track movement, and monitor populations.',
      careers: [
        'Wildlife technician / biological science technician',
        'Field ecologist',
        'Wildlife biologist',
        'Reintroduction / release field technician',
        'Post-release monitoring biologist',
        'Behavioral ecologist'
      ]
    },
    {
      id: 'protect', icon: '△', title: 'Protect species and habitats',
      description: 'Restore habitat, plan conservation, support recovery, and manage wildlife.',
      careers: [
        'Species recovery biologist',
        'Conservation biologist',
        'Habitat restoration / ecological-monitoring specialist',
        'Habitat / wildlife management biologist',
        'Conservation delivery / habitat program coordinator',
        'Endangered-species biologist'
      ]
    },
    {
      id: 'research', icon: '◇', title: 'Investigate biological questions',
      description: 'Design studies, run experiments, analyze evidence, and build knowledge.',
      careers: [
        'Animal behavior research assistant / technician',
        'University / laboratory research assistant',
        'Comparative cognition researcher',
        'Animal learning researcher',
        'Evolutionary biologist studying animals',
        'Neuroethologist / neural-behavior researcher'
      ]
    },
    {
      id: 'data', icon: '▦', title: 'Use data to guide decisions',
      description: 'Map, model, measure, and translate evidence for agencies or organizations.',
      careers: [
        'GIS / wildlife spatial analyst',
        'Quantitative ecology research assistant',
        'Ecological data scientist',
        'eDNA / molecular ecology technician',
        'Ecological research technician',
        'Research statistician — ecology/biology'
      ]
    },
    {
      id: 'communicate', icon: '◌', title: 'Teach and communicate science',
      description: 'Interpret, educate, write, present, and help people connect with science.',
      careers: [
        'Wildlife / environmental educator',
        'Naturalist / interpretive educator',
        'Science writer / communicator — biology and animals',
        'Conservation outreach / program coordinator',
        'Museum / natural-history education or collections work',
        'Ambassador animal specialist / animal programs keeper'
      ]
    }
  ];

  const taskByTag = {
    'Animal care': 'Provide routine care, notice changes in health or behavior, and keep clear records.',
    'Behavior / training': 'Observe behavior and use learning, training, or enrichment methods to improve outcomes.',
    'Fieldwork': 'Collect reliable observations or samples outdoors using repeatable field methods.',
    'Conservation': 'Connect day-to-day work to species, population, habitat, or recovery goals.',
    'Data / statistics': 'Organize and analyze evidence so a team can understand patterns and make decisions.',
    'GIS / spatial': 'Work with mapped locations, habitat information, or animal movement data.',
    'Research': 'Help frame questions, follow study protocols, document results, and communicate findings.',
    'Education / public': 'Explain science clearly to visitors, students, partners, or the public.'
  };

  const steps = {
    start: { label: 'Start anywhere', number: '1 of 4', width: '25%' },
    worlds: { label: 'Notice what draws you in', number: '1 of 4', width: '25%' },
    roles: { label: 'Sample the work', number: '2 of 4', width: '50%' },
    role: { label: 'React to a real role', number: '3 of 4', width: '75%' },
    shortlist: { label: 'Look for patterns', number: '4 of 4', width: '100%' }
  };

  let state = loadState();
  let currentScreen = 'start';
  let searchText = '';
  let currentRoleId = '';
  let roleLimit = 12;

  function blankState() {
    return { selectedWorlds: [], reactions: {}, viewed: [] };
  }

  function loadState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return { ...blankState(), ...parsed };
    } catch (_) {
      return blankState();
    }
  }

  function saveState() {
    localStorage.setItem(storageKey, JSON.stringify(state));
    updateHeader();
  }

  function esc(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[char]);
  }

  function careerByName(name) { return D.careers.find(career => career.name === name); }
  function careerById(id) { return D.careers.find(career => career.id === id); }

  function updateHeader() {
    const count = shortlistedCareers().length;
    document.getElementById('navShortlistCount').textContent = count;
    document.querySelectorAll('.discovery-nav-link').forEach(link => {
      const target = link.dataset.screenLink;
      link.classList.toggle('active', target === currentScreen || (target === 'start' && ['worlds', 'roles', 'role'].includes(currentScreen)));
    });
  }

  function updateJourney(screen) {
    const step = steps[screen];
    document.getElementById('journeyLabel').textContent = step.label;
    document.getElementById('journeyStep').textContent = step.number;
    document.getElementById('journeyProgress').style.width = step.width;
  }

  function showScreen(screen, options = {}) {
    currentScreen = screen;
    updateJourney(screen);
    updateHeader();
    if (screen === 'start') renderStart();
    if (screen === 'worlds') renderWorlds();
    if (screen === 'roles') renderRoles();
    if (screen === 'role') renderRole();
    if (screen === 'shortlist') renderShortlist(options);
    document.getElementById('discoveryNav').classList.remove('open');
    document.getElementById('mobileMenuButton').setAttribute('aria-expanded', 'false');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    root.focus({ preventScroll: true });
  }

  function renderStart() {
    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Explore without committing</div>
        <h1>What kind of animal work might be worth exploring?</h1>
        <p class="lead">You do not need to know your future career. Choose the easiest starting point; you can change direction at any time.</p>

        <div class="choice-grid">
          <button class="choice-card" type="button" data-start="worlds">
            <span class="choice-icon">✦</span>
            <strong>Start with what sounds interesting</strong>
            <span>Choose concrete activities such as caring, observing, researching, protecting, or teaching.</span>
          </button>
          <button class="choice-card" type="button" data-start="worlds">
            <span class="choice-icon">⌁</span>
            <strong>Browse types of animal work</strong>
            <span>See a small set of career worlds before looking at individual job titles.</span>
          </button>
          <button class="choice-card" type="button" data-start="search">
            <span class="choice-icon">⌕</span>
            <strong>I already have something in mind</strong>
            <span>Search for a familiar role and use it as a doorway to related possibilities.</span>
          </button>
        </div>

        <p class="reassurance">This is exploration, not a test. “Maybe,” “not for me,” and “I need to learn more” are all useful answers.</p>
        ${shortlistedCareers().length ? `<div class="button-row"><button class="btn soft" type="button" data-go="shortlist">Continue with my ${shortlistedCareers().length}-role shortlist</button></div>` : ''}
      </section>`;
  }

  function renderWorlds() {
    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Career worlds</div>
        <h1>Which kinds of work deserve a closer look?</h1>
        <p class="lead">Choose one or more based on the work itself—not whether you recognize a job title.</p>

        <div class="world-grid" style="margin-top:28px">
          ${worlds.map(world => `
            <button class="world-card" type="button" data-world="${world.id}" aria-pressed="${state.selectedWorlds.includes(world.id)}">
              <span class="world-icon">${world.icon}</span>
              <strong>${esc(world.title)}</strong>
              <span>${esc(world.description)}</span>
              <span class="world-count">Sample ${world.careers.length} different roles</span>
            </button>`).join('')}
        </div>

        <div class="button-row">
          <button class="btn" type="button" data-go="start">Back</button>
          <button class="btn primary" id="seeRolesButton" type="button" ${state.selectedWorlds.length ? '' : 'disabled'}>See roles from my choices</button>
          <button class="btn text" type="button" data-browse-all>Browse all 93 careers instead</button>
        </div>
      </section>`;
  }

  function rolePool() {
    if (!state.selectedWorlds.length) return D.careers.filter(c => c.roleKind !== 'education_pathway');
    const names = [];
    state.selectedWorlds.forEach(id => {
      const world = worlds.find(item => item.id === id);
      (world?.careers || []).forEach(name => { if (!names.includes(name)) names.push(name); });
    });
    return names.map(careerByName).filter(Boolean);
  }

  function matchesSearch(career, query) {
    if (!query) return true;
    const text = [career.name, career.roleFocus, career.category, career.roleFamily?.name, ...(career.workTags || []), ...(career.aliases || [])].join(' ').toLowerCase();
    return text.includes(query.toLowerCase());
  }

  function renderRoles() {
    const selectedLabels = state.selectedWorlds.map(id => worlds.find(world => world.id === id)?.title).filter(Boolean);
    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Representative roles</div>
        <h1>Sample the work, not just the title.</h1>
        <p class="lead">Open a role to see its purpose, typical duties, setting, degree reality, and what might be easy to overlook.</p>

        <div class="search-wrap">
          <label class="sr-only" for="roleSearch">Search careers</label>
          <input id="roleSearch" class="search-input" type="search" value="${esc(searchText)}" placeholder="Search a role, activity, or setting">
        </div>
        ${selectedLabels.length ? `<div class="pill-row">${selectedLabels.map(label => `<span class="pill green">${esc(label)}</span>`).join('')}</div>` : '<p class="muted small">Showing the complete career library. Search to narrow it.</p>'}
        <div id="roleResults"></div>

        <div class="button-row">
          <button class="btn" type="button" data-go="worlds">Change career worlds</button>
          ${shortlistedCareers().length ? `<button class="btn soft" type="button" data-go="shortlist">See my shortlist (${shortlistedCareers().length})</button>` : ''}
        </div>
      </section>`;
    updateRoleResults();
    document.getElementById('roleSearch').addEventListener('input', event => {
      searchText = event.target.value;
      updateRoleResults();
    });
  }

  function updateRoleResults() {
    const container = document.getElementById('roleResults');
    if (!container) return;
    const pool = rolePool().filter(career => matchesSearch(career, searchText));
    const visible = searchText ? pool : pool.slice(0, roleLimit);
    container.innerHTML = `
      <div class="results-bar"><span>Showing ${visible.length} of ${pool.length} role${pool.length === 1 ? '' : 's'}</span><span>${shortlistedCareers().length} on your shortlist</span></div>
      <div class="role-grid">
        ${visible.length ? visible.map(roleCard).join('') : '<div class="empty-state">No roles match that search. Try a broader activity or job word.</div>'}
      </div>
      ${visible.length < pool.length ? '<div class="button-row"><button class="btn soft" type="button" data-show-more>Show more roles</button></div>' : ''}`;
  }

  function roleCard(career) {
    const reaction = state.reactions[career.id];
    return `
      <button class="role-card" type="button" data-role="${esc(career.id)}">
        <span class="role-family">${esc(career.roleFamily?.name || career.category)}</span>
        <strong>${esc(career.name)}</strong>
        <span class="role-purpose">${esc(career.roleFocus || 'Explore the purpose, work, and preparation for this role.')}</span>
        <span class="pill-row">
          <span class="pill green">${esc(contactLabel(career.directContact))}</span>
          <span class="pill blue">${esc(degreeShort(career.educationBand))}</span>
        </span>
        ${reaction ? `<span class="reaction-summary">Your reaction: ${esc(reaction)}</span>` : ''}
      </button>`;
  }

  function contactLabel(value) {
    if ((value || '').startsWith('High')) return 'High animal contact';
    if ((value || '').startsWith('Moderate')) return 'Some animal contact';
    return 'Limited or variable contact';
  }

  function degreeShort(value) {
    const text = value || '';
    if (text.includes('Graduate study pathway')) return 'Graduate-school pathway';
    if (text.includes('Graduate degree typical')) return 'Graduate degree typical';
    if (text.includes('graduate study often useful')) return 'Graduate study often useful';
    if (text.includes('later career') || text.includes('substantial')) return 'Usually a later-career role';
    if (text.includes('advanced certification')) return 'Experience + certification';
    return 'Bachelor’s-accessible';
  }

  function roleTasks(career) {
    const tasks = (career.workTags || []).map(tag => taskByTag[tag]).filter(Boolean);
    const fallback = [
      'Work with a team to plan, document, and carry out role-specific responsibilities.',
      'Use scientific information and professional judgment to solve practical problems.',
      'Keep learning through supervised experience, feedback, and changing evidence.'
    ];
    return [...new Set([...tasks, ...fallback])].slice(0, 3);
  }

  function surpriseText(career) {
    const band = career.educationBand || '';
    if (band.includes('Graduate degree typical')) return 'The interesting title is usually not the first job. Undergraduate research, methods courses, and early technician work often come before graduate specialization.';
    if (band.includes('later career') || band.includes('substantial') || band.includes('progressive')) return 'This is generally a destination role rather than an entry job. Early positions build the experience needed to reach it.';
    if ((career.directContact || '').startsWith('High')) return 'High animal contact does not mean the whole day is hands-on. Cleaning, preparation, safety, documentation, and teamwork can take substantial time.';
    if ((career.directContact || '').startsWith('Low')) return 'Working for animals does not always mean working directly with them. Data, habitats, research protocols, writing, or people may occupy most of the day.';
    return 'The same title can look quite different across employers. Setting and day-to-day duties matter more than the title alone.';
  }

  function earlyTest(career) {
    const tags = career.workTags || [];
    if (tags.includes('Animal care')) return 'Try structured animal-care work that includes cleaning, observation, recordkeeping, and feedback—not only casual animal contact.';
    if (tags.includes('Fieldwork')) return 'Try a field survey, habitat-monitoring project, or outdoor volunteer role with real data collection.';
    if (tags.includes('Data / statistics')) return 'Try organizing and analyzing a small biology or ecology dataset, then explain what the evidence does and does not show.';
    if (tags.includes('Education / public')) return 'Try explaining an animal or conservation topic to a real audience through teaching, interpretation, or writing.';
    return 'Look for a supervised experience that exposes the routine parts of the work, not only its most exciting moments.';
  }

  function renderRole() {
    const career = careerById(currentRoleId) || rolePool()[0];
    if (!career) return showScreen('roles');
    currentRoleId = career.id;
    if (!state.viewed.includes(career.id)) {
      state.viewed.push(career.id);
      saveState();
    }
    const reaction = state.reactions[career.id] || '';
    const details = career.details || {};
    const tasks = roleTasks(career);
    const competencies = (career.competencies || []).slice(0, 6);
    const observed = (career.observedTitles || []).slice(0, 6);

    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">${esc(career.roleFamily?.name || career.category)}</div>
        <h1>${esc(career.name)}</h1>
        <p class="lead">${esc(career.roleFocus || '')}</p>

        <div class="role-layout">
          <article class="card role-main">
            <h2>What the work may include</h2>
            <div class="task-list">
              ${tasks.map((task, index) => `<div class="task-item"><span class="task-number">${index + 1}</span><span>${esc(task)}</span></div>`).join('')}
            </div>

            <div class="surprise"><strong>What might surprise you</strong>${esc(surpriseText(career))}</div>

            <div class="reaction-panel">
              <h2>Your reaction</h2>
              <p>React to the actual work—not whether the title sounds impressive.</p>
              <div class="reaction-buttons">
                ${['Interesting', 'Maybe', 'Not for me', 'Need to learn more'].map(label => `<button class="btn reaction-btn" type="button" data-reaction="${esc(label)}" aria-pressed="${reaction === label}">${esc(label)}</button>`).join('')}
              </div>
              <p id="reactionStatus" class="small">${reaction ? `Saved as “${esc(reaction)}.”` : 'No reaction selected yet.'}</p>
            </div>
          </article>

          <aside class="card role-facts">
            <div class="facts-label">One example—not a recommendation</div>
            <div class="fact"><small>Typical settings</small><strong>${esc(details['Typical work settings'] || career.category)}</strong></div>
            <div class="fact"><small>Animal contact</small><strong>${esc(career.directContact || 'Varies by employer')}</strong></div>
            <div class="fact"><small>School reality</small><strong>${esc(career.educationBand || details['Typical education / progression'] || 'Preparation varies')}</strong></div>
            <div class="fact"><small>Good to test early</small><strong>${esc(earlyTest(career))}</strong></div>
          </aside>
        </div>

        <details class="card deep-details">
          <summary>Dig deeper: qualifications, evidence, titles, and progression</summary>
          <div class="deep-content">
            <div class="deep-grid">
              <div class="deep-box"><h3>Useful undergraduate preparation</h3><p>${esc(details['Undergraduate preparation most useful'] || 'Build relevant science, methods, communication, and supervised experience.')}</p></div>
              <div class="deep-box"><h3>Education and progression</h3><p>${esc(details['Typical education / progression'] || career.educationBand || 'Varies by employer and specialty.')}</p></div>
              <div class="deep-box"><h3>Core competencies</h3>${competencies.length ? `<ul>${competencies.map(item => `<li>${esc(item.name)}</li>`).join('')}</ul>` : '<p>No competency detail is recorded yet.</p>'}</div>
              <div class="deep-box"><h3>Observed or searchable titles</h3>${observed.length ? `<ul>${observed.map(item => `<li>${esc(item.title)}</li>`).join('')}</ul>` : `<p>${esc(details['Searchable job titles'] || 'No directly observed titles are recorded yet.')}</p>`}</div>
              <div class="deep-box"><h3>Evidence status</h3><p>${esc(career.marketStatus || details['Market status'] || 'Established career concept')}${career.lastVerified ? ` · Last reviewed ${esc(career.lastVerified)}` : ''}</p></div>
              <div class="deep-box"><h3>Salary context</h3><p>${esc(details['Salary context'] || 'Salary varies by employer, location, experience, and education. Treat broad ranges as orientation, not a promise.')}</p></div>
            </div>
          </div>
        </details>

        <div class="button-row">
          <button class="btn" type="button" data-go="roles">Back to roles</button>
          <button class="btn primary" type="button" data-next-role>${reaction ? 'See another role' : 'Skip for now and see another'}</button>
          ${shortlistedCareers().length ? `<button class="btn soft" type="button" data-go="shortlist">See what connects (${shortlistedCareers().length})</button>` : ''}
        </div>
      </section>`;
  }

  function shortlistedCareers() {
    const included = new Set(['Interesting', 'Maybe', 'Need to learn more']);
    return D.careers.filter(career => included.has(state.reactions[career.id]));
  }

  function shortlistPatterns(careers) {
    if (!careers.length) return [];
    return D.dimLabels.map((label, index) => ({
      label,
      score: careers.reduce((sum, career) => sum + (career.dims?.[index] || 0), 0) / careers.length
    })).sort((a, b) => b.score - a.score).slice(0, 4).filter(item => item.score >= 1.25);
  }

  function supportStrength(value) {
    if (value === 'S' || value === 'SG') return 3;
    if (value === 'C' || value === 'C*') return 2;
    if (value === 'G') return 1;
    return 0;
  }

  function programMatches(careers) {
    if (!careers.length) return [];
    return D.programs.map(program => {
      const strengths = careers.map(career => ({ career, value: supportStrength(career.support?.[program.code]) }));
      const score = strengths.reduce((sum, item) => sum + item.value, 0) / careers.length;
      const strongFor = strengths.filter(item => item.value >= 2).map(item => item.career.name);
      return { program, score, strongFor };
    }).sort((a, b) => b.score - a.score).slice(0, 3);
  }

  function programReason(match) {
    if (match.strongFor.length >= 2) return `Provides meaningful undergraduate preparation for ${match.strongFor.slice(0, 2).join(' and ')}.`;
    if (match.strongFor.length === 1) return `Directly supports ${match.strongFor[0]} while keeping some related options open.`;
    return 'Offers adjacent preparation, but important experience or coursework would need to be built outside the core program.';
  }

  function renderShortlist(options = {}) {
    const careers = shortlistedCareers();
    const patterns = shortlistPatterns(careers);
    const programs = programMatches(careers);

    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Your emerging shortlist</div>
        <h1>Look for patterns before choosing a college path.</h1>
        <p class="lead">These roles are starting points. The useful question is what they share—and which programs preserve several possibilities.</p>

        ${careers.length ? `
          <div class="shortlist-layout">
            <div class="card shortlist-card">
              <h2>${careers.length} role${careers.length === 1 ? '' : 's'} worth keeping in view</h2>
              ${careers.map(career => `
                <div class="shortlist-row">
                  <div><strong>${esc(career.name)}</strong><p>${esc(career.roleFocus || '')}</p><span class="pill ${state.reactions[career.id] === 'Interesting' ? 'green' : 'blue'}">${esc(state.reactions[career.id])}</span></div>
                  <div class="shortlist-actions"><button class="btn small-btn" type="button" data-role="${esc(career.id)}">Open</button><button class="btn small-btn text" type="button" data-remove="${esc(career.id)}">Remove</button></div>
                </div>`).join('')}
            </div>
            <aside class="card shortlist-card pattern-card">
              <div class="eyebrow" style="color:#bfe8da">Patterns to notice</div>
              <h2>Your choices currently lean toward</h2>
              <div class="pill-row" style="margin-top:16px">${patterns.map(item => `<span class="pill">${esc(item.label)}</span>`).join('') || '<span class="pill">Keep exploring to reveal a pattern</span>'}</div>
              <p style="margin-top:18px">A pattern is more useful than a single title. It can guide courses, volunteering, and college comparisons while leaving room to change.</p>
            </aside>
          </div>

          <section id="programConnections" class="program-section">
            <div class="section-heading"><div><h2>Programs that preserve these possibilities</h2><p>Examples from the researched college set—not a ranking or final list.</p></div></div>
            <div class="program-grid">
              ${programs.map(match => `
                <article class="card program-card">
                  <span class="school">${esc(match.program.school)}</span>
                  <h3>${esc(match.program.title)}</h3>
                  <p class="match-reason"><strong>Why it connects:</strong> ${esc(programReason(match))}</p>
                  <p><strong>Best when:</strong> ${esc(match.program.bestWhen || 'The program’s strengths match the kind of work the student wants to test.')}</p>
                  <div class="pill-row">${(match.program.experienceTags || []).slice(0, 4).map(tag => `<span class="pill">${esc(tag)}</span>`).join('')}</div>
                  <div class="button-row"><a class="btn small-btn" href="index.html#programs">Compare in full explorer</a></div>
                </article>`).join('')}
            </div>
            <div class="context-note"><strong>Sequence matters:</strong> first identify work worth testing, then compare how well a program builds the science, methods, and experience needed across several possible roles.</div>
          </section>
        ` : `
          <div class="empty-state" style="margin-top:28px">
            <h2>No roles are on your shortlist yet</h2>
            <p>Explore a few roles and choose “Interesting,” “Maybe,” or “Need to learn more.”</p>
            <button class="btn primary" type="button" data-go="worlds">Choose a career world</button>
          </div>`}

        <div class="next-actions">
          <div class="button-row">
            <button class="btn" type="button" data-go="worlds">Explore another career world</button>
            <button class="btn soft" type="button" data-go="roles">Browse more roles</button>
            <a class="btn" href="index.html">Use the full research explorer</a>
          </div>
        </div>
      </section>`;

    if (options.focusPrograms && careers.length) {
      requestAnimationFrame(() => document.getElementById('programConnections')?.scrollIntoView({ behavior: 'smooth' }));
    }
  }

  function openRole(id) {
    currentRoleId = id;
    showScreen('role');
  }

  function nextRole() {
    const pool = rolePool();
    const index = pool.findIndex(career => career.id === currentRoleId);
    const next = pool[(index + 1) % pool.length] || pool[0];
    if (next) openRole(next.id);
  }

  root.addEventListener('click', event => {
    const start = event.target.closest('[data-start]');
    if (start) {
      searchText = '';
      roleLimit = 12;
      if (start.dataset.start === 'search') {
        state.selectedWorlds = [];
        saveState();
        showScreen('roles');
        requestAnimationFrame(() => document.getElementById('roleSearch')?.focus());
      } else showScreen('worlds');
      return;
    }

    const go = event.target.closest('[data-go]');
    if (go) { showScreen(go.dataset.go); return; }

    const worldButton = event.target.closest('[data-world]');
    if (worldButton) {
      const id = worldButton.dataset.world;
      state.selectedWorlds = state.selectedWorlds.includes(id)
        ? state.selectedWorlds.filter(item => item !== id)
        : [...state.selectedWorlds, id];
      saveState();
      roleLimit = 12;
      renderWorlds();
      return;
    }

    if (event.target.closest('#seeRolesButton')) { searchText = ''; roleLimit = 12; showScreen('roles'); return; }
    if (event.target.closest('[data-browse-all]')) { state.selectedWorlds = []; searchText = ''; roleLimit = 12; saveState(); showScreen('roles'); return; }

    if (event.target.closest('[data-show-more]')) {
      roleLimit += 12;
      updateRoleResults();
      return;
    }

    const role = event.target.closest('[data-role]');
    if (role) { openRole(role.dataset.role); return; }

    const reaction = event.target.closest('[data-reaction]');
    if (reaction) {
      state.reactions[currentRoleId] = reaction.dataset.reaction;
      saveState();
      renderRole();
      return;
    }

    if (event.target.closest('[data-next-role]')) { nextRole(); return; }

    const remove = event.target.closest('[data-remove]');
    if (remove) {
      delete state.reactions[remove.dataset.remove];
      saveState();
      renderShortlist();
    }
  });

  document.querySelectorAll('[data-screen-link]').forEach(button => {
    button.addEventListener('click', () => showScreen(button.dataset.screenLink, { focusPrograms: button.hasAttribute('data-focus-programs') }));
  });

  document.getElementById('mobileMenuButton').addEventListener('click', event => {
    const nav = document.getElementById('discoveryNav');
    const open = nav.classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });

  showScreen('start');
})();
