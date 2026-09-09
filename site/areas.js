(function () {
  'use strict';

  const D = window.EXPLORER_DATA;
  const app = document.getElementById('app');
  const storageKey = 'animalExplorerAreasV1';

  const groups = [
    { id: 'organismal', title: 'Biological & organismal sciences', description: 'Fields centered on animals as organisms, their biological systems, their diversity, and their relationships with environments.', color: '#176d8c' },
    { id: 'wild', title: 'Wildlife & environmental sciences', description: 'Fields centered on free-ranging animals, populations, habitats, marine systems, and conservation decisions.', color: '#087d72' },
    { id: 'behavior', title: 'Behavior, cognition & welfare', description: 'Fields centered on what animals do, how they process information, and how their experiences and wellbeing can be studied and improved.', color: '#6457a6' },
    { id: 'managed', title: 'Animals under human care', description: 'Fields centered on the biology, care, management, behavior, and welfare of domesticated or managed animals.', color: '#b95622' },
    { id: 'health', title: 'Health, treatment & rehabilitation', description: 'Fields centered on preventing or treating illness and injury, restoring function, and preparing animals for continued care or release.', color: '#a83c61' }
  ];

  const areas = [
    {
      id: 'animal-biology', group: 'organismal', title: 'Animal Biology',
      short: 'How animals function biologically, from cells and physiological systems to whole organisms.',
      bigPicture: 'Animal biology studies the biological structure and function of animals. Programs can range from molecular and physiological science to whole-animal biology, behavior, ecology, and evolution.',
      focus: ['Physiology and metabolism', 'Genetics, development, and reproduction', 'Anatomy and organismal function', 'Hormones, health, and biological responses'],
      questions: [
        'How does an animal regulate temperature, energy, or water balance?',
        'How do hormones influence reproduction, stress, or behavior?',
        'How do genetics and development produce physical or behavioral traits?',
        'How do biological systems differ across animal groups?'
      ],
      responsibilities: [
        'Conduct laboratory or organism-level experiments and follow research protocols.',
        'Collect biological measurements, samples, images, or observational data.',
        'Analyze results and connect cellular or physiological processes to whole-animal function.',
        'Read scientific literature and communicate methods, findings, and limitations.'
      ],
      knowledgeSkills: ['Cell biology, genetics, anatomy, and physiology', 'Chemistry and biochemistry', 'Experimental design and statistics', 'Laboratory methods and careful measurement', 'Scientific writing and data interpretation'],
      variations: [
        ['Scale of study', 'Work may focus on molecules and cells, organs and systems, or intact animals.'],
        ['Animal contact', 'Some studies require direct handling; others use tissues, samples, images, or existing datasets.'],
        ['Research environment', 'Work can occur in laboratories, field stations, veterinary settings, museums, universities, or government facilities.'],
        ['Program identity', 'At the undergraduate level, animal biology and zoology may be nearly identical or may emphasize very different faculty specialties.']
      ],
      settings: ['Laboratories and research facilities', 'Universities and museums', 'Government or nonprofit research programs', 'Field stations and animal-care facilities'],
      realities: ['Many independent research roles require graduate education.', 'Laboratory work may involve repetitive protocols and detailed documentation.', 'Direct animal contact may be limited even when the research is entirely animal-focused.', 'Strong chemistry, quantitative, and writing preparation is often important.'],
      careers: ['Animal physiologist', 'Evolutionary biologist studying animals', 'Conservation geneticist / wildlife genomicist', 'eDNA / molecular ecology technician', 'University / laboratory research assistant', 'Research scientist / principal investigator'],
      programCodes: ['ME-ZOO', 'UMA-BIO', 'UNE-AN', 'UNE-AB'],
      related: ['zoology', 'animal-behavior', 'animal-cognition', 'veterinary-science'],
      references: [
        ['O*NET: Biological Technicians', 'Occupational data', 'https://www.onetonline.org/link/summary/19-4021.00'],
        ['University of Maine: Zoology', 'Undergraduate example', 'https://sbe.umaine.edu/undergraduate/zoology/'],
        ['UMass Amherst: Biology electives', 'Undergraduate example', 'https://www.umass.edu/biology/academics/undergraduate-program/courses-approved-major-electives']
      ]
    },
    {
      id: 'zoology', group: 'organismal', title: 'Zoology',
      short: 'The broad scientific study of animals, their diversity, evolution, structure, function, behavior, and ecology.',
      bigPicture: 'Zoology is organized around animals as a group of organisms. It can span molecular biology, anatomy, physiology, taxonomy, evolution, behavior, and ecology rather than prescribing one kind of job.',
      focus: ['Animal diversity and classification', 'Comparative anatomy and physiology', 'Evolution and adaptation', 'Behavior, ecology, and life history'],
      questions: [
        'How are different groups of animals related evolutionarily?',
        'Why did particular anatomical, physiological, or behavioral traits evolve?',
        'How do different species survive, reproduce, and interact with their environments?',
        'How can animal diversity be documented and understood?'
      ],
      responsibilities: [
        'Identify, observe, sample, or compare animals and their biological traits.',
        'Conduct laboratory, museum, collection, or field research.',
        'Maintain specimens, records, datasets, or research equipment.',
        'Analyze evidence and communicate findings through reports, papers, exhibits, or presentations.'
      ],
      knowledgeSkills: ['Animal diversity and natural history', 'Evolution, ecology, anatomy, and physiology', 'Species identification and comparative methods', 'Research design and statistics', 'Field, laboratory, or collections techniques'],
      variations: [
        ['Specialization', 'A zoologist may specialize in mammals, birds, reptiles, insects, marine animals, physiology, behavior, or another taxon or process.'],
        ['Work setting', 'The same degree can lead toward field research, laboratory science, museums, conservation, education, or graduate study.'],
        ['Breadth', 'Some programs retain broad animal diversity; others function much like general biology with animal-focused electives.'],
        ['Career title', 'Many people trained in zoology work under titles such as biologist, research technician, ecologist, curator, or environmental scientist.']
      ],
      settings: ['Universities and research institutes', 'Museums and biological collections', 'Government and conservation organizations', 'Laboratories, field stations, and natural areas'],
      realities: ['“Zoologist” is less common as a job title than many specialized biologist titles.', 'Broad programs require deliberate choices to build a distinctive specialty and experience record.', 'Field and laboratory opportunities depend heavily on faculty, location, and student initiative.', 'Graduate education is common for independent research and taxonomic specialties.'],
      careers: ['Zoologist', 'Mammalogist', 'Ornithologist', 'Herpetologist', 'Ecological research technician', 'Museum / natural-history education or collections work'],
      programCodes: ['ME-ZOO', 'UMA-BIO', 'ME-WE', 'URI-W'],
      related: ['animal-biology', 'ecology', 'wildlife-biology', 'animal-behavior'],
      references: [
        ['BLS: Zoologists and Wildlife Biologists', 'Occupational overview', 'https://www.bls.gov/ooh/life-physical-and-social-science/zoologists-and-wildlife-biologists.htm'],
        ['O*NET: Zoologists and Wildlife Biologists', 'Tasks and skills', 'https://www.onetonline.org/link/summary/19-1023.00'],
        ['University of Maine: Zoology', 'Undergraduate example', 'https://sbe.umaine.edu/undergraduate/zoology/'],
        ['SPNHC: Job Opportunities', 'Collections and natural-history jobs', 'https://spnhc.org/category/job-opportunities/']
      ]
    },
    {
      id: 'ecology', group: 'organismal', title: 'Ecology',
      short: 'How organisms interact with each other and with their physical environments.',
      bigPicture: 'Ecology examines relationships at several levels—from individual organisms and populations to communities and ecosystems. It supplies much of the scientific foundation used in wildlife biology, conservation, restoration, and environmental management.',
      focus: ['Populations and communities', 'Food webs and species interactions', 'Habitats and environmental change', 'Ecosystem processes and restoration'],
      questions: [
        'Why is a population increasing, declining, moving, or changing?',
        'How does one species affect other organisms in a community?',
        'What determines where organisms can live and reproduce?',
        'How do climate, disturbance, or restoration change ecological systems?'
      ],
      responsibilities: [
        'Design surveys or experiments in field, laboratory, or computational settings.',
        'Measure organisms, populations, habitats, or environmental conditions.',
        'Use statistics, GIS, models, or long-term datasets to test ecological explanations.',
        'Translate findings into scientific publications, monitoring plans, or management recommendations.'
      ],
      knowledgeSkills: ['Population, community, and ecosystem ecology', 'Evolution and organismal biology', 'Sampling design and statistics', 'Field identification and measurement', 'GIS, coding, modeling, or data visualization'],
      variations: [
        ['Organisms', 'Ecologists may study animals, plants, microbes, whole communities, or interactions among them.'],
        ['Methods', 'Projects range from intensive outdoor sampling to laboratory experiments, remote sensing, mathematical modeling, and existing-data analysis.'],
        ['Purpose', 'Some ecology is curiosity-driven research; other work directly supports restoration, regulation, land management, or conservation.'],
        ['Time scale', 'Studies may examine a short behavioral interaction or decades of population and ecosystem change.']
      ],
      settings: ['Natural areas and field stations', 'Universities and laboratories', 'Government agencies and consulting firms', 'Conservation organizations and restoration projects'],
      realities: ['Fieldwork is common but not universal.', 'Data management, statistics, coding, and writing often occupy more time than animal observation.', 'Seasonal or temporary positions are common early in field-based careers.', 'Ecological conclusions often involve uncertainty, incomplete detection, and long time scales.'],
      careers: ['Field ecologist', 'Ecological research technician', 'Research ecologist', 'Population ecologist', 'Quantitative ecologist / biometrician', 'Habitat restoration / ecological-monitoring specialist'],
      programCodes: ['ME-WE', 'UMA-WEC', 'URI-W', 'ME-ZOO', 'UMA-BIO'],
      related: ['wildlife-biology', 'wildlife-conservation', 'zoology', 'marine-biology'],
      references: [
        ['O*NET: Environmental Restoration Planners', 'Applied ecology tasks', 'https://www.onetonline.org/link/summary/19-2041.02'],
        ['The Wildlife Society: Career paths', 'Professional field guide', 'https://wildlife.org/paths-to-becoming-a-wildlifer/'],
        ['UMass: Wildlife Ecology & Conservation', 'Undergraduate example', 'https://www.umass.edu/environmental-conservation/academics/undergraduate-programs/natural-resources-conservation/major/wildlife-ecology-conservation-concentration'],
        ['URI: Wildlife & Conservation curriculum', 'Undergraduate example', 'https://web.uri.edu/nrs/academics/wildlife-and-conservation-biology/curriculum/']
      ]
    },
    {
      id: 'wildlife-biology', group: 'wild', title: 'Wildlife Biology',
      short: 'Wild animals as members of populations and ecosystems: their survival, movement, reproduction, and habitats.',
      bigPicture: 'Wildlife biology focuses primarily on free-ranging animals, their populations, and their ecological relationships. Fieldwork is visible, but the work also depends on statistics, GIS, population models, genetics, remote sensing, permits, and technical writing.',
      focus: ['Population size, survival, and reproduction', 'Movement, migration, and habitat use', 'Wildlife disease and human–wildlife interactions', 'Monitoring, management, and applied research'],
      questions: [
        'How many animals remain, and how confidently can we estimate that number?',
        'Where do animals move during different seasons?',
        'Which habitat conditions predict survival or reproduction?',
        'What biological or human pressures explain a population change?'
      ],
      responsibilities: [
        'Conduct wildlife surveys, capture or observe animals, and collect samples or habitat data.',
        'Deploy cameras, acoustic sensors, telemetry, GPS, or other monitoring equipment.',
        'Clean and analyze population, movement, habitat, or survival data.',
        'Prepare permits, protocols, maps, reports, and recommendations for agencies or partners.'
      ],
      knowledgeSkills: ['Wildlife ecology and natural history', 'Population biology and habitat relationships', 'Field sampling, species identification, and safety', 'Statistics, GIS, and data management', 'Permitting, technical writing, and teamwork'],
      variations: [
        ['Field intensity', 'Some roles spend months outdoors; others coordinate field crews or analyze data primarily from an office.'],
        ['Animal contact', 'Work may involve capture and handling, distant observation, automated sensors, samples, or no direct contact.'],
        ['Employer', 'Agencies, universities, consulting firms, nonprofits, parks, tribes, and private landowners have different missions and constraints.'],
        ['Species and methods', 'Bird, mammal, reptile, fisheries, disease, movement, habitat, and population specialties can produce very different workdays.']
      ],
      settings: ['Parks, refuges, forests, wetlands, and other field sites', 'Government wildlife agencies', 'Universities and research projects', 'Environmental consulting and conservation organizations'],
      realities: ['Entry work may be seasonal, geographically mobile, and physically demanding.', 'Early mornings, nights, weather, insects, and difficult terrain may be part of some projects.', 'Federal wildlife-biologist positions have specific college-course requirements.', 'Many professional roles combine field experience with substantial analysis and reporting.'],
      careers: ['Wildlife technician / biological science technician', 'Wildlife biologist', 'Movement / spatial ecologist', 'Wildlife disease / ecophysiology specialist', 'Natural-resource agency biologist', 'Post-release monitoring biologist'],
      programCodes: ['ME-WE', 'UMA-WEC', 'URI-W', 'URI-WZ', 'ME-ZOO'],
      related: ['ecology', 'wildlife-conservation', 'animal-behavior', 'wildlife-rehabilitation'],
      references: [
        ['BLS: Zoologists and Wildlife Biologists', 'Occupational overview', 'https://www.bls.gov/ooh/life-physical-and-social-science/zoologists-and-wildlife-biologists.htm'],
        ['OPM Wildlife Biology Series 0486', 'Federal qualification standard', 'https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/wildlife-biology-series-0486/'],
        ['The Wildlife Society: Career paths', 'Professional field guide', 'https://wildlife.org/paths-to-becoming-a-wildlifer/'],
        ['Texas A&M Wildlife Job Board', 'Current field opportunities', 'https://jobs.rwfm.tamu.edu/']
      ]
    },
    {
      id: 'wildlife-conservation', group: 'wild', title: 'Wildlife Conservation',
      short: 'Applying science, management, policy, and collaboration to protect species, populations, and habitats.',
      bigPicture: 'Wildlife conservation uses biological and ecological evidence to decide and carry out actions intended to maintain biodiversity or recover threatened species and habitats. The same professional may conduct both wildlife biology and conservation work.',
      focus: ['Endangered-species recovery', 'Habitat protection and restoration', 'Population and threat management', 'Conservation planning, policy, and implementation'],
      questions: [
        'What action is most likely to help a declining population recover?',
        'Which habitats or ecological connections should receive priority?',
        'How can development, roads, recreation, or conflict be managed?',
        'Should animals be translocated or reintroduced, and how should success be measured?'
      ],
      responsibilities: [
        'Assess species, habitats, threats, and the strength of available evidence.',
        'Design or implement recovery, restoration, monitoring, or conflict-reduction actions.',
        'Coordinate projects involving agencies, landowners, scientists, communities, and funders.',
        'Prepare management plans, environmental documents, grants, budgets, and progress reports.'
      ],
      knowledgeSkills: ['Conservation biology and population ecology', 'Habitat management and restoration', 'Environmental law, policy, and permitting', 'Project planning and program evaluation', 'Communication, negotiation, and stakeholder collaboration'],
      variations: [
        ['Role emphasis', 'A conservation role may emphasize science, land management, policy, community engagement, fundraising, or project delivery.'],
        ['Animal contact', 'Most conservation work affects animals indirectly through populations, habitats, policy, or people.'],
        ['Organization', 'Agency, nonprofit, consulting, zoo, and academic programs differ in authority, pace, funding, and measures of success.'],
        ['Scale', 'Projects range from one local population or habitat parcel to regional, national, or international planning.']
      ],
      settings: ['Government agencies and protected areas', 'Conservation nonprofits and land trusts', 'Consulting firms and restoration projects', 'Zoos, universities, and community partnerships'],
      realities: ['Conservation outcomes depend heavily on people, budgets, land use, law, and politics.', 'Progress can be slow and difficult to measure.', 'The work often includes meetings, planning, documentation, and coordination alongside science.', 'Tradeoffs among species, habitats, communities, and limited resources are common.'],
      careers: ['Conservation delivery / habitat program coordinator', 'Conservation biologist', 'Endangered-species biologist', 'Species recovery biologist', 'Conservation NGO scientist / coordinator', 'Human-wildlife conflict specialist'],
      programCodes: ['ME-WE', 'UMA-WEC', 'URI-W', 'URI-WZ', 'ME-ZOO'],
      related: ['wildlife-biology', 'ecology', 'zoo-aquarium-science', 'marine-biology'],
      references: [
        ['The Wildlife Society: Certifications', 'Professional preparation', 'https://wildlife.org/tws-certifications/'],
        ['O*NET: Conservation Scientists', 'Tasks and skills', 'https://www.onetonline.org/link/summary/19-1031.00'],
        ['UMass: Wildlife Ecology & Conservation', 'Undergraduate example', 'https://www.umass.edu/environmental-conservation/academics/undergraduate-programs/natural-resources-conservation/major/wildlife-ecology-conservation-concentration'],
        ['URI: Wildlife research', 'University research example', 'https://web.uri.edu/nrs/research/wildlife-and-conservation-biology/']
      ]
    },
    {
      id: 'marine-biology', group: 'wild', title: 'Marine Biology',
      short: 'Organisms and biological processes associated with oceans, coasts, estuaries, and marine environments.',
      bigPicture: 'Marine biology is defined mainly by the organisms and environment being studied, not by one scientific method. A marine biologist may specialize in ecology, behavior, physiology, genetics, fisheries, conservation, or animal care.',
      focus: ['Marine ecology and coastal ecosystems', 'Fish, marine mammals, invertebrates, and algae', 'Marine physiology and adaptation', 'Fisheries, ocean change, and conservation'],
      questions: [
        'How do marine animals communicate, migrate, forage, or reproduce?',
        'How do warming, acidification, pollution, or habitat change affect marine life?',
        'How do fishing and other human activities affect populations?',
        'How are marine organisms physiologically adapted to their environments?'
      ],
      responsibilities: [
        'Conduct boat-, shore-, dive-, aquarium-, laboratory-, or sensor-based research.',
        'Identify organisms and collect biological, behavioral, water, or habitat data.',
        'Analyze movement, population, ecological, physiological, or fisheries information.',
        'Maintain equipment, specimens, permits, safety procedures, and technical records.'
      ],
      knowledgeSkills: ['Marine ecology and oceanography', 'Organismal biology and species identification', 'Statistics, GIS, acoustics, or telemetry', 'Laboratory, aquarium, boating, or diving methods', 'Field safety and scientific communication'],
      variations: [
        ['Environment', 'Work may occur on boats, coasts, underwater, in aquariums, laboratories, offices, or entirely through remote data.'],
        ['Specialty', 'Marine mammal behavior, fisheries biology, coral ecology, physiology, conservation, and aquaculture have different methods and career markets.'],
        ['Animal contact', 'Some aquarists provide daily care; many marine researchers observe remotely or work with samples and data.'],
        ['Schedule', 'Tides, weather, research cruises, seasonal migrations, and animal-care schedules can shape the work.']
      ],
      settings: ['Oceans, coasts, estuaries, and research vessels', 'Aquariums and marine laboratories', 'Universities and government science agencies', 'Fisheries, conservation, and environmental consulting'],
      realities: ['A marine subject does not guarantee frequent time at sea or direct animal contact.', 'Boat work, diving, and remote field sites require specialized training and safety practices.', 'Quantitative, laboratory, and writing skills remain central.', 'Independent research roles commonly require graduate education.'],
      careers: [
        { name: 'Marine biologist', focus: 'Studies marine organisms or systems using ecological, physiological, behavioral, genetic, or conservation approaches.', educationBand: 'B.S. entry roles; graduate study common for research leadership', workTags: ['Research', 'Fieldwork', 'Data / statistics'] },
        { name: 'Fisheries biologist', focus: 'Studies and helps manage fish populations, aquatic habitats, harvest, and ecosystem effects.', educationBand: 'B.S.-accessible; graduate study useful for advanced roles', workTags: ['Fieldwork', 'Conservation', 'Data / statistics'] },
        'Aquarist / aquarium animal-care specialist', 'Animal communication researcher', 'Movement / spatial ecologist', 'Ecological research technician'
      ],
      programCodes: ['URI-W', 'URI-WZ', 'ME-ZOO', 'UMA-BIO', 'ME-WE'],
      related: ['ecology', 'wildlife-biology', 'animal-behavior', 'zoo-aquarium-science'],
      references: [
        ['O*NET: Zoologists and Wildlife Biologists', 'Related occupational data', 'https://www.onetonline.org/link/summary/19-1023.00'],
        ['URI: Wildlife research', 'Coastal-state research example', 'https://web.uri.edu/nrs/research/wildlife-and-conservation-biology/'],
        ['URI: Undergraduate research', 'Research opportunities', 'https://web.uri.edu/undergraduate-research/programs-and-funding/'],
        ['AZA Career Center', 'Aquarium and zoo jobs', 'https://www.aza.org/jobs']
      ]
    },
    {
      id: 'animal-behavior', group: 'behavior', title: 'Animal Behavior / Ethology',
      short: 'What animals do, how behavior develops and changes, and why behavioral patterns occur.',
      bigPicture: 'Animal behavior examines actions, communication, learning, social relationships, decision-making, and responses to the environment. It can be studied in wild, companion, farm, laboratory, shelter, or zoo animals.',
      focus: ['Social and reproductive behavior', 'Communication and sensory behavior', 'Learning and behavioral development', 'Foraging, movement, and environmental responses'],
      questions: [
        'Why does an animal choose one social partner, food source, or habitat over another?',
        'How does experience change behavior?',
        'How do animals communicate and interpret signals?',
        'How do social and environmental conditions affect behavior?'
      ],
      responsibilities: [
        'Define behaviors clearly and develop an observation or coding system.',
        'Observe animals directly or from video and record behavior systematically.',
        'Design experiments or compare behavior across individuals, groups, species, or conditions.',
        'Analyze behavioral data and explain conclusions, uncertainty, and practical implications.'
      ],
      knowledgeSkills: ['Ethology, evolution, ecology, and natural history', 'Learning theory and behavioral development', 'Behavioral observation and ethograms', 'Research design and statistics', 'Scientific writing and interpretation'],
      variations: [
        ['Purpose', 'Behavior research may build basic knowledge or support welfare, training, conservation, or management decisions.'],
        ['Setting', 'The work can occur in natural habitats, zoos, farms, shelters, homes, laboratories, or through archived video and datasets.'],
        ['Animal contact', 'Systematic observation may involve little handling; applied training and husbandry may involve frequent direct contact.'],
        ['Career structure', 'Technician and applied roles can be B.S.-accessible, while independent research positions usually require graduate training.']
      ],
      settings: ['Universities and research laboratories', 'Zoos, aquariums, farms, and shelters', 'Wildlife field projects', 'Animal-welfare and training programs'],
      realities: ['Behavioral research can involve long periods of observation, coding, data cleaning, and writing.', 'Interesting animal behavior does not necessarily mean frequent animal handling.', 'Applied roles often require substantial hands-on experience in addition to academic knowledge.', 'Behavioral explanations must separate evidence from assumptions about intention or emotion.'],
      careers: ['Animal behavior research assistant / technician', 'Animal behaviorist / applied animal behavior scientist', 'Behavioral ecologist', 'Animal communication researcher', 'Behavioral husbandry specialist', 'Science-based animal trainer'],
      programCodes: ['UNE-AB', 'UNE-AN', 'UMA-BIO', 'ME-ZOO', 'URI-WZ'],
      related: ['animal-cognition', 'animal-welfare', 'wildlife-biology', 'zoo-aquarium-science'],
      references: [
        ['Animal Behavior Society', 'Professional society and opportunities', 'https://www.animalbehaviorsociety.org/web/news.php'],
        ['Animal Behavior Society: Applied certification', 'Professional pathway', 'https://www.animalbehaviorsociety.org/web/committees-applied-behavior-caab.php'],
        ['UNE: Animal Behavior B.S.', 'Undergraduate example', 'https://www.une.edu/cas/schools/social-behavioral-sciences/programs/bs-animal-behavior'],
        ['O*NET: Animal Trainers', 'Related occupational data', 'https://www.onetonline.org/link/summary/39-2011.00']
      ]
    },
    {
      id: 'animal-cognition', group: 'behavior', title: 'Animal Cognition / Comparative Psychology',
      short: 'How animals perceive, learn, remember, solve problems, make decisions, and process information.',
      bigPicture: 'Animal cognition focuses on the mental and information-processing mechanisms underlying behavior. It is commonly studied within psychology, neuroscience, biology, or animal-behavior programs rather than offered as a separate undergraduate major.',
      focus: ['Learning and memory', 'Perception and attention', 'Problem-solving and decision-making', 'Social cognition and communication'],
      questions: [
        'What information can an animal perceive and remember?',
        'How does an animal solve a novel problem?',
        'Can animals recognize individuals, quantities, signals, or relationships?',
        'How do cognition and decision-making differ across species and environments?'
      ],
      responsibilities: [
        'Design tasks that isolate a specific learning, memory, perception, or decision process.',
        'Train or habituate animals to participate safely and voluntarily in research procedures.',
        'Record choices, response times, behavior, or physiological measures.',
        'Use careful controls and statistical analysis to evaluate competing explanations.'
      ],
      knowledgeSkills: ['Comparative psychology and learning theory', 'Animal behavior, biology, and neuroscience', 'Experimental design and measurement', 'Statistics, programming, and data visualization', 'Patient animal work and precise protocol control'],
      variations: [
        ['Disciplinary home', 'A project may be grounded in psychology, biology, neuroscience, animal behavior, or philosophy of cognition.'],
        ['Species', 'Research can involve primates, birds, dogs, rodents, fish, insects, zoo animals, or many other groups.'],
        ['Method', 'Studies range from controlled laboratory tasks to field experiments, eye tracking, neuroscience, and analysis of spontaneous behavior.'],
        ['Application', 'Cognition work can inform basic science, enrichment, training, welfare assessment, conservation, and human–animal communication.']
      ],
      settings: ['Psychology and biology laboratories', 'Zoos and comparative-cognition research programs', 'Universities and neuroscience centers', 'Field research and companion-animal studies'],
      realities: ['Research questions that sound intuitive can be difficult to test without alternative explanations.', 'Studies may require many sessions, patient shaping, video coding, and small sample sizes.', 'Independent researcher roles normally require a Ph.D.', 'The undergraduate route may be less obvious because relevant work spans several departments.'],
      careers: ['Comparative cognition researcher', 'Animal learning researcher', 'Companion-animal behavior researcher', 'Neuroethologist / neural-behavior researcher', 'Animal behavior research assistant / technician', 'Zoo / aquarium behavioral researcher'],
      programCodes: ['UNE-AN', 'UNE-AB', 'UMA-BIO', 'ME-ZOO', 'URI-AZ'],
      related: ['animal-behavior', 'animal-biology', 'animal-welfare', 'zoo-aquarium-science'],
      references: [
        ['Animal Behavior Society', 'Professional field', 'https://www.animalbehaviorsociety.org/web/news.php'],
        ['UNE: Animal Behavior B.S.', 'Undergraduate example', 'https://www.une.edu/cas/schools/social-behavioral-sciences/programs/bs-animal-behavior'],
        ['UNE: Neuroscience', 'Mechanistic undergraduate option', 'https://www.une.edu/catalog/2025-2026/undergraduate/neuroscience'],
        ['UMass Biology: Jeffrey Podos', 'Faculty research example', 'https://www.umass.edu/biology/about/directory/jeffrey-podos']
      ]
    },
    {
      id: 'animal-welfare', group: 'behavior', title: 'Animal Welfare Science',
      short: 'Scientifically evaluating and improving animals’ physical and psychological wellbeing.',
      bigPicture: 'Animal welfare science asks how animals experience their lives and how that experience can be improved. It combines behavioral, physiological, veterinary, environmental, and management evidence. Ethical values influence decisions, but the scientific measurements are empirical.',
      focus: ['Stress, pain, fear, and health', 'Positive states, choice, and behavioral needs', 'Housing, enrichment, and human–animal interactions', 'Welfare indicators and quality-of-life assessment'],
      questions: [
        'What evidence indicates that an animal is coping well or poorly?',
        'Does enrichment, training, or environmental change improve welfare?',
        'Which housing or management system better supports important behavior?',
        'How should behavioral and physiological indicators be combined?'
      ],
      responsibilities: [
        'Develop and apply behavioral, health, or physiological welfare measures.',
        'Observe animals and evaluate housing, routines, enrichment, handling, or social conditions.',
        'Design studies or program evaluations and analyze outcomes.',
        'Translate findings into practical recommendations, protocols, staff training, or policy.'
      ],
      knowledgeSkills: ['Animal behavior and species-specific needs', 'Physiology, health, and indicators of stress or positive welfare', 'Welfare assessment and research design', 'Statistics and program evaluation', 'Communication across care, veterinary, research, and management teams'],
      variations: [
        ['Species and sector', 'Welfare science includes farm, companion, laboratory, shelter, working, zoo, aquarium, and sometimes wild animals.'],
        ['Work balance', 'Roles may emphasize research, direct assessment, program coordination, policy, auditing, training, or animal care.'],
        ['Animal contact', 'Some specialists work regularly around animals; others analyze data, develop standards, or advise organizations.'],
        ['Education', 'Applied coordinator roles may be experience-driven, while welfare-scientist positions commonly require graduate study.']
      ],
      settings: ['Zoos, aquariums, shelters, farms, and laboratories', 'Universities and research institutes', 'Animal-welfare organizations and certifiers', 'Government, consulting, and industry programs'],
      realities: ['Welfare conclusions may require balancing imperfect behavioral, health, and physiological indicators.', 'Some work involves distress, poor conditions, difficult decisions, or euthanasia.', 'Changing practice requires communication and institutional cooperation, not evidence alone.', 'Daily work may contain more documentation, staff consultation, and analysis than animal handling.'],
      careers: ['Animal welfare scientist', 'Animal welfare / behavior coordinator', 'Zoo / aquarium welfare specialist', 'Shelter behavior specialist / coordinator', 'Enrichment coordinator / specialist', 'Behavioral husbandry specialist'],
      programCodes: ['UNE-AB', 'UNE-AN', 'URI-AZ', 'URI-WZ', 'UMA-AS'],
      related: ['animal-behavior', 'zoo-aquarium-science', 'animal-science', 'veterinary-science'],
      references: [
        ['Animal Behavior Society: Applied certification', 'Professional pathway', 'https://www.animalbehaviorsociety.org/web/committees-applied-behavior-caab.php'],
        ['URI: Zoo & Aquarium Science certificate', 'Undergraduate example', 'https://web.uri.edu/favs/academics/zoo-and-aquarium-science-certificate/'],
        ['UNE: Animal Behavior B.S.', 'Undergraduate example', 'https://www.une.edu/cas/schools/social-behavioral-sciences/programs/bs-animal-behavior'],
        ['O*NET: Animal Caretakers', 'Related occupational data', 'https://www.onetonline.org/link/summary/39-2021.00']
      ]
    },
    {
      id: 'animal-science', group: 'managed', title: 'Animal Science',
      short: 'The biology, care, management, and use of domesticated animals, traditionally with an agricultural emphasis.',
      bigPicture: 'Animal science combines biological science with management of domesticated animals. Programs differ considerably: some emphasize livestock production, while others provide meaningful options in companion animals, equine science, behavior, welfare, nutrition, or pre-veterinary preparation.',
      focus: ['Nutrition, physiology, and health', 'Genetics, breeding, and reproduction', 'Husbandry and production systems', 'Behavior, welfare, and animal management'],
      questions: [
        'What nutrition best supports animal health, growth, or performance?',
        'How do genetics and breeding influence traits and health?',
        'How do housing, handling, or management affect welfare and behavior?',
        'How can reproductive, production, or health outcomes be managed responsibly?'
      ],
      responsibilities: [
        'Provide or supervise feeding, handling, husbandry, health observation, and recordkeeping.',
        'Collect and analyze nutrition, reproduction, growth, health, behavior, or welfare data.',
        'Implement management, breeding, research, or quality-assurance protocols.',
        'Communicate with veterinarians, producers, researchers, caregivers, and regulatory personnel.'
      ],
      knowledgeSkills: ['Anatomy, physiology, nutrition, and reproduction', 'Genetics, microbiology, and animal health', 'Husbandry, handling, and welfare', 'Statistics and experimental methods', 'Management, records, biosecurity, and communication'],
      variations: [
        ['Species', 'Programs may concentrate on livestock, horses, companion animals, laboratory animals, or a broader combination.'],
        ['Purpose', 'Careers can involve hands-on management, research, industry, welfare, nutrition, breeding, extension, or veterinary preparation.'],
        ['Curriculum', 'Two programs with the same title may allocate very different amounts of coursework to agriculture, health science, behavior, or exotic animals.'],
        ['Animal contact', 'Farm and management roles may be hands-on; laboratory, nutrition, genetics, and industry roles may be less so.']
      ],
      settings: ['Farms, equine facilities, kennels, and animal-care operations', 'Universities and research laboratories', 'Feed, genetics, pharmaceutical, and agricultural organizations', 'Zoos, shelters, veterinary, and companion-animal programs'],
      realities: ['Agricultural and livestock coursework is central in many programs.', 'Hands-on animal work can be physical, scheduled around animal needs, and subject to biosecurity rules.', 'Pre-veterinary preparation is not the same thing as a veterinary degree or guaranteed admission.', 'Program details matter more than the major title when behavior, welfare, or zoo work is the goal.'],
      careers: [
        { name: 'Animal scientist', focus: 'Studies nutrition, genetics, reproduction, physiology, management, or welfare in domesticated animals.', educationBand: 'Graduate study common for scientist roles', workTags: ['Research', 'Data / statistics', 'Animal care'] },
        'Animal welfare / behavior coordinator', 'Service-dog / assistance-animal trainer', 'Animal collection / management specialist', 'Zoo animal nutritionist / nutrition coordinator', 'University / laboratory research assistant'
      ],
      programCodes: ['UMA-AS', 'URI-AZ', 'UNE-AB', 'UMA-BIO'],
      related: ['animal-welfare', 'zoo-aquarium-science', 'veterinary-science', 'animal-biology'],
      references: [
        ['O*NET: Animal Scientists', 'Tasks and skills', 'https://www.onetonline.org/link/summary/19-1011.00'],
        ['UMass Amherst: Animal Science', 'Undergraduate example', 'https://www.umass.edu/veterinary-animal-sciences/animal-science-major'],
        ['UMass: Animal Management concentration', 'Undergraduate example', 'https://www.umass.edu/veterinary-animal-sciences/animal-science-major/animal-management-concentration'],
        ['URI: Animal Science option', 'Undergraduate example', 'https://web.uri.edu/favs/academics/animal-and-veterinary-science-b-s/animal-science-option/']
      ]
    },
    {
      id: 'zoo-aquarium-science', group: 'managed', title: 'Zoo & Aquarium Science / Captive Wildlife Management',
      short: 'The care, behavior, welfare, management, and conservation of wild animals living under human care.',
      bigPicture: 'This area sits at the intersection of husbandry, behavior, welfare, animal health, conservation breeding, education, and facility operations. Direct care is one part of a much wider managed-animal system.',
      focus: ['Daily husbandry and animal health observation', 'Enrichment, training, and behavioral management', 'Welfare assessment and habitat design', 'Conservation breeding and population management'],
      questions: [
        'What care and environment support species-appropriate behavior and good welfare?',
        'How should social groups, feeding, enrichment, and training be structured?',
        'How can animals voluntarily participate in veterinary procedures?',
        'How can managed populations contribute responsibly to conservation?'
      ],
      responsibilities: [
        'Prepare diets, clean habitats, inspect facilities, observe animals, and maintain detailed records.',
        'Plan enrichment or training and evaluate behavioral and welfare outcomes.',
        'Support veterinary care, transport, breeding, introductions, and safety procedures.',
        'Contribute to conservation, research, education, population planning, or program coordination.'
      ],
      knowledgeSkills: ['Species biology, natural history, and husbandry', 'Behavior, learning, enrichment, and welfare', 'Nutrition, health observation, and biosecurity', 'Safe handling, facilities, and emergency procedures', 'Recordkeeping, teamwork, and public communication'],
      variations: [
        ['Department', 'Keeper, aquarist, training, welfare, nutrition, research, population management, education, and curatorial roles differ greatly.'],
        ['Animal contact', 'Care staff work closely with animals; researchers, planners, educators, and managers may have much less direct contact.'],
        ['Taxa and facility', 'Aquarium systems, bird programs, large mammals, reptiles, ambassador animals, sanctuaries, and conservation centers require different expertise.'],
        ['Career stage', 'Early roles are often physical and routine-intensive; later roles may shift toward planning, supervision, coordination, or specialization.']
      ],
      settings: ['Zoos, aquariums, sanctuaries, and conservation centers', 'Breeding and population-management programs', 'Animal hospitals and nutrition facilities', 'Education, research, and administrative departments'],
      realities: ['Animal-care schedules commonly include early mornings, weekends, holidays, cleaning, and outdoor work.', 'Jobs are competitive, and substantial volunteer, internship, or paid animal-care experience is often expected.', 'Emotional demands can include illness, aging animals, transfers, safety risks, and euthanasia.', 'Some specialized roles require graduate education or years of operational experience.'],
      careers: ['Zookeeper / animal-care specialist', 'Aquarist / aquarium animal-care specialist', 'Zoo behavioral-husbandry specialist', 'Zoo / aquarium welfare specialist', 'Conservation-breeding technician', 'Population biologist / zoo population management scientist', 'Zoo animal curator', 'Zoo research coordinator'],
      programCodes: ['URI-AZ', 'URI-WZ', 'UNE-AB', 'UNE-AN', 'UMA-AS'],
      related: ['animal-welfare', 'animal-behavior', 'animal-science', 'wildlife-conservation'],
      references: [
        ['AZA Career Center', 'Zoo and aquarium job examples', 'https://www.aza.org/jobs'],
        ['URI: Zoo & Aquarium Science certificate', 'Undergraduate example', 'https://web.uri.edu/favs/academics/zoo-and-aquarium-science-certificate/'],
        ['O*NET: Animal Caretakers', 'Related occupational data', 'https://www.onetonline.org/link/summary/39-2021.00'],
        ['O*NET: Animal Trainers', 'Related occupational data', 'https://www.onetonline.org/link/summary/39-2011.00']
      ]
    },
    {
      id: 'veterinary-science', group: 'health', title: 'Animal Health / Veterinary Science',
      short: 'Preventing, diagnosing, and treating animal disease, injury, pain, and other health problems.',
      bigPicture: 'Animal health work focuses on disease prevention, diagnosis, treatment, recovery, and population health. Veterinary medicine requires professional education, but many undergraduate majors can provide the prerequisites and scientific foundation.',
      focus: ['Anatomy, physiology, pathology, and disease', 'Diagnosis, treatment, surgery, and pain management', 'Preventive medicine, nutrition, and epidemiology', 'Clinical care, population health, and biosecurity'],
      questions: [
        'What is causing an animal’s illness, injury, pain, or change in function?',
        'Which diagnostic evidence is needed to choose a treatment?',
        'How can disease or injury be prevented?',
        'How do diseases spread among animals, people, or environments?'
      ],
      responsibilities: [
        'Examine animals, gather histories, collect samples, and interpret diagnostic information.',
        'Provide or assist with treatment, medication, surgery, nursing care, or rehabilitation.',
        'Maintain medical records, infection-control procedures, equipment, and legal documentation.',
        'Communicate risks, options, prognosis, welfare considerations, and care instructions.'
      ],
      knowledgeSkills: ['Anatomy, physiology, pathology, and pharmacology', 'Microbiology, immunology, and epidemiology', 'Clinical observation and diagnostic reasoning', 'Technical procedures, hygiene, and biosecurity', 'Communication, teamwork, ethics, and decision-making'],
      variations: [
        ['Professional role', 'Veterinarians, veterinary technicians, assistants, pathologists, epidemiologists, nutritionists, and researchers have different education and duties.'],
        ['Species', 'Companion, farm, equine, laboratory, zoo, wildlife, aquatic, and public-health work require different knowledge and settings.'],
        ['Clinical contact', 'Some roles provide continuous patient care; others focus on diagnostics, pathology, population health, research, or regulation.'],
        ['Work context', 'Private practice, shelters, government, universities, industry, zoos, and field programs differ in resources and decisions.']
      ],
      settings: ['Veterinary hospitals and clinics', 'Shelters, farms, zoos, aquariums, and rehabilitation centers', 'Diagnostic laboratories and universities', 'Government, public-health, research, and industry programs'],
      realities: ['Veterinary school is competitive, lengthy, and potentially expensive.', 'Clinical work can include emergencies, bodily fluids, injury, distress, euthanasia, and difficult client conversations.', 'Schedules vary from regular laboratory hours to nights, weekends, and on-call coverage.', 'Strong science preparation must be paired with clinical judgment, technical skill, and communication.'],
      careers: [
        { name: 'Veterinarian', focus: 'Diagnoses, treats, and prevents disease and injury and advises on animal health and welfare.', educationBand: 'Doctor of Veterinary Medicine and licensure required', workTags: ['Animal care', 'Research', 'Education / public'] },
        { name: 'Veterinary technician', focus: 'Provides nursing, diagnostic, laboratory, anesthesia, and treatment support under veterinary supervision.', educationBand: 'Accredited veterinary-technology education and credentialing typically required', workTags: ['Animal care', 'Laboratory'] },
        'Wildlife disease / ecophysiology specialist', 'Animal physiologist', 'Zoo animal nutritionist / nutrition coordinator', 'Wildlife rehabilitator'
      ],
      programCodes: ['UMA-AS', 'URI-AZ', 'UMA-BIO', 'ME-ZOO', 'UNE-AN'],
      related: ['animal-biology', 'animal-science', 'animal-welfare', 'wildlife-rehabilitation'],
      references: [
        ['BLS: Veterinarians', 'Occupational overview', 'https://www.bls.gov/ooh/healthcare/veterinarians.htm'],
        ['UMass Amherst: Animal Science', 'Undergraduate preparation example', 'https://www.umass.edu/veterinary-animal-sciences/animal-science-major'],
        ['URI: Animal Science option', 'Undergraduate preparation example', 'https://web.uri.edu/favs/academics/animal-and-veterinary-science-b-s/animal-science-option/'],
        ['O*NET: Biological Technicians', 'Related laboratory work', 'https://www.onetonline.org/link/summary/19-4021.00']
      ]
    },
    {
      id: 'wildlife-rehabilitation', group: 'health', title: 'Wildlife Rehabilitation',
      short: 'Temporary care and treatment of injured, sick, displaced, or orphaned wild animals with release as the goal when possible.',
      bigPicture: 'Wildlife rehabilitation combines individual-animal care, species-specific husbandry, health support, behavioral preparation, legal requirements, and release assessment. It differs from population-focused wildlife biology, although rehabilitation organizations may contribute to research and conservation.',
      focus: ['Emergency stabilization and supportive care', 'Species-specific nutrition and husbandry', 'Preventing habituation and preserving wild behavior', 'Conditioning, release decisions, and post-release learning'],
      questions: [
        'Can this animal recover sufficiently to survive independently?',
        'What care does an orphan require without becoming habituated to people?',
        'Can the animal fly, hunt, forage, navigate, or behave normally enough for release?',
        'When, where, and under what conditions should release occur?'
      ],
      responsibilities: [
        'Intake and assess animals, provide stabilization, and follow veterinary or rehabilitation plans.',
        'Prepare diets, feed, clean, medicate, maintain enclosures, and document progress.',
        'Minimize stress and habituation while evaluating behavior and physical function.',
        'Coordinate permits, release sites, volunteers, transport, public calls, and sometimes post-release monitoring.'
      ],
      knowledgeSkills: ['Species identification, natural history, and behavior', 'Nutrition, husbandry, basic health, and biosecurity', 'Safe handling, restraint, and enclosure management', 'Behavioral and physical release assessment', 'Recordkeeping, permits, volunteer coordination, and public communication'],
      variations: [
        ['Facility', 'Large hospitals, small nonprofit centers, home-based permittees, and species-specialty programs have different staffing and resources.'],
        ['Role', 'Animal-care, veterinary, education, volunteer-coordination, operations, research, and release-monitoring work can coexist.'],
        ['Species', 'Birds, mammals, reptiles, marine wildlife, and large animals require different facilities, permits, and expertise.'],
        ['Season', 'Caseload, hours, species, and staffing can change dramatically during nesting, migration, weather events, or disease outbreaks.']
      ],
      settings: ['Wildlife rehabilitation centers and hospitals', 'Veterinary and diagnostic facilities', 'Home-based or species-specialty programs', 'Release sites and post-release field projects'],
      realities: ['The work is physically demanding and includes extensive feeding, cleaning, laundry, and sanitation.', 'High caseloads, limited resources, irregular hours, and unpaid or low-paid entry experiences are common.', 'Not every animal can be released; suffering, mortality, and euthanasia are part of the work.', 'Permits define what activities are legal, and requirements vary by species and jurisdiction.'],
      careers: ['Wildlife rehabilitator', 'Wildlife rehabilitation / release coordinator', 'Wildlife rehabilitation program manager', 'Reintroduction / release field technician', 'Post-release monitoring biologist', 'Wildlife disease / ecophysiology specialist'],
      programCodes: ['ME-WE', 'URI-WZ', 'URI-W', 'UNE-AB', 'ME-ZOO'],
      related: ['veterinary-science', 'wildlife-biology', 'animal-welfare', 'wildlife-conservation'],
      references: [
        ['National Wildlife Rehabilitators Association', 'Professional network and opportunities', 'https://www.nwrawildlife.org/networking/'],
        ['U.S. Fish & Wildlife Service: Migratory bird rehabilitation', 'Federal permit guidance', 'https://www.fws.gov/service/3-200-10b-migratory-bird-rehabilitation'],
        ['Texas A&M Wildlife Job Board', 'Current field opportunities', 'https://jobs.rwfm.tamu.edu/'],
        ['O*NET: Animal Caretakers', 'Related occupational data', 'https://www.onetonline.org/link/summary/39-2021.00']
      ]
    }
  ];

  const curatedDetails = {
    'wildlife-rehabilitation': { topics: [
      { explanation: 'The first priority is to identify immediate threats to life and reduce pain, shock, dehydration, breathing difficulty, or heat loss. A rehabilitator works within legal and clinical limits and involves a veterinarian when diagnosis, surgery, prescription medication, or advanced treatment is needed.', examples: [
        ['Intake example', 'A window-strike bird may need a quiet, dark holding space and evaluation for head or eye trauma before anyone can judge whether release is appropriate.'],
        ['Supportive-care example', 'An orphaned mammal may need careful warming and fluid support before feeding; giving food too early or using the wrong technique can cause additional harm.'],
        ['What gets documented', 'Time and location found, body condition, weight, temperature, injuries, behavior, initial care, and changes after treatment.']
      ], referenceIndex: 0 },
      { explanation: 'Nutrition and housing have to match the species, age, medical condition, and stage of rehabilitation. The goal is not simply to keep an animal fed—it is to support normal growth, movement, digestion, feather or coat condition, and behavior without creating preventable disease.', examples: [
        ['Diet example', 'An insect-eating songbird, a raptor, and a young rabbit have different nutrient needs, feeding schedules, and safe feeding methods.'],
        ['Housing example', 'Temperature, humidity, substrates, perches, water access, hiding places, and enclosure size change as an animal stabilizes and becomes more active.'],
        ['Daily evidence', 'Food intake, feces, hydration, weight trend, mobility, and response to the enclosure help determine whether the care plan is working.']
      ], referenceIndex: 0 },
      { explanation: 'A healthy wild animal also needs species-appropriate behavior. Care is arranged to limit unnecessary exposure to people, pets, household sounds, and predictable human rewards, especially during sensitive developmental periods.', examples: [
        ['Care practice', 'Staff may use visual barriers, quiet routines, remote feeding, or conspecific housing so an animal does not associate people with comfort or food.'],
        ['Behavioral sign', 'Appropriate avoidance of people, normal social behavior, foraging, predator awareness, and species-typical movement can matter as much as a healed injury.'],
        ['Why it matters', 'An animal that approaches people or lacks survival behavior may be physically healthy but still unsafe to release.']
      ], referenceIndex: 1 },
      { explanation: 'Recovery has to be translated into the functions an animal will need in the wild. Release decisions combine health, behavior, weather, season, habitat, food availability, legal requirements, and sometimes what can be learned after release.', examples: [
        ['Conditioning example', 'A bird may progress to a flight enclosure where endurance, maneuvering, landing, and feather condition can be observed.'],
        ['Release decision', 'The team considers whether the animal can obtain food, avoid danger, move normally, and return to suitable habitat at an appropriate time.'],
        ['Post-release learning', 'Bands, tags, radio transmitters, sightings, or recapture records can reveal survival, movement, and whether rehabilitation methods need improvement.']
      ], referenceIndex: 1 }
    ] }
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

  function groupFor(area) { return groups.find(group => group.id === area.group); }
  function areaById(id) { return areas.find(area => area.id === id); }
  function programByCode(code) { return D.programs.find(program => program.code === code); }
  function careerByName(name) { return D.careers.find(career => career.name === name); }
  function aspectKey(areaId, kind, index) { return `${areaId}::${kind}::${index}`; }
  function reactionFor(key) { return state.reactions[key] || ''; }

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
            <div class="eyebrow">13 overlapping fields and work areas</div>
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
    renderAreaGroups(q);
    document.getElementById('areaSearch').addEventListener('input', event => renderAreaGroups(event.target.value.trim().toLowerCase()));
  }

  function renderAreaGroups(q) {
    const root = document.getElementById('areaGroups');
    root.innerHTML = groups.map(group => {
      const matches = areas.filter(arealabs => {
        if (arealabs.group !== group.id) return false;
        const blob = [arealabs.title, arealabs.short, arealabs.bigPicture, ...arealabs.focus, ...arealabs.knowledgeSkills].join(' ').toLowerCase();
        return !q || blob.includes(q);
      });
      if (!matches.length) return '';
      return `<section class="group" style="--group-color:${group.color}">
        <div class="group-heading"><span class="group-line" aria-hidden="true"></span><div><h2>${esc(group.title)}</h2><p>${esc(group.description)}</p></div></div>
        <div class="area-grid">${matches.map((area, index) => areaCard(area, index)).join('')}</div>
      </section>`;
    }).join('') || '<div class="empty">No areas match that search.</div>';
  }

  function areaCard(area, index) {
    const group = groupFor(area);
    const saved = state.savedAreas.includes(area.id);
    return `<article class="area-card" style="--group-color:${group.color}">
      <span class="area-number">${String(index + 1).padStart(2, '0')} · ${esc(group.title)}</span>
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

  function itemText(item) { return Array.isArray(item) ? item.join(': ') : item; }
  function referenceFor(area, kind, index, preferredIndex) {
    if (!area.references.length) return null;
    const offsets = { topics: 0, questions: 1, activities: 0, skills: 2, settings: 1, realities: 1 };
    const selectedIndex = preferredIndex == null ? (index + (offsets[kind] || 0)) % area.references.length : preferredIndex;
    return area.references[selectedIndex % area.references.length];
  }
  function detailFor(area, kind, item, index) {
    const curated = curatedDetails[area.id]?.[kind]?.[index];
    if (curated) return { ...curated, reference: referenceFor(area, kind, index, curated.referenceIndex) };
    const responsibility = area.responsibilities[index % area.responsibilities.length];
    const question = area.questions[index % area.questions.length];
    const skill = area.knowledgeSkills[index % area.knowledgeSkills.length];
    const setting = area.settings[index % area.settings.length];
    const variation = area.variations[index % area.variations.length];
    const career = area.careers[index % area.careers.length];
    const careerName = typeof career === 'object' ? career.name : career;
    const text = itemText(item);
    const details = {
      topics: { explanation: `${text} is one lens within ${area.title}, not a requirement of every position. It can become a specialty, combine with other parts of the field, or appear only in certain projects or seasons.`, examples: [['A question it can raise', question], ['How it may appear in the work', responsibility], ['Useful preparation', skill]] },
      questions: { explanation: 'This kind of question is usually answered by combining observations or measurements with knowledge of the animal, its environment, and the limits of the available evidence. Different roles may investigate it experimentally, through field monitoring, during care, or by analyzing existing records.', examples: [['One relevant activity', responsibility], ['Knowledge or skill used', skill], ['A possible work context', setting]] },
      activities: { explanation: `This responsibility can be a central duty in one ${area.title} role and a small part of another. The tools, level of independence, animal contact, and decision-making authority change with training, employer, and project purpose.`, examples: [['Knowledge that supports it', skill], ['Where it may happen', setting], ['A related career example', careerName]] },
      skills: { explanation: 'This knowledge or skill becomes useful when it helps someone collect reliable evidence, care for animals safely, make a defensible decision, or communicate work to others. Introductory exposure and professional mastery are very different levels of preparation.', examples: [['Applied to', responsibility], ['Helps investigate', question], ['One setting for practice', setting]] },
      settings: { explanation: 'Jobs in this setting can differ in mission, pace, staffing, resources, and contact with animals. The setting alone does not determine the work: a researcher, technician, educator, manager, or care specialist may experience the same organization very differently.', examples: [['Work that may occur here', responsibility], ['A skill that may matter', skill], ['Role example', careerName]] },
      realities: { explanation: 'This is worth investigating before committing to a path because it can affect daily routine, training, job availability, schedule, emotional load, or working conditions. Its importance varies substantially among employers and roles.', examples: [['A dimension to compare', `${variation[0]} — ${variation[1]}`], ['A related responsibility', responsibility], ['A setting to ask about', setting]] }
    };
    return { ...details[kind], reference: referenceFor(area, kind, index) };
  }
  function drillCard(area, kind, item, index) {
    const text = itemText(item);
    const key = aspectKey(area.id, kind, index);
    const detail = detailFor(area, kind, item, index);
    const reference = detail.reference;
    return `<details class="drill-card"><summary><span class="drill-number">${String(index + 1).padStart(2, '0')}</span><span class="drill-title">${esc(text)}</span><span class="drill-cue">Details &amp; examples</span></summary>
      <div class="drill-content"><p class="drill-explanation">${esc(detail.explanation)}</p>
        <div class="example-list">${detail.examples.map(example => `<div class="example-item"><strong>${esc(example[0])}</strong><span>${esc(example[1])}</span></div>`).join('')}</div>
        <div class="drill-footer">${reference ? `<a class="source-link" href="${esc(reference[2])}" target="_blank" rel="noopener"><span>${esc(reference[1])}</span>${esc(reference[0])} ↗</a>` : '<span></span>'}${reactionButtons(key)}</div>
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
    const group = groupFor(area);
    const saved = state.savedAreas.includes(area.id);
    const programs = area.programCodes.map(programByCode).filter(Boolean);
    app.innerHTML = `<div class="page">
      <div class="detail-shell">
        ${areaNavigation(area.id)}
        <div class="detail-main" style="--group-color:${group.color}">
          <a class="back" href="#areas">← All areas</a>
          <section class="detail-hero">
            <div class="eyebrow">${esc(group.title)}</div>
            <h1>${esc(area.title)}</h1>
            <p class="lead">${esc(area.bigPicture)}</p>
            <div class="hero-actions"><button id="saveArea" class="btn ${saved ? 'saved' : ''}" type="button">${saved ? 'Saved area' : 'Save area'}</button></div>
          </section>
          <nav class="section-jump" aria-label="On this page"><strong>On this page</strong><a href="#topics">Focus</a><a href="#questions">Questions</a><a href="#activities">Work</a><a href="#skills">Skills</a><a href="#settings">Settings</a><a href="#realities">Realities</a><a href="#careers">Careers</a><a href="#programs">College paths</a><a href="#references">Sources</a></nav>

          ${aspectSection(area, 'topics', 'What this area commonly focuses on', 'These are important parts of the field, but not every role emphasizes all of them.', area.focus, 'Topics')}
          ${aspectSection(area, 'questions', 'Questions people may investigate', 'The questions can be scientific, clinical, operational, or management-oriented depending on the role.', area.questions, 'Questions')}
          ${aspectSection(area, 'activities', 'Responsibilities and activities', 'These examples describe work that occurs somewhere within the area; they are not a checklist for every job.', area.responsibilities, 'Work')}

          <section class="content-section" id="variety">
            <div class="section-head"><div><h2>How work within this area varies</h2><p>The same field can produce very different workdays, settings, and relationships with animals.</p></div><span class="section-tag">Range</span></div>
            <div class="variation-grid">${area.variations.map(item => `<div class="info-box variation"><h3>${esc(item[0])}</h3><p>${esc(item[1])}</p></div>`).join('')}</div>
          </section>

          ${aspectSection(area, 'skills', 'Knowledge and skills', 'These can be developed through coursework, research, employment, internships, volunteering, and practice.', area.knowledgeSkills, 'Preparation')}
          ${aspectSection(area, 'settings', 'Work settings', 'Organizations and individual positions vary, even when they use the same field name.', area.settings, 'Environment')}
          ${aspectSection(area, 'realities', 'Practical realities', 'These are common enough to consider, but their intensity differs across employers and roles.', area.realities, 'Conditions')}

          <section class="content-section" id="careers">
            <div class="section-head"><div><h2>Related careers</h2><p>Examples from the broader career database, plus a small number of important area examples. They are not an exhaustive list.</p></div><span class="section-tag">${area.careers.length} examples</span></div>
            <div class="career-grid">${area.careers.map(careerCard).join('')}</div>
            <p><a class="btn text" href="index.html#careers">Browse all 93 researched roles →</a></p>
          </section>

          <section class="content-section" id="programs">
            <div class="section-head"><div><h2>Undergraduate paths to examine</h2><p>These researched paths provide different combinations of breadth, specialization, experience, and preparation. Their inclusion does not mean they are the only routes into the area.</p></div><span class="section-tag">College</span></div>
            <div class="program-grid">${programs.map(program => `<article class="program-card"><span class="school">${esc(program.school)}</span><h3>${esc(program.code)} · ${esc(program.title)}</h3><p>${esc(program.fundamental)}</p><div class="pill-row">${(program.experienceTags || []).slice(0, 5).map(tag => `<span class="pill">${esc(tag)}</span>`).join('')}</div></article>`).join('')}</div>
            <p><a class="btn text" href="index.html#programs">Compare all researched college paths →</a></p>
          </section>

          <section class="content-section" id="related">
            <div class="section-head"><div><h2>Related and overlapping areas</h2><p>Many careers combine more than one field.</p></div><span class="section-tag">Connections</span></div>
            <div class="pill-row">${area.related.map(relatedId => { const related = areaById(relatedId); return `<a class="btn small" href="#area/${related.id}">${esc(related.title)}</a>`; }).join('')}</div>
          </section>

          <section class="content-section" id="references">
            <div class="section-head"><div><h2>Learn more from field and program sources</h2><p>Professional organizations, occupational references, qualification standards, job boards, and official university pages from the project research.</p></div><span class="section-tag">Sources</span></div>
            <div class="reference-grid">${area.references.map(reference => `<article class="reference-card"><span class="source-type">${esc(reference[1])}</span><h3>${esc(reference[0])}</h3><a href="${esc(reference[2])}" target="_blank" rel="noopener">Open source ↗</a></article>`).join('')}</div>
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
          if (value) entries.push({ area, kind, text: Array.isArray(item) ? item.join(': ') : item, value });
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

  window.addEventListener('hashchange', route);
  route();
})();
