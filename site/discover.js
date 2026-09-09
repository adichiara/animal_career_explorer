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

  const interestPrompts = {
    care: 'Caring for individual animals and noticing what they need',
    behavior: 'Figuring out why animals behave, learn, or respond as they do',
    wildlife: 'Observing animals outdoors and understanding how they live',
    protect: 'Helping species recover and improving the habitats they depend on',
    research: 'Answering biological questions through systematic investigation',
    data: 'Finding patterns in measurements, maps, or scientific evidence',
    communicate: 'Explaining animal science and conservation to other people'
  };

  const areaDetails = {
    care: {
      settings: 'Zoos, aquariums, sanctuaries, rehabilitation centers, breeding programs, shelters, and assistance-animal organizations.',
      responsibilities: [
        'Prepare food, feed animals, clean and maintain living spaces, and monitor daily routines.',
        'Observe health and behavior, recognize changes, and maintain accurate records.',
        'Provide enrichment or training, support veterinary procedures, and follow safety protocols.'
      ],
      knowledge: ['Species biology and natural history', 'Husbandry, nutrition, welfare, and basic health', 'Learning principles, safety procedures, ethics, and regulations'],
      skills: ['Detailed observation', 'Safe handling and husbandry techniques', 'Reliability, teamwork, recordkeeping, and physical stamina'],
      realities: 'Often physical and repetitive. Schedules may include early mornings, weekends, holidays, outdoor work, cleaning, and strict safety routines.'
    },
    behavior: {
      settings: 'Zoos, aquariums, shelters, universities, laboratories, farms, consulting practices, and animal-welfare programs.',
      responsibilities: [
        'Define and observe behavior systematically using ethograms, logs, video, or other measures.',
        'Develop enrichment, training, management, or research plans based on behavior and welfare goals.',
        'Evaluate outcomes, interpret evidence, and communicate recommendations to caregivers, researchers, or clients.'
      ],
      knowledge: ['Ethology, cognition, and learning theory', 'Animal welfare and species-specific behavior', 'Research design, measurement, and statistics'],
      skills: ['Behavioral observation and coding', 'Humane training or intervention design', 'Data interpretation, clear writing, and collaborative problem-solving'],
      realities: 'Direct animal contact varies widely. Many roles involve more observation, documentation, data analysis, and staff communication than handling.'
    },
    wildlife: {
      settings: 'Field stations, universities, consulting firms, parks, refuges, government agencies, and conservation organizations.',
      responsibilities: [
        'Conduct surveys, identify species, collect samples, and record habitat or population data.',
        'Use tools such as cameras, acoustic sensors, telemetry, GPS, or GIS to monitor wildlife.',
        'Manage field protocols, equipment, permits, data quality, and reports.'
      ],
      knowledge: ['Ecology, evolution, and natural history', 'Population biology and habitat relationships', 'Sampling design, statistics, GIS, and field safety'],
      skills: ['Species identification and field observation', 'Accurate data collection under variable conditions', 'Navigation, equipment use, teamwork, and technical writing'],
      realities: 'Work can involve travel, irregular hours, weather, insects, difficult terrain, seasonal appointments, and long periods with limited animal contact.'
    },
    protect: {
      settings: 'Government agencies, conservation nonprofits, land trusts, parks, refuges, consulting firms, and species-recovery programs.',
      responsibilities: [
        'Assess species, populations, habitats, and threats using field and existing evidence.',
        'Plan or implement recovery, restoration, monitoring, compliance, or management actions.',
        'Coordinate with landowners, agencies, scientists, community groups, and funders.'
      ],
      knowledge: ['Conservation biology and population ecology', 'Habitat management, restoration, and environmental policy', 'Monitoring methods, GIS, statistics, and project planning'],
      skills: ['Evaluating evidence and tradeoffs', 'Project coordination and regulatory documentation', 'Field methods, mapping, communication, and stakeholder work'],
      realities: 'Conservation outcomes depend heavily on people, budgets, land use, policy, and long timelines—not only biological knowledge.'
    },
    research: {
      settings: 'Universities, government laboratories, zoos, museums, nonprofit institutes, field stations, and private research organizations.',
      responsibilities: [
        'Turn a broad question into testable hypotheses, measures, and a workable study design.',
        'Collect, manage, analyze, and document data while following research and animal-care protocols.',
        'Interpret results, identify limitations, and communicate findings through reports, papers, or presentations.'
      ],
      knowledge: ['Biology relevant to the research question', 'Experimental and observational research methods', 'Statistics, scientific ethics, and literature evaluation'],
      skills: ['Careful measurement and protocol adherence', 'Data analysis and scientific reasoning', 'Technical writing, persistence, and troubleshooting'],
      realities: 'Independent scientist roles usually require graduate training. Undergraduate entry points are commonly assistant, technician, laboratory, or field positions.'
    },
    data: {
      settings: 'Government agencies, universities, consulting firms, conservation organizations, environmental companies, and research teams.',
      responsibilities: [
        'Clean, organize, document, and assess the quality of biological or environmental data.',
        'Analyze patterns using statistics, code, databases, GIS, remote sensing, or models.',
        'Create maps, figures, reports, or decision tools and explain uncertainty to non-specialists.'
      ],
      knowledge: ['Ecology or biological science', 'Statistics, study design, and data quality', 'Programming, databases, GIS, remote sensing, or quantitative modeling'],
      skills: ['Structured analytical thinking', 'Reproducible data management and visualization', 'Explaining assumptions, uncertainty, and results clearly'],
      realities: 'Most time is computer-based. Strong biological context is still important because technically correct analysis can be scientifically misleading.'
    },
    communicate: {
      settings: 'Zoos, aquariums, museums, schools, parks, nature centers, nonprofits, media organizations, and public agencies.',
      responsibilities: [
        'Translate animal science or conservation information for a specific audience.',
        'Develop programs, lessons, exhibits, articles, presentations, or public events.',
        'Evaluate audience needs, coordinate logistics, and revise content for accuracy and accessibility.'
      ],
      knowledge: ['Animal biology, ecology, or conservation', 'Learning, interpretation, and audience engagement', 'Writing, media, program design, and information accuracy'],
      skills: ['Public speaking and explanatory writing', 'Adapting content for different audiences', 'Facilitation, planning, collaboration, and feedback'],
      realities: 'The work often combines science with customer service, scheduling, event logistics, writing, and repeated delivery to varied audiences.'
    }
  };

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
    start: { label: 'Choose a starting point', number: '1 of 5', width: '20%' },
    interests: { label: 'Select interests', number: '1 of 5', width: '20%' },
    worlds: { label: 'Select work areas', number: '1 of 5', width: '20%' },
    areas: { label: 'Understand the work areas', number: '2 of 5', width: '40%' },
    roles: { label: 'View related roles', number: '3 of 5', width: '60%' },
    role: { label: 'Examine a role', number: '4 of 5', width: '80%' },
    shortlist: { label: 'Compare roles and programs', number: '5 of 5', width: '100%' }
  };

  let state = loadState();
  let currentScreen = 'start';
  let searchText = '';
  let currentRoleId = '';
  let roleLimit = 12;
  let areaSource = 'worlds';

  function blankState() {
    return { selectedWorlds: [], reactions: {}, viewed: [] };
  }

  function loadState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return { ...blankState(), ...parsed, selectedWorlds: (parsed.selectedWorlds || []).slice(0, 3) };
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

  function excerpt(value, max = 240) {
    const text = String(value || '').trim();
    if (text.length <= max) return text;
    const shortened = text.slice(0, max);
    const boundary = Math.max(shortened.lastIndexOf('. '), shortened.lastIndexOf('; '), shortened.lastIndexOf(', '));
    return `${shortened.slice(0, boundary > max * .55 ? boundary + 1 : max).trim()}…`;
  }

  function careerByName(name) { return D.careers.find(career => career.name === name); }
  function careerById(id) { return D.careers.find(career => career.id === id); }

  function updateHeader() {
    const count = shortlistedCareers().length;
    document.getElementById('navShortlistCount').textContent = count;
    document.querySelectorAll('.discovery-nav-link').forEach(link => {
      const target = link.dataset.screenLink;
      link.classList.toggle('active', target === currentScreen || (target === 'start' && ['interests', 'worlds', 'areas', 'roles', 'role'].includes(currentScreen)));
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
    if (screen === 'interests') renderInterests();
    if (screen === 'worlds') renderWorlds();
    if (screen === 'areas') renderAreas();
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
        <div class="eyebrow">Career exploration</div>
        <h1>Explore animal-related work from different starting points.</h1>
        <p class="lead">Begin with interests, broad work areas, or a role you already know.</p>

        <div class="choice-grid">
          <button class="choice-card" type="button" data-start="interests">
            <span class="choice-icon">✦</span>
            <strong>Start with what sounds interesting</strong>
            <span>Select topics and activities first, without needing to know career categories.</span>
          </button>
          <button class="choice-card" type="button" data-start="worlds">
            <span class="choice-icon">⌁</span>
            <strong>Browse types of animal work</strong>
            <span>Compare seven broad areas of work and the kinds of roles found within them.</span>
          </button>
          <button class="choice-card" type="button" data-start="search">
            <span class="choice-icon">⌕</span>
            <strong>I already have something in mind</strong>
            <span>Search the career library by role, activity, specialty, or setting.</span>
          </button>
        </div>

        ${shortlistedCareers().length ? `<div class="button-row"><button class="btn soft" type="button" data-go="shortlist">Continue with my ${shortlistedCareers().length}-role shortlist</button></div>` : ''}
      </section>`;
  }

  function renderInterests() {
    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Interest areas</div>
        <h1>What sounds interesting?</h1>
        <p class="lead">Select up to three. The next page explains the responsibilities, knowledge, and skills connected with each choice.</p>

        <div class="interest-grid">
          ${worlds.map(world => `
            <button class="interest-card" type="button" data-interest="${world.id}" aria-pressed="${state.selectedWorlds.includes(world.id)}">
              <span class="world-icon">${world.icon}</span>
              <strong>${esc(interestPrompts[world.id])}</strong>
              <span class="interest-area-label">Related area: ${esc(world.title)}</span>
            </button>`).join('')}
        </div>
        <p id="selectionHint" class="selection-hint">${state.selectedWorlds.length} of 3 selected</p>

        <div class="button-row">
          <button class="btn" type="button" data-go="start">Back</button>
          <button class="btn primary" id="understandInterestsButton" type="button" ${state.selectedWorlds.length ? '' : 'disabled'}>Understand these interest areas</button>
        </div>
      </section>`;
  }

  function renderWorlds() {
    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Career worlds</div>
        <h1>Types of animal-related work</h1>
        <p class="lead">Select up to three areas to compare their responsibilities, knowledge, skills, settings, and working conditions.</p>

        <div class="world-grid" style="margin-top:28px">
          ${worlds.map(world => `
            <button class="world-card" type="button" data-world="${world.id}" aria-pressed="${state.selectedWorlds.includes(world.id)}">
              <span class="world-icon">${world.icon}</span>
              <strong>${esc(world.title)}</strong>
              <span>${esc(world.description)}</span>
              <span class="world-count">Sample ${world.careers.length} different roles</span>
            </button>`).join('')}
        </div>

        <p id="selectionHint" class="selection-hint">${state.selectedWorlds.length} of 3 selected</p>
        <div class="button-row">
          <button class="btn" type="button" data-go="start">Back</button>
          <button class="btn primary" id="seeRolesButton" type="button" ${state.selectedWorlds.length ? '' : 'disabled'}>Understand selected areas</button>
          <button class="btn text" type="button" data-browse-all>Browse all 93 careers instead</button>
        </div>
      </section>`;
  }

  function renderAreas() {
    const selected = state.selectedWorlds.map(id => worlds.find(world => world.id === id)).filter(Boolean);
    if (!selected.length) return showScreen(areaSource);
    root.innerHTML = `
      <section class="screen">
        <div class="eyebrow">Work-area briefing</div>
        <h1>What these areas involve</h1>
        <p class="lead">Responsibilities describe the work performed. Knowledge is what workers need to understand. Skills are capabilities used to do the work effectively.</p>

        <div class="area-stack">
          ${selected.map(world => {
            const info = areaDetails[world.id];
            return `
              <article class="card area-card">
                <header class="area-card-header">
                  <span class="world-icon">${world.icon}</span>
                  <div><h2>${esc(world.title)}</h2><p>${esc(world.description)}</p></div>
                  <button class="btn small-btn text" type="button" data-remove-area="${world.id}">Remove</button>
                </header>
                <div class="area-setting"><strong>Common settings</strong><span>${esc(info.settings)}</span></div>
                <div class="area-examples"><strong>Example roles</strong><span>${world.careers.slice(0, 5).map(esc).join(' · ')}</span></div>
                <div class="area-info-grid">
                  <section><h3>Responsibilities</h3><ul>${info.responsibilities.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section>
                  <section><h3>Knowledge</h3><ul>${info.knowledge.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section>
                  <section><h3>Skills</h3><ul>${info.skills.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section>
                </div>
                <div class="area-realities"><strong>Typical work realities</strong><span>${esc(info.realities)}</span></div>
              </article>`;
          }).join('')}
        </div>

        <div class="button-row">
          <button class="btn" type="button" data-go="${areaSource}">${areaSource === 'interests' ? 'Change interests' : 'Change work areas'}</button>
          <button class="btn primary" type="button" data-go="roles">View ${rolePool().length} related roles</button>
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
        <h1>${selectedLabels.length ? 'Roles related to the selected work areas' : 'Career role library'}</h1>
        <p class="lead">Each profile summarizes purpose, responsibilities, setting, animal contact, education, experience, and supporting evidence.</p>

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
    if (band.includes('Graduate degree typical')) return 'The title is usually not an entry role. Undergraduate research, methods courses, and early technician work often come before graduate specialization.';
    if (band.includes('later career') || band.includes('substantial') || band.includes('progressive')) return 'This is generally a destination role rather than an entry job. Early positions build the experience needed to reach it.';
    if ((career.directContact || '').startsWith('High')) return 'High animal contact does not mean the whole day is hands-on. Cleaning, preparation, safety, documentation, and teamwork can take substantial time.';
    if ((career.directContact || '').startsWith('Low')) return 'Working for animals does not always mean working directly with them. Data, habitats, research protocols, writing, or people may occupy most of the day.';
    return 'The same title can look quite different across employers. Setting and day-to-day duties matter more than the title alone.';
  }

  function earlyTest(career) {
    const tags = career.workTags || [];
    if (tags.includes('Animal care')) return 'Structured animal-care work that includes cleaning, observation, recordkeeping, feedback, and safety procedures.';
    if (tags.includes('Fieldwork')) return 'Field surveys, habitat-monitoring projects, or outdoor volunteer roles with systematic data collection.';
    if (tags.includes('Data / statistics')) return 'Organizing and analyzing biology or ecology data, including explaining results and limitations.';
    if (tags.includes('Education / public')) return 'Teaching, interpretation, or science writing for a real audience.';
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

            <div class="surprise"><strong>Commonly overlooked part of the work</strong>${esc(surpriseText(career))}</div>

            <div class="reaction-panel">
              <h2>Your reaction</h2>
              <p>Consider the responsibilities, setting, contact level, and preparation.</p>
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
            <div class="fact"><small>Relevant early experience</small><strong>${esc(earlyTest(career))}</strong></div>
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
          <button class="btn primary" type="button" data-next-role>Next role</button>
          ${shortlistedCareers().length ? `<button class="btn soft" type="button" data-go="shortlist">Compare shortlist (${shortlistedCareers().length})</button>` : ''}
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
        <h1>Compare selected roles and college preparation.</h1>
        <p class="lead">Shared content areas are calculated from the career profiles. Program connections use the project’s curriculum-support mappings.</p>

        ${careers.length ? `
          <div class="shortlist-layout">
            <div class="card shortlist-card">
              <h2>${careers.length} selected role${careers.length === 1 ? '' : 's'}</h2>
              ${careers.map(career => `
                <div class="shortlist-row">
                  <div><strong>${esc(career.name)}</strong><p>${esc(career.roleFocus || '')}</p><span class="pill ${state.reactions[career.id] === 'Interesting' ? 'green' : 'blue'}">${esc(state.reactions[career.id])}</span></div>
                  <div class="shortlist-actions"><button class="btn small-btn" type="button" data-role="${esc(career.id)}">Open</button><button class="btn small-btn text" type="button" data-remove="${esc(career.id)}">Remove</button></div>
                </div>`).join('')}
            </div>
            <aside class="card shortlist-card pattern-card">
              <div class="eyebrow" style="color:#bfe8da">Shared career content</div>
              <h2>Strongest areas across these roles</h2>
              <div class="pill-row" style="margin-top:16px">${patterns.map(item => `<span class="pill">${esc(item.label)}</span>`).join('') || '<span class="pill">Not enough profile overlap yet</span>'}</div>
              <p style="margin-top:18px">These areas are based on the highest average profile dimensions among the selected careers.</p>
            </aside>
          </div>

          <section id="programConnections" class="program-section">
            <div class="section-heading"><div><h2>Programs with the strongest mapped support</h2><p>Top three among the ten researched programs for the current shortlist.</p></div></div>
            <div class="program-grid">
              ${programs.map(match => `
                <article class="card program-card">
                  <span class="school">${esc(match.program.school)}</span>
                  <h3>${esc(match.program.title)}</h3>
                  <p class="match-reason"><strong>Why it connects:</strong> ${esc(programReason(match))}</p>
                  <p><strong>Program focus:</strong> ${esc(excerpt(match.program.fundamental, 260))}</p>
                  <p><strong>Experience structure:</strong> ${esc(excerpt(match.program.experience, 220))}</p>
                  ${(match.program.tradeoffs || []).length ? `<p><strong>Important limitation:</strong> ${esc(match.program.tradeoffs[0])}</p>` : ''}
                  <div class="pill-row">${(match.program.experienceTags || []).slice(0, 4).map(tag => `<span class="pill">${esc(tag)}</span>`).join('')}</div>
                  <div class="button-row"><a class="btn small-btn" href="index.html#programs">Compare in full explorer</a></div>
                </article>`).join('')}
            </div>
            <div class="context-note"><strong>How connections are calculated:</strong> each career is mapped to programs as strong preparation, complementary preparation, general background, or not a direct fit. The cards above have the highest average support across the current shortlist.</div>
          </section>
        ` : `
          <div class="empty-state" style="margin-top:28px">
            <h2>No roles are on your shortlist yet</h2>
            <p>Explore a few roles and choose “Interesting,” “Maybe,” or “Need to learn more.”</p>
            <button class="btn primary" type="button" data-go="worlds">Choose a career world</button>
          </div>`}

        <div class="next-actions">
          <div class="button-row">
            <button class="btn" type="button" data-go="worlds">Select different work areas</button>
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

  function toggleArea(id, screen) {
    const index = state.selectedWorlds.indexOf(id);
    if (index >= 0) state.selectedWorlds.splice(index, 1);
    else if (state.selectedWorlds.length < 3) state.selectedWorlds.push(id);
    else {
      const hint = document.getElementById('selectionHint');
      if (hint) hint.textContent = 'Three areas are already selected. Remove one to add another.';
      return;
    }
    saveState();
    roleLimit = 12;
    if (screen === 'interests') renderInterests();
    else renderWorlds();
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
      } else {
        areaSource = start.dataset.start;
        showScreen(start.dataset.start);
      }
      return;
    }

    const go = event.target.closest('[data-go]');
    if (go) { showScreen(go.dataset.go); return; }

    const worldButton = event.target.closest('[data-world]');
    if (worldButton) {
      toggleArea(worldButton.dataset.world, 'worlds');
      return;
    }

    const interestButton = event.target.closest('[data-interest]');
    if (interestButton) {
      toggleArea(interestButton.dataset.interest, 'interests');
      return;
    }

    if (event.target.closest('#seeRolesButton') || event.target.closest('#understandInterestsButton')) { areaSource = currentScreen; searchText = ''; roleLimit = 12; showScreen('areas'); return; }
    if (event.target.closest('[data-browse-all]')) { state.selectedWorlds = []; searchText = ''; roleLimit = 12; saveState(); showScreen('roles'); return; }

    if (event.target.closest('[data-show-more]')) {
      roleLimit += 12;
      updateRoleResults();
      return;
    }

    const removeArea = event.target.closest('[data-remove-area]');
    if (removeArea) {
      state.selectedWorlds = state.selectedWorlds.filter(id => id !== removeArea.dataset.removeArea);
      saveState();
      showScreen(state.selectedWorlds.length ? 'areas' : areaSource);
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
