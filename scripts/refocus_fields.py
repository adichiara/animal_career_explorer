#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PRIMARY_IDS = [
    "animal-biology",
    "zoology",
    "wildlife-ecology-management",
    "animal-behavior",
    "animal-welfare",
    "animal-science",
    "zoo-aquarium-science",
    "veterinary-technology",
]

STARTER_RESOURCES = {
    "animal-biology": [
        {
            "title": "SICB — Career Information",
            "description": "A broad map of animal biology specialties, including physiology, endocrinology, neurobiology, morphology, evolution, behavior, and comparative biology.",
            "url": "https://sicb.org/resources/career-information/",
        }
    ],
    "zoology": [
        {
            "title": "SICB — Career Information",
            "description": "Explore zoology and comparative-biology specialties and see how modern animal research spans organismal, physiological, evolutionary, and behavioral questions.",
            "url": "https://sicb.org/resources/career-information/",
        }
    ],
    "wildlife-ecology-management": [
        {
            "title": "The Wildlife Society — Professional Development",
            "description": "Student and early-career resources from the professional society that certifies wildlife biologists.",
            "url": "https://wildlife.org/professional-development/",
        }
    ],
    "animal-behavior": [
        {
            "title": "Animal Behavior Society — Applied Animal Behavior",
            "description": "Shows how behavior science is applied to companion, farm, zoo, laboratory, and wild animals to improve care and welfare.",
            "url": "https://www.animalbehaviorsociety.org/web/committees-applied-behavior.php",
        }
    ],
    "animal-welfare": [
        {
            "title": "Lincoln Park Zoo — Animal Welfare Science Program",
            "description": "A concrete look at welfare science using behavioral monitoring, habitat use, hormones, sensors, enrichment, and evidence-based changes to care.",
            "url": "https://www.lpzoo.org/conservation-science/science-centers/animal-welfare-science-program/",
        }
    ],
    "animal-science": [
        {
            "title": "American Society of Animal Science — What Is Animal Science?",
            "description": "A useful introduction to the discipline and its traditional scope. Compare it with each college curriculum because programs vary greatly in agricultural versus companion, welfare, behavior, and managed-animal emphasis.",
            "url": "https://www.asas.org/services/student-resources/what-is-animal-science",
        }
    ],
    "zoo-aquarium-science": [
        {
            "title": "Association of Zoos & Aquariums — Careers in Zoos and Aquariums",
            "description": "An overview of the many professional roles in zoos and aquariums, beyond the single label of zookeeper.",
            "url": "https://www.aza.org/careers_in_zoos_and_aquariums?locale=en",
        }
    ],
    "veterinary-technology": [
        {
            "title": "AVMA — Veterinary Technicians",
            "description": "Introduces veterinary technology as its own credentialed profession and outlines clinical duties and specialty options.",
            "url": "https://ebusiness.avma.org/files/productdownloads/mcm-clientbroch-veterinary-tech-2024.pdf",
        },
        {
            "title": "UMass Amherst — Veterinary Technology Major",
            "description": "A current example of an AVMA-accredited four-year veterinary technology pathway with clinical nursing, diagnostics, anesthesia, surgery, and internships.",
            "url": "https://www.umass.edu/veterinary-animal-sciences/veterinary-technology-major",
        },
    ],
}

FOCUS_MAP = {
    "ME-WE": ["Wildlife Biology"],
    "ME-ZOO": ["Animal Biology", "Zoology"],
    "UMA-BIO": ["Animal Biology"],
    "UNE-AB": ["Animal Behavior", "Animal Welfare Science"],
    "UNE-AN": ["Animal Behavior"],
    "URI-AZ": ["Animal Science (non-ag emphasis)", "Zoo & Aquarium Science / Managed Animal Care", "Animal Welfare Science"],
    "URI-W": ["Wildlife Biology"],
    "URI-WZ": ["Wildlife Biology", "Zoo & Aquarium Science / Managed Animal Care"],
    "CAN-ABEC": ["Animal Behavior", "Animal Welfare Science"],
    "DRAKE-ZCS": ["Animal Behavior", "Zoo & Aquarium Science / Managed Animal Care"],
    "OTT-ZCS": ["Zoo & Aquarium Science / Managed Animal Care", "Animal Welfare Science"],
    "BUCK-ANBE": ["Animal Behavior"],
    "ECK-AS": ["Animal Behavior", "Animal Welfare Science"],
    "UMA-VT": ["Veterinary Technology"],
}

ANIMAL_BIOLOGY = {
    "id": "animal-biology",
    "title": "Animal Biology",
    "short": "How animals function as living organisms, from cells and tissues through physiology, development, reproduction, and whole-body integration.",
    "bigPicture": "Animal biology is a broad way of studying animals as living systems. It can follow a question from genes and cells into tissues, organs, physiology, development, reproduction, behavior, and the whole animal. Programs using this name vary widely, so the curriculum matters more than the label. The field overlaps heavily with zoology; animal biology tends to foreground biological mechanisms and function, while zoology more often foregrounds animal diversity, comparison, and evolutionary relationships.",
    "guideTier": "primary",
    "starterResources": STARTER_RESOURCES["animal-biology"],
    "distinction": {
        "title": "Animal Biology and Zoology",
        "summary": "There is no universal boundary between these names. Many universities could place the same course or research lab under either one.",
        "items": [
            {
                "label": "Animal Biology",
                "description": "Usually emphasizes how animals function: physiology, anatomy, development, reproduction, genetics, and integrated whole-animal biology. Some programs also include behavior and ecology.",
            },
            {
                "label": "Zoology",
                "description": "Usually organizes the curriculum around animals as a diverse group of organisms, with stronger emphasis on comparative anatomy, evolution, systematics, natural history, and animal diversity while still including physiology, behavior, and ecology.",
            },
        ],
    },
    "terms": [
        {"term": "Organismal biology", "definition": "Biology studied at the level of the whole animal and the integration of its body systems."},
        {"term": "Physiology", "definition": "The study of how living systems function, from cells and tissues through organs and whole-body processes."},
        {"term": "Endocrinology", "definition": "The study of hormones and how they regulate growth, reproduction, metabolism, stress, and behavior."},
        {"term": "Developmental biology", "definition": "The study of how an animal grows and changes from embryo through adulthood."},
        {"term": "Comparative biology", "definition": "Using differences and similarities among species to understand biological function, adaptation, and evolution."},
        {"term": "Homeostasis", "definition": "The regulation of internal conditions such as temperature, water balance, and blood chemistry despite external change."},
    ],
    "focus": [
        {
            "title": "Physiology and whole-animal function",
            "description": "Understanding how organ systems work together to support movement, metabolism, thermoregulation, digestion, reproduction, and survival.",
            "source": "SICB — Career Information",
        },
        {"title": "Development and reproduction", "description": "Studying how animals grow, mature, reproduce, and regulate those processes through genes, hormones, nutrition, and environmental conditions."},
        {"title": "Genes, cells, and tissues in animal context", "description": "Connecting molecular and cellular processes to visible traits, health, development, and performance in the whole animal."},
        {
            "title": "Comparative and integrative questions",
            "description": "Comparing species or biological levels to discover which mechanisms are general and which are adaptations to a particular way of life.",
            "source": "SICB — Career Information",
        },
    ],
    "questions": [
        {"question": "How does this animal maintain body temperature, water balance, or energy supply?", "approach": "Measure physiological variables under defined conditions and connect changes in cells, tissues, and organs to whole-animal performance."},
        {"question": "How do hormones affect reproduction, growth, stress, or behavior?", "approach": "Combine hormone measurements, experimental manipulation, and behavioral or physiological outcomes while controlling alternative explanations."},
        {"question": "Why do related species solve the same biological problem differently?", "approach": "Compare anatomy, physiology, genetics, and environmental context across species while accounting for evolutionary relationships."},
        {"question": "How does development change what an animal can do?", "approach": "Track structural, physiological, and behavioral change across life stages and test which mechanisms drive the transition."},
        {"question": "How does a biological mechanism matter outside the laboratory?", "approach": "Connect controlled measurements to health, behavior, environmental tolerance, reproduction, or survival in realistic conditions."},
    ],
    "responsibilities": [
        "Design or assist with laboratory and whole-animal studies.",
        "Measure anatomy, physiology, hormones, metabolism, genetics, development, or behavior.",
        "Analyze biological data and connect findings across levels from cells to the whole animal.",
        "Maintain careful animal-care, research, and laboratory records where live-animal work is involved.",
    ],
    "knowledgeSkills": [
        "Animal anatomy and physiology",
        "Cell biology, genetics, and development",
        "Endocrinology, reproduction, and metabolism",
        "Statistics, experimental design, and scientific writing",
        "Animal handling or laboratory methods when required by the research",
    ],
    "variations": [
        {"label": "Degree names vary", "description": "Animal Biology, Zoology, Organismal Biology, Integrative Biology, and general Biology programs can contain very similar coursework. Read the required courses and faculty research instead of treating the major title as decisive."},
        {"label": "Laboratory to whole animal", "description": "Some researchers work mainly with cells, tissues, or instruments; others measure intact animals in laboratories, field stations, farms, zoos, or wildlife settings."},
        {"label": "Species breadth", "description": "The field can involve model organisms, companion animals, livestock, wildlife, zoo species, fish, insects, or many taxa in comparative studies."},
        {"label": "Where it leads", "description": "Animal biology can support later specialization in behavior, welfare, physiology, veterinary and animal health work, zoology, wildlife biology, or biomedical research."},
    ],
    "settings": [
        "University biology and physiology laboratories",
        "Field stations and organismal research facilities",
        "Zoos, aquariums, animal-care, and veterinary research settings",
        "Government, biomedical, biotechnology, and conservation research organizations",
    ],
    "realities": [
        "The title Animal Biology does not guarantee an animal-heavy curriculum; some programs become molecular quickly, while others remain strongly organismal.",
        "Research careers commonly require graduate study, but bachelor's-level research-assistant and technician roles can provide direct experience.",
        "Hands-on animal contact varies enormously by laboratory and program.",
        "For college comparison, upper-level course availability and faculty research are more informative than the major name.",
    ],
    "careers": [
        "Animal physiologist / comparative physiologist",
        "Animal behavior research assistant / technician",
        "University / laboratory research assistant",
        "Zoologist",
        "Animal welfare scientist / welfare research specialist",
    ],
    "programs": [
        {"code": "ME-ZOO", "school": "University of Maine", "title": "Zoology B.S. with Ecology concentration"},
        {"code": "UMA-BIO", "school": "University of Massachusetts Amherst", "title": "Biology B.S. (ecology and behavior electives)"},
    ],
    "programCodes": ["ME-ZOO", "UMA-BIO"],
    "related": ["zoology", "animal-physiology", "animal-behavior", "animal-welfare"],
    "references": [
        {"title": "SICB — Career Information", "type": "Professional society career overview", "url": "https://sicb.org/resources/career-information/"},
        {"title": "SICB — Divisions", "type": "Professional society field map", "url": "https://sicb.org/divisions/"},
    ],
}

VET_TECH = {
    "id": "veterinary-technology",
    "title": "Veterinary Technology",
    "short": "Hands-on clinical nursing, diagnostics, anesthesia, surgery support, patient monitoring, and animal care as part of the veterinary medical team.",
    "bigPicture": "Veterinary technology is its own credentialed animal-health profession. Veterinary technicians and technologists provide much of the hands-on clinical nursing and technical work that allows a veterinary team to diagnose, treat, anesthetize, monitor, and care for animal patients. The role is not a shorter version of becoming a veterinarian: technicians work within a defined scope, develop their own clinical expertise, and can specialize in areas such as anesthesia, emergency care, behavior, rehabilitation, or zoological medicine.",
    "guideTier": "primary",
    "starterResources": STARTER_RESOURCES["veterinary-technology"],
    "distinction": {
        "title": "Veterinary Technology and Veterinary Medicine",
        "summary": "Both work on the same clinical team, but the education, legal scope, and day-to-day responsibilities are different.",
        "items": [
            {"label": "Veterinary Technology", "description": "Focuses on nursing care, patient monitoring, anesthesia, laboratory procedures, imaging, surgical assistance, husbandry, client communication, and technical execution. Graduates of accredited programs are prepared for credentialing as veterinary technicians or technologists."},
            {"label": "Veterinary Medicine", "description": "Veterinarians diagnose disease, prescribe treatment, perform surgery within their professional scope, and carry legal responsibility for medical decisions. Becoming a veterinarian requires a Doctor of Veterinary Medicine or equivalent professional degree."},
        ],
    },
    "terms": [
        {"term": "Veterinary technician / technologist", "definition": "A credentialed veterinary professional trained in clinical nursing and technical procedures. Titles and legal definitions vary by jurisdiction and degree level."},
        {"term": "VTNE", "definition": "The Veterinary Technician National Examination, used as part of credentialing in the United States and Canada."},
        {"term": "CVTEA", "definition": "The American Veterinary Medical Association committee that accredits veterinary technology education programs."},
        {"term": "Anesthesia monitoring", "definition": "Preparing and monitoring a patient before, during, and after anesthesia, including vital signs, equipment, records, and recovery."},
        {"term": "Diagnostic imaging", "definition": "Producing clinical images such as radiographs using positioning, safety, and technical procedures within the veterinary team."},
        {"term": "Veterinary Technician Specialist", "definition": "An advanced specialty credential earned after professional experience, specialized training, documentation, and examination in a recognized area."},
    ],
    "focus": [
        {"title": "Clinical nursing and patient monitoring", "description": "Assessing patients, carrying out nursing plans, administering permitted treatments, monitoring change, maintaining records, and communicating observations to the veterinarian.", "source": "AVMA — Veterinary Technicians"},
        {"title": "Anesthesia and surgical support", "description": "Preparing patients and equipment, monitoring anesthesia, assisting during procedures, maintaining sterile technique, and supporting recovery.", "source": "AVMA — Veterinary Technicians"},
        {"title": "Diagnostics and laboratory work", "description": "Collecting and handling samples, running laboratory procedures, assisting with imaging, and producing reliable technical information for clinical decisions.", "source": "UMass Amherst — Veterinary Technology Major"},
        {"title": "Handling, behavior, and welfare", "description": "Using safe, low-stress handling, recognizing behavioral and welfare changes, and adapting care to species, temperament, pain, fear, and medical condition."},
        {"title": "Specialized settings", "description": "Technicians can work in general practice, emergency and specialty hospitals, biomedical research, shelters, zoos, aquariums, exotics, and other animal-health settings.", "source": "UMass Amherst — BS in Veterinary Technology"},
    ],
    "questions": [
        {"question": "What does this patient need during the next hour of care?", "approach": "Combine the treatment plan with direct observation, vital signs, pain and behavior cues, fluid and medication schedules, and clear escalation when something changes."},
        {"question": "Is this animal safe for anesthesia and how is it responding?", "approach": "Prepare equipment, establish baseline measures, monitor vital signs continuously, document changes, and communicate promptly with the veterinarian."},
        {"question": "Can this sample or image answer the clinical question reliably?", "approach": "Use correct collection, labeling, positioning, quality-control, and handling procedures so technical error does not become a diagnostic error."},
        {"question": "How can a procedure be completed with less fear and safer handling?", "approach": "Read behavior, use appropriate restraint and cooperative-care techniques, prepare the environment, and adjust the plan to the individual animal."},
        {"question": "Which work setting fits the kind of animals and medicine I want?", "approach": "Compare species, pace, shift patterns, technical responsibilities, credential requirements, and opportunities for specialty training before choosing a pathway."},
    ],
    "responsibilities": [
        "Provide nursing care and monitor animal patients.",
        "Assist with anesthesia, surgery, imaging, laboratory diagnostics, dentistry, and other clinical procedures within legal scope.",
        "Handle and position animals safely while monitoring stress, pain, and behavior.",
        "Maintain medical records, equipment, medications, samples, and infection-control procedures.",
        "Communicate observations and instructions with veterinarians, clients, researchers, and animal-care teams.",
    ],
    "knowledgeSkills": [
        "Animal anatomy, physiology, pharmacology, and disease processes",
        "Clinical nursing, anesthesia, and patient monitoring",
        "Laboratory diagnostics and imaging",
        "Animal handling, behavior, welfare, and husbandry",
        "Medical records, teamwork, client communication, and professional ethics",
    ],
    "variations": [
        {"label": "Degree level", "description": "Accredited programs may award associate or bachelor's degrees. A bachelor's program can add broader science, research, management, or specialty preparation, but credential rules depend on the jurisdiction."},
        {"label": "Practice setting", "description": "General practice, emergency and critical care, specialty hospitals, research, shelter medicine, zoo and wildlife medicine, and exotics can feel like very different careers even though the core profession is the same."},
        {"label": "Species", "description": "Some technicians work mainly with dogs and cats; others build experience with horses, farm animals, laboratory species, birds, reptiles, fish, wildlife, or zoo animals."},
        {"label": "Specialization", "description": "Experienced technicians can pursue advanced specialty credentials in areas including behavior, anesthesia and analgesia, emergency and critical care, rehabilitation, surgery, nutrition, and zoological medicine.", "source": "AVMA — Veterinary Technicians"},
    ],
    "settings": [
        "Companion-animal veterinary hospitals and clinics",
        "Emergency, specialty, and referral hospitals",
        "Zoos, aquariums, exotic-animal, wildlife, and shelter medicine settings",
        "Biomedical research, diagnostic laboratories, and research-animal facilities",
    ],
    "realities": [
        "This is a hands-on medical career with cleaning, restraint, bodily fluids, detailed records, and physical work as well as the more visible clinical procedures.",
        "Schedules can include early mornings, nights, weekends, emergencies, and emotionally difficult cases depending on the setting.",
        "Technicians do not independently practice veterinary medicine; legal scope and credential titles vary by state or jurisdiction.",
        "Zoo, wildlife, and exotic positions are a smaller and more competitive slice of the profession, so broad clinical competence and targeted experience matter.",
        "An accredited program and successful credentialing are central considerations when comparing college pathways.",
    ],
    "careers": [
        "Veterinary technician / technologist",
        "Zoo / wildlife veterinary technician",
        "Emergency and critical care veterinary technician",
        "Laboratory animal veterinary technician",
        "Veterinary technician specialist",
    ],
    "programs": [{"code": "UMA-VT", "school": "University of Massachusetts Amherst", "title": "Veterinary Technology B.S."}],
    "programCodes": ["UMA-VT"],
    "related": ["veterinary-science", "animal-physiology", "animal-welfare", "zoo-aquarium-science"],
    "references": [
        {"title": "AVMA — Veterinary Technicians", "type": "Professional overview", "url": "https://ebusiness.avma.org/files/productdownloads/mcm-clientbroch-veterinary-tech-2024.pdf"},
        {"title": "UMass Amherst — Veterinary Technology Major", "type": "Accredited undergraduate program", "url": "https://www.umass.edu/veterinary-animal-sciences/veterinary-technology-major"},
        {"title": "UMass Amherst — BS in Veterinary Technology", "type": "Program outcomes and settings", "url": "https://www.umass.edu/charles-river/academics/veterinary-technology"},
    ],
}

AREA_ORDER = [
    "animal-biology",
    "zoology",
    "wildlife-ecology-management",
    "animal-behavior",
    "animal-welfare",
    "animal-science",
    "zoo-aquarium-science",
    "veterinary-technology",
    "animal-physiology",
    "animal-cognition",
    "ecology",
    "conservation-biology",
    "veterinary-science",
    "wildlife-health",
    "wildlife-rehabilitation",
    "environmental-education",
    "anthrozoology",
]

UMA_VT_PROGRAM = {
    "code": "UMA-VT",
    "collection": "additional",
    "title": "Veterinary Technology B.S.",
    "school": "University of Massachusetts Amherst",
    "type": "Veterinary technology and clinical animal health",
    "scale": "Public research university · Amherst and Charles River Campus, Newton, Massachusetts",
    "lastVerified": "2026-10-21",
    "overview": "UMass Amherst offers a four-year Bachelor of Science in Veterinary Technology accredited by the American Veterinary Medical Association. Students spend the first two years in Amherst building science and clinical-nursing foundations, then move to the Charles River Campus in Newton for the final two years of specialized clinical work. The program prepares graduates for the Veterinary Technician National Examination and careers as veterinary technologists in veterinary medicine or biomedical research.",
    "fundamental": "A professional bachelor's pathway for students who want hands-on clinical animal care, diagnostics, anesthesia, surgery support, nursing, and technical responsibility as a veterinary technologist.",
    "scienceFoundation": [
        "Biology and general chemistry",
        "Vertebrate anatomy and physiology",
        "Veterinary microbiology and clinical laboratory methods",
        "Pharmacology, parasitology, pathology, and immunology",
        "Statistics, medical mathematics, and evidence-based clinical reasoning",
    ],
    "animalContent": [
        "Veterinary clinical nursing and patient monitoring",
        "Large-animal and small-animal clinical skills",
        "Radiography and diagnostic imaging",
        "Anesthesia, surgery, dentistry, and post-operative care",
        "Animal behavior, husbandry, nutrition, preventive care, and public health",
        "Research-animal management and biomedical-research settings",
    ],
    "experience": "The first two years combine laboratories, classrooms, and farm/animal experience in Amherst. The final two years move to the dedicated Veterinary Technology facility at the Charles River Campus in Newton for advanced clinical training. UMass states that senior students participate in internships at veterinary clinics and research-animal facilities.",
    "research": "The bachelor's curriculum explicitly prepares students for work in biomedical research as well as clinical veterinary medicine. Research-animal management is part of the upper-level curriculum, and the broader UMass research environment can support students who want to connect clinical technique with laboratory or translational work.",
    "progression": [
        "Year 1: begin biology, chemistry, introductory veterinary technology, and clinical nursing.",
        "Year 2: deepen anatomy and physiology, microbiology, large-animal nursing, laboratory skills, and statistics while completing the Amherst phase.",
        "Year 3: move to the Charles River Campus for advanced clinical nursing, pharmacology, imaging, anesthesia, surgery, pathology, parasitology, and specialty-oriented coursework.",
        "Year 4: complete advanced clinical work, internships in veterinary or research-animal settings, and preparation for the Veterinary Technician National Examination.",
    ],
    "resume": "B.S. in Veterinary Technology from an AVMA-accredited program; clinical nursing, anesthesia and surgery support, diagnostic imaging, laboratory methods, anatomy and physiology, pharmacology, microbiology, animal behavior and husbandry, internship experience, and eligibility to pursue veterinary-technician credentialing after the VTNE.",
    "advantages": [
        "One of the clearest direct pathways in the current comparison for hands-on animal health work without making the DVM the default goal.",
        "Combines a full bachelor's science foundation with extensive clinical and technical preparation.",
        "UMass lists career settings that include companion-animal hospitals, farm and equine practice, biotechnology, diagnostic laboratories, zoos, aquariums, exotics, and specialty practice.",
        "The first two years overlap enough with UMass Animal Science and Pre-Veterinary study that early redirection is possible with planning.",
    ],
    "tradeoffs": [
        "Students relocate from Amherst to Newton for the final two years, so the four-year experience is split across two campuses.",
        "This pathway prepares for the veterinary-technician/technologist profession, not independent veterinary practice; students whose goal becomes a DVM should follow the veterinary-school prerequisite route instead.",
        "Zoo, aquarium, wildlife, and exotic positions are specialized and competitive; the degree provides the clinical foundation but does not guarantee those settings.",
    ],
    "bestWhen": "Especially relevant when the student wants substantial direct animal contact and medical skill, likes physiology and health, and is drawn to clinical nursing, diagnostics, anesthesia, surgery support, or eventual zoo/exotic veterinary-technology work.",
    "experienceTags": ["veterinary technology", "animal care", "animal health", "clinical nursing", "laboratory", "anesthesia", "surgery", "research", "zoo/exotics"],
    "competencies": [
        {"id": "comp_clinical_nursing", "name": "Veterinary clinical nursing", "category": "Animal health", "description": "Hands-on patient care, monitoring, treatment support, records, and communication within the veterinary team.", "strength": 3},
        {"id": "comp_anesthesia", "name": "Anesthesia & surgical support", "category": "Animal health", "description": "Patient preparation, anesthetic monitoring, sterile technique, surgical assistance, and recovery care.", "strength": 3},
        {"id": "comp_diagnostics", "name": "Diagnostics & imaging", "category": "Animal health", "description": "Laboratory procedures, sample handling, radiography, imaging support, and quality control.", "strength": 3},
        {"id": "comp_physiology", "name": "Animal physiology", "category": "Biological mechanisms", "description": "Anatomy, organ systems, disease processes, pharmacology, and functional biology.", "strength": 2.8},
        {"id": "comp_husbandry", "name": "Animal handling & husbandry", "category": "Applied animal care", "description": "Safe handling, nursing husbandry, preventive care, nutrition, sanitation, and species-appropriate management.", "strength": 2.8},
        {"id": "comp_behavior_obs", "name": "Behavioral observation", "category": "Behavior & welfare", "description": "Recognizing stress, pain, behavioral change, and handling needs during clinical care.", "strength": 2.4},
        {"id": "comp_research", "name": "Biomedical research support", "category": "Methods", "description": "Research-animal management, laboratory procedures, records, and technical work in biomedical settings.", "strength": 2.3},
    ],
    "sources": [
        "https://www.umass.edu/veterinary-animal-sciences/veterinary-technology-major",
        "https://www.umass.edu/natural-sciences/academics/bs-vet-tech",
        "https://www.umass.edu/charles-river/academics/veterinary-technology",
    ],
}


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)


def dump(path, obj):
    (ROOT / path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def patch_generator():
    path = ROOT / "scripts/areas_build.py"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        ' "URI-WZ": ("University of Rhode Island",\n   "Wildlife & Conservation Biology B.S. + Zoo & Aquarium Science Certificate"),\n}',
        ' "URI-WZ": ("University of Rhode Island",\n   "Wildlife & Conservation Biology B.S. + Zoo & Aquarium Science Certificate"),\n "UMA-VT": ("University of Massachusetts Amherst",\n   "Veterinary Technology B.S."),\n}',
        "add UMA-VT program",
    )

    config = (
        "PRIMARY_AREA_IDS = set(json.loads(r'''"
        + json.dumps(PRIMARY_IDS, ensure_ascii=False)
        + "'''))\nSTARTER_RESOURCES = json.loads(r'''"
        + json.dumps(STARTER_RESOURCES, ensure_ascii=False)
        + "''')\n\n\n"
    )
    text = replace_once(
        text,
        "# ============================================ collector used by the area calls\nREF = {k: v[0] for k, v in REFS.items()}",
        config + "# ============================================ collector used by the area calls\nREF = {k: v[0] for k, v in REFS.items()}",
        "insert priority configuration",
    )

    text = replace_once(
        text,
        'def area(**kw):\n    kw["terms"] = [{"term": t, "definition": d} for t, d in kw["terms"]]',
        'def area(**kw):\n    kw["guideTier"] = "primary" if kw["id"] in PRIMARY_AREA_IDS else "related"\n    kw["starterResources"] = STARTER_RESOURCES.get(kw["id"], [])\n    kw["terms"] = [{"term": t, "definition": d} for t, d in kw["terms"]]',
        "add area metadata",
    )

    text = text.replace("Wildlife Ecology & Management", "Wildlife Biology")
    text = text.replace("wildlife ecology and management", "wildlife biology")
    text = replace_once(text, 'title="Veterinary & Animal Health Sciences",', 'title="Veterinary Medicine & Animal Health",', "rename veterinary guide")
    text = replace_once(text, 'title="Zoo & Aquarium Science",', 'title="Zoo & Aquarium Science / Managed Animal Care",', "rename zoo guide")
    text = replace_once(
        text,
        ' short="The biology, care, management, and use of domesticated animals, traditionally "\n        "with an agricultural emphasis.",',
        ' short="Domesticated-animal biology and management, with this guide emphasizing companion, "\n        "managed-animal, behavior, welfare, and health pathways while keeping the field\'s "\n        "agricultural roots visible.",',
        "retarget animal science short",
    )

    supplemental = json.dumps([ANIMAL_BIOLOGY, VET_TECH], ensure_ascii=False)
    order = json.dumps(AREA_ORDER, ensure_ascii=False)
    insertion = (
        "# Supplemental guides added after the October 2026 field review.\n"
        "AREAS.extend(json.loads(r'''"
        + supplemental
        + "'''))\n"
        "AREA_ORDER = json.loads(r'''"
        + order
        + "''')\n"
        "AREA_RANK = {area_id: index for index, area_id in enumerate(AREA_ORDER)}\n"
        "AREAS.sort(key=lambda item: AREA_RANK[item[\"id\"]])\n\n"
        "# ================================================================ build steps\n"
        'KEY_ORDER = ["id", "title", "short", "bigPicture", "guideTier", "starterResources", "senses", "distinction", "terms",'
    )
    text = replace_once(
        text,
        '# ================================================================ build steps\nKEY_ORDER = ["id", "title", "short", "bigPicture", "senses", "distinction", "terms",',
        insertion,
        "add supplemental guides and key order",
    )
    text = text.replace("Single source of truth for the fifteen field guides.", "Single source of truth for the field guides.")
    path.write_text(text, encoding="utf-8")


def patch_photos():
    path = ROOT / "site/content/areas/photos.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    photos = data["photos"]
    animal = dict(photos["animal-physiology"])
    animal["alt"] = "A labeled anatomical diagram identifies major organs and body systems, illustrating the whole-animal focus of animal biology."
    photos["animal-biology"] = animal
    vt = dict(photos["veterinary-science"])
    vt["alt"] = "Two veterinary professionals examine a cat during hands-on clinical care."
    photos["veterinary-technology"] = vt
    dump("site/content/areas/photos.json", data)


def patch_area_pages():
    base = (ROOT / "site/areas/zoology.html").read_text(encoding="utf-8")
    (ROOT / "site/areas/animal-biology.html").write_text(base.replace('data-area="zoology"', 'data-area="animal-biology"'), encoding="utf-8")
    (ROOT / "site/areas/veterinary-technology.html").write_text(base.replace('data-area="zoology"', 'data-area="veterinary-technology"'), encoding="utf-8")


def patch_area_index_js():
    path = ROOT / "site/areas.js"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "    const matches = areas.filter(area => !q || searchableText(area).includes(q));\n    app.innerHTML = \`<div class=\"index-page\">",
        "    const matches = areas.filter(area => !q || searchableText(area).includes(q));\n"
        "    const core = matches.filter(area => area.guideTier === 'primary');\n"
        "    const related = matches.filter(area => area.guideTier !== 'primary');\n"
        "    const group = (title, description, items, start) => !items.length ? '' : \`<section class=\"index-group\"><h3>\${esc(title)}</h3><p class=\"section-intro\">\${esc(description)}</p><div class=\"guide-list\">\${items.map((area, offset) => \`<a class=\"guide-link\" href=\"areas/\${esc(area.id)}.html\">\n"
        "          <span class=\"guide-count\">\${String(start + offset + 1).padStart(2, '0')}</span>\n"
        "          <span class=\"guide-copy\"><strong>\${esc(area.title)}</strong><span>\${esc(area.short)}</span><span class=\"index-meta\">\${area.guideTier === 'primary' ? 'Drives college-fit comparisons' : 'Included for context and completeness'}</span></span>\n"
        "          <span class=\"guide-arrow\" aria-hidden=\"true\">Read guide&nbsp;→</span>\n"
        "        </a>\`).join('')}</div></section>\`;\n"
        "    app.innerHTML = \`<div class=\"index-page\">",
        "area grouping",
    )
    text = replace_once(
        text,
        '        <h1>Field Guides</h1>\n        <label class="guide-search" for="areaSearch"><span>Find a field or topic</span><input id="areaSearch" type="search" placeholder="Try behavior, rehabilitation, ecology…" value="\${esc(query || \'\')}"></label>',
        '        <h1>Field Guides</h1>\n        <p class="section-intro">The first eight areas are the current college-exploration focus. Related fields remain available for context, but they do not independently drive school recommendations. Marine biology is treated as an environment that can cut across several fields, not as an emphasized recommendation category.</p>\n        <label class="guide-search" for="areaSearch"><span>Find a field or topic</span><input id="areaSearch" type="search" placeholder="Try behavior, welfare, wildlife, physiology…" value="\${esc(query || \'\')}"></label>',
        "area index intro",
    )
    old = '''        <div class="section-heading"><p class="section-number">Field guide index</p><h2 id="guideIndexTitle">Choose an area to read</h2></div>
        <div class="guide-list">\${matches.length ? matches.map((area, index) => \`<a class="guide-link" href="areas/\${esc(area.id)}.html">
          <span class="guide-count">\${String(index + 1).padStart(2, '0')}</span>
          <span class="guide-copy"><strong>\${esc(area.title)}</strong><span>\${esc(area.short)}</span></span>
          <span class="guide-arrow" aria-hidden="true">Read guide&nbsp;→</span>
        </a>\`).join('') : '<p class="empty">No field guides match that search.</p>'}</div>'''
    new = '''        <div class="section-heading"><p class="section-number">Field guide index</p><h2 id="guideIndexTitle">Choose an area to read</h2></div>
        \${matches.length ? group('Core exploration areas', 'These eight fields are the basis for college-fit comparisons and future school recommendations.', core, 0) + group('Related fields and specializations', 'Useful for understanding the wider landscape. These areas can matter within a program, but they do not create a school recommendation by themselves.', related, core.length) : '<p class="empty">No field guides match that search.</p>'}'''
    text = replace_once(text, old, new, "area grouped render")
    path.write_text(text, encoding="utf-8")


def patch_area_article():
    path = ROOT / "site/area-article.js"
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, "  let areas = [];\n  let photos = {};", "  let areas = [];\n  let photos = {};\n  let programs = (D.programs || []).slice();", "area article programs")
    text = replace_once(text, "  function programByCode(code) { return D.programs.find(program => program.code === code); }", "  function programByCode(code) { return programs.find(program => program.code === code); }", "area article lookup")
    text = replace_once(
        text,
        '        <div class="hero-copy"><div class="eyebrow">Field guide</div><h1>\${esc(area.title)}</h1><p class="standfirst">\${esc(area.short)}</p></div>',
        '        <div class="hero-copy"><div class="eyebrow">\${area.guideTier === \'primary\' ? \'Core exploration field\' : \'Related field / specialization\'}</div><h1>\${esc(area.title)}</h1><p class="standfirst">\${esc(area.short)}</p></div>',
        "area article tier",
    )
    text = replace_once(
        text,
        '            <p class="section-intro">A major is one part of preparation. Course selection, research, fieldwork, internships, volunteering, and technical skills can change what a program makes possible.</p>',
        '            <p class="section-intro">\${area.guideTier === \'primary\' ? \'This field is part of the current college-fit focus. A major is only one part of preparation; courses, research, internships, and direct experience determine how well a program supports it.\' : \'This guide is included for context and completeness. Its college examples are informative, but this field does not independently drive school recommendations.\'}</p>',
        "area article study note",
    )
    text = replace_once(
        text,
        '            <h3 class="group-heading first">References and further reading</h3><ul class="source-list">\${area.references.map(item => \`<li><a href="\${esc(item.url)}" target="_blank" rel="noopener">\${esc(item.title)}</a><span>\${esc(item.type)}</span></li>\`).join(\'\')}</ul>',
        '            \${Array.isArray(area.starterResources) && area.starterResources.length ? \`<h3 class="group-heading first">Good starting points</h3><ul class="source-list">\${area.starterResources.map(item => \`<li><a href="\${esc(item.url)}" target="_blank" rel="noopener">\${esc(item.title)}</a><span>\${esc(item.description || \'\')}</span></li>\`).join(\'\')}</ul>\` : \'\'}\n            <h3 class="group-heading \${Array.isArray(area.starterResources) && area.starterResources.length ? \'\' : \'first\'}">References and further reading</h3><ul class="source-list">\${area.references.map(item => \`<li><a href="\${esc(item.url)}" target="_blank" rel="noopener">\${esc(item.title)}</a><span>\${esc(item.type)}</span></li>\`).join(\'\')}</ul>',
        "area article starters",
    )
    text = replace_once(
        text,
        '''      const [manifest, photoManifest] = await Promise.all([
        fetchJson(`\${root}index.json`),
        fetchJson(`\${root}photos.json`)
      ]);
      photos = photoManifest.photos || photoManifest;
      areas = await Promise.all(manifest.areas.map(file => fetchJson(`\${root}\${file}`)));''',
        '''      const [manifest, photoManifest, additions] = await Promise.all([
        fetchJson(`\${root}index.json`),
        fetchJson(`\${root}photos.json`),
        fetchJson('../content/programs/additional-programs.json').catch(() => [])
      ]);
      photos = photoManifest.photos || photoManifest;
      const codes = new Set(programs.map(program => program.code));
      programs = [...programs, ...(Array.isArray(additions) ? additions.filter(program => program && program.code && !codes.has(program.code)) : [])];
      areas = await Promise.all(manifest.areas.map(file => fetchJson(`\${root}\${file}`)));''',
        "area article additions",
    )
    path.write_text(text, encoding="utf-8")


def patch_programs():
    add_path = ROOT / "site/content/programs/additional-programs.json"
    additions = json.loads(add_path.read_text(encoding="utf-8"))
    additions = [p for p in additions if p.get("code") != "UMA-VT"] + [UMA_VT_PROGRAM]
    dump("site/content/programs/additional-programs.json", additions)

    focus_js = "(function () {\n  'use strict';\n  window.PROGRAM_FOCUS_AREAS = " + json.dumps(FOCUS_MAP, indent=2, ensure_ascii=False) + ";\n})();\n"
    (ROOT / "site/program-focus.js").write_text(focus_js, encoding="utf-8")

    path = ROOT / "site/programs.js"
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, "  let loadWarning = '';", "  let loadWarning = '';\n  const CURRENT_FOCUS = window.PROGRAM_FOCUS_AREAS || {};", "program focus constant")
    text = replace_once(
        text,
        "    return [program.school, program.title, program.type, program.scale, program.fundamental, ...(program.scienceFoundation || []), ...(program.animalContent || []), ...(program.experienceTags || [])].join(' ').toLowerCase();",
        "    return [program.school, program.title, program.type, program.scale, program.fundamental, ...(program.scienceFoundation || []), ...(program.animalContent || []), ...(program.experienceTags || []), ...(CURRENT_FOCUS[program.code] || [])].join(' ').toLowerCase();",
        "program searchable focus",
    )
    text = replace_once(text, "    const inCollection = matches.filter(program => program.collection === collection.key);", "    const inCollection = matches.filter(collection.test);", "program collection filter")
    text = replace_once(
        text,
        '      <div class="collection-heading"><p class="eyebrow">\${esc(collection.eyebrow)}</p><h2 id="\${collection.key}Title">\${esc(collection.title)}</h2><p>\${esc(collection.description)}</p></div>',
        '      <div class="collection-heading"><p class="eyebrow">\${esc(collection.eyebrow.replace(\'{count}\', String(inCollection.length)))}</p><h2 id="\${collection.key}Title">\${esc(collection.title)}</h2><p>\${esc(collection.description)}</p></div>',
        "program dynamic count",
    )
    text = replace_once(
        text,
        '<span class="index-meta">\${esc(program.type)} · \${esc(program.scale)}</span></span><span class="guide-arrow"',
        '<span class="index-meta">\${esc(program.type)} · \${esc(program.scale)}</span>\${CURRENT_FOCUS[program.code] ? \`<span class="index-meta"><strong>Current-focus match:</strong> \${CURRENT_FOCUS[program.code].map(esc).join(\' · \')}</span>\` : \'<span class="index-meta">Related comparison only; does not independently drive recommendations</span>\'}</span><span class="guide-arrow"',
        "program focus labels",
    )
    text = replace_once(
        text,
        """    const collections = [
      { key: 'focused', eyebrow: 'Focused comparison · 10 pathways', title: 'Original shortlist', description: 'The regional programs examined most closely in the original comparison, including different ways to shape a degree at the same university.' },
      { key: 'additional', eyebrow: 'Broader research · 7 programs', title: 'Additional programs with merit', description: 'Distinctive national and regional options retained for completeness. These expand the landscape without implying that they rank below or above the focused comparison.' }
    ];""",
        """    const collections = [
      { key: 'focus', eyebrow: 'Current focus · {count} pathways', title: 'Programs that match the current animal-career focus', description: 'These programs have documented strength in at least one recommendation-driving area: animal biology, zoology, wildlife biology, animal behavior, animal welfare science, non-agricultural animal science, zoo/aquarium managed-animal care, or veterinary technology. This is a relevance filter, not a ranking.', test: program => Boolean(CURRENT_FOCUS[program.code]) },
      { key: 'context', eyebrow: 'Context · {count} pathways', title: 'Related programs kept for comparison', description: 'These are legitimate animal-related pathways, but their center of gravity is in adjacent areas such as conservation/ecology, agriculture/pre-vet, or wildlife rehabilitation. They remain visible for completeness and do not independently drive school recommendations.', test: program => !CURRENT_FOCUS[program.code] }
    ];""",
        "program collections",
    )
    text = replace_once(
        text,
        "        <h1>College Programs</h1>",
        "        <h1>College Programs</h1>\n        <p class=\"section-intro\">School-fit comparisons are now anchored to eight core fields. Marine biology remains available as a species/environment context but is not an emphasized recommendation category.</p>",
        "program intro",
    )
    path.write_text(text, encoding="utf-8")

    path = ROOT / "site/program-article.js"
    text = path.read_text(encoding="utf-8")
    text = replace_once(text, "  let programs = [];", "  let programs = [];\n  const CURRENT_FOCUS = window.PROGRAM_FOCUS_AREAS || {};", "program article focus")
    text = replace_once(
        text,
        '<div><dt>Research set</dt><dd>\${program.collection === \'additional\' ? \'Additional researched option\' : \'Focused comparison\'}</dd></div><div><dt>Research verified</dt><dd>\${esc(program.lastVerified || \'See sources\')}</dd></div>',
        '<div><dt>Source set</dt><dd>\${program.collection === \'additional\' ? \'Additional researched option\' : \'Original researched set\'}</dd></div><div><dt>Current-focus relevance</dt><dd>\${CURRENT_FOCUS[program.code] ? esc(CURRENT_FOCUS[program.code].join(\' · \')) : \'Related context only\'}</dd></div><div><dt>Research verified</dt><dd>\${esc(program.lastVerified || \'See sources\')}</dd></div>',
        "program article facts",
    )
    path.write_text(text, encoding="utf-8")

    for filename, script in [("site/programs.html", "programs.js"), ("site/program.html", "program-article.js")]:
        p = ROOT / filename
        text = p.read_text(encoding="utf-8")
        text = text.replace(f'<script src="data.js"></script><script src="{script}"></script>', f'<script src="data.js"></script><script src="program-focus.js"></script><script src="{script}"></script>')
        p.write_text(text, encoding="utf-8")


def patch_docs():
    path = ROOT / "site/index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace('<span class="home-section-copy"><span class="eyebrow">15 in-depth guides</span><strong>Field Guides</strong>', '<span class="home-section-copy"><span class="eyebrow">8 core areas + related guides</span><strong>Field Guides</strong>')
    text = text.replace('<span class="home-section-copy"><span class="eyebrow">17 researched pathways</span><strong>College Programs</strong>', '<span class="home-section-copy"><span class="eyebrow">Researched undergraduate pathways</span><strong>College Programs</strong>')
    path.write_text(text, encoding="utf-8")

    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("**Field Guides** — 15 long-form guides loaded from editable JSON files in `site/content/areas/`.", "**Field Guides** — 17 long-form guides loaded from editable JSON files in `site/content/areas/`, grouped into eight recommendation-driving areas and nine related fields/specializations.")
    text = text.replace("**College Programs** — 17 researched undergraduate pathway guides: the 10-path focused comparison from the validated site export plus 7 additional programs retained from the broader research.", "**College Programs** — 18 researched undergraduate pathway guides: the 10-path original comparison from the validated site export plus 8 additional programs retained from the broader research.")
    path.write_text(text, encoding="utf-8")

    path = ROOT / "docs/AREA_EXPLORER.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("the 7 hand-editable broader options", "the 8 hand-editable broader options")
    text = text.replace("The 15 photographs are stored locally as cropped 1200 × 675 WebP files", "The field-guide photographs are stored locally as cropped 1200 × 675 WebP files")
    if "## Current recommendation focus" not in text:
        text += "\n## Current recommendation focus\n\nCollege-fit comparisons are anchored to eight areas: Animal Biology, Zoology, Wildlife Biology, Animal Behavior, Animal Welfare Science, Animal Science where the curriculum has a meaningful non-agricultural/managed-animal emphasis, Zoo & Aquarium Science / Managed Animal Care, and Veterinary Technology. Other guides remain available for context and completeness but do not independently drive school recommendations. Marine biology is treated as an environment/taxon context that can cut across several fields, not as an emphasized recommendation category.\n"
    path.write_text(text, encoding="utf-8")

    path = ROOT / "docs/CONTENT_UPDATE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("15 field guides + index.json", "17 field guides + index.json")
    text = text.replace("fifteen field guides", "field guides")
    path.write_text(text, encoding="utf-8")


def main():
    patch_generator()
    patch_photos()
    patch_area_pages()
    patch_area_index_js()
    patch_area_article()
    patch_programs()
    patch_docs()


if __name__ == "__main__":
    main()
