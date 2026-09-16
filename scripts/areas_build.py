#!/usr/bin/env python3
"""Build the field-guide content for animal_career_explorer.

Single source of truth for the fifteen field guides. Edit the area() calls
below, then run:

    python3 areas_build.py [OUTPUT_DIR]        # default: site/content/areas

REFS        every citable source, listed once. Areas cite by key, never by URL.
PROGRAMS    program code -> school and full program title.
area(...)   one call per guide. Prose lives here and nowhere else.

Build steps applied after the content is assembled:
  - reference keys expand into full reference objects
  - programCodes expand into programs[] carrying school and full title
  - validation checks every source: pointer and related: id resolves

The build never rewrites prose. It assembles content and then checks it.
If an acronym is used without its full form appearing in the same guide, the
build fails and names the guide, so the sentence gets fixed at the source
where a human controls the articles and the capitalisation.

Program codes are back-end identifiers. They must never appear in prose.
"""
import json, re, sys, pathlib

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                   else "/mnt/user-data/outputs/areas")

# ============================================================= reference bank
REFS = {
 "society_integrative_comparative": ("Society for Integrative and Comparative Biology",
   "Professional society",
   "https://sicb.org/"),
 "sicb_mission_history": ("SICB: mission and history",
   "Professional society",
   "https://sicb.org/our-mission/"),
 "integrative_comparative_biology": ("Integrative and Comparative Biology (formerly American Zoologist)",
   "Field journal",
   "https://academic.oup.com/icb/"),
 "american_physiological_society": ("American Physiological Society (APS): Comparative & Evolutionary Physiology Section",
   "Professional society",
   "https://www.physiology.org/community/aps-communities/sections/Comparative-Evolutionary"),
 "american_physiological_society2": ("American Physiological Society (APS): Lessons from Comparative and Evolutionary Physiology",
   "Field perspective",
   "https://journals.physiology.org/doi/full/10.1152/physiol.00003.2015"),
 "animal_behavior_society": ("Animal Behavior Society: Applied Animal Behavior",
   "Professional society",
   "https://www.animalbehaviorsociety.org/web/committees-applied-behavior.php"),
 "animal_behavior_society2": ("Animal Behavior Society (ABS): Certified Applied Animal Behaviorist requirements",
   "Credential requirements",
   "https://www.animalbehaviorsociety.org/web/committees-applied-behavior-caab.php"),
 "association_study_animal": ("Association for the Study of Animal Behaviour (ASAB): the journal Animal Behaviour",
   "Field journal",
   "https://www.asab.org/journal"),
 "applied_animal_behaviour": ("Applied Animal Behaviour Science",
   "Field journal",
   "https://www.sciencedirect.com/journal/applied-animal-behaviour-science"),
 "international_society_applied": ("International Society for Applied Ethology",
   "Professional society",
   "https://www.applied-ethology.org/Applied_Animal_Behaviour_Science.html"),
 "university_new_england": ("University of New England: Animal Behavior program",
   "Undergraduate program statement",
   "https://www.une.edu/cas/schools/social-behavioral-sciences/programs/bs-animal-behavior"),
 "american_psychological_association": ("American Psychological Association (APA): Journal of Comparative Psychology",
   "Field journal",
   "https://www.apa.org/pubs/journals/com/"),
 "international_journal_comparative": ("International Journal of Comparative Psychology",
   "Field journal",
   "https://doaj.org/toc/2168-3344"),
 "science_animal_welfare": ("Science for Animal Welfare (formerly the Universities Federation for Animal Welfare, UFAW)",
   "Professional society",
   "https://scienceforanimalwelfare.org/"),
 "science_animal_welfare2": ("Science for Animal Welfare: publications",
   "Field journal",
   "https://scienceforanimalwelfare.org/for-scientists/publication-library/"),
 "journal_applied_animal": ("Journal of Applied Animal Welfare Science",
   "Field journal",
   "https://www.tandfonline.com/journals/haaw20"),
 "ecological_society_america": ("Ecological Society of America",
   "Professional society",
   "https://esa.org/about/what-does-ecology-have-to-do-with-me/"),
 "ecological_society_america2": ("Ecological Society of America (ESA): Certified Ecologist program",
   "Credential",
   "https://esa.org/career-development/certification-from-esa/"),
 "wildlife_society": ("The Wildlife Society",
   "Professional society",
   "https://wildlife.org/"),
 "wildlife_society_tws": ("The Wildlife Society (TWS): wildlife biologist certification",
   "Credential",
   "https://wildlife.org/certification-programs/"),
 "michigan_state_wildlife": ("Michigan State: Wildlife Ecology and Management B.S.",
   "Undergraduate example",
   "https://www.canr.msu.edu/fw/undergraduate/Majors/Wildlife-Ecology-and-Management"),
 "umaine_wildlife_fisheries": ("UMaine: Wildlife, Fisheries, and Conservation Biology",
   "Undergraduate example",
   "https://umaine.edu/wle/undergraduate-program/"),
 "society_conservation_biology": ("Society for Conservation Biology journals",
   "Professional society",
   "https://conbio.onlinelibrary.wiley.com/"),
 "biological_conservation": ("Biological Conservation",
   "Field journal",
   "https://www.sciencedirect.com/journal/biological-conservation"),
 "merck_veterinary_manual": ("Merck Veterinary Manual: shelter medicine",
   "Clinical reference",
   "https://www.merckvetmanual.com/special-subjects/shelter-medicine/overview-of-shelter-medicine"),
 "american_veterinary_medical": ("American Veterinary Medical Association (AVMA): shelter medicine as a specialty",
   "Professional body",
   "https://www.avma.org/javma-news/2014-06-01/specialty-whose-time-has-come"),
 "wildlife_disease_association": ("Wildlife Disease Association",
   "Professional society",
   "https://wildlifedisease.site-ym.com/"),
 "journal_wildlife_diseases": ("Journal of Wildlife Diseases: scope",
   "Field journal",
   "https://bioone.org/journals/journal-of-wildlife-diseases/scope-and-details"),
 "toward_modernized_definition": ("Toward a Modernized Definition of Wildlife Health",
   "Field perspective",
   "https://meridian.allenpress.com/jwd/article/50/3/427/123351/TOWARD-A-MODERNIZED-DEFINITION-OF-WILDLIFE-HEALTH"),
 "onet_occupational_information": ("O*NET Occupational Information Network: Animal Scientists",
   "Tasks and skills",
   "https://www.onetonline.org/link/summary/19-1011.00"),
 "american_society_animal": ("American Society of Animal Science (ASAS): What is Animal Science",
   "Professional society definition",
   "https://www.asas.org/services/student-resources/what-is-animal-science"),
 "bls_oews_animal": ("BLS OEWS: Animal Scientists (19-1011)",
   "Occupational wage data",
   "https://www.bls.gov/news.release/ocwage.t01.htm"),
 "association_zoos_aquariums": ("Association of Zoos & Aquariums: about",
   "Professional society",
   "https://www.aza.org/about-us"),
 "association_zoos_aquariums2": ("Association of Zoos & Aquariums (AZA): what accreditation means",
   "Accreditation standard",
   "https://www.aza.org/what-is-accreditation"),
 "association_zoos_aquariums3": ("Association of Zoos & Aquariums (AZA): careers in zoos and aquariums",
   "Career guidance",
   "https://www.aza.org/careers_in_zoos_and_aquariums"),
 "michigan_state_zoo": ("Michigan State: Zoo and Aquarium Science",
   "Undergraduate example",
   "https://integrativebiology.natsci.msu.edu/undergraduate-program/undergraduate-degrees/zoo-and-aquarium-science.aspx"),
 "international_wildlife_rehabilitation": ("International Wildlife Rehabilitation Council (IWRC): how to become a wildlife rehabilitator",
   "Professional society",
   "https://theiwrc.org/how-to-become-a-wildlife-rehabilitator/"),
 "international_wildlife_rehabilitation2": ("International Wildlife Rehabilitation Council (IWRC): certification questions and answers",
   "Credential requirements",
   "https://theiwrc.org/faq2-0/"),
 "north_american_association": ("North American Association for Environmental Education (NAAEE): careers in interpretation",
   "Professional society",
   "https://jobs.naaee.org/careers/interpretation"),
 "national_association_interpretation": ("National Association for Interpretation (NAI): Certified Interpretive Guide program",
   "Credential",
   "https://eepro.naaee.org/learning/certified-interpretive-guide-programs"),
 "international_society_anthrozoology": ("International Society for Anthrozoology",
   "Professional society",
   "https://isaz.net/"),
 "anthrozoos": ("Anthrozoos",
   "Field journal",
   "https://isaz.net/journal/journal.html"),
}

# ======================================== program code -> full program name
PROGRAMS = {
 "ME-WE": ("University of Maine",
   "Wildlife Ecology B.S."),
 "ME-ZOO": ("University of Maine",
   "Zoology B.S. with Ecology concentration"),
 "UMA-AS": ("University of Massachusetts Amherst",
   "Animal Science B.S. (Animal Management concentration)"),
 "UMA-BIO": ("University of Massachusetts Amherst",
   "Biology B.S. (ecology and behavior electives)"),
 "UMA-WEC": ("University of Massachusetts Amherst",
   "Natural Resources Conservation B.S. (Wildlife Ecology & Conservation concentration)"),
 "UNE-AB": ("University of New England",
   "Animal Behavior B.S."),
 "UNE-AN": ("University of New England",
   "Animal Behavior B.S. with Neuroscience minor"),
 "URI-AZ": ("University of Rhode Island",
   "Animal and Veterinary Science B.S. (Animal Science option) + Zoo and Aquarium Science Certificate"),
 "URI-W": ("University of Rhode Island",
   "Wildlife & Conservation Biology"),
 "URI-WZ": ("University of Rhode Island",
   "Wildlife & Conservation Biology B.S. + Zoo & Aquarium Science Certificate"),
}

# ===== acronyms the build LINTS for. it never rewrites prose; if an acronym
# ===== is used without its full form present, the build fails and you fix it.
ACRONYMS = {
 "ASAS": "American Society of Animal Science",
 "AVMA": "American Veterinary Medical Association",
 "AZA": "Association of Zoos & Aquariums",
 "DVM": "Doctor of Veterinary Medicine",
 "ESA": "Ecological Society of America",
 "GIS": "geographic information systems",
 "IWRC": "International Wildlife Rehabilitation Council",
 "NAI": "National Association for Interpretation",
 "NGO": "nongovernmental organization",
 "SSP": "Species Survival Plan",
 "TWS": "The Wildlife Society",
 "USDA": "U.S. Department of Agriculture",
}


# ============================================ collector used by the area calls
REF = {k: v[0] for k, v in REFS.items()}

AREAS = []
def area(**kw):
    kw["terms"] = [{"term": t, "definition": d} for t, d in kw["terms"]]
    kw["questions"] = [{"question": q_, "approach": a_} for q_, a_ in kw["questions"]]
    for blk in ("focus", "variations"):
        kw[blk] = [{k: v for k, v in it.items() if v is not None} for it in kw[blk]]
    kw["programs"] = [{"code": c, "school": PROGRAMS[c][0], "title": PROGRAMS[c][1]}
                      for c in kw["programCodes"]]
    kw["references"] = [{"title": REFS[k][0], "type": REFS[k][1], "url": REFS[k][2]}
                        for k in kw["references"]]
    AREAS.append(kw)

# ==================================================================== areas
area(
 id="zoology",
 title="Zoology",
 short="How animal species differ, how they are related, and how bodies are built across "
        "the animal kingdom. Comparison and classification are the core methods.",
 bigPicture="Zoology asks what animals are and how they work. Its subject can be the "
             "skeleton of a bat's wing, the life cycle of a parasite, the relationship "
             "between two beetle families, or how a whale finds food. Zoologists compare "
             "across species to separate general principles from the quirks of any one "
             "animal, and most specialize eventually — mammals, birds, reptiles, fishes, "
             "insects. The name is older than much of what it now contains, and it "
             "appears on degrees more often than on job listings.",
 terms=[
  ("Systematics",
   "The study of how organisms are related and how they should be classified, using "
   "evidence from anatomy, genetics, and the fossil record."),
  ("Taxonomy",
   "The specific practice of naming and formally describing species and higher groups "
   "within a classification."),
  ("Phylogeny",
   "The evolutionary tree showing how a set of species descended from common ancestors."),
  ("Comparative anatomy",
   "Comparing body structures across species to work out shared ancestry, function, and "
   "constraint."),
  ("Organismal biology",
   "Biology studied at the level of the whole animal, not cells, molecules, or ecosystems."),
  ("Natural history",
   "Detailed descriptive knowledge of how a species actually lives — diet, habitat, "
   "breeding, daily and seasonal patterns."),
 ],
 focus=[
  dict(title="Diversity and classification",
       description="Describing what animal groups exist, how they are distinguished, and "
                   "how they are related. Systematics, taxonomy, and comparative "
                   "morphology give the rest of the animal sciences their vocabulary.",
       source=REF["society_integrative_comparative"]),
  dict(title="Comparative anatomy and form",
       description="How bodies are built across groups, and what structural differences "
                   "reveal about ancestry, constraint, and way of life. Vertebrate "
                   "morphology and invertebrate zoology are long-standing specialties.",
       source=REF["sicb_mission_history"]),
  dict(title="Evolution and natural history",
       description="How lineages changed over time, and how a species actually lives: "
                   "what it eats, where it goes, how it reproduces, and how it interacts "
                   "with others. Natural history knowledge remains the backbone of field "
                   "work.",
       source=REF["integrative_comparative_biology"]),
  dict(title="Taxon specialization",
       description="Many zoologists work within one group: mammalogy, ornithology, "
                   "herpetology, ichthyology, entomology. Specialization usually develops "
                   "in graduate school, not as an undergraduate.",
       source=REF["society_integrative_comparative"]),
 ],
 questions=[
  ("What animal groups exist, and how are they related to each other?",
   "By combining morphological comparison with molecular phylogenetics: sequencing genes "
   "across species, building trees, and testing them against anatomical and fossil "
   "evidence."),
  ("How does body structure differ across species, and why?",
   "Through comparative anatomy — dissection, imaging, and museum specimens — asking "
   "whether a difference reflects shared ancestry, an adaptation, or a developmental "
   "constraint."),
  ("How does this species actually live in the wild?",
   "By sustained field observation and natural history work: following individuals, "
   "recording diet and habitat use, and building a picture over seasons, not days."),
  ("Is this population actually a distinct species?",
   "By testing whether groups are reproductively or genetically separated, using genetic "
   "markers plus morphological and behavioral comparison, then arguing it against "
   "existing taxonomy."),
  ("What did this lineage look like in the past?",
   "By reading fossils and comparative development together, and mapping traits onto a "
   "phylogeny to infer what ancestral forms most likely had."),
  ("What can comparison across many species reveal that studying one cannot?",
   "By assembling data from many species and asking whether a pattern holds broadly, "
   "which separates general biological principles from quirks of a single organism."),
 ],
 responsibilities=[
  "Identify, describe, and classify organisms using morphological or molecular evidence.",
  "Conduct field and laboratory studies of species biology and natural history.",
  "Manage or contribute to collections, specimens, and species records.",
  "Publish, teach, and communicate findings to scientific and public audiences.",
 ],
 knowledgeSkills=[
  "Comparative anatomy, physiology, and development",
  "Evolution, systematics, and phylogenetics",
  "Species identification and natural history",
  "Field and laboratory methods",
  "Scientific writing and data management",
 ],
 settings=[
  "Universities and research institutes",
  "Natural history museums and collections",
  "State and federal agencies",
  "Field stations and research sites",
 ],
 realities=[
  "Job listings rarely use the word zoology. Searching by that term alone will badly "
   "understate what is out there.",
  "Independent research positions generally require graduate study. A bachelor's more "
   "often opens technician, collections, or education work.",
  "Museum and collections roles are a real bachelor's-level entry point, and natural "
   "history knowledge is valued precisely because fewer programs still teach it well.",
  "Field and collections work can mean travel, seasonal contracts, and physical conditions.",
  "Taxon specialization usually arrives in graduate school, so there is no need to have "
   "picked one at seventeen.",
 ],
 careers=[
  "Zoologist",
  "Mammalogist",
  "Ornithologist",
  "Herpetologist",
  "Evolutionary biologist studying animals",
  "Museum / natural-history education or collections work",
  "M.S. / Ph.D. in zoology / organismal biology",
 ],
 variations=[
  dict(label="The name versus the work",
       description="Zoology persists strongly as a degree title but weakly as a job "
                   "title. Positions are more often advertised as biologist, ecologist, "
                   "curator, or a taxon specialty. The society that once carried the name "
                   "dropped it in 1996. This is not a warning about the degree; it is a "
                   "warning about searching for jobs by that word.",
       source=REF["sicb_mission_history"]),
  dict(label="Taxon focus",
       description="Work can concentrate on mammals, birds, reptiles and amphibians, "
                   "fishes, or invertebrates, and the day-to-day methods differ "
                   "considerably between them.",
       ),
  dict(label="Setting",
       description="Zoology supports museum and collections work, university research and "
                   "teaching, agency biology, and field science.",
       ),
  dict(label="Scale",
       description="Some zoologists work at the level of tissue and structure; others "
                   "work on whole animals in the field. Both are zoology.",
       ),
 ],
 programCodes=["ME-ZOO", "UMA-BIO"],
 related=["animal-physiology", "ecology", "animal-behavior", "wildlife-ecology-management"],
 references=["society_integrative_comparative", "sicb_mission_history", "integrative_comparative_biology"],
)

area(
 id="animal-physiology",
 title="Animal Physiology / Comparative Physiology",
 short="How an individual animal's body works. Organs, hormones, metabolism, and the "
        "laboratory tools used to study them.",
 bigPicture="Physiology asks how an animal's body works. How a hummingbird fuels a "
             "wingbeat, how a camel goes without water, how a hibernating ground squirrel "
             "drops its body temperature close to freezing and comes back. The "
             "comparative branch treats that variety as the point, picking whichever "
             "species makes a question answerable instead of defaulting to mice and rats. "
             "Most of the work is measurement — oxygen use, hormone levels, blood "
             "chemistry, temperature — under conditions the researcher controls.",
 terms=[
  ("Homeostasis",
   "Keeping internal conditions such as temperature, water balance, and blood chemistry "
   "stable despite changes outside the body."),
  ("Endocrinology",
   "The study of hormones and the glands producing them, and how they regulate body "
   "processes and behavior."),
  ("Metabolic rate",
   "The rate at which an animal uses energy, often measured through oxygen consumption."),
  ("Thermoregulation",
   "How an animal controls its body temperature, by behavior, physiology, or both."),
  ("Krogh's principle",
   "The research strategy of choosing whichever species is best suited to the question "
   "instead of defaulting to a standard laboratory animal."),
  ("Ecophysiology",
   "Physiology studied in environmental context, asking how physiological limits shape "
   "where and how an animal can live."),
 ],
 focus=[
  dict(title="Systems and mechanisms",
       description="How circulation, respiration, digestion, excretion, muscle, and "
                   "nervous systems work, and how they are coordinated. This is the "
                   "mechanistic core that clinical and applied animal fields build on.",
       source=REF["american_physiological_society"]),
  dict(title="Regulation and homeostasis",
       description="How animals hold internal conditions stable against changing external "
                   "ones, including thermoregulation, water and salt balance, and "
                   "endocrine control.",
       source=REF["american_physiological_society"]),
  dict(title="Comparison across species",
       description="Comparing physiological responses across many species to separate "
                   "general principles from specific adaptations, and to understand how "
                   "some animals tolerate conditions others cannot.",
       source=REF["american_physiological_society2"]),
  dict(title="Physiology in ecological context",
       description="Extending mechanism into the environment: how physiological limits "
                   "shape where animals can live, how they respond to stress, heat, or "
                   "scarcity, and what that means under environmental change.",
       source=REF["american_physiological_society2"]),
 ],
 questions=[
  ("How does this body system actually work in this animal?",
   "By measuring function directly — respirometry, blood chemistry, hormone assays, "
   "telemetry — and then manipulating one variable at a time to see what changes."),
  ("How does the animal keep internal conditions stable when external ones change?",
   "By exposing animals to controlled changes in temperature, oxygen, or water "
   "availability and tracking the physiological response, including how fast it engages "
   "and how long it lasts."),
  ("What does comparing species reveal that studying one species cannot?",
   "By choosing species that face very different demands and testing the same system in "
   "each, following the principle of picking the animal best suited to the question."),
  ("Where are this animal's physiological limits, and what happens near them?",
   "By stepwise testing toward the limit under controlled conditions, measuring "
   "performance and recovery, with ethical review setting the boundaries of how far "
   "testing goes."),
  ("How does physiology explain where a species can and cannot live?",
   "By pairing laboratory measurements of tolerance with field data on where the animal "
   "actually occurs, then testing whether the physiological limit predicts the "
   "distribution."),
  ("What is happening at the molecular level behind this response?",
   "Through gene expression, protein, and metabolite work in tissue samples, connecting "
   "whole-animal responses to the mechanisms producing them."),
 ],
 responsibilities=[
  "Design and run controlled laboratory or field experiments on physiological function.",
  "Collect and analyze physiological measurements, samples, and time-series data.",
  "Maintain animals, equipment, and protocols to research and ethical standards.",
  "Interpret mechanism in evolutionary or ecological terms and publish results.",
 ],
 knowledgeSkills=[
  "Anatomy, physiology, and endocrinology",
  "Cell and molecular biology, biochemistry",
  "Experimental design and quantitative analysis",
  "Laboratory instrumentation and technique",
  "Research ethics and animal-use protocols",
 ],
 settings=[
  "University and institute laboratories",
  "Veterinary and biomedical research settings",
  "Field research programs",
  "Industry and applied research organizations",
 ],
 realities=[
  "Most of this work happens indoors, with instruments, and not with animals in their "
   "own environment.",
  "Research careers generally require graduate study; bachelor's-level roles are "
   "technician and research assistant positions.",
  "The skills transfer well. Physiology training is a route into biomedical research, "
   "veterinary medicine, and the physiological side of ecology.",
  "Animal research runs under institutional review and animal-use protocols, and "
   "learning that framework is part of the job.",
  "Because “comparative” is used loosely, read course descriptions instead of course "
   "titles.",
 ],
 careers=[
  "Animal physiologist",
  "Neuroethologist / neural-behavior researcher",
  "University / laboratory research assistant",
  "Research / laboratory manager — behavioral or biological science",
  "Research scientist / principal investigator",
 ],
 variations=[
  dict(label="Two names, one field",
       description="Animal physiology is the phrase you will meet as a course and "
                   "textbook title. Comparative physiology is what the professional "
                   "community calls itself, with sections and societies in many "
                   "countries. Practitioners do not entirely agree it is a discipline at "
                   "all, as opposed to an approach, and the term is used somewhat "
                   "differently by different researchers.",
       source=REF["american_physiological_society2"]),
  dict(label="Where it sits",
       description="Physiology courses live in biology, animal science, veterinary, "
                   "neuroscience, and pre-health programs. Which department teaches it "
                   "changes the emphasis considerably.",
       ),
  dict(label="Laboratory versus field",
       description="Some work is controlled and instrument-heavy; some is done on "
                   "free-living animals in their own environment, which is often treated "
                   "as the harder standard.",
       ),
  dict(label="Adjacent paths",
       description="This area feeds veterinary medicine, biomedical research, animal "
                   "welfare science, and the physiological side of ecology.",
       ),
 ],
 programCodes=["UMA-BIO", "UNE-AN", "ME-ZOO"],
 related=["zoology", "animal-behavior", "veterinary-science", "animal-science"],
 references=["american_physiological_society", "american_physiological_society2", "society_integrative_comparative"],
)

area(
 id="animal-behavior",
 title="Animal Behavior / Ethology",
 short="What animals actually do in the world: how a behavior develops, what triggers "
        "it, and what purpose it serves.",
 bigPicture="Animal behavior asks what animals do and why. Why a bird sings before dawn, "
             "why a wolf pack splits, why a dog that was fine last week now lunges at the "
             "mailbox. The work begins with watching closely enough to describe a "
             "behavior precisely, then testing explanations instead of settling for the "
             "plausible one. The same science supports research on wild populations and "
             "practical work with the animals people keep.",
 distinction=dict(
   title="Animal Behavior and Animal Science",
   summary="Both are animal-related degrees and they are routinely confused with each "
           "other — one program page answers the question directly, saying animal science "
           "and animal behavior are not the same. They differ in which animals they "
           "centre on, which questions they ask, and which departments house them.",
   source=REF["university_new_england"],
   items=[
    dict(label="Animal Behavior / Ethology",
         description="Centres on what animals do and why, across wild and domesticated "
                      "species alike. Usually housed in biology, psychology, or "
                      "behavioural science departments. Typical products include "
                      "behavioural data and ethograms, training and enrichment plans, and "
                      "published findings on what causes a behaviour and what it "
                      "accomplishes."),
    dict(label="Animal Science",
         description="Centres on domesticated animals — livestock, horses, and companion "
                      "species — and on how nutrition, genetics, reproduction, and "
                      "management shape their health, growth, and productivity. Usually "
                      "housed in agriculture or veterinary science departments. Typical "
                      "products include feeding and breeding programmes, husbandry "
                      "protocols, and health and production records."),
   ]
 ),
 terms=[
  ("Ethology",
   "The biological study of animal behavior, especially in natural conditions and with "
   "attention to how behavior evolved."),
  ("Ethogram",
   "A catalogue of the distinct behaviors a species performs, defined precisely enough "
   "that different observers score them the same way."),
  ("Behavioral ecology",
   "The study of how behavior contributes to survival and reproduction in a given "
   "environment."),
  ("Operant conditioning",
   "Learning in which the consequences of a behavior change how often it occurs; the "
   "basis of most modern animal training."),
  ("Positive reinforcement",
   "Adding something the animal wants after a behavior, making that behavior more likely "
   "to happen again."),
  ("Applied animal behavior",
   "Using behavioral science to solve practical problems in training, husbandry, welfare, "
   "and problem behavior."),
  ("Playback experiment",
   "Playing a recorded signal to an animal and measuring the response, used to test what "
   "a signal communicates."),
 ],
 focus=[
  dict(title="Mechanism and development",
       description="What causes a behavior in the moment, and how it emerges over an "
                   "animal's lifetime through genetics, maturation, experience, and "
                   "learning.",
       source=REF["association_study_animal"]),
  dict(title="Function and evolution",
       description="What a behavior accomplishes for the animal and how selection shaped "
                   "it. Behavioral ecology sits here, connecting behavior to survival, "
                   "reproduction, and environment.",
       source=REF["association_study_animal"]),
  dict(title="Social behavior and communication",
       description="How animals signal, coordinate, compete, cooperate, and organize into "
                   "groups, and how those systems break down or shift under changed "
                   "conditions.",
       source=REF["association_study_animal"]),
  dict(title="Applied animal behavior",
       description="Using behavioral science to solve practical problems: training, "
                   "behavior modification, husbandry, enrichment, handling, and resolving "
                   "problem behavior in animals under human care.",
       source=REF["animal_behavior_society"]),
 ],
 questions=[
  ("Why does this animal do this, and what triggers it?",
   "By building an ethogram, recording behavior systematically against context, and then "
   "testing candidate triggers experimentally instead of inferring them from observation "
   "alone."),
  ("How does this behavior develop, and how much of it is learned?",
   "By following individuals from early life, comparing animals with different "
   "experience, and running controlled learning tests to separate maturation from "
   "experience."),
  ("What does the behavior accomplish for the animal?",
   "By measuring consequences — feeding success, mating outcomes, survival — and "
   "comparing individuals or species that do it more or less."),
  ("How do these animals communicate?",
   "By recording signals, characterizing their structure, and running playback or "
   "presentation experiments to see how receivers respond."),
  ("Why do individuals of the same species behave differently?",
   "By repeated testing of the same individuals across contexts to see whether "
   "differences are consistent, then relating them to sex, age, condition, or history."),
  ("How can behavioral knowledge improve care, training, or management?",
   "By defining the target behavior in observable terms, applying learning principles in "
   "a structured plan, and measuring whether the behavior actually changed."),
 ],
 responsibilities=[
  "Design observation protocols and collect systematic behavioral data.",
  "Analyze behavioral data and test hypotheses about cause or function.",
  "Apply behavioral principles to training, enrichment, handling, or problem behavior.",
  "Advise caretakers, owners, or managers and document outcomes.",
 ],
 knowledgeSkills=[
  "Ethological observation and behavioral coding",
  "Learning theory and behavior modification",
  "Experimental design and statistics",
  "Species-specific natural history and husbandry",
  "Written and interpersonal communication",
 ],
 settings=[
  "Universities and research programs",
  "Zoos, aquariums, and sanctuaries",
  "Shelters and companion-animal practice",
  "Farms and managed-animal facilities",
 ],
 realities=[
  "There is no single required major. People arrive from biology, psychology, animal "
   "science, wildlife biology, and zoology, and the applied credential recognizes all of "
   "those routes.",
  "Applied certification is another matter: it requires graduate coursework plus "
   "documented professional experience, not hours of hands-on time alone.",
  "Observation is slow. Collecting the data usually takes far longer than analyzing it.",
  "Many applied practitioners are self-employed or consulting, not salaried.",
  "“Animal behaviorist” is not a protected title, which is exactly why credentials carry "
   "weight.",
 ],
 careers=[
  "Animal behaviorist / applied animal behavior scientist",
  "Animal behavior research assistant / technician",
  "Science-based animal trainer",
  "Canine behavior consultant",
  "Shelter behavior specialist / coordinator",
  "Companion-animal behavior researcher",
  "Behavioral ecologist",
  "M.S. in animal behavior / ethology",
 ],
 variations=[
  dict(label="Research versus applied",
       description="Research behavior work asks why animals do what they do; applied "
                   "behavior work uses that knowledge to change outcomes for specific "
                   "animals. The Animal Behavior Society certifies applied practitioners "
                   "at two levels, requiring graduate-level behavioral coursework plus at "
                   "least two years of professional experience.",
       source=REF["animal_behavior_society2"]),
  dict(label="Entry disciplines",
       description="Behaviorists come out of animal science, ethology, psychology, "
                   "wildlife biology, behavioral ecology, and zoology. There is no single "
                   "required major, which is unusual in this space.",
       source=REF["animal_behavior_society2"]),
  dict(label="Setting",
       description="The same science supports work in laboratories, zoos, farms, "
                   "shelters, universities, and private consulting.",
       ),
  dict(label="Species",
       description="Wild, farm, companion, and laboratory animals all have behavior "
                   "specialists, and the applied literature is largely organized by that "
                   "split.",
       source=REF["applied_animal_behaviour"]),
 ],
 programCodes=["UNE-AB", "UNE-AN", "UMA-BIO", "ME-WE"],
 related=["animal-cognition", "animal-welfare", "zoo-aquarium-science", "anthrozoology"],
 references=["animal_behavior_society", "animal_behavior_society2", "association_study_animal", "applied_animal_behaviour", "international_society_applied", "university_new_england"],
)

area(
 id="animal-cognition",
 title="Animal Cognition / Comparative Psychology",
 short="What happens inside an animal before it acts. Perception, memory, learning, "
        "problem-solving, and decision-making.",
 bigPicture="Animal cognition asks what is happening inside an animal before it acts — "
             "what it perceives, what it remembers, what it learns, and how it decides. "
             "Since you cannot ask the subject what it was thinking, everything depends "
             "on task design: a result only counts if the design rules out the simpler "
             "explanation. Comparative psychology is the same territory entered from "
             "psychology, and in practice the two labels are largely interchangeable.",
 terms=[
  ("Cognition",
   "The mental processes an animal uses to take in, store, and act on information — "
   "perception, memory, learning, and decision-making."),
  ("Comparative psychology",
   "The study of behavior and cognition across species from an evolutionary perspective, "
   "based in psychology."),
  ("Discrimination task",
   "A test in which an animal is rewarded for responding to one stimulus and not another, "
   "used to find the limits of what it can tell apart."),
  ("Associative learning",
   "Learning that two things go together; often the simpler explanation that a cognition "
   "study must rule out before claiming more."),
  ("Transfer test",
   "Presenting a new version of a problem to check whether the animal learned a general "
   "rule or just a specific response."),
  ("Theory of mind",
   "The ability to attribute knowledge or intentions to others; a contested and carefully "
   "tested question in animal research."),
 ],
 focus=[
  dict(title="Perception and attention",
       description="What animals can detect and what they attend to, including senses "
                   "humans do not share, and how sensory worlds differ between species.",
       source=REF["american_psychological_association"]),
  dict(title="Learning and memory",
       description="How animals acquire, store, and use information, and what learning "
                   "experiments reveal about the mechanisms behind it.",
       source=REF["international_journal_comparative"]),
  dict(title="Problem-solving and reasoning",
       description="How animals handle novel problems, use tools, plan, or draw "
                   "inferences, and how researchers design tasks that test this without "
                   "over-reading the results.",
       source=REF["international_journal_comparative"]),
  dict(title="Comparison across species",
       description="Comparing cognitive abilities across a wide phylogenetic range to "
                   "understand how cognition evolved and which abilities are shared or "
                   "distinct.",
       source=REF["american_psychological_association"]),
 ],
 questions=[
  ("What can this animal perceive, and what does it attend to?",
   "Through discrimination tasks where the animal is rewarded for responding to one "
   "stimulus and not another, mapping the threshold at which it can no longer tell them "
   "apart."),
  ("How does it learn, and what does it remember?",
   "By controlled training and delayed-response tasks that vary the interval, the "
   "interference, and the amount of information the animal has to hold."),
  ("How does it solve a problem it has not seen before?",
   "By presenting genuinely novel tasks and analyzing the route to the solution, not just "
   "whether it was solved, since the path reveals more than the outcome."),
  ("Does the animal understand something, or has it just learned an association?",
   "By designing controls that rule out simpler explanations — transfer tests, novel "
   "configurations, and probe trials with no reward available."),
  ("Does this species have a sense of others' knowledge or intentions?",
   "Through tasks where the correct action depends on what a partner can or cannot see, "
   "with careful controls for cues the animal could be reading instead."),
  ("What does comparing species tell us about how cognition evolved?",
   "By running comparable tasks across distantly related species and asking whether "
   "shared abilities reflect common ancestry or independent evolution."),
 ],
 responsibilities=[
  "Design cognitive tasks and controlled experimental procedures.",
  "Train and test animals under standardized conditions.",
  "Analyze performance data and evaluate competing explanations.",
  "Publish findings and communicate carefully about what results do and do not show.",
 ],
 knowledgeSkills=[
  "Experimental psychology and research design",
  "Learning theory and cognitive testing methods",
  "Statistics and data analysis",
  "Animal handling, training, and welfare",
  "Careful scientific reasoning about interpretation",
 ],
 settings=[
  "University psychology and biology laboratories",
  "Zoos, aquariums, and research facilities",
  "Field research programs",
  "Companion-animal research settings",
 ],
 realities=[
  "This is the most graduate-degree-dependent area on the site. Independent research "
   "effectively requires a Ph.D.",
  "Academic positions are limited relative to the number of people trained for them.",
  "Undergraduate research is often available, because cognitive tasks need many hands to "
   "run.",
  "Experiments are slow, and ambiguous or negative results are ordinary.",
  "Overclaiming is treated as a serious error here. Learning to say what a result does "
   "not show is part of the training.",
 ],
 careers=[
  "Comparative cognition researcher",
  "Animal learning researcher",
  "Animal communication researcher",
  "Animal behavior research assistant / technician",
  "University professor",
  "Research scientist / principal investigator",
 ],
 variations=[
  dict(label="Two traditions",
       description="Animal cognition tends to come through biology and behavioral "
                   "science; comparative psychology comes through psychology departments "
                   "and has its own society history and journals. They study much the "
                   "same thing with different emphases and vocabularies.",
       source=REF["american_psychological_association"]),
  dict(label="Species",
       description="Work ranges across primates, birds, dogs, marine mammals, and "
                   "invertebrates, and in recent decades has broadened well beyond the "
                   "traditional laboratory species.",
       ),
  dict(label="Setting",
       description="Cognition research happens in university laboratories, at zoos and "
                   "aquariums, at field sites, and increasingly with companion animals.",
       ),
  dict(label="Interpretation",
       description="A central and ongoing debate in the field concerns when a result "
                   "reflects reasoning and when a simpler associative explanation "
                   "suffices. Learning to hold that question carefully is part of the "
                   "training.",
       ),
 ],
 programCodes=["UNE-AB", "UNE-AN", "UMA-BIO"],
 related=["animal-behavior", "animal-welfare", "zoology", "anthrozoology"],
 references=["american_psychological_association", "international_journal_comparative", "animal_behavior_society2"],
)

area(
 id="animal-welfare",
 title="Animal Welfare Science",
 short="How to measure what an animal's life is actually like, and use that evidence to "
        "improve it.",
 bigPicture="Animal welfare science asks how an animal's life is going and how anyone "
             "could tell. It replaces impression with measurement: behavior, body "
             "condition, stress physiology, health records, and what an animal will work "
             "to get. Those findings then meet budgets, staffing, and safety rules, which "
             "is why the field puts as much effort into getting evidence implemented as "
             "into producing it. It applies wherever animals are kept — farms, "
             "laboratories, homes, shelters, zoos — and increasingly to wild animals too.",
 terms=[
  ("Welfare",
   "The physical and mental state of an animal, including both health and how the animal "
   "experiences its situation."),
  ("Welfare indicator",
   "A measurable sign — behavioral, physiological, or health-related — used to assess "
   "welfare, which must be validated before it is trusted."),
  ("Preference test",
   "Letting an animal choose between options to find out what it prefers."),
  ("Motivation test",
   "Measuring how much work an animal will do for access to something, as an indicator of "
   "how much it matters to the animal."),
  ("Enrichment",
   "Changes to environment or routine that give animals more opportunity to perform "
   "behaviors they are motivated to perform."),
  ("Five Domains",
   "A widely used framework for structured welfare assessment covering nutrition, "
   "environment, health, behavior, and mental state."),
  ("Capacity for care",
   "In sheltering, the number of animals an organization can house at an acceptable "
   "welfare standard given its actual staff and space."),
 ],
 focus=[
  dict(title="Measuring welfare",
       description="Developing and validating indicators of welfare from behavior, "
                   "physiology, health, and productivity, so that claims about how an "
                   "animal is doing rest on evidence, not impression.",
       source=REF["science_animal_welfare"]),
  dict(title="Housing, handling, and management",
       description="Testing how enclosure design, group composition, handling, transport, "
                   "and routine procedures affect welfare, and translating findings into "
                   "practice.",
       source=REF["journal_applied_animal"]),
  dict(title="Behavioral needs and enrichment",
       description="Identifying what animals are motivated to do and designing "
                   "environments and routines that let them do it, then measuring whether "
                   "the intervention worked.",
       source=REF["international_society_applied"]),
  dict(title="Welfare across settings",
       description="The same framework is applied in laboratory, farm, companion, "
                   "shelter, zoo, and wild contexts, and the constraints differ sharply "
                   "between them.",
       source=REF["science_animal_welfare2"]),
 ],
 questions=[
  ("How do we know whether this animal is doing well?",
   "By combining behavioral indicators, physiological measures, health records, and body "
   "condition, since no single measure captures welfare on its own."),
  ("Which indicators actually track welfare, and which only look like they do?",
   "By validating candidate measures against conditions already known to be better or "
   "worse, and discarding indicators that fail to discriminate."),
  ("What does this animal want, and how strongly?",
   "Through preference tests and motivation studies where the animal works for access to "
   "a resource, with the effort it will expend as the measure of how much it matters."),
  ("Does this change in housing, handling, or routine improve outcomes?",
   "By measuring before and after, ideally with a comparison group, and pre-specifying "
   "which indicators count so the result is not chosen afterward."),
  ("How do welfare goals trade off against cost, safety, or other constraints?",
   "By costing options explicitly and being clear about which part is evidence and which "
   "part is a value judgment about acceptable trade-offs."),
  ("Is a welfare problem systemic or specific to this animal?",
   "By assessing across the whole group and over time, since a single distressed animal "
   "and a poorly designed system call for different responses."),
 ],
 responsibilities=[
  "Conduct welfare assessments using validated behavioral and physiological measures.",
  "Design and evaluate enrichment, housing, or handling interventions.",
  "Write and review protocols, standards, and welfare policies.",
  "Train staff and communicate findings to people who make day-to-day decisions.",
 ],
 knowledgeSkills=[
  "Behavioral observation and welfare assessment methods",
  "Physiology, health, and stress measurement",
  "Experimental design and statistics",
  "Ethics and applied reasoning about trade-offs",
  "Training, communication, and protocol writing",
 ],
 settings=[
  "Universities and research institutes",
  "Zoos, aquariums, and sanctuaries",
  "Shelters and rescue organizations",
  "Farms, laboratories, and industry",
 ],
 realities=[
  "Coordinator and specialist roles exist inside institutions, and they are a route into "
   "this work that does not require a doctorate.",
  "Research positions generally do require graduate study.",
  "Those institutional roles often carry limited formal authority. Influence comes "
   "through evidence and relationships.",
  "The work regularly involves situations that cannot be fully fixed within existing "
   "resources.",
  "Standards and terminology move as the science advances, so what you learn will need "
   "updating.",
 ],
 careers=[
  "Animal welfare scientist",
  "Animal welfare / behavior coordinator",
  "Zoo / aquarium welfare specialist",
  "Behavioral husbandry specialist",
  "Enrichment coordinator / specialist",
  "Shelter behavior specialist / coordinator",
  "M.S. / Ph.D. in animal welfare science",
 ],
 variations=[
  dict(label="Science and advocacy are not the same thing",
       description="Welfare science produces evidence about how animals fare; what should "
                   "be done about it involves values, economics, and policy. The field is "
                   "explicit that both matter and that debate is part of scientific "
                   "progress, but they are different activities and conflating them "
                   "weakens both.",
       source=REF["science_animal_welfare"]),
  dict(label="Setting",
       description="Farm, laboratory, companion, shelter, zoo, and wild-animal welfare "
                   "each have distinct literatures, constraints, and professional "
                   "communities.",
       ),
  dict(label="Shelter and companion welfare",
       description="Population welfare in shelters, length of stay, capacity for care, "
                   "and adoption outcomes form a substantial applied strand, sitting "
                   "alongside the veterinary specialty of shelter medicine.",
       ),
  dict(label="Role type",
       description="Some positions are research; others are coordinator or specialist "
                   "roles inside an institution, responsible for assessment and program "
                   "design, not publication.",
       ),
 ],
 programCodes=["UMA-AS", "URI-AZ", "UNE-AB"],
 related=["animal-behavior", "zoo-aquarium-science", "veterinary-science", "animal-science"],
 references=["science_animal_welfare", "science_animal_welfare2", "journal_applied_animal", "international_society_applied"],
)

area(
 id="ecology",
 title="Ecology",
 short="The broad science of relationships among organisms and their environments—from "
        "individual responses and population change to communities, food webs, nutrients, "
        "and whole ecosystems.",
 bigPicture="Ecology asks how living systems work. Its subject can be a bacterial "
             "population, a plant community, a predator–prey relationship, a watershed, "
             "or the movement of energy and nutrients through an ecosystem. Ecologists "
             "build explanations from observation, experiments, long-term monitoring, and "
             "models. Their findings support conservation and natural-resource decisions, "
             "but the field itself is broader than wildlife and broader than management.",
 distinction=dict(
   title="Ecology and Wildlife Ecology & Management",
   summary="The fields share population biology, field sampling, statistics, and spatial "
           "analysis. What they centre on, and what they produce, are different.",
   items=[
    dict(label="Ecology",
         description="Examines relationships across living systems. A project might "
                      "center on microbes, plants, animals, species interactions, "
                      "nutrient cycles, disturbance, or ecosystem function. Typical "
                      "products include scientific explanations, models, monitoring "
                      "results, and environmental assessments."),
    dict(label="Wildlife Ecology & Management",
         description="Centers on free-ranging wild animals, their populations, and the "
                      "habitats and people affecting them. Typical products include "
                      "population estimates, species and habitat plans, harvest or "
                      "protection recommendations, permits, and evaluated management "
                      "actions."),
   ]
 ),
 terms=[
  ("Population",
   "A group of individuals of one species in a defined area, treated as a unit for study "
   "and management."),
  ("Community",
   "All the interacting species present in an area."),
  ("Ecosystem",
   "A community together with its physical environment, studied as a system of energy and "
   "material flows."),
  ("Trophic level",
   "An organism's position in the food chain — producer, herbivore, predator — used to "
   "describe energy flow."),
  ("Carrying capacity",
   "The population size an environment can sustain over time given available resources."),
  ("Long-term monitoring",
   "Repeated standardized measurement over many years, which is what makes it possible to "
   "distinguish a real trend from normal variation."),
 ],
 focus=[
  dict(title="Relationships across levels of life",
       description="How individual organisms respond to conditions, how populations "
                   "change, how species interact, and how those processes combine into "
                   "communities and ecosystems.",
       source=REF["ecological_society_america"]),
  dict(title="Ecosystems and energy flow",
       description="How energy and matter move through systems, and how disturbance, "
                   "nutrients, and climate shape what those systems can support.",
       source=REF["ecological_society_america"]),
  dict(title="Field measurement and monitoring",
       description="Designing sampling schemes, running surveys, and building long-term "
                   "datasets, since most ecological claims depend on how the data were "
                   "collected.",
       source=REF["ecological_society_america"]),
  dict(title="Applied and environmental ecology",
       description="Using ecological science in restoration, land management, "
                   "environmental assessment, and policy, which is where a large share of "
                   "the jobs are.",
       source=REF["ecological_society_america2"]),
 ],
 questions=[
  ("What determines where a species can live and how many there are?",
   "By combining occurrence surveys with environmental measurements, then modeling which "
   "conditions predict presence and testing predictions in new areas."),
  ("How do species interactions structure a community?",
   "Through removal or exclusion experiments, long-term observation, and comparison "
   "across sites where interacting species are present or absent."),
  ("How does energy or matter move through this system?",
   "By measuring inputs, outputs, and standing stocks, using isotopes and flux "
   "measurements to trace pathways instead of assuming them."),
  ("How will this system respond to disturbance or environmental change?",
   "By studying past disturbances, running manipulations where possible, and building "
   "models that project forward with stated uncertainty."),
  ("Is what we are seeing a real trend or normal variation?",
   "By analyzing long-term monitoring data with enough years to distinguish signal from "
   "noise, which is why long-running datasets are so valuable."),
  ("Did the restoration or management action work?",
   "By defining success measures before acting, monitoring treated and untreated areas, "
   "and continuing long enough for slow responses to appear."),
 ],
 responsibilities=[
  "Design and carry out field sampling, surveys, and monitoring.",
  "Analyze ecological data and model system behavior.",
  "Write technical reports, assessments, and peer-reviewed papers.",
  "Advise on management, restoration, or regulatory decisions.",
 ],
 knowledgeSkills=[
  "Population, community, and ecosystem ecology",
  "Field sampling design and identification skills",
  "Statistics, R, and data management",
  "geographic information systems (GIS) and spatial analysis",
  "Technical writing and reporting",
 ],
 settings=[
  "Universities and research institutes",
  "Environmental consulting firms",
  "State and federal agencies",
  "Conservation nonprofits and land trusts",
 ],
 realities=[
  "Statistical and data skills increasingly separate competitive candidates from the "
   "rest — and they are buildable as an undergraduate, deliberately.",
  "Early field positions are commonly seasonal and modestly paid. Stacking several is a "
   "normal way in.",
  "Expect coursework on plants, soils, and water. Animals are one part of the subject.",
  "A good deal of applied ecology is report writing and regulatory compliance.",
 ],
 careers=[
  "Field ecologist",
  "Research ecologist",
  "Ecological research technician",
  "Habitat restoration / ecological-monitoring specialist",
  "Environmental consultant — wildlife/ecology",
  "Environmental permitting / compliance biologist",
  "M.S. / Ph.D. in wildlife ecology / conservation",
 ],
 variations=[
  dict(label="Scale and subject",
       description="Ecological work moves among organisms, populations, communities, and "
                   "ecosystems. Plants, animals, microbes, soils, water, climate, and "
                   "disturbance can all be central parts of the same investigation.",
       source=REF["ecological_society_america"]),
  dict(label="There is a credential",
       description="the Ecological Society of America (ESA) runs a professional "
                   "certification program with a Certified Ecologist designation, "
                   "assessed on education and experience and backed by a code of ethics. "
                   "It is well known in consulting and agency work.",
       source=REF["ecological_society_america2"]),
  dict(label="Basic versus applied",
       description="Research ecology and applied ecology in consulting, restoration, or "
                   "agencies use the same science but differ in pace, output, and who the "
                   "client is.",
       ),
  dict(label="Quantitative demand",
       description="Ecology is a statistically heavy field, and comfort with data "
                   "analysis increasingly separates competitive candidates from the rest.",
       ),
 ],
 programCodes=["ME-ZOO", "ME-WE", "UMA-WEC", "URI-W"],
 related=["wildlife-ecology-management", "conservation-biology", "zoology"],
 references=["ecological_society_america", "ecological_society_america2"],
)

area(
 id="wildlife-ecology-management",
 title="Wildlife Ecology & Management",
 short="The science and professional management of free-ranging wild animals: estimating "
        "populations, understanding movement and habitat, and deciding how agencies and "
        "organizations should act.",
 bigPicture="Wildlife ecology and management applies ecological science to free-ranging "
             "animal populations and the habitats and human systems that shape them. It "
             "combines population estimation, movement and habitat analysis, field "
             "techniques, law, policy, and public decision-making. The work is organized "
             "around practical questions: whether a population is secure, what is causing "
             "change, which action is feasible, and how its results will be measured.",
 distinction=dict(
   title="Wildlife Ecology & Management and Ecology",
   summary="The fields share population biology, field sampling, statistics, and spatial "
           "analysis. What they centre on, and what they produce, are different.",
   items=[
    dict(label="Wildlife Ecology & Management",
         description="Centers on free-ranging wild animals, their populations, and the "
                      "habitats and people affecting them. Typical products include "
                      "population estimates, species and habitat plans, harvest or "
                      "protection recommendations, permits, and evaluated management "
                      "actions."),
    dict(label="Ecology",
         description="Examines relationships across living systems. A project might "
                      "center on microbes, plants, animals, species interactions, "
                      "nutrient cycles, disturbance, or ecosystem function. Typical "
                      "products include scientific explanations, models, monitoring "
                      "results, and environmental assessments."),
   ]
 ),
 terms=[
  ("Mark-recapture",
   "Marking a sample of animals, then using how many marked animals turn up later to "
   "estimate total population size."),
  ("Occupancy modeling",
   "Estimating what fraction of sites a species occupies while accounting for the times "
   "it was present but not detected."),
  ("Detection probability",
   "The chance of recording an animal that is actually there; ignoring it makes every "
   "count an underestimate."),
  ("Distance sampling",
   "A survey method that uses how far detected animals were from the observer to correct "
   "for animals missed at greater distances."),
  ("Telemetry",
   "Tracking animals using radio, satellite, or GPS devices to record where they go over "
   "time."),
  ("Home range",
   "The area an individual animal uses in its normal activities over a given period."),
  ("Human dimensions",
   "The social-science side of wildlife management: stakeholder attitudes, conflict, and "
   "public expectations."),
  ("Nongame species",
   "Wildlife not hunted or fished, which agencies still manage but which historically "
   "received less funding."),
 ],
 focus=[
  dict(title="Focal wildlife populations",
       description="Estimating abundance, survival, reproduction, distribution, and trend "
                   "for particular wild species using surveys, marking, and statistical "
                   "estimation.",
       source=REF["wildlife_society"]),
  dict(title="Habitat and land management",
       description="Evaluating what habitat a species needs and managing land to provide "
                   "it, including restoration, disturbance regimes, and working with "
                   "landowners.",
       source=REF["michigan_state_wildlife"]),
  dict(title="Species and program management",
       description="Setting and implementing management for game, nongame, endangered, "
                   "and invasive species, usually inside an agency framework with legal "
                   "mandates.",
       source=REF["michigan_state_wildlife"]),
  dict(title="Human dimensions",
       description="Wildlife management is as much about people as animals: stakeholders, "
                   "conflict, regulation, and public expectation are part of the "
                   "professional core, not an add-on.",
       source=REF["michigan_state_wildlife"]),
 ],
 questions=[
  ("How many are there, and is the number changing?",
   "Through survey designs that account for animals you fail to detect — mark-recapture, "
   "distance sampling, occupancy modeling — since raw counts almost always undercount."),
  ("What habitat does this population need, and is it available?",
   "By relating animal locations to measured habitat features, often with tracking data "
   "and remote sensing, then mapping where suitable habitat actually exists."),
  ("Where do these animals go, and when?",
   "By fitting tracking devices and analyzing movement paths for migration routes, home "
   "ranges, corridors, and barriers."),
  ("What management action would change the outcome, and at what cost?",
   "By modeling alternative scenarios against population objectives and comparing "
   "expected results to budget and staff realities."),
  ("Is this harvest or take level sustainable?",
   "By combining population estimates with survival and reproduction data in a population "
   "model, then setting limits with a margin for uncertainty."),
  ("How do people's interests and behavior shape what is possible?",
   "Through stakeholder surveys, public meetings, and human dimensions research, treating "
   "social data with the same rigor as biological data."),
 ],
 responsibilities=[
  "Plan and conduct field surveys, capture, and monitoring programs.",
  "Analyze population and habitat data and produce estimates with uncertainty.",
  "Write management plans, technical reports, and permit documentation.",
  "Coordinate with landowners, agencies, and the public.",
 ],
 knowledgeSkills=[
  "Population ecology and estimation methods",
  "Field survey, capture, and handling techniques",
  "Statistics, R, and geographic information systems (GIS)",
  "Wildlife law, policy, and agency process",
  "Communication with non-scientific audiences",
 ],
 settings=[
  "State and federal wildlife agencies",
  "Environmental consulting firms",
  "Conservation nonprofits",
  "Universities and research programs",
 ],
 realities=[
  "Certification is coursework-driven, which means the specific classes taken as an "
   "undergraduate matter more here than almost anywhere else — and that is something you "
   "can plan for now.",
  "Entry usually runs through seasonal technician work, often several seasons in "
   "different states.",
  "Writing, permitting, and public meetings are part of the job, not a distraction from it.",
  "Agency hiring follows budget cycles and can be slow or intermittent.",
 ],
 careers=[
  "Wildlife biologist",
  "Wildlife technician / biological science technician",
  "Wildlife diversity / nongame biologist",
  "Habitat / wildlife management biologist",
  "Natural-resource agency biologist",
  "Population ecologist",
  "Wildlife program manager",
  "Human-wildlife conflict specialist",
 ],
 variations=[
  dict(label="Degree names differ, requirements do not",
       description="Programs appear as Wildlife Ecology and Management, Wildlife Ecology, "
                   "Wildlife Biology, or Wildlife and Fisheries. What matters is whether "
                   "the coursework meets The Wildlife Society (TWS) certification "
                   "requirements, which many programs are explicitly designed around. TWS "
                   "has also moved away from requiring a wildlife-titled degree, focusing "
                   "on the courses taken instead.",
       source=REF["wildlife_society_tws"]),
  dict(label="Fisheries alongside wildlife",
       description="Many departments combine wildlife and fisheries, and some curricula "
                   "let students meet either The Wildlife Society or American Fisheries "
                   "Society requirements.",
       source=REF["umaine_wildlife_fisheries"]),
  dict(label="From evidence to management",
       description="Population estimates and habitat analyses feed into species plans, "
                   "land-management actions, harvest or protection rules, environmental "
                   "review, permits, and measures of whether an intervention worked.",
       ),
  dict(label="Certification levels",
       description="TWS offers an associate-level certification for those meeting "
                   "education requirements and a full certification once experience "
                   "requirements are met, renewable on a five-year cycle.",
       source=REF["wildlife_society_tws"]),
 ],
 programCodes=["ME-WE", "UMA-WEC", "URI-W", "URI-WZ"],
 related=["ecology", "conservation-biology", "wildlife-health"],
 references=["wildlife_society", "wildlife_society_tws", "michigan_state_wildlife", "umaine_wildlife_fisheries"],
)

area(
 id="conservation-biology",
 title="Conservation Biology",
 short="Deciding and carrying out what should be done about species and habitats, "
        "including the laws, funding, and human conflicts that shape those decisions.",
 bigPicture="Conservation biology asks what is being lost, why, and what can be done "
             "about it with the money and time available. It is biology plus everything "
             "that determines whether biology gets acted on: land ownership, law, funding "
             "cycles, and the people who live alongside the species in question. The "
             "field has never claimed to be neutral — it exists because its practitioners "
             "think biodiversity loss is worth preventing. Keeping that commitment "
             "separate from the evidence is treated as a professional skill.",
 terms=[
  ("Biodiversity",
   "The variety of life at all levels — genetic, species, and ecosystem."),
  ("Population viability analysis",
   "Modeling a population forward under different assumptions to estimate its risk of "
   "extinction."),
  ("Conservation genetics",
   "Using genetic data to assess diversity, inbreeding, and connectivity, and to guide "
   "breeding and translocation decisions."),
  ("Inbreeding depression",
   "Reduced survival or reproduction caused by breeding between close relatives in a "
   "small population."),
  ("Translocation",
   "Deliberately moving animals to a new location, whether to reestablish or to reinforce "
   "a population."),
  ("Reintroduction",
   "Releasing animals into an area where the species previously occurred but has been lost."),
  ("Normative discipline",
   "A field that openly holds a goal — here, conserving biodiversity — which makes "
   "separating evidence from advocacy a professional skill."),
 ],
 focus=[
  dict(title="Threat assessment and prioritization",
       description="Identifying what is declining, why, and where limited effort produces "
                   "the most benefit, which is as much a decision science problem as a "
                   "biological one.",
       source=REF["society_conservation_biology"]),
  dict(title="Population viability and genetics",
       description="Assessing whether small populations can persist, and using genetic "
                   "tools to understand connectivity, inbreeding, and recovery potential.",
       source=REF["society_conservation_biology"]),
  dict(title="Recovery and intervention",
       description="Designing and running reintroductions, translocations, habitat "
                   "protection, and species recovery programs, then monitoring whether "
                   "they worked.",
       source=REF["biological_conservation"]),
  dict(title="People, policy, and economics",
       description="The social, economic, ethical, and legal dimensions of conservation, "
                   "including conflict, land use, and the machinery through which "
                   "decisions actually get made.",
       source=REF["biological_conservation"]),
 ],
 questions=[
  ("What is declining, and what is driving it?",
   "By assembling trend data from monitoring and museum records, then testing candidate "
   "drivers against the spatial and temporal pattern of decline."),
  ("Can this population persist, and under what conditions?",
   "Through population viability analysis, projecting forward under different survival, "
   "reproduction, and threat scenarios to estimate extinction risk."),
  ("Is this population genetically healthy?",
   "By sampling genetic markers to assess diversity, inbreeding, and connectivity with "
   "other populations, which often reveals problems that counting individuals misses."),
  ("Which intervention gives the most benefit for the resources available?",
   "By costing options and comparing expected gains explicitly, since the binding "
   "constraint is almost always money and staff, not knowledge."),
  ("Did the reintroduction work?",
   "By monitoring released animals for survival, reproduction, and establishment over "
   "years, with success defined as a self-sustaining population, not survival to release."),
  ("Who decides, who is affected, and how does that shape what is possible?",
   "Through stakeholder analysis, interviews, and reading the legal and funding "
   "structures, because a biologically sound plan that no one will implement changes "
   "nothing."),
 ],
 responsibilities=[
  "Assess species status and threats using field and analytical evidence.",
  "Design, implement, and evaluate conservation interventions.",
  "Prepare plans, proposals, and regulatory documentation.",
  "Work with communities, landowners, agencies, and funders.",
 ],
 knowledgeSkills=[
  "Population biology and conservation genetics",
  "Field survey and monitoring methods",
  "Statistics, geographic information systems (GIS), and modeling",
  "Environmental law, policy, and funding mechanisms",
  "Negotiation, facilitation, and writing",
 ],
 settings=[
  "Conservation nonprofits and NGOs",
  "State, federal, and international agencies",
  "Universities and research institutes",
  "Zoos, aquariums, and botanical institutions",
 ],
 realities=[
  "Social and political skill counts as much as biological skill in most positions, so "
   "strengths outside the lab are genuinely an asset here.",
  "Much of the work is grant-funded, and programs end when the funding does.",
  "Outcomes are slow and usually partial. Practitioners describe this as the hardest "
   "part of the job.",
  "Field-based entry roles are often seasonal and geographically demanding.",
 ],
 careers=[
  "Conservation biologist",
  "Endangered-species biologist",
  "Species recovery biologist",
  "Conservation NGO scientist / coordinator",
  "Conservation geneticist / wildlife genomicist",
  "Conservation delivery / habitat program coordinator",
  "Human dimensions / conservation social scientist",
  "Post-release monitoring biologist",
 ],
 variations=[
  dict(label="Watch the occupational label",
       description="Federal occupational data has a category called Conservation "
                   "Scientists that mostly covers soil, rangeland, and forest "
                   "conservation. It is not the same profession as conservation biology, "
                   "and salary or outlook figures taken from it describe different work. "
                   "This is a genuine trap when researching the field.",
       ),
  dict(label="Biology or science",
       description="Conservation biology is the established name, with a society and "
                   "journal behind it since the 1980s. Conservation science is a newer "
                   "and broader term some departments have adopted to signal the social "
                   "and economic dimensions. Both are in use; the older name will find "
                   "more programs.",
       source=REF["society_conservation_biology"]),
  dict(label="Science and advocacy",
       description="The field openly holds a normative goal, and practitioners are "
                   "expected to be able to separate what the evidence shows from what "
                   "they think should be done.",
       ),
  dict(label="Scale",
       description="Work runs from single-species recovery to landscape planning to "
                   "international policy, and these involve very different daily "
                   "activities.",
       ),
 ],
 programCodes=["URI-W", "UMA-WEC", "ME-WE", "URI-WZ"],
 related=["wildlife-ecology-management", "ecology", "environmental-education"],
 references=["society_conservation_biology", "biological_conservation"],
)

area(
 id="veterinary-science",
 title="Veterinary & Animal Health Sciences",
 short="Diagnosing and treating disease and injury in individual animals, and the "
        "clinical training that requires.",
 bigPicture="Veterinary medicine asks what is wrong with this animal and what can be "
             "done about it. The patient cannot describe the problem, the person paying "
             "has a limit, and the answer often has to be reached from a physical exam "
             "and a handful of tests. The Doctor of Veterinary Medicine (DVM) anchors the "
             "field, but a great deal of animal health work is done by technicians, "
             "nutritionists, pathologists, and laboratory staff who do not hold one.",
 terms=[
  ("Doctor of Veterinary Medicine (DVM)",
   "The professional doctorate required to practice veterinary medicine, with its own "
   "separate admissions process."),
  ("Veterinary technician",
   "A credentialed clinical professional who performs much of the hands-on nursing, "
   "laboratory, and anesthesia work, trained in far less time than a DVM."),
  ("Differential diagnosis",
   "The list of conditions that could explain what is being seen, worked through "
   "systematically toward the most likely one."),
  ("Board certification",
   "Advanced credentialing in a recognized specialty, earned through residency and "
   "examination after the DVM."),
  ("Shelter medicine",
   "A recognized veterinary specialty balancing individual care against population health "
   "and resource limits in sheltering organizations."),
  ("Biosecurity",
   "Procedures that prevent disease from entering, spreading within, or leaving a facility."),
  ("Pre-veterinary",
   "A set of prerequisite courses for veterinary school admission, completable within "
   "many majors; not itself a degree or credential."),
 ],
 focus=[
  dict(title="Clinical diagnosis and treatment",
       description="Examining animals, interpreting diagnostics, and delivering medical "
                   "or surgical care, with the practical constraint that the patient "
                   "cannot describe the problem.",
       source=REF["merck_veterinary_manual"]),
  dict(title="Preventive and population health",
       description="Vaccination, parasite control, nutrition, and biosecurity, and "
                   "managing health at the level of a herd, colony, or facility, not one "
                   "animal.",
       source=REF["merck_veterinary_manual"]),
  dict(title="Specialties and settings",
       description="Small animal, large animal, equine, exotic, zoo and wildlife, "
                   "laboratory animal, pathology, and shelter medicine are distinct "
                   "practice areas with their own training routes.",
       source=REF["american_veterinary_medical"]),
  dict(title="Support and technical roles",
       description="Veterinary technicians and technologists, assistants, and practice "
                   "staff perform much of the clinical work, with their own credentialing "
                   "and considerably shorter training.",
       source=REF["merck_veterinary_manual"]),
 ],
 questions=[
  ("What is wrong with this animal, and how do we know?",
   "By history, physical examination, and diagnostics — imaging, bloodwork, cytology — "
   "working from a differential list toward the most likely explanation."),
  ("What treatment is appropriate given the animal, the owner, and the resources?",
   "By weighing likely outcome, cost, and the animal's welfare, and presenting realistic "
   "options instead of only the ideal one."),
  ("Is this a problem in one animal or across the population?",
   "By reviewing records across the herd, colony, or facility for pattern, and sampling "
   "more broadly when one case suggests a shared cause."),
  ("How do we prevent this instead of treating it one animal at a time?",
   "Through vaccination, parasite control, nutrition, and biosecurity protocols, then "
   "auditing whether the protocol is actually being followed."),
  ("What are the ethical limits of what should be done here?",
   "By weighing prognosis, suffering, and quality of life against what intervention would "
   "cost the animal, which is a judgment the evidence informs but does not settle."),
  ("How do we know a treatment works?",
   "By reading the clinical evidence base critically, since much of veterinary practice "
   "rests on smaller trials than human medicine does."),
 ],
 responsibilities=[
  "Examine animals, order and interpret diagnostics, and deliver treatment.",
  "Perform or assist with surgery, anesthesia, and clinical procedures.",
  "Maintain medical records and comply with regulatory requirements.",
  "Communicate diagnoses, options, and costs to owners or managers.",
 ],
 knowledgeSkills=[
  "Anatomy, physiology, pharmacology, and pathology",
  "Clinical examination and diagnostic reasoning",
  "Surgical and anesthetic technique",
  "Animal handling and restraint",
  "Client communication and ethical decision-making",
 ],
 settings=[
  "Clinical practices and animal hospitals",
  "Shelters and community medicine programs",
  "Zoos, aquariums, and wildlife facilities",
  "Laboratories, industry, and government agencies",
 ],
 realities=[
  "Many rewarding animal-health careers require no DVM at all — technician, nutrition, "
   "pathology, laboratory, and practice management among them.",
  "Veterinary school admission is highly competitive, and the degree is expensive "
   "relative to typical starting salaries.",
  "Pre-veterinary preparation is a set of prerequisite courses. It is not a credential "
   "and it guarantees nothing.",
  "Clinical work carries real emotional weight, including euthanasia and cases limited "
   "by what an owner can pay.",
 ],
 careers=[
  "Zoo animal nutritionist / nutrition coordinator",
  "Wildlife disease / ecophysiology specialist",
  "University / laboratory research assistant",
  "Animal welfare / behavior coordinator",
 ],
 variations=[
  dict(label="The DVM is one route, not the area",
       description="Veterinary technicians, nutritionists, pathologists, laboratory "
                   "staff, and researchers all work in animal health without a DVM, with "
                   "substantially shorter and less competitive training paths.",
       ),
  dict(label="Shelter medicine",
       description="A recognized veterinary specialty, provisionally recognized in 2014 "
                   "and fully recognized in 2023, requiring practitioners to balance "
                   "individual animal care against population health, resource limits, "
                   "and community needs. It is a growing area with a small number of "
                   "board-certified specialists.",
       source=REF["american_veterinary_medical"]),
  dict(label="Wildlife and zoo practice",
       description="Zoo, wildlife, and exotic practice are small, competitive specialties "
                   "usually entered through internship and residency, not directly.",
       ),
  dict(label="Pre-vet is not a major",
       description="Pre-veterinary is a set of prerequisite courses that can be completed "
                   "within many majors. It is not itself a degree, and completing it "
                   "guarantees nothing about admission.",
       ),
 ],
 programCodes=["URI-AZ", "UMA-AS", "UMA-BIO"],
 related=["wildlife-health", "animal-science", "animal-welfare", "zoo-aquarium-science"],
 references=["merck_veterinary_manual", "american_veterinary_medical"],
)

area(
 id="wildlife-health",
 title="Wildlife Health / One Health",
 short="Health at the population scale, where wildlife, domestic animals, and people "
        "meet. Surveillance and investigation, not treating patients.",
 bigPicture="Wildlife health asks why free-ranging populations are getting sick, dying, "
             "or failing to thrive. Sometimes the answer is a pathogen. Often it is a "
             "contaminant, a nutritional shortfall, a habitat change, or several of those "
             "at once. The work happens at the scale of populations, not patients: "
             "sampling, necropsy, laboratory diagnosis, and surveillance designed to "
             "catch a problem before it shows up as a die-off.",
 terms=[
  ("Epidemiology",
   "The study of how disease is distributed in populations and what determines that "
   "distribution."),
  ("Surveillance",
   "Ongoing systematic collection of health data from a population so problems are "
   "detected early, before a visible die-off."),
  ("Zoonosis",
   "A disease that can pass between animals and people."),
  ("Spillover",
   "Transmission of a pathogen from one host species into another, such as from wildlife "
   "into livestock or people."),
  ("One Health",
   "An approach treating human, animal, and environmental health as connected and "
   "requiring coordinated work across all three."),
  ("Necropsy",
   "Post-mortem examination of an animal to determine cause of death and document findings."),
  ("Sentinel site",
   "A location monitored consistently over time as an early-warning indicator for a wider "
   "area."),
 ],
 focus=[
  dict(title="Disease surveillance and investigation",
       description="Detecting, diagnosing, and tracking disease in free-ranging "
                   "populations, including mortality events, emerging pathogens, and "
                   "long-running conditions.",
       source=REF["journal_wildlife_diseases"]),
  dict(title="Beyond pathogens",
       description="Toxic, nutritional, developmental, and physiological factors "
                   "affecting wild animal health, alongside contamination and "
                   "environmental stressors.",
       source=REF["journal_wildlife_diseases"]),
  dict(title="The wildlife, livestock, human interface",
       description="Zoonoses, spillover, and shared disease risk between wild animals, "
                   "domestic animals, and people, which is where One Health work "
                   "concentrates.",
       source=REF["wildlife_disease_association"]),
  dict(title="Health as more than absence of disease",
       description="An active effort within the field to define wildlife health in terms "
                   "of vulnerability, resilience, and sustainability, recognizing that "
                   "habitat loss, trade, land-use pressure, and climate change are "
                   "drivers alongside pathogens.",
       source=REF["toward_modernized_definition"]),
 ],
 questions=[
  ("What is causing mortality or decline in this population?",
   "By collecting carcasses, running necropsy and laboratory diagnostics, and comparing "
   "affected and unaffected animals instead of assuming the first pathogen found is the "
   "cause."),
  ("Is this pathogen moving between wildlife, livestock, and people?",
   "Through coordinated sampling across all three groups and genetic comparison of "
   "isolates to reconstruct who transmitted to whom."),
  ("How do we detect a problem early enough to act?",
   "By running ongoing surveillance — hunter-harvested samples, sentinel sites, mortality "
   "reporting — not waiting for a visible die-off."),
  ("How far and how fast will this spread?",
   "By fitting epidemiological models to observed cases with data on host density and "
   "movement, and testing what control measures would change."),
  ("Is this population healthy in a broader sense than absence of disease?",
   "By assessing body condition, stress physiology, reproduction, and contaminant load "
   "together, in line with the field's argument that health means more than not being "
   "infected."),
  ("Is a contaminant or nutritional factor involved instead of a pathogen?",
   "Through toxicology and tissue analysis alongside pathology, since non-infectious "
   "causes are easy to miss when the search starts with pathogens."),
 ],
 responsibilities=[
  "Conduct surveillance, sampling, and necropsy in field and laboratory settings.",
  "Diagnose and characterize disease and other health threats.",
  "Analyze epidemiological data and report findings to agencies.",
  "Coordinate across wildlife, veterinary, agricultural, and public health bodies.",
 ],
 knowledgeSkills=[
  "Epidemiology and disease ecology",
  "Pathology, microbiology, and parasitology",
  "Field sampling, necropsy, and biosafety",
  "Statistics and spatial analysis",
  "Cross-agency coordination and reporting",
 ],
 settings=[
  "State and federal wildlife and agriculture agencies",
  "Diagnostic and research laboratories",
  "Universities and research institutes",
  "International and public health organizations",
 ],
 realities=[
  "Entry routes are unusually varied: veterinary medicine, epidemiology, ecology, and "
   "laboratory diagnostics all lead here.",
  "Most positions still require graduate or veterinary training.",
  "The work involves necropsy, biosafety protocols, and occasionally large mortality "
   "events.",
  "Funding and attention spike during outbreaks and recede between them.",
  "Findings feed policy decisions, which brings scrutiny and deadlines.",
 ],
 careers=[
  "Wildlife disease / ecophysiology specialist",
  "Wildlife biologist",
  "Natural-resource agency biologist",
  "University / laboratory research assistant",
  "Research scientist / principal investigator",
 ],
 variations=[
  dict(label="Health versus disease",
       description="The older framing of the field is wildlife disease; the newer framing "
                   "is wildlife health, which is broader. The distinction is not "
                   "cosmetic: the disease framing shapes what gets funded and monitored, "
                   "and the field has published directly on the limits of defining health "
                   "as the absence of disease.",
       source=REF["toward_modernized_definition"]),
  dict(label="Entry routes",
       description="People arrive with a Doctor of Veterinary Medicine (DVM), with a "
                   "graduate degree in epidemiology or ecology, or through laboratory and "
                   "diagnostic pathways. It is not a veterinary-only field, though "
                   "veterinary training opens the most doors.",
       ),
  dict(label="One Health scope",
       description="One Health links human, animal, and environmental health. "
                   "Practitioners note that its emphasis has often been on wildlife as a "
                   "source of human infection rather than on wildlife health as an end in "
                   "itself.",
       source=REF["toward_modernized_definition"]),
  dict(label="Employer type",
       description="State and federal agencies, universities, diagnostic laboratories, "
                   "and international organizations all employ in this space.",
       ),
 ],
 programCodes=["ME-WE", "UMA-WEC", "URI-W"],
 related=["veterinary-science", "wildlife-ecology-management", "wildlife-rehabilitation", "ecology"],
 references=["wildlife_disease_association", "journal_wildlife_diseases", "toward_modernized_definition"],
)

area(
 id="animal-science",
 title="Animal Science",
 short="The biology, care, management, and use of domesticated animals, traditionally "
        "with an agricultural emphasis.",
 bigPicture="Animal science asks how domesticated animals grow, reproduce, stay healthy, "
             "and are cared for, and how management changes those outcomes. It grew out "
             "of agriculture and livestock remain at its center, but what a given program "
             "actually covers varies more than the shared title suggests. Concentrations "
             "may emphasize production, companion animals, equine science, behavior, "
             "welfare, nutrition, biotechnology, or pre-veterinary preparation.",
 senses=dict(
   title="Three things called “animal science”",
   summary="The same phrase is used for an occupation, a degree, and a general idea. They "
           "point in different directions, so it is worth knowing which one a page, a "
           "person, or a program means.",
   items=[
    dict(label="The occupation",
         description="Federal labor statistics count about 3,100 animal scientists in "
                      "the United States, with a median wage near $68,930. The work is "
                      "mostly graduate-level research on the nutrition, genetics, "
                      "reproduction, and management of domesticated animals, carried out "
                      "at universities and in the feed, genetics, and pharmaceutical "
                      "industries. For comparison, the same data counts roughly 18,120 "
                      "zoologists and wildlife biologists.",
         source=REF["bls_oews_animal"]),
    dict(label="The degree",
         description="A B.S. in Animal Science is a container whose contents are set by "
                      "the concentration inside it. The science is real and rigorous, and "
                      "the degree is a common route toward veterinary school, but its "
                      "foundations are agricultural and the required hands-on coursework "
                      "often involves livestock. Two programs sharing the title can be "
                      "built very differently."),
    dict(label="The everyday phrase",
         description="Most people who say they are interested in animal science mean "
                      "science about animals in general. That interest is broader than "
                      "this field: it runs through behavior, welfare, ecology, wildlife, "
                      "zoo and aquarium work, veterinary medicine, and more. If that is "
                      "the sense you mean, this guide is one option among many, not the "
                      "place to start."),
   ]
 ),
 distinction=dict(
   title="Animal Science and Animal Behavior",
   summary="Both are animal-related degrees and they are routinely confused with each "
           "other — one program page answers the question directly, saying animal science "
           "and animal behavior are not the same. They differ in which animals they "
           "centre on, which questions they ask, and which departments house them.",
   source=REF["university_new_england"],
   items=[
    dict(label="Animal Science",
         description="Centres on domesticated animals — livestock, horses, and companion "
                      "species — and on how nutrition, genetics, reproduction, and "
                      "management shape their health, growth, and productivity. Usually "
                      "housed in agriculture or veterinary science departments. Typical "
                      "products include feeding and breeding programmes, husbandry "
                      "protocols, and health and production records."),
    dict(label="Animal Behavior / Ethology",
         description="Centres on what animals do and why, across wild and domesticated "
                      "species alike. Usually housed in biology, psychology, or "
                      "behavioural science departments. Typical products include "
                      "behavioural data and ethograms, training and enrichment plans, and "
                      "published findings on what causes a behaviour and what it "
                      "accomplishes."),
   ]
 ),
 terms=[
  ("Husbandry",
   "The day-to-day practice of keeping animals: feeding, housing, handling, breeding, and "
   "health monitoring."),
  ("Production animals",
   "Animals raised for food, fiber, or other products; the historical center of the "
   "discipline."),
  ("Ruminant",
   "An animal such as cattle, sheep, or goats with a multi-chambered stomach that "
   "ferments plant material."),
  ("Breeding value",
   "An estimate of the genetic merit an animal would pass to its offspring, calculated "
   "from pedigree and performance records."),
  ("Heritability",
   "The proportion of variation in a trait within a population that is due to genetic "
   "differences."),
  ("Extension",
   "University outreach that delivers research-based information directly to producers "
   "and the public."),
  ("Concentration",
   "A defined track within a major that determines much of the required coursework; the "
   "main reason two same-named degrees can differ so much."),
 ],
 focus=[
  dict(title="Nutrition, physiology, and health",
       description="Nutrition connects feed composition and digestion to growth, "
                   "reproduction, immunity, health, and performance. Physiology explains "
                   "how animals use those nutrients and respond to management and "
                   "environmental conditions.",
       source=REF["onet_occupational_information"]),
  dict(title="Genetics, breeding, and reproduction",
       description="Genetics and breeding use pedigrees, performance records, and genomic "
                   "information to select traits. Reproductive science includes "
                   "fertility, gestation, birth, reproductive technologies, and "
                   "management of breeding animals.",
       source=REF["onet_occupational_information"]),
  dict(title="Husbandry and production systems",
       description="Husbandry systems organize feeding, housing, sanitation, handling, "
                   "breeding, health monitoring, and recordkeeping. Production science "
                   "evaluates how those systems affect animals, workers, resources, food, "
                   "and farm outcomes. This is the part of the field that most directly "
                   "reflects its agricultural origins, and in many programs it is where "
                   "the required hands-on coursework happens.",
       source=REF["american_society_animal"]),
  dict(title="Behavior, welfare, and animal management",
       description="Behavior and welfare inform handling, housing, social management, "
                   "enrichment, transport, and routine care. Animal managers use these "
                   "observations with health and production data to adjust practices.",
       source=REF["onet_occupational_information"]),
 ],
 questions=[
  ("What nutrition best supports animal health, growth, or performance?",
   "Through controlled feeding trials comparing formulated diets, with intake, growth, "
   "health, and product measures recorded against a control group."),
  ("How do genetics and breeding influence traits and health?",
   "By analyzing pedigrees and performance records, increasingly with genomic markers, to "
   "estimate how much of a trait is heritable and predict breeding value."),
  ("How do housing, handling, or management affect welfare and behavior?",
   "By comparing systems using behavioral observation, physiological stress measures, "
   "health records, and productivity together."),
  ("Why is reproduction failing in this group?",
   "By working through nutrition, body condition, hormone profiles, timing, and "
   "management practice systematically instead of fixing on the first plausible cause."),
  ("Is this practice economically viable as well as sound?",
   "By costing inputs against outcomes, since a practice that improves animals but "
   "bankrupts the operation will not be adopted."),
  ("How can reproductive, production, or health outcomes be managed responsibly?",
   "By setting protocols against published standards, recording outcomes, and auditing "
   "whether practice matches the written protocol."),
 ],
 responsibilities=[
  "Provide or supervise feeding, handling, husbandry, health observation, and "
   "recordkeeping.",
  "Collect and analyze nutrition, reproduction, growth, health, behavior, or welfare data.",
  "Implement management, breeding, research, or quality-assurance protocols.",
  "Communicate with veterinarians, producers, researchers, caregivers, and regulatory "
   "personnel.",
 ],
 knowledgeSkills=[
  "Anatomy, physiology, nutrition, and reproduction",
  "Genetics, microbiology, and animal health",
  "Husbandry, handling, and welfare",
  "Statistics and experimental methods",
  "Management, records, biosecurity, and communication",
 ],
 settings=[
  "Farms, equine facilities, kennels, and animal-care operations",
  "Universities and research laboratories",
  "Feed, genetics, pharmaceutical, and agricultural organizations",
  "Zoos, shelters, veterinary, and companion-animal programs",
 ],
 realities=[
  "Concentrations are the steering wheel. Behavior, welfare, and pre-veterinary paths "
   "exist inside this degree if you choose them deliberately.",
  "Agricultural and livestock coursework is central in many programs, including ones "
   "whose concentrations point elsewhere.",
  "Program titles are not stable. Departments rename majors between catalog years, so "
   "trust the current curriculum sheet over the name.",
  "Hands-on work is physical, scheduled around animals, and subject to biosecurity rules.",
  "Pre-veterinary preparation is not a veterinary degree and not a guarantee of admission.",
 ],
 careers=[
  "Animal scientist",
  "Animal welfare / behavior coordinator",
  "Service-dog / assistance-animal trainer",
  "Animal collection / management specialist",
  "Zoo animal nutritionist / nutrition coordinator",
  "University / laboratory research assistant",
 ],
 variations=[
  dict(label="Agricultural roots",
       description="Animal science developed as an agricultural discipline, and much of "
                   "its core science—nutrition, reproduction, genetics, herd health—was "
                   "built around production animals. The field's main professional "
                   "society still describes animal science as concerned with the science "
                   "and business of producing domestic livestock. That inheritance stays "
                   "visible in course titles, department names, and the farm facilities "
                   "many programs teach on, even in concentrations aimed at companion "
                   "animals or behavior. A program does not have to be agricultural in "
                   "its goals to be agricultural in its foundations.",
       source=REF["american_society_animal"]),
  dict(label="How programs differ",
       description="Two degrees sharing this title can be built very differently. Some "
                   "are anchored in production agriculture and required livestock "
                   "coursework. Some are anchored in biomedical science and "
                   "pre-veterinary preparation, and say plainly that they offer limited "
                   "exotic or wildlife experience. Some leave real room for behavior, "
                   "welfare, or animals in zoos and aquariums. Departments also rename "
                   "majors and reshuffle concentrations between catalog years, so the "
                   "name on the degree is a weak signal. The current curriculum sheet and "
                   "course requirements are the only reliable way to tell two programs "
                   "apart.",
       ),
  dict(label="Species",
       description="Programs may concentrate on livestock, horses, companion animals, "
                   "laboratory animals, or a broader combination.",
       ),
  dict(label="Purpose",
       description="Careers can involve hands-on management, research, industry, welfare, "
                   "nutrition, breeding, extension, or veterinary preparation.",
       ),
  dict(label="Animal contact",
       description="Farm and management roles may be hands-on; laboratory, nutrition, "
                   "genetics, and industry roles may be less so.",
       ),
 ],
 programCodes=["UMA-AS", "URI-AZ", "UNE-AB", "UMA-BIO"],
 related=["animal-welfare", "zoo-aquarium-science", "veterinary-science", "animal-physiology"],
 references=["onet_occupational_information", "american_society_animal", "bls_oews_animal", "university_new_england"],
)

area(
 id="zoo-aquarium-science",
 title="Zoo & Aquarium Science",
 short="Daily care, behavior, welfare, and population management of wild species living "
        "permanently in human care.",
 bigPicture="Zoo and aquarium science is the daily work of keeping wild animals healthy "
             "in human care. Feeding, cleaning, health checks, enrichment, training "
             "animals to take part in their own medical procedures, and records detailed "
             "enough that the next keeper knows what changed overnight. Behind that sits "
             "population management run across institutions — which animals breed, which "
             "move where — so that a species held in many places is managed as one "
             "population, not dozens.",
 terms=[
  ("Accreditation",
   "Independent evaluation against professional standards, involving a detailed "
   "application and a multi-day on-site inspection by expert teams."),
  ("Animals in human care",
   "Current professional usage for animals living in managed facilities, replacing the "
   "older term captive animals."),
  ("Behavioral husbandry",
   "Using behavior and training knowledge as part of routine daily care, not a separate "
   "activity."),
  ("Cooperative care",
   "Training animals to participate voluntarily in their own medical and husbandry "
   "procedures."),
  ("Enrichment",
   "Environmental and routine changes that give animals opportunity to perform "
   "species-typical behaviors."),
  ("Studbook",
   "A record of every individual of a species in a managed population, with pedigree and "
   "transfer history."),
  ("Species Survival Plan (SSP)",
   "A cooperative breeding and management program run across accredited institutions for "
   "a single species."),
  ("Registrar",
   "The staff member responsible for animal records, permits, transfers, and regulatory "
   "compliance."),
 ],
 focus=[
  dict(title="Husbandry and daily care",
       description="Feeding, cleaning, enrichment, training, health observation, and "
                   "record-keeping. Keepers and aquarists provide direct care and are the "
                   "people who notice when something changes.",
       source=REF["association_zoos_aquariums3"]),
  dict(title="Behavior, training, and welfare",
       description="Behavioral husbandry, cooperative care training, enrichment design, "
                   "and welfare assessment, drawing directly on applied behavior and "
                   "welfare science.",
       source=REF["association_zoos_aquariums"]),
  dict(title="Population and collection management",
       description="Cooperative breeding programs, studbooks, transfers, and collection "
                   "planning coordinated across institutions, not facility by facility.",
       source=REF["michigan_state_zoo"]),
  dict(title="Conservation, research, and education",
       description="Field conservation support, in-house research, and public education "
                   "programs, which accredited institutions treat as part of their "
                   "mandate, not an extra.",
       source=REF["association_zoos_aquariums"]),
 ],
 questions=[
  ("What does this species need to thrive in this setting?",
   "By starting from wild natural history — diet, space, social structure, climate — and "
   "adapting it to what the facility can actually provide."),
  ("How do we know whether this animal's welfare is good?",
   "Through behavioral observation against a species ethogram, body condition and health "
   "records, and physiological measures where available."),
  ("Is this enrichment actually working?",
   "By recording behavior before, during, and after, and checking whether the target "
   "behavior changed, not whether the animal looked engaged."),
  ("How do we train an animal to take part in its own care?",
   "Through positive reinforcement training built in small approximations, so procedures "
   "like blood draws happen voluntarily instead of under restraint."),
  ("How should this population be managed across institutions over time?",
   "Using studbooks and population software to track pedigrees and recommend transfers "
   "and pairings that keep genetic diversity across the whole managed population."),
  ("What should visitors take away, and does the program achieve it?",
   "By setting explicit learning or behavior-change goals and evaluating with surveys and "
   "observation, instead of assuming exposure produces understanding."),
 ],
 responsibilities=[
  "Provide daily husbandry, feeding, cleaning, and health monitoring.",
  "Design and deliver enrichment and training programs.",
  "Keep detailed animal records and follow institutional protocols.",
  "Support conservation, research, and public education activities.",
 ],
 knowledgeSkills=[
  "Species husbandry and natural history",
  "Behavior, training, and enrichment",
  "Welfare assessment and record-keeping",
  "Safety, handling, and facility protocols",
  "Public speaking and visitor interaction",
 ],
 settings=[
  "Accredited zoos and aquariums",
  "Sanctuaries and wildlife parks",
  "Science centers and nature centers",
  "Related conservation and research programs",
 ],
 realities=[
  "Accreditation is a checkable signal, and it is one of the few quality filters "
   "available to someone choosing where to intern.",
  "Entry is competitive and usually runs through internships and volunteering; starting "
   "pay is low relative to the education required.",
  "The work is physical, scheduled around the animals, not the staff, and includes "
   "weekends, holidays, and weather.",
  "Much of the day is cleaning, food preparation, and record-keeping.",
  "Advancement is limited by how many positions any one institution has, and often means "
   "relocating.",
 ],
 careers=[
  "Zookeeper / animal-care specialist",
  "Aquarist / aquarium animal-care specialist",
  "Zoo / aquarium animal trainer",
  "Ambassador animal specialist / animal programs keeper",
  "Zoo behavioral-husbandry specialist",
  "Zoo / aquarium welfare specialist",
  "Zoo registrar / animal records & permits specialist",
  "Zoo animal curator",
  "SSP coordinator / studbook keeper",
  "Zoo / aquarium educator",
 ],
 variations=[
  dict(label="Accreditation matters",
       description="The Association of Zoos & Aquariums (AZA) is the independent "
                   "accrediting body, and its process involves a detailed application and "
                   "a multi-day on-site inspection by expert teams. Fewer than ten "
                   "percent of U.S. Department of Agriculture (USDA)-licensed wildlife "
                   "exhibitors are accredited. For someone choosing internships or a "
                   "first job, accreditation is one of the clearest available signals of "
                   "professional standards.",
       source=REF["association_zoos_aquariums"]),
  dict(label="Program shape",
       description="This appears as a degree concentration inside a zoology or biology "
                   "B.S., as a certificate alongside another major, and as a "
                   "community-college technical curriculum. Programs are typically built "
                   "around partnerships with accredited institutions and a required "
                   "internship.",
       source=REF["michigan_state_zoo"]),
  dict(label="Terminology",
       description="Current professional usage is animals in human care rather than "
                   "captive animals. The older phrasing still appears in some program "
                   "titles and course descriptions.",
       ),
  dict(label="Role range",
       description="Keeper and aquarist work, training, education, veterinary support, "
                   "records and registrar work, nutrition, curation, and research all sit "
                   "inside these institutions.",
       ),
 ],
 programCodes=["URI-AZ", "URI-WZ", "UMA-AS"],
 related=["animal-welfare", "animal-behavior", "environmental-education", "conservation-biology"],
 references=["association_zoos_aquariums", "association_zoos_aquariums2", "association_zoos_aquariums3", "michigan_state_zoo"],
)

area(
 id="wildlife-rehabilitation",
 title="Wildlife Rehabilitation",
 short="Temporary treatment of injured, sick, or orphaned wild animals, with release as "
        "the goal. Permit-bound and focused on the individual animal.",
 bigPicture="Wildlife rehabilitation is the care of sick, injured, and orphaned wild "
             "animals with the aim of putting them back. Every decision runs against that "
             "goal: an animal that recovers physically but loses its wariness of people "
             "usually cannot be released. The field is bounded by law as much as by "
             "biology — holding native wildlife requires a state permit, and migratory "
             "birds and certain other species carry federal requirements on top.",
 terms=[
  ("Rehabilitation",
   "Professional care of sick, injured, or orphaned wild animals with the goal of "
   "returning them to the wild."),
  ("Permit",
   "The legal authorization from a state agency, and for some species a federal one, that "
   "allows a person to hold native wildlife."),
  ("Certification",
   "A voluntary professional credential earned by continuing education and examination; "
   "separate from a permit and not a substitute for one."),
  ("Triage",
   "Rapid assessment on arrival to decide priority, treatment, and whether recovery to "
   "release is realistic."),
  ("Habituation",
   "An animal losing its natural wariness of humans, which usually makes release unsafe "
   "or impossible."),
  ("Conspecific",
   "Another animal of the same species; raising young with conspecifics helps prevent "
   "habituation and misdirected imprinting."),
  ("Soft release",
   "Releasing an animal gradually with continued support such as supplemental food and a "
   "familiar enclosure."),
 ],
 focus=[
  dict(title="Intake, triage, and assessment",
       description="Evaluating an animal on arrival, deciding what care is possible, and "
                   "making honest judgments about prognosis and whether release is "
                   "realistic.",
       source=REF["international_wildlife_rehabilitation"]),
  dict(title="Species-appropriate care",
       description="Housing, diets, and handling that differ substantially by species and "
                   "life stage, guided by published standards, not improvisation.",
       source=REF["international_wildlife_rehabilitation"]),
  dict(title="Minimizing habituation",
       description="Caring for an animal while limiting its association with humans, "
                   "since an animal that loses its wariness cannot usually be released.",
       ),
  dict(title="Release and outcome",
       description="Conditioning, timing, site selection, and post-release "
                   "considerations, with release as the measure of success, not survival "
                   "in care.",
       ),
 ],
 questions=[
  ("Can this animal recover well enough to survive in the wild?",
   "Through intake examination against species-specific criteria, veterinary assessment, "
   "and honest judgment about function the animal will need after release."),
  ("What does this species need at this life stage?",
   "By working from published rehabilitation standards and species care protocols instead "
   "of improvising, especially for diet and housing of young animals."),
  ("Is this animal orphaned, or should it be left alone?",
   "By asking the finder about circumstances and duration, since many apparently "
   "abandoned young are being cared for and removing them causes the harm."),
  ("How do we provide care without habituating the animal to people?",
   "By minimizing contact and noise, using visual barriers and species-appropriate "
   "housing, and raising young with conspecifics wherever possible."),
  ("Is release realistic, and if not, what is the right decision?",
   "By assessing residual disability against what the animal needs to survive, and "
   "choosing between placement and euthanasia instead of indefinite holding."),
  ("Where and when should this animal be released?",
   "By matching site to species and season, considering the original capture location, "
   "habitat quality, and whether the animal is conditioned for release."),
 ],
 responsibilities=[
  "Perform intake, triage, and daily care under permit conditions.",
  "Administer treatment in coordination with a veterinarian.",
  "Maintain detailed records required by permitting agencies.",
  "Handle public intake calls, education, and volunteer coordination.",
 ],
 knowledgeSkills=[
  "Species natural history, diets, and life stages",
  "Triage, handling, and basic clinical technique",
  "Permit requirements and regulatory recordkeeping",
  "Zoonotic disease awareness and safety practice",
  "Public communication and volunteer management",
 ],
 settings=[
  "Wildlife rehabilitation centers",
  "Home-based permitted operations",
  "Nature centers and sanctuaries",
  "Veterinary practices treating wildlife",
 ],
 realities=[
  "The credentials are reachable without a degree, and volunteering at a permitted "
   "center is an entry point available while still in high school.",
  "Paid positions, though, are limited. Much of the field runs on volunteers and "
   "seasonal staff.",
  "The legal framework is strict and varies by state. Unpermitted care of native "
   "wildlife is illegal.",
  "Mortality is routine, and euthanasia decisions are frequent.",
  "Intake is highly seasonal — spring and summer are far busier than the rest of the year.",
 ],
 careers=[
  "Wildlife rehabilitator",
  "Wildlife rehabilitation / release coordinator",
  "Wildlife rehabilitation program manager",
  "Reintroduction / release field technician",
  "Sanctuary animal caregiver",
 ],
 variations=[
  dict(label="Certification is not a license",
       description="the International Wildlife Rehabilitation Council (IWRC) offers "
                   "Associate Wildlife Rehabilitator and Certified Wildlife Rehabilitator "
                   "credentials, based on continuing education and an exam and renewable "
                   "every two years. Neither one authorizes you to hold wildlife. The "
                   "state permit does that, and in most places it requires apprenticeship "
                   "under a licensed rehabilitator plus a relationship with a "
                   "veterinarian.",
       source=REF["international_wildlife_rehabilitation2"]),
  dict(label="Standards exist",
       description="IWRC and the National Wildlife Rehabilitators Association jointly "
                   "publish standards covering ethics, species-specific care, housing, "
                   "and disinfection, so this is not a field where practice is left to "
                   "individual judgment.",
       source=REF["international_wildlife_rehabilitation"]),
  dict(label="Facility type",
       description="Work ranges from large centers with veterinary staff to small "
                   "home-based operations, with very different resources and daily "
                   "rhythms.",
       ),
  dict(label="Species focus",
       description="Many rehabilitators specialize in raptors, songbirds, small mammals, "
                   "marine mammals, or reptiles, and permits are often species-specific.",
       ),
 ],
 programCodes=["URI-W", "ME-WE", "URI-WZ"],
 related=["wildlife-health", "veterinary-science", "animal-welfare", "wildlife-ecology-management"],
 references=["international_wildlife_rehabilitation", "international_wildlife_rehabilitation2"],
)

area(
 id="environmental-education",
 title="Environmental Education & Interpretation",
 short="Helping the public understand animals and the science about them, in zoos, "
        "museums, parks, classrooms, and media.",
 bigPicture="This is the work of helping people understand animals and the science about "
             "them — on a trail, in front of a tank, in a classroom, or in writing. Good "
             "interpretation is built around one idea the audience takes away, tied to "
             "something they already care about, and it is judged on whether that "
             "happened, not on whether people enjoyed themselves. For many people it is "
             "the first paid job in this field; for some it becomes the career.",
 terms=[
  ("Interpretation",
   "The profession of connecting audiences to natural and cultural resources through "
   "programs built on a theme, not a list of facts."),
  ("Environmental education",
   "The broader field of teaching about environmental systems and issues, in schools and "
   "community settings as well as at sites."),
  ("Thematic programming",
   "Building a program around one central message so audiences leave with a takeaway "
   "instead of assorted facts."),
  ("Docent",
   "A trained volunteer who delivers educational programs or staffs interpretive stations."),
  ("Formative evaluation",
   "Testing a program while developing it so it can be improved before full delivery."),
  ("Science communication",
   "Translating research for general audiences without distorting what the research "
   "actually shows."),
  ("State science standards",
   "The required content for each grade level, which programs are mapped to so schools "
   "can justify the visit."),
 ],
 focus=[
  dict(title="Interpretation",
       description="Designing and delivering programs that connect visitors to natural "
                   "and cultural resources, built on an established body of theory about "
                   "how to make programs purposeful, relevant, and thematic instead of "
                   "merely informative.",
       source=REF["national_association_interpretation"]),
  dict(title="Program design and evaluation",
       description="Building curricula and public programs against learning goals, and "
                   "assessing whether audiences actually took away what was intended.",
       source=REF["north_american_association"]),
  dict(title="Science communication",
       description="Translating research for general audiences through writing, media, "
                   "exhibits, and public speaking without distorting it.",
       ),
  dict(title="Working with schools and communities",
       description="Partnering with teachers, districts, and community groups so programs "
                   "connect to curricula and reach people who would not otherwise come.",
       source=REF["north_american_association"]),
 ],
 questions=[
  ("What should this audience take away, and why does it matter to them?",
   "By identifying the audience first, then building the program around a single clear "
   "theme connected to something they already care about."),
  ("How do we know whether the program worked?",
   "Through evaluation designed in advance — pre- and post-questions, observation, "
   "follow-up — not on whether the audience seemed to enjoy it."),
  ("How do we stay accurate while making it accessible?",
   "By working from primary sources, having content reviewed by someone with subject "
   "expertise, and being explicit about uncertainty instead of smoothing it over."),
  ("How do we handle a contested or uncomfortable topic?",
   "By presenting evidence clearly, acknowledging genuine disagreement where it exists, "
   "and distinguishing what is known from what is debated."),
  ("Who is not being reached, and what would change that?",
   "By looking at who actually attends against who lives nearby, and asking "
   "non-participants directly what the barriers are."),
  ("How do we connect this to what teachers already have to cover?",
   "By mapping programs to state science standards and working with teachers on what fits "
   "their existing curriculum and schedule."),
 ],
 responsibilities=[
  "Develop and deliver interpretive programs, tours, and lessons.",
  "Create exhibit text, signage, and educational materials.",
  "Train and coordinate volunteers, docents, and seasonal staff.",
  "Evaluate programs and adjust based on results.",
 ],
 knowledgeSkills=[
  "Interpretive theory and program design",
  "Public speaking and audience management",
  "Solid grounding in the underlying science",
  "Writing for general audiences",
  "Evaluation and basic program assessment",
 ],
 settings=[
  "Parks, refuges, and public lands",
  "Zoos, aquariums, and nature centers",
  "Museums and science centers",
  "Nonprofits, schools, and community programs",
 ],
 realities=[
  "The National Association for Interpretation (NAI) certification is reachable before "
   "graduation, which makes this one of the few areas here where a meaningful credential "
   "is within reach now.",
  "Seasonal and part-time positions are common, particularly at the start.",
  "Pay is generally lower than in research or agency biology.",
  "The work is public-facing and performance-heavy. That suits some people and not others.",
  "Accuracy still matters. Being engaging is not a substitute for being right.",
 ],
 careers=[
  "Naturalist / interpretive educator",
  "Wildlife / environmental educator",
  "Zoo / aquarium educator",
  "Conservation outreach / program coordinator",
  "Science writer / communicator — biology and animals",
  "Museum / natural-history education or collections work",
 ],
 variations=[
  dict(label="There is a credential",
       description="The National Association for Interpretation offers Certified "
                   "Interpretive Guide and related certifications, delivered through "
                   "multi-day training courses. Many agencies and employers actively look "
                   "for them, and they are accessible early, which makes this one of the "
                   "few areas here where a meaningful credential is within reach before "
                   "graduation.",
       source=REF["national_association_interpretation"]),
  dict(label="Two umbrellas",
       description="Interpretation, associated with parks, nature centers, zoos, and "
                   "heritage sites, and environmental education, associated with schools, "
                   "curricula, and community programs, overlap heavily but have distinct "
                   "professional communities.",
       source=REF["north_american_association"]),
  dict(label="Not classroom teaching",
       description="This is not the same as K-12 science education, which requires "
                   "teacher licensure and follows a different route entirely.",
       ),
  dict(label="Entry point or destination",
       description="Many people pass through education roles on the way elsewhere; others "
                   "build entire careers in interpretation, program management, and "
                   "exhibit development.",
       ),
 ],
 programCodes=["URI-W", "ME-WE", "UMA-WEC"],
 related=["zoo-aquarium-science", "conservation-biology", "anthrozoology", "ecology"],
 references=["north_american_association", "national_association_interpretation"],
)

area(
 id="anthrozoology",
 title="Human–Animal Interaction / Anthrozoology",
 short="How people and animals affect each other, including assistance animals, working "
        "animals, and everyday companionship.",
 bigPicture="Anthrozoology studies the relationship between people and animals as a "
             "subject in its own right. What a service dog actually changes for its "
             "handler. Whether an animal-assisted program works, and how anyone would "
             "know. What the arrangement costs the animal. Why two people can look at the "
             "same species and feel completely differently about it. It draws on "
             "psychology, anthropology, sociology, veterinary medicine, and ethology, and "
             "it is small — most researchers hold a post in one of those departments.",
 terms=[
  ("Anthrozoology",
   "The scholarly study of interactions and relationships between humans and other "
   "animals, drawing on many disciplines."),
  ("Human-animal interaction (HAI)",
   "The same research field under the name most used by its professional society."),
  ("Human-animal bond",
   "The mutual relationship between a person and an animal, and the effects it has on both."),
  ("Animal-assisted intervention",
   "Structured use of animals in therapeutic, educational, or healthcare programs with "
   "defined goals."),
  ("Assistance animal",
   "An animal trained to perform specific tasks for a person with a disability."),
  ("Wash-out rate",
   "The proportion of animals entering an assistance-animal training program that do not "
   "complete it."),
  ("Relinquishment",
   "Surrender of an animal by its owner, studied for what it reveals about why "
   "relationships end."),
 ],
 focus=[
  dict(title="The human-animal bond",
       description="How relationships between people and animals form, what they provide "
                   "on both sides, and how they are affected by loss, conflict, or "
                   "change.",
       source=REF["international_society_anthrozoology"]),
  dict(title="Assistance and working animals",
       description="Service dogs, assistance animals, and working animals: selection, "
                   "training, effectiveness, and welfare of the animals doing the work.",
       ),
  dict(title="Animal-assisted intervention",
       description="Programs using animals in therapeutic, educational, and healthcare "
                   "settings, and the evidence about whether and how they help.",
       source=REF["anthrozoos"]),
  dict(title="Attitudes and society",
       description="How people think about animals, why attitudes differ across cultures "
                   "and contexts, and how those attitudes shape policy, food systems, and "
                   "pet keeping.",
       source=REF["anthrozoos"]),
 ],
 questions=[
  ("What do people and animals actually get from this relationship?",
   "Through surveys and interviews with people alongside behavioral and physiological "
   "measures on the animals, since self-report alone tells only one side."),
  ("Does this animal-assisted intervention work, and how would we know?",
   "By running controlled studies with comparison conditions and pre-specified outcomes, "
   "because much of the existing literature lacks controls."),
  ("What is the welfare cost to the animal in this arrangement?",
   "By assessing the animal's behavior and stress physiology during and after sessions, "
   "and checking whether it can opt out."),
  ("Why do attitudes toward animals differ so sharply between people and cultures?",
   "Through validated attitude scales, cross-cultural comparison, and qualitative work on "
   "how people explain their own views."),
  ("What makes an assistance animal succeed or wash out?",
   "By following cohorts from selection through training and placement, and relating "
   "outcomes to temperament, early experience, and training method."),
  ("How does the relationship change when it ends?",
   "Through studies of loss, relinquishment, and grief, using both interview data and "
   "standard psychological measures."),
 ],
 responsibilities=[
  "Design and conduct studies involving both human and animal participants.",
  "Collect and analyze survey, observational, and physiological data.",
  "Navigate ethical review for research involving people and animals.",
  "Publish and advise programs that place animals with people.",
 ],
 knowledgeSkills=[
  "Research methods in psychology and social science",
  "Animal behavior and welfare assessment",
  "Statistics and survey design",
  "Research ethics across human and animal subjects",
  "Interdisciplinary reading and writing",
 ],
 settings=[
  "Universities and research centers",
  "Assistance and service-animal organizations",
  "Healthcare, education, and therapy programs",
  "Shelters and animal welfare nonprofits",
 ],
 realities=[
  "The employment picture is mostly outside universities: assistance-animal "
   "organizations, intervention programs, shelters, and welfare nonprofits.",
  "Academic positions specifically in this field are scarce; most researchers are "
   "appointed in another department.",
  "Evidence quality varies widely across animal-assisted intervention research, and "
   "reading it critically is part of the training.",
  "Programs that place animals with people carry welfare obligations to the animal that "
   "are easy to underweight.",
  "There are few dedicated undergraduate degrees, so the path is usually assembled.",
 ],
 careers=[
  "Service-dog / assistance-animal trainer",
  "Companion-animal behavior researcher",
  "Animal behaviorist / applied animal behavior scientist",
  "Canine behavior consultant",
  "Science writer / communicator — biology and animals",
 ],
 variations=[
  dict(label="Two names, one field",
       description="Anthrozoology and human-animal interaction are used interchangeably "
                   "by the same professional community, and human-animal studies appears "
                   "as a third. The society describes its purpose as advancing "
                   "scholarship on human-animal interactions and relationships.",
       source=REF["international_society_anthrozoology"]),
  dict(label="Genuinely interdisciplinary",
       description="Published work comes from anthropology, archaeozoology, art and "
                   "literature, education, ethology, history, human medicine, psychology, "
                   "sociology, and veterinary medicine. There is no single home "
                   "department.",
       source=REF["anthrozoos"]),
  dict(label="Small field, real base",
       description="University-based centers exist in the United States, Europe, and "
                   "Australia, and coursework has become more common, but few "
                   "institutions offer a dedicated undergraduate degree. Most people "
                   "arrive through psychology, animal science, or veterinary routes.",
       ),
  dict(label="Where the jobs are",
       description="Research positions are limited. The larger employment picture is in "
                   "assistance-animal organizations, animal-assisted intervention "
                   "programs, shelters, and welfare nonprofits, where the research "
                   "informs practice.",
       ),
 ],
 programCodes=["UNE-AB", "UMA-AS", "UMA-BIO"],
 related=["animal-behavior", "animal-welfare", "environmental-education", "animal-cognition"],
 references=["international_society_anthrozoology", "anthrozoos"],
)

# ================================================================ build steps
KEY_ORDER = ["id", "title", "short", "bigPicture", "senses", "distinction", "terms",
             "focus", "questions", "responsibilities", "knowledgeSkills", "variations",
             "settings", "realities", "careers", "programs", "programCodes", "related",
             "references"]

PROSE_FIELDS = ["short", "bigPicture", "senses", "distinction", "terms", "focus",
                "questions", "responsibilities", "knowledgeSkills", "variations",
                "settings", "realities"]


def prose_of(area):
    """Every human-readable string in a guide, excluding urls and source pointers."""
    out = []

    def walk(obj):
        if isinstance(obj, str):
            out.append(obj)
        elif isinstance(obj, list):
            for x in obj:
                walk(x)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if k not in ("url", "source"):
                    walk(v)

    for k in PROSE_FIELDS:
        if k in area:
            walk(area[k])
    return " ".join(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ids = [a["id"] for a in AREAS]
    problems = []

    for a in AREAS:
        ordered = {k: a[k] for k in KEY_ORDER if k in a}
        prose = prose_of(ordered)

        titles = {r["title"] for r in ordered["references"]}
        checks = list(ordered["focus"]) + list(ordered["variations"])
        for blk in ("senses", "distinction"):
            if blk in ordered:
                checks.append(ordered[blk]); checks += ordered[blk]["items"]
        for item in checks:
            if item.get("source") and item["source"] not in titles:
                problems.append(f"{a['id']}: source not in references -> {item['source']}")

        for rel in ordered["related"]:
            if rel not in ids:
                problems.append(f"{a['id']}: related id not found -> {rel}")

        for c in ordered["programCodes"]:
            if c not in PROGRAMS:
                problems.append(f"{a['id']}: unknown program code -> {c}")

        # program codes are back-end identifiers and must not appear in prose
        for c in PROGRAMS:
            if re.search(rf"\b{re.escape(c)}\b", prose):
                problems.append(f"{a['id']}: program code in prose -> {c}")

        # acronyms must be spelled out somewhere in the same guide
        for acr, full in ACRONYMS.items():
            if re.search(rf"\b{re.escape(acr)}\b", prose) and full not in prose:
                problems.append(
                    f"{a['id']}: '{acr}' used but '{full}' never appears - "
                    f"spell it out at first use")

        (OUT / f"{a['id']}.json").write_text(
            json.dumps(ordered, indent=2, ensure_ascii=False) + "\n")

    (OUT / "index.json").write_text(
        json.dumps({"areas": [f"{i}.json" for i in ids]}, indent=2) + "\n")

    print(f"wrote {len(AREAS)} areas + index.json to {OUT}")
    print("validation problems:", len(problems))
    for p in problems:
        print("  -", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
