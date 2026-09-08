from __future__ import annotations
import json, sqlite3, re, os, hashlib, shutil
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
BASE_DATA=ROOT/'imports'/'legacy_site_data.json'
SCHEMA=ROOT/'database'/'schema.sql'
DB=ROOT/'database'/'careers.sqlite'
TODAY='2026-09-08'
DIM_KEYS=['behavior_cognition','welfare_husbandry','zoo_managed','wildlife_field','rehab_release','biology_mechanisms','conservation_habitat','quant_environment','research_science','education_comm']


def load_base():
    return json.loads(BASE_DATA.read_text(encoding='utf-8'))

D=load_base()

# --- Taxonomy ---
DOMAINS=[
('dm_behavior','Animal behavior, cognition & welfare','Behavioral science, welfare, training, enrichment, and applied behavior.'),
('dm_managed','Zoos, aquariums & managed animals','Animal care, husbandry, training, collection management, population management, research, and conservation within managed settings.'),
('dm_wildlife','Wildlife, rehabilitation & conservation','Field wildlife science, rehabilitation, release, species recovery, habitat, and wildlife management.'),
('dm_organismal','Organismal & evolutionary biology','Whole-animal biology, physiology, taxonomy, evolution, neuroethology, and natural history.'),
('dm_quant','Quantitative, environmental & agency science','GIS, statistics, ecological data, environmental consulting, restoration, and agency/resource work.'),
('dm_research','Research & academia','Research support, graduate research pathways, laboratories, independent science, and academic careers.'),
('dm_education','Education, outreach & communication','Interpretation, education, outreach, museums, collections, and science communication.'),
]
FAMILIES=[
('rf_behavior_research','dm_behavior','Behavioral research & cognition','Research on behavior, cognition, learning, communication, and comparative psychology.'),
('rf_applied_behavior','dm_behavior','Applied behavior & training','Science-based training, behavior modification, service-animal work, and applied behavior.'),
('rf_welfare_husbandry','dm_behavior','Welfare, enrichment & behavioral husbandry','Welfare assessment, enrichment, behavioral husbandry, and applied animal-care behavior.'),
('rf_shelter_companion','dm_behavior','Shelter & companion-animal behavior','Shelter behavior, companion-animal behavior, and complex behavior consulting.'),
('rf_animal_care','dm_managed','Animal care & husbandry','Daily care, keeper work, sanctuary care, and managed-animal husbandry.'),
('rf_aquatic_care','dm_managed','Aquatic animal care','Aquarist work and related aquatic animal care.'),
('rf_zoo_training','dm_managed','Zoo training & ambassador animal programs','Animal training and ambassador-animal care/education within zoological settings.'),
('rf_population','dm_managed','Conservation breeding & population management','Conservation breeding, population biology, studbooks, and SSP population-management work.'),
('rf_records_nutrition','dm_managed','Records, nutrition & collection operations','Animal records/permits, nutrition, and collection planning/operations.'),
('rf_zoo_science_leadership','dm_managed','Zoo research, conservation & leadership','Zoo/aquarium research, conservation coordination, collection leadership, and curation.'),
('rf_wildlife_tech','dm_wildlife','Wildlife field & technical work','Field technicians, monitoring, species surveys, and biological-science technical work.'),
('rf_wildlife_biology','dm_wildlife','Wildlife biology & management','Professional wildlife biology, nongame/diversity biology, and wildlife program work.'),
('rf_rehab','dm_wildlife','Wildlife rehabilitation & release','Wildlife rehabilitation, release coordination, and rehabilitation-center operations.'),
('rf_reintroduction','dm_wildlife','Species recovery & reintroduction','Release, reintroduction, post-release monitoring, and species recovery.'),
('rf_habitat','dm_wildlife','Habitat & conservation delivery','Habitat biology, restoration delivery, conservation planning, and refuge management.'),
('rf_movement','dm_wildlife','Movement, monitoring & spatial ecology','Movement ecology, telemetry, spatial ecology, and post-release monitoring.'),
('rf_wildlife_health','dm_wildlife','Wildlife health & ecophysiology','Wildlife disease, physiology, stress, and ecophysiology.'),
('rf_human_dimensions','dm_wildlife','Human-wildlife & social dimensions','Human-wildlife conflict and conservation social science.'),
('rf_taxon','dm_organismal','Taxon & natural-history specialists','Zoology and organismal specialties such as mammalogy, ornithology, and herpetology.'),
('rf_physiology','dm_organismal','Physiology & neuroethology','Animal physiology, neuroethology, and mechanisms of behavior.'),
('rf_evolution','dm_organismal','Evolutionary & ecological science','Evolutionary biology and broad ecological science involving animals.'),
('rf_gis','dm_quant','GIS, remote sensing & spatial analysis','GIS, remote sensing, spatial analysis, and geospatial ecology.'),
('rf_quant','dm_quant','Quantitative ecology & data science','Statistics, ecological modeling, data science, and quantitative ecology.'),
('rf_env_consult','dm_quant','Environmental consulting & compliance','Environmental consulting, permitting, regulatory, and compliance biology.'),
('rf_agency','dm_quant','Natural-resource agency & management','Agency biology, park/resource work, natural-resource management, and program management.'),
('rf_restoration','dm_quant','Restoration & ecological monitoring','Habitat restoration, ecological monitoring, and environmental field implementation.'),
('rf_research_support','dm_research','Research support & lab operations','Research assistants, technicians, laboratory managers, and research coordination.'),
('rf_grad','dm_research','Graduate research pathways','Research M.S./Ph.D. routes into advanced science.'),
('rf_independent_research','dm_research','Independent research & academia','Research scientists, principal investigators, and professors.'),
('rf_zoo_education','dm_education','Zoo/aquarium education','Zoo/aquarium education, interpretation, and public programs.'),
('rf_wildlife_education','dm_education','Wildlife interpretation & outreach','Wildlife/environmental education, naturalist work, and conservation outreach.'),
('rf_scicomm','dm_education','Science communication & museum work','Science writing, communication, natural-history museums, and collections.'),
]


def family_for(name, category):
    n=name.lower()
    if category.startswith('Animal behavior'):
        if any(k in n for k in ['welfare','husbandry','enrichment']): return 'rf_welfare_husbandry'
        if any(k in n for k in ['trainer','service-dog','behaviorist / applied']): return 'rf_applied_behavior'
        if any(k in n for k in ['shelter','companion']): return 'rf_shelter_companion'
        return 'rf_behavior_research'
    if category.startswith('Zoos'):
        if 'aquarist' in n: return 'rf_aquatic_care'
        if any(k in n for k in ['conservation-breeding']): return 'rf_population'
        if any(k in n for k in ['collection','curator','conservation coordinator','research coordinator']): return 'rf_zoo_science_leadership'
        if any(k in n for k in ['behavioral-husbandry','welfare','behavioral researcher']): return 'rf_welfare_husbandry'
        return 'rf_animal_care'
    if category.startswith('Wildlife'):
        if any(k in n for k in ['rehabilitator','rehabilitation / release coordinator']): return 'rf_rehab'
        if any(k in n for k in ['reintroduction','post-release','endangered-species']): return 'rf_reintroduction'
        if any(k in n for k in ['movement','spatial']): return 'rf_movement'
        if any(k in n for k in ['disease','ecophysiology']): return 'rf_wildlife_health'
        if 'human-wildlife' in n: return 'rf_human_dimensions'
        if 'habitat / wildlife management' in n: return 'rf_habitat'
        if 'technician' in n: return 'rf_wildlife_tech'
        return 'rf_wildlife_biology'
    if category.startswith('Organismal'):
        if any(k in n for k in ['physiologist','neuroethologist']): return 'rf_physiology'
        if 'evolutionary' in n or 'field ecologist' in n or 'ecological research' in n: return 'rf_evolution'
        return 'rf_taxon'
    if category.startswith('Quantitative'):
        if 'gis' in n or 'spatial analyst' in n: return 'rf_gis'
        if 'quantitative' in n or 'biometrician' in n: return 'rf_quant'
        if any(k in n for k in ['consultant','permitting','compliance']): return 'rf_env_consult'
        if 'restoration' in n or 'monitoring specialist' in n: return 'rf_restoration'
        return 'rf_agency'
    if category.startswith('Research'):
        if n.startswith('m.s.') or n.startswith('m.s. / ph.d.'): return 'rf_grad'
        if any(k in n for k in ['principal investigator','professor']): return 'rf_independent_research'
        return 'rf_research_support'
    if category.startswith('Education'):
        if 'zoo / aquarium educator' in n: return 'rf_zoo_education'
        if any(k in n for k in ['wildlife / environmental','naturalist','outreach']): return 'rf_wildlife_education'
        return 'rf_scicomm'
    return 'rf_research_support'


def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def role_kind(base):
    status=(base.get('details',{}).get('Market status','') or '').upper()
    if status.startswith('EDU') or 'Graduate study pathway' in base.get('educationBand',''): return 'education_path'
    if 'later career' in (base.get('educationBand','') or '').lower(): return 'later_career'
    if status.startswith('F'): return 'scientific_specialty'
    return 'career'

def evidence_status(base):
    status=(base.get('details',{}).get('Market status','') or '').upper()
    if status.startswith('E'): return 'verified_occupation_or_title'
    if status.startswith('R'): return 'verified_function_title_varies'
    if status.startswith('F'): return 'established_scientific_specialty'
    if status.startswith('EDU'): return 'education_path'
    return 'supported'

def career_stage(base):
    n=base['name'].lower(); e=(base.get('educationBand') or '').lower()
    if 'graduate study pathway' in e: return 'education'
    if 'later career' in e or any(k in n for k in ['curator','manager','principal investigator','professor']): return 'leadership'
    if any(k in n for k in ['technician','assistant','keeper','caretaker','caregiver','trainer','aquarist','educator','naturalist','rehabilitator']): return 'entry_or_early'
    if any(k in n for k in ['coordinator','specialist','scientist','biologist','ecologist','zoologist','mammalogist','ornithologist','herpetologist','physiologist','consultant']): return 'professional_or_specialist'
    return 'variable'

# New canonical career roles that broaden the existing scope without changing direction.
NEW_ROLES=[
{
'name':'Population biologist / zoo population management scientist','category':'Zoos, aquariums, sanctuaries & managed wildlife','family_id':'rf_population','role_kind':'scientific_specialty','market_status':'Established professional/scientific role; payroll titles vary','evidence_status':'verified_professional_role','description':'Uses demographic, genetic, and population analyses to assess managed conservation populations, forecast population trajectories, and develop breeding/transfer recommendations for zoo and aquarium populations.','educationBand':'B.S. + graduate study often useful','directContact':'Low / variable','career_stage':'professional_or_specialist','workTags':['Research','Data / statistics','Conservation','GIS / spatial'],'dims':[1.2,0.8,2.2,1.0,0.5,2.2,2.5,3.0,3.0,0.9],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'G','UMA-WEC':'C','UMA-AS':'C','ME-WE':'C','ME-ZOO':'G','URI-W':'C','URI-WZ':'C','URI-AZ':'C'},
'details':{'Typical work settings':'AZA population-management programs, zoological institutions, conservation science centers, universities.','Undergraduate preparation most useful':'Population biology, genetics, statistics, research design, data management, conservation biology, scientific writing.','Searchable job titles':'Population Biologist; Population Management Scientist; Wildlife Planning Manager; Population Management Researcher','Alternate names / terms':'Population management; demographic analysis; managed population planning','Typical education / progression':'Strong quantitative B.S. foundation; M.S./Ph.D. commonly useful for independent population-science roles.','O*NET / BLS proxy':'Biological Scientists / Zoologists-Wildlife Biologists (broad proxy)','Job outlook':'No dedicated federal occupation; use current postings and related biological-science benchmarks.','Salary context':'Use current postings, institutional salary data, and related biological-scientist benchmarks.'}},
{
'name':'SSP coordinator / studbook keeper','category':'Zoos, aquariums, sanctuaries & managed wildlife','family_id':'rf_population','role_kind':'professional_assignment','market_status':'Established AZA Animal Program leadership assignment','evidence_status':'verified_professional_assignment','description':'Coordinates an AZA Species Survival Plan or maintains a regional studbook, helping manage population records, breeding/transfer planning, and communication across participating institutions.','educationBand':'B.S. + substantial zoological experience','directContact':'Low / variable','career_stage':'professional_or_specialist','workTags':['Conservation','Data / statistics','Animal care'],'dims':[1.2,1.1,2.8,0.8,0.5,1.7,2.7,2.1,1.6,1.5],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'C','UMA-WEC':'C','UMA-AS':'C','ME-WE':'C','ME-ZOO':'C','URI-W':'C','URI-WZ':'S','URI-AZ':'S'},
'details':{'Typical work settings':'AZA-accredited institutions; work is commonly an added professional leadership responsibility rather than a standalone full-time job.','Undergraduate preparation most useful':'Animal management, conservation breeding, population biology, records/databases, statistics, communication.','Searchable job titles':'SSP Coordinator; SSP Program Leader; Studbook Keeper; Animal Program Leader','Alternate names / terms':'Species Survival Plan leadership; regional studbook','Typical education / progression':'Usually develops after professional zoo/aquarium experience; AZA training and institutional support are required for program-leader assignments.','Job outlook':'Professional assignment rather than a separately counted occupation.','Salary context':'Compensation is generally tied to the person’s primary zoo/aquarium position, not the SSP/studbook assignment itself.'}},
{
'name':'Zoo registrar / animal records & permits specialist','category':'Zoos, aquariums, sanctuaries & managed wildlife','family_id':'rf_records_nutrition','role_kind':'career','market_status':'Verified current market title','evidence_status':'verified_current_market','description':'Maintains animal records, permits, inventories, transfers, regulatory documentation, and institutional animal databases such as ZIMS; may coordinate transaction, training, enrichment, and diet records.','educationBand':'B.S.-accessible / experience-driven','directContact':'Low / variable','career_stage':'professional_or_specialist','workTags':['Data / statistics','Animal care','Conservation'],'dims':[0.7,1.0,2.6,0.5,0.3,0.7,1.2,2.3,1.0,1.3],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'C','UMA-WEC':'C','UMA-AS':'C','ME-WE':'C','ME-ZOO':'C','URI-W':'C','URI-WZ':'S','URI-AZ':'S'},
'details':{'Typical work settings':'Zoos, aquariums, wildlife centers, and conservation breeding institutions.','Undergraduate preparation most useful':'Animal biology/management, database skills, records management, permits/regulation, scientific writing, attention to detail.','Searchable job titles':'Registrar; Animal Registrar; Wildlife Records Specialist; Animal Records Coordinator','Alternate names / terms':'ZIMS registrar; animal records; permits and transactions','Typical education / progression':'B.S. in biology, zoology, animal science or related field plus records/database experience is common; specialized records training can be valuable.','Job outlook':'No dedicated O*NET occupation; validate through zoo/aquarium postings.','Salary context':'Use employer postings and institutional salary ranges rather than animal-caretaker proxies.'}},
{
'name':'Zoo animal nutritionist / nutrition coordinator','category':'Zoos, aquariums, sanctuaries & managed wildlife','family_id':'rf_records_nutrition','role_kind':'career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Plans, prepares, evaluates, and manages diets and food systems for zoological collections, often working with keepers, veterinarians, commissary staff, and animal-management teams.','educationBand':'B.S. + graduate study often useful','directContact':'Low / variable','career_stage':'professional_or_specialist','workTags':['Animal care','Research','Data / statistics'],'dims':[0.4,1.7,2.7,0.2,0.2,2.5,0.4,1.1,1.6,0.5],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'C','UMA-WEC':'N','UMA-AS':'S','ME-WE':'N','ME-ZOO':'C','URI-W':'N','URI-WZ':'C','URI-AZ':'S'},
'details':{'Typical work settings':'Zoo/aquarium nutrition departments, commissaries, conservation centers, research programs.','Undergraduate preparation most useful':'Animal physiology, nutrition, chemistry, biology, statistics, animal management, research methods.','Searchable job titles':'Animal Nutrition Coordinator; Zoo Nutritionist; Animal Nutrition Manager; Commissary Coordinator','Alternate names / terms':'Zoological nutrition; zoo commissary; animal diet management','Typical education / progression':'B.S. may support technician/coordinator work; specialized nutrition science and leadership can favor graduate study or substantial experience.','Job outlook':'No dedicated zoo-nutrition occupation; use employer postings and related animal-science benchmarks.','Salary context':'Use employer postings and related animal-science/nutrition benchmarks.'}},
{
'name':'Zoo / aquarium animal trainer','category':'Zoos, aquariums, sanctuaries & managed wildlife','family_id':'rf_zoo_training','role_kind':'career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Uses learning principles and positive-reinforcement training with zoo or aquarium animals for husbandry, cooperative medical behavior, presentations, enrichment, and welfare.','educationBand':'B.S.-accessible / experience-driven','directContact':'High','career_stage':'entry_or_early','workTags':['Animal care','Behavior / training','Education / public'],'dims':[2.8,2.8,3.0,0.5,0.2,1.5,0.6,0.4,1.4,1.8],
'support':{'UNE-AB':'S','UNE-AN':'S','UMA-BIO':'C','UMA-WEC':'N','UMA-AS':'C','ME-WE':'N','ME-ZOO':'C','URI-W':'C','URI-WZ':'S','URI-AZ':'S'},
'details':{'Typical work settings':'Aquariums, zoos, wildlife presentation programs, marine mammal teams, ambassador-animal programs.','Undergraduate preparation most useful':'Learning theory, animal behavior, husbandry, welfare, observation, communication, direct animal experience.','Searchable job titles':'Animal Trainer; Senior Trainer; Assistant Trainer; Marine Mammal Trainer; Behavior Trainer','Alternate names / terms':'Oceanarium trainer; pinniped trainer; animal behavior trainer','Typical education / progression':'B.S. and extensive hands-on training/husbandry experience are common; progression may include senior trainer, supervisor, behavioral husbandry, or program leadership.','O*NET / BLS proxy':'Animal Trainers (broad proxy)','Job outlook':'Use Animal Trainers as a broad benchmark plus zoo/aquarium postings.','Salary context':'Use employer postings; zoo/aquarium trainer pay can differ materially from broad animal-trainer data.'}},
{
'name':'Ambassador animal specialist / animal programs keeper','category':'Zoos, aquariums, sanctuaries & managed wildlife','family_id':'rf_zoo_training','role_kind':'career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Cares for and trains animals used in public programs, while combining husbandry, behavior, welfare, presentation, and conservation education.','educationBand':'B.S.-accessible / experience-driven','directContact':'High','career_stage':'entry_or_early','workTags':['Animal care','Behavior / training','Education / public'],'dims':[2.1,2.5,3.0,0.6,0.2,1.0,1.1,0.3,0.9,2.8],
'support':{'UNE-AB':'S','UNE-AN':'S','UMA-BIO':'C','UMA-WEC':'N','UMA-AS':'C','ME-WE':'N','ME-ZOO':'C','URI-W':'C','URI-WZ':'S','URI-AZ':'S'},
'details':{'Typical work settings':'Zoo/aquarium ambassador-animal departments, conservation education programs, outreach animal programs.','Undergraduate preparation most useful':'Husbandry, training, animal behavior, welfare, public speaking, conservation education.','Searchable job titles':'Animal Ambassador Lead; Ambassador Animal Keeper; Zoological Care Specialist - Ambassador Animals; Animal Programs Keeper','Alternate names / terms':'Animal ambassador team; education keeper; presentation animals','Typical education / progression':'B.S. plus direct animal-care/training experience is common; advancement can include lead, supervisor, training, behavioral husbandry, or education leadership.','Job outlook':'No dedicated federal occupation; validate through zoo/aquarium postings.','Salary context':'Use employer postings and related keeper/trainer benchmarks.'}},
{
'name':'Canine behavior consultant','category':'Animal behavior, cognition, welfare & training','family_id':'rf_shelter_companion','role_kind':'career','market_status':'Established professional role; title and regulation vary','evidence_status':'verified_professional_role','description':'Assesses and helps modify complex canine behavior problems such as fear, aggression, anxiety, compulsive behavior, and reactivity using behavior science and client/handler coaching.','educationBand':'Experience-driven; advanced certification valuable','directContact':'High','career_stage':'professional_or_specialist','workTags':['Behavior / training','Animal care','Education / public'],'dims':[3.0,2.8,1.1,0.1,0.1,1.3,0.1,0.4,1.1,2.0],
'support':{'UNE-AB':'S','UNE-AN':'S','UMA-BIO':'C','UMA-WEC':'N','UMA-AS':'S','ME-WE':'N','ME-ZOO':'C','URI-W':'N','URI-WZ':'C','URI-AZ':'S'},
'details':{'Typical work settings':'Private behavior practice, shelters/rescues, training organizations, humane societies, service-animal programs.','Undergraduate preparation most useful':'Learning theory, ethology, behavior observation, animal welfare, applied behavior analysis, physiology, client communication.','Searchable job titles':'Canine Behavior Consultant; Dog Behavior Consultant; Behavior Specialist; Behavior Modification Consultant','Alternate names / terms':'CBCC-KA; behavior consultant; canine behavior specialist','Typical education / progression':'Formal degree requirements vary; substantial supervised experience and independent certification can be important. Advanced applied-animal-behavior science may require research graduate education.','Job outlook':'No dedicated federal occupation; use certification organizations and real postings/practice data.','Salary context':'Highly variable by employer, geography, and self-employment; broad animal-trainer wages are an imperfect proxy.'}},
{
'name':'Wildlife diversity / nongame biologist','category':'Wildlife, rehabilitation & conservation','family_id':'rf_wildlife_biology','role_kind':'career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Studies and manages nongame species and biodiversity, often combining surveys, species-status assessments, habitat work, data management, and conservation planning for less-harvested or at-risk taxa.','educationBand':'B.S.-accessible; M.S. often useful','directContact':'Moderate','career_stage':'professional_or_specialist','workTags':['Fieldwork','Research','Conservation','Data / statistics','GIS / spatial'],'dims':[1.3,0.4,0.2,3.0,0.6,2.1,3.0,2.3,2.1,0.9],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'S','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'S','URI-W':'S','URI-WZ':'S','URI-AZ':'N'},
'details':{'Typical work settings':'State wildlife agencies, natural heritage programs, NGOs, consulting firms, universities.','Undergraduate preparation most useful':'Wildlife biology, ecology, taxonomy/species ID, field sampling, GIS, statistics, scientific writing.','Searchable job titles':'Wildlife Diversity Biologist; Nongame Biologist; Natural Heritage Zoologist; Wildlife Diversity Specialist','Alternate names / terms':'Nongame wildlife; biodiversity biologist; natural heritage zoology','Typical education / progression':'B.S. supports technician and some biologist roles; M.S. often improves competitiveness for specialist positions.','O*NET / BLS proxy':'Zoologists and Wildlife Biologists','Job outlook':'Use wildlife-biologist benchmarks plus state/NGO postings.','Salary context':'Use state-agency/posting salary ranges and wildlife-biologist benchmarks.'}},
{
'name':'Species recovery biologist','category':'Wildlife, rehabilitation & conservation','family_id':'rf_reintroduction','role_kind':'career','market_status':'Verified professional function; titles vary','evidence_status':'verified_function_title_varies','description':'Plans or implements recovery actions for threatened or endangered species, integrating population monitoring, habitat needs, reintroduction, regulatory requirements, and partner coordination.','educationBand':'B.S. + graduate study often useful','directContact':'Moderate','career_stage':'professional_or_specialist','workTags':['Fieldwork','Research','Conservation','GIS / spatial'],'dims':[1.1,0.4,0.2,2.8,2.4,1.6,3.0,2.2,2.3,1.1],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'S','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'S','URI-W':'S','URI-WZ':'S','URI-AZ':'C'},
'details':{'Typical work settings':'Federal/state agencies, conservation NGOs, zoos/conservation centers, universities, species-recovery partnerships.','Undergraduate preparation most useful':'Population ecology, field methods, conservation biology, GIS, statistics, endangered-species policy, scientific writing.','Searchable job titles':'Species Recovery Biologist; Recovery Biologist; Endangered Species Biologist; Recovery Program Biologist','Alternate names / terms':'Species recovery; threatened and endangered species; recovery planning','Typical education / progression':'B.S. may support implementation roles; M.S. often useful for independent planning/science leadership.','O*NET / BLS proxy':'Zoologists and Wildlife Biologists / Biological Scientists','Job outlook':'Use wildlife-biologist and biological-scientist benchmarks plus agency postings.','Salary context':'Use federal/state/NGO postings and related biological-science benchmarks.'}},
{
'name':'Wildlife refuge manager','category':'Wildlife, rehabilitation & conservation','family_id':'rf_habitat','role_kind':'later_career','market_status':'Verified federal occupational series and current titles','evidence_status':'verified_current_market','description':'Manages public lands and waters designated as wildlife refuges, integrating wildlife and habitat conservation, land/water management, planning, administration, public relations, supervision, and regulatory responsibilities.','educationBand':'B.S. + progressive professional experience','directContact':'Low / variable','career_stage':'leadership','workTags':['Fieldwork','Conservation','Education / public'],'dims':[0.5,0.2,0.1,2.4,0.4,1.0,3.0,1.5,1.2,1.9],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'C','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'C','URI-W':'S','URI-WZ':'S','URI-AZ':'N'},
'details':{'Typical work settings':'National wildlife refuges and federal land/wildlife programs.','Undergraduate preparation most useful':'Wildlife biology, habitat management, ecology, botany, conservation biology, public communication, project/program management.','Searchable job titles':'Wildlife Refuge Manager; Wildlife Refuge Specialist; Deputy Refuge Manager; Supervisory Wildlife Refuge Specialist','Alternate names / terms':'Federal refuge management; refuge specialist','Typical education / progression':'Specific OPM coursework requirements apply; manager roles generally follow progressive wildlife/refuge-management experience.','Job outlook':'Federal occupational series 0485; use current USAJOBS postings and federal staffing data.','Salary context':'Use current GS/locality postings rather than O*NET animal-care proxies.'}},
{
'name':'Conservation delivery / habitat program coordinator','category':'Wildlife, rehabilitation & conservation','family_id':'rf_habitat','role_kind':'career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Coordinates habitat conservation delivery across agencies, NGOs, landowners, and partners, translating conservation plans into habitat projects, incentives, restoration, and implementation.','educationBand':'B.S.-accessible / experience-driven','directContact':'Low / variable','career_stage':'professional_or_specialist','workTags':['Conservation','Fieldwork','Education / public','GIS / spatial'],'dims':[0.4,0.1,0.1,2.0,0.2,0.8,3.0,2.0,1.2,1.6],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'C','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'C','URI-W':'S','URI-WZ':'S','URI-AZ':'N'},
'details':{'Typical work settings':'Conservation NGOs, joint ventures, state/federal agencies, landowner partnerships, habitat programs.','Undergraduate preparation most useful':'Wildlife ecology, habitat management, GIS, conservation planning, technical writing, stakeholder communication.','Searchable job titles':'Conservation Delivery Specialist; Habitat Delivery Coordinator; Habitat Program Manager; Conservation Delivery Coordinator','Alternate names / terms':'Habitat delivery; conservation implementation; joint venture coordinator','Typical education / progression':'B.S. is common; 3–5 years of applied conservation/project experience often appears in coordinator roles.','Job outlook':'No dedicated O*NET occupation; use current NGO/agency postings.','Salary context':'Use employer postings; current examples can differ substantially by responsibility and region.'}},
{
'name':'Wildlife program manager','category':'Wildlife, rehabilitation & conservation','family_id':'rf_wildlife_biology','role_kind':'later_career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Leads wildlife programs, multidisciplinary staff, regional priorities, budgets, partnerships, and conservation delivery across species, habitat, recreation, and agency functions.','educationBand':'B.S. + substantial professional experience','directContact':'Low','career_stage':'leadership','workTags':['Conservation','Research','Education / public'],'dims':[0.5,0.2,0.1,2.2,0.3,1.0,2.8,1.8,1.6,1.7],
'support':{'UNE-AB':'C*','UNE-AN':'C*','UMA-BIO':'C*','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'C*','URI-W':'S','URI-WZ':'S','URI-AZ':'N'},
'details':{'Typical work settings':'State wildlife agencies, federal programs, NGOs, large conservation organizations.','Undergraduate preparation most useful':'Wildlife science, management, policy, project management, communication, budgeting, staff supervision.','Searchable job titles':'Regional Wildlife Program Manager; Wildlife Program Manager; Applied Research Section Manager; Supervisory Wildlife Biologist','Alternate names / terms':'Wildlife program leadership; regional wildlife manager','Typical education / progression':'Usually a later-career role after several years of professional wildlife work; graduate study may help but is not always required.','Job outlook':'Use agency/NGO postings and management benchmarks.','Salary context':'Use agency salary schedules and current management postings.'}},
{
'name':'Conservation geneticist / wildlife genomicist','category':'Organismal biology & ecological science','family_id':'rf_evolution','role_kind':'scientific_specialty','market_status':'Established scientific specialty with verified institutional titles','evidence_status':'verified_current_market','description':'Uses genetics and genomics to study population structure, diversity, gene flow, relatedness, adaptation, and conservation management of wildlife or managed populations.','educationBand':'Graduate degree typical','directContact':'Low','career_stage':'professional_or_specialist','workTags':['Research','Data / statistics','Conservation'],'dims':[0.5,0.2,0.5,1.5,0.2,3.0,2.6,2.6,3.0,0.8],
'support':{'UNE-AB':'C','UNE-AN':'G','UMA-BIO':'G','UMA-WEC':'C','UMA-AS':'C','ME-WE':'C','ME-ZOO':'G','URI-W':'C','URI-WZ':'C','URI-AZ':'C'},
'details':{'Typical work settings':'USGS and other government science centers, zoo conservation-genetics programs, universities, NGOs, genomic laboratories.','Undergraduate preparation most useful':'Genetics, molecular/cellular biology, population biology, statistics, bioinformatics, ecology, research.','Searchable job titles':'Research Geneticist; Conservation Geneticist; Wildlife Geneticist; Population Genomics Scientist','Alternate names / terms':'Conservation genomics; population genetics; molecular ecology','Typical education / progression':'Research technician roles may begin after a B.S.; independent research commonly requires a Ph.D.','O*NET / BLS proxy':'Biological Scientists / Geneticists (broad proxy)','Job outlook':'No narrow conservation-genetics benchmark; use federal genetics series, biological-science data, and current postings.','Salary context':'Use government/institutional postings and research-scientist benchmarks.'}},
{
'name':'Research ecologist','category':'Organismal biology & ecological science','family_id':'rf_evolution','role_kind':'scientific_specialty','market_status':'Verified federal/institutional title','evidence_status':'verified_professional_role','description':'Conducts ecological research on species, populations, communities, habitats, landscapes, or environmental change, often using field data, experiments, models, or long-term monitoring.','educationBand':'Graduate degree typical','directContact':'Low / variable','career_stage':'professional_or_specialist','workTags':['Fieldwork','Research','Data / statistics','Conservation'],'dims':[0.8,0.2,0.1,2.2,0.3,2.2,2.5,2.7,3.0,0.8],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'G','UMA-WEC':'G','UMA-AS':'N','ME-WE':'G','ME-ZOO':'G','URI-W':'G','URI-WZ':'G','URI-AZ':'N'},
'details':{'Typical work settings':'USGS science centers, universities, agencies, NGOs, environmental research organizations.','Undergraduate preparation most useful':'Ecology, statistics, research design, field methods, GIS, scientific writing, programming/data analysis.','Searchable job titles':'Research Ecologist; Ecologist; Supervisory Research Ecologist','Alternate names / terms':'Applied ecologist; ecological scientist','Typical education / progression':'B.S. supports research-assistant/technician roles; Ph.D. is common for independent federal/university research ecologist positions.','O*NET / BLS proxy':'Biological Scientists / Environmental Scientists (broad proxy)','Job outlook':'Use federal ecology series and biological/environmental-science benchmarks.','Salary context':'Use federal/institutional research postings and related scientific benchmarks.'}},
{
'name':'Ecological data scientist','category':'Quantitative, environmental & agency careers','family_id':'rf_quant','role_kind':'scientific_specialty','market_status':'Verified institutional title variants','evidence_status':'verified_professional_role','description':'Builds, manages, analyzes, and models ecological or wildlife datasets, often integrating monitoring, spatial, remote-sensing, population, or citizen-science data.','educationBand':'B.S. + graduate study often useful','directContact':'Low','career_stage':'professional_or_specialist','workTags':['Data / statistics','GIS / spatial','Research','Conservation'],'dims':[0.3,0.1,0.0,1.5,0.2,1.2,2.1,3.0,2.8,0.8],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'S','UMA-WEC':'S','UMA-AS':'C','ME-WE':'S','ME-ZOO':'S','URI-W':'S','URI-WZ':'S','URI-AZ':'C'},
'details':{'Typical work settings':'Government science centers, universities, conservation NGOs, consulting firms, research programs.','Undergraduate preparation most useful':'Statistics, data management, programming, ecology, GIS, research design, scientific communication.','Searchable job titles':'Biologist (Data Scientist); Ecological Data Scientist; Wildlife Data Scientist; Biodiversity Data Analyst','Alternate names / terms':'Ecological informatics; conservation data science','Typical education / progression':'B.S. can support analyst/assistant roles; M.S./Ph.D. often useful for advanced modeling or independent research.','Job outlook':'No single dedicated occupation; use data/statistics plus biological-science evidence.','Salary context':'Posting-specific data are preferable to generic computer-occupation proxies.'}},
{
'name':'Research statistician — ecology/biology','category':'Quantitative, environmental & agency careers','family_id':'rf_quant','role_kind':'scientific_specialty','market_status':'Verified federal/institutional title','evidence_status':'verified_professional_role','description':'Develops and applies statistical methods to biological and ecological research, including abundance, occupancy, survival, movement, population dynamics, and study design.','educationBand':'Graduate degree typical','directContact':'Low','career_stage':'professional_or_specialist','workTags':['Data / statistics','Research'],'dims':[0.2,0.0,0.0,1.1,0.0,1.1,1.7,3.0,3.0,0.8],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'G','UMA-WEC':'G','UMA-AS':'C','ME-WE':'G','ME-ZOO':'G','URI-W':'G','URI-WZ':'G','URI-AZ':'C'},
'details':{'Typical work settings':'USGS and government science centers, universities, conservation organizations, quantitative ecology labs.','Undergraduate preparation most useful':'Statistics, mathematics, programming, research design, ecology/biology, data management.','Searchable job titles':'Research Statistician; Research Statistician (Biology); Biometrician; Quantitative Ecologist','Alternate names / terms':'Biological statistician; ecological statistician','Typical education / progression':'Advanced quantitative roles commonly require graduate training in statistics, quantitative ecology, or related fields.','O*NET / BLS proxy':'Statisticians / Biostatisticians (proxy)','Job outlook':'Use statistics occupations plus domain-specific postings.','Salary context':'Use research/statistics postings; generic data-science salaries may overstate ecology-specific pay.'}},
{
'name':'eDNA / molecular ecology technician','category':'Quantitative, environmental & agency careers','family_id':'rf_quant','role_kind':'career','market_status':'Verified current market title variants','evidence_status':'verified_current_market','description':'Supports environmental DNA or molecular-ecology projects by processing biological samples, running laboratory workflows, managing data, and connecting molecular detections to wildlife or ecological monitoring.','educationBand':'B.S.-accessible / experience-driven','directContact':'Low','career_stage':'entry_or_early','workTags':['Research','Data / statistics','Conservation'],'dims':[0.2,0.1,0.0,1.2,0.1,2.5,2.0,2.2,2.6,0.4],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'S','UMA-WEC':'C','UMA-AS':'C','ME-WE':'C','ME-ZOO':'S','URI-W':'C','URI-WZ':'C','URI-AZ':'C'},
'details':{'Typical work settings':'Molecular ecology labs, conservation genetics programs, government laboratories, universities, environmental research organizations.','Undergraduate preparation most useful':'Molecular/cellular biology, genetics, ecology, laboratory methods, data management, statistics.','Searchable job titles':'Environmental DNA Lab Technician; eDNA Technician; Molecular Ecology Technician; Conservation Genetics Technician','Alternate names / terms':'Molecular ecology lab tech; eDNA analyst','Typical education / progression':'B.S. commonly sufficient for technician roles; graduate study can lead to molecular ecologist/geneticist positions.','Job outlook':'No dedicated O*NET occupation; use biological technician/genetics data and current postings.','Salary context':'Use laboratory and conservation-science postings.'}},
{
'name':'Remote sensing / geospatial ecologist','category':'Quantitative, environmental & agency careers','family_id':'rf_gis','role_kind':'scientific_specialty','market_status':'Established professional/scientific role; titles vary','evidence_status':'verified_professional_role','description':'Uses satellite, aerial, drone, GIS, and other spatial data to study wildlife habitat, landscape change, movement, distribution, or conservation priorities.','educationBand':'B.S. + graduate study often useful','directContact':'Low','career_stage':'professional_or_specialist','workTags':['GIS / spatial','Data / statistics','Research','Conservation'],'dims':[0.2,0.0,0.0,1.8,0.1,0.8,2.3,3.0,2.5,0.5],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'S','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'S','URI-W':'S','URI-WZ':'S','URI-AZ':'N'},
'details':{'Typical work settings':'USGS, wildlife agencies, conservation NGOs, universities, environmental consulting, remote-sensing programs.','Undergraduate preparation most useful':'GIS, remote sensing, statistics, ecology, programming, spatial analysis, field validation.','Searchable job titles':'Geospatial Ecologist; Remote Sensing Ecologist; GIS Specialist; Spatial Ecologist; Geospatial Scientist','Alternate names / terms':'Landscape ecology; spatial ecology; remote sensing','Typical education / progression':'B.S. can support GIS analyst roles; advanced ecological interpretation/modeling often benefits from graduate study.','Job outlook':'Use GIS/geospatial and environmental-science benchmarks cautiously.','Salary context':'Posting-specific ecology/geospatial salaries are preferable to broad computer-occupation proxies.'}},
{
'name':'Human dimensions / conservation social scientist','category':'Wildlife, rehabilitation & conservation','family_id':'rf_human_dimensions','role_kind':'scientific_specialty','market_status':'Established conservation specialty with verified government titles','evidence_status':'verified_professional_role','description':'Studies how people perceive, value, use, or interact with wildlife and conservation, supporting conflict management, policy, public engagement, and conservation decisions.','educationBand':'Graduate degree often useful','directContact':'Low','career_stage':'professional_or_specialist','workTags':['Research','Education / public','Conservation','Data / statistics'],'dims':[0.3,0.1,0.0,1.0,0.1,0.4,2.4,2.0,2.5,2.7],
'support':{'UNE-AB':'C','UNE-AN':'C','UMA-BIO':'C','UMA-WEC':'S','UMA-AS':'N','ME-WE':'S','ME-ZOO':'C','URI-W':'S','URI-WZ':'S','URI-AZ':'N'},
'details':{'Typical work settings':'Wildlife agencies, USGS, universities, conservation NGOs, human-wildlife conflict programs.','Undergraduate preparation most useful':'Wildlife/ecology, psychology or social science, survey/research methods, statistics, communication, policy.','Searchable job titles':'Research Social Scientist; Human Dimensions Specialist; Wildlife Human Dimensions Scientist; Conservation Social Scientist','Alternate names / terms':'Human dimensions of wildlife; conservation social science','Typical education / progression':'Graduate training is common for independent research; applied outreach/conflict roles may be B.S.-accessible with strong field/communication experience.','Job outlook':'No narrow benchmark; use social-science and wildlife/conservation postings.','Salary context':'Use agency/university/NGO postings.'}},
{
'name':'Wildlife rehabilitation program manager','category':'Wildlife, rehabilitation & conservation','family_id':'rf_rehab','role_kind':'later_career','market_status':'Verified current market titles','evidence_status':'verified_current_market','description':'Directs or supervises rehabilitation-center operations, staff/volunteers, animal-care protocols, records, permits, budgets, training, release decisions, and public-facing program responsibilities.','educationBand':'B.S. + 3–5+ years progressive rehabilitation experience','directContact':'High','career_stage':'leadership','workTags':['Animal care','Conservation','Education / public'],'dims':[0.7,2.2,1.0,1.7,3.0,1.2,2.2,0.7,1.2,1.6],
'support':{'UNE-AB':'C*','UNE-AN':'C*','UMA-BIO':'C*','UMA-WEC':'C*','UMA-AS':'C*','ME-WE':'S','ME-ZOO':'C*','URI-W':'S','URI-WZ':'S','URI-AZ':'C*'},
'details':{'Typical work settings':'Wildlife rehabilitation centers, wildlife hospitals, park-district wildlife centers, nonprofit rehabilitation organizations.','Undergraduate preparation most useful':'Wildlife biology, animal care, rehabilitation experience, staff/volunteer supervision, records, permits, biosecurity, communication.','Searchable job titles':'Wildlife Care Manager; Rehabilitation Manager; Wildlife Rehabilitation Program Manager; Senior Rehabilitator','Alternate names / terms':'Wildlife center manager; rehabilitation supervisor','Typical education / progression':'Usually follows several years of hands-on rehabilitation plus supervisory/program responsibility; permits and center-specific requirements matter.','Job outlook':'No dedicated O*NET occupation; NWRA postings provide direct market evidence.','Salary context':'Use wildlife-rehabilitation postings and nonprofit/park-district salary data.'}},
]

SOURCES=[
('src_aza_types','Association of Zoos and Aquariums','professional_reference','Types of Zoo and Aquarium Jobs','https://www.aza.org/types-of-zoo-and-aquarium-jobs',None,TODAY,'B','Official AZA career taxonomy and role descriptions.'),
('src_aza_jobs','Association of Zoos and Aquariums','job_board','AZA Career Center','https://www.aza.org/Jobs/',None,TODAY,'B','Current and recent zoo/aquarium job postings.'),
('src_aza_pmc','Association of Zoos and Aquariums','professional_reference','Population Management Center','https://www.aza.org/population-management-center',None,TODAY,'B','Population biologists, planning coordinator, research support, and managed-population planning.'),
('src_aza_programs','Association of Zoos and Aquariums','professional_reference','Animal Program Deadlines and Program Leader Roles','https://www.aza.org/animal-program-deadlines',None,TODAY,'B','SSP and studbook role requirements/deadlines.'),
('src_aza_program_roles','Association of Zoos and Aquariums','professional_reference','Updates to AZA Animal Programs - Role Descriptions','https://annual.aza.org/2024/documents/Boland__Marissa_Updates_to_AZA_s_Animal_Programs.pdf','2024',TODAY,'B','SSP Coordinator and Studbook Keeper role descriptions.'),
('src_tws_jobs','The Wildlife Society','job_board','The Wildlife Society Career Center','https://careers.wildlife.org/',None,TODAY,'B','Current wildlife-industry job postings.'),
('src_nwra_jobs','National Wildlife Rehabilitators Association','job_board','NWRA Career Center','https://www.nwrawildlife.org/networking/',None,TODAY,'B','Current wildlife rehabilitation jobs and internships.'),
('src_usgs_eesc','U.S. Geological Survey','employee_directory','Eastern Ecological Science Center - Employee Directory','https://www.usgs.gov/centers/eesc/connect',None,TODAY,'A','Current scientific titles in federal ecological research.'),
('src_usgs_werc','U.S. Geological Survey','employee_directory','Western Ecological Research Center - Employee Directory','https://www.usgs.gov/centers/werc/connect',None,TODAY,'A','Current scientific titles in federal ecological research.'),
('src_usgs_npwrc','U.S. Geological Survey','employee_directory','Northern Prairie Wildlife Research Center - Employee Directory','https://www.usgs.gov/centers/northern-prairie-wildlife-research-center/connect',None,TODAY,'A','Current scientific/geospatial titles in federal wildlife research.'),
('src_opm_0486','U.S. Office of Personnel Management','qualification_standard','Wildlife Biology Series 0486','https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/wildlife-biology-series-0486/',None,TODAY,'A','Federal wildlife-biologist education requirements.'),
('src_opm_0485','U.S. Office of Personnel Management','qualification_standard','Wildlife Refuge Management Series 0485','https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/wildlife-refuge-management-series-0485/',None,TODAY,'A','Federal wildlife-refuge management education requirements.'),
('src_opm_0410','U.S. Office of Personnel Management','qualification_standard','Zoology Series 0410','https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/zoology-series-0410/',None,TODAY,'A','Federal zoology education requirements.'),
('src_opm_0408','U.S. Office of Personnel Management','qualification_standard','Ecology Series 0408','https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/ecology-series-0408/',None,TODAY,'A','Federal ecology education requirements.'),
('src_opm_0440','U.S. Office of Personnel Management','qualification_standard','Genetics Series 0440','https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/genetics-series-0440/',None,TODAY,'A','Federal genetics education requirements.'),
('src_fws_rehab','U.S. Fish and Wildlife Service','permit_standard','Migratory Bird Rehabilitation Permit 3-200-10b','https://www.fws.gov/service/3-200-10b-migratory-bird-rehabilitation',None,TODAY,'A','Federal migratory-bird rehabilitation permit and experience requirements.'),
('src_tws_cert','The Wildlife Society','credential_standard','TWS Wildlife Biologist Certifications','https://wildlife.org/tws-certifications/',None,TODAY,'B','AWB/CWB certification structure and experience requirements.'),
('src_abs_caab','Animal Behavior Society','credential_standard','CAAB / ACAAB Certification Requirements','https://www.animalbehaviorsociety.org/web/committees-applied-behavior-caab.php',None,TODAY,'B','Research-based graduate education and experience requirements for applied-animal-behavior certification.'),
('src_ccpdt_cbcc','Certification Council for Professional Dog Trainers','credential_standard','Certified Behavior Consultant Canine - Knowledge Assessed','https://www.ccpdt.org/certification/dog-behavior-consultant/',None,TODAY,'B','Canine behavior-consultant experience and certification requirements.'),
('src_iaabc_shelter','International Association of Animal Behavior Consultants','credential_standard','Shelter Behavior Affiliate Credential','https://iaabc.org/en/affiliate-credentials',None,TODAY,'B','Shelter-behavior credential and recommended experience.'),
]

# Specific current/recent source pages used for detailed postings.
SPECIFIC_SOURCES=[
('src_aza_curator_behavior','Gladys Porter Zoo / AZA','job_posting','Curator of Behavioral Husbandry','https://www.aza.org/jobs?job=51772',None,TODAY,'C','Detailed role posting.'),
('src_aza_senior_trainer','John G. Shedd Aquarium / AZA','job_posting','(Sr.) Trainer','https://www.aza.org/JOBS?job=52529',None,TODAY,'C','Trainer/senior trainer posting with pay range.'),
('src_aza_wildlife_behavior','San Diego Zoo Wildlife Alliance / AZA','job_posting','Wildlife Care Specialist, Behavior','https://www.aza.org/jobs?job=51629',None,TODAY,'C','Behavior/training wildlife-care posting.'),
('src_aza_registrar','Lee Richardson Zoo / AZA','job_posting','Registrar','https://www.aza.org/Jobs?job=52409',None,TODAY,'C','Animal records, permits, transfer, ZIMS, and database role.'),
('src_aza_curator','Mesker Park Zoo / AZA','job_posting','Animal Curator','https://www.aza.org/Jobs/?job=52644','2026-09-06',TODAY,'C','Current curator posting with salary.'),
('src_aza_animalcare','Greenville Zoo / AZA','job_posting','Animal Care Specialist','https://www.aza.org/JOBS?job=52646','2026-09-07',TODAY,'C','Current animal-care posting with salary and education/experience.'),
('src_aza_aquariumcare','Kansas City Zoo & Aquarium / AZA','job_posting','Animal Care Specialist - Aquarium Team','https://www.aza.org/jobs?job=51307',None,TODAY,'C','Aquarium animal-care posting with salary and dive requirements.'),
('src_aza_elephantcomm','San Diego Zoo Wildlife Alliance / AZA','job_posting','Post Doctoral Associate, Elephant Communication','https://www.aza.org/jobs?job=51494','2026-05-25',TODAY,'C','Advanced communication research posting with salary.'),
('src_aza_genetics','San Diego Zoo Wildlife Alliance / AZA','job_posting','Conservation Genetics Post Doctoral Associate','https://www.aza.org/jobs?job=51965',None,TODAY,'C','Conservation genetics posting with salary.'),
('src_tws_diversitytech','West Virginia DNR / TWS','job_posting','Wildlife Diversity/Natural Heritage Zoology Technician','https://careers.wildlife.org/job/wildlife-diversitynatural-heritage-zoology-technician-west-virginia/85441685/',None,TODAY,'C','Current wildlife-diversity technician posting.'),
('src_tws_habitatdelivery','American Bird Conservancy / TWS','job_posting','GCJV Habitat Delivery Coordinator','https://careers.wildlife.org/job/gulf-coast-joint-venture-gcjv-coastal-grassland-incentive-program-cgrip-and-habitat-delivery-coordinator/85122735/',None,TODAY,'C','Habitat delivery posting with salary and education.'),
('src_tws_wildlife_manager','Washington Department of Fish & Wildlife / TWS','job_posting','Regional Wildlife Program Manager','https://careers.wildlife.org/job/regional-wildlife-program-manager-north-puget-sound-region-4/85512902/',None,TODAY,'C','Regional wildlife leadership posting with salary and experience.'),
('src_tws_labmanager','East Texas A&M University / TWS','job_posting','Quail Research Laboratory Manager','https://careers.wildlife.org/jobs/function/Wildlife/',None,TODAY,'C','Research laboratory manager posting with salary and B.S. requirement.'),
('src_nwra_tech','Ohio Wildlife Center / NWRA','job_posting','Wildlife Rehabilitation Technician','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1097691&view=2','2026-08-24',TODAY,'C','Current rehabilitation technician posting.'),
('src_nwra_rehab','Tucson Wildlife Center / NWRA','job_posting','Rehabilitator','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1097520&view=2','2026-08-21',TODAY,'C','Current rehabilitation leadership posting.'),
('src_nwra_specialist','Chintimini Wildlife Center / NWRA','job_posting','Wildlife Rehabilitation Specialist','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1097322&view=2','2026-08-19',TODAY,'C','Current rehabilitation specialist posting.'),
('src_nwra_manager','Lake Metroparks / NWRA','job_posting','Wildlife Care Manager','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1096932&view=2','2026-08-14',TODAY,'C','Wildlife-care management posting with salary and experience.'),
('src_nwra_avian','Native Songbird Care & Conservation / NWRA','job_posting','Seasonal Avian Care Technician','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1065489&view=2','2026-02-15',TODAY,'C','Seasonal rehabilitation posting with salary.'),
('src_usajobs_wildtech','National Park Service / USAJOBS','job_posting','Biological Science Technician (Wildlife)','https://www.usajobs.gov/job/882687500',None,TODAY,'A','Current GS-7 wildlife technician posting.'),
('src_usajobs_refuge','U.S. Fish and Wildlife Service / USAJOBS','job_posting','Wildlife Refuge Manager - Winona','https://www.usajobs.gov/job/883089800',None,TODAY,'A','Current GS-12 refuge manager posting.'),
('src_usajobs_refuge2','U.S. Fish and Wildlife Service / USAJOBS','job_posting','Wildlife Refuge Manager - Willapa','https://www.usajobs.gov/job/883251400',None,TODAY,'A','Current GS-13 refuge manager posting.'),
('src_usajobs_fwbio','U.S. Fish and Wildlife Service / USAJOBS','job_posting','Fish and Wildlife Biologist - State College','https://www.usajobs.gov/job/882387200',None,TODAY,'A','Current GS-12 fish and wildlife biologist posting.'),
('src_usajobs_seniorbio','U.S. Fish and Wildlife Service / USAJOBS','job_posting','Senior Fish and Wildlife Biologist - Fort Worth','https://doi.usajobs.gov/job/882813600',None,TODAY,'A','Current GS-12 senior fish and wildlife biologist posting.'),
]

# Current/recent job-market observations. Posted dates are exact where surfaced; otherwise month-level/unknown is left null.
POSTINGS=[
# AZA current/recent
('Zookeeper / animal-care specialist','Primates - Animal Care Specialist','Brookfield Zoo Chicago','Brookfield, IL','2026-09-08',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zookeeper / animal-care specialist','Herpetology Keeper I or II','Nashville Zoo','Nashville, TN','2026-09-08',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Ambassador animal specialist / animal programs keeper','Animal Ambassador Lead','Virginia Zoo Society','Norfolk, VA','2026-09-08',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zoo / aquarium animal trainer','Full-Time Animal Trainer','Natural Encounters, Inc.','Winter Haven, FL','2026-09-08',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zookeeper / animal-care specialist','Animal Keeper I','Sunset Zoo','Manhattan, KS','2026-09-07',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zookeeper / animal-care specialist','Animal Care Specialist','Greenville Zoo','Greenville, SC','2026-09-07','High school; related associate/bachelor preferred','1 year professional exotic animal care',44512,56472,'annual','src_aza_animalcare','https://www.aza.org/JOBS?job=52646','Current posting; related college degree preferred.'),
('Zoo animal curator','Animal Curator','Mesker Park Zoo and Botanic Garden','Evansville, IN','2026-09-06',None,'5 years animal curator preferred',68000,68000,'annual','src_aza_curator','https://www.aza.org/Jobs/?job=52644','Current posting.'),
('Zoo animal curator','Assistant / Associate Curator (Avian Team)','Akron Zoo','Akron, OH','2026-09-04',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zookeeper / animal-care specialist','Elephant Keeper','Fort Worth Zoo','Fort Worth, TX','2026-09-04',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Conservation outreach / program coordinator','Outreach Specialist','Fort Worth Zoo','Fort Worth, TX','2026-09-04',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zookeeper / animal-care specialist','Pachyderm Animal Care Support Tech','Oklahoma City Zoo','Oklahoma City, OK','2026-09-04',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Sanctuary animal caregiver','Avian Care Specialist','Oasis Sanctuary Foundation','Benson, AZ','2026-09-04',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS/','Current on AZA board.'),
('Zoo animal nutritionist / nutrition coordinator','Animal Nutrition Coordinator','Houston Zoo','Houston, TX','2026-09-03',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/Jobs/','Current on AZA board.'),
('Zoo / aquarium animal trainer','Senior Training - Pinnipeds','Georgia Aquarium','Atlanta, GA','2026-09-02',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/Jobs/','Current on AZA board.'),
('Aquarist / aquarium animal-care specialist','Dive Coordinator','Texas State Aquarium','Corpus Christi, TX','2026-09-02',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/Jobs/','Adjacent aquarium-care/operations role.'),
('Wildlife rehabilitator','Wildlife Care Specialist Hospital','San Diego Zoo Wildlife Alliance','San Diego, CA','2026-09-01',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS?LOCALE=EN','Current on AZA board.'),
('Wildlife / environmental educator','Wildlife Education Curator','Arizona Game and Fish Department','Phoenix, AZ','2026-09-01',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS?LOCALE=EN','Current on AZA board.'),
('Zoo / aquarium animal trainer','Assistant Trainer - Belugas','Mystic Aquarium','Mystic, CT','2026-09-01',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS?LOCALE=EN','Current on AZA board.'),
('Wildlife technician / biological science technician','OCIC Field Technician','Central Florida Zoo','Sanford, FL','2026-09-01',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/JOBS?LOCALE=EN','Current conservation field role on AZA board.'),
('Zoo behavioral-husbandry specialist','Curator of Behavioral Husbandry','Gladys Porter Zoo','Brownsville, TX','2026-06-18',None,'Highly experienced',None,None,'annual','src_aza_curator_behavior','https://www.aza.org/jobs?job=51772','Institution-wide behavioral-husbandry leadership.'),
('Zoo behavioral-husbandry specialist','Wildlife Care Specialist, Behavior','San Diego Zoo Wildlife Alliance','Escondido, CA','2026-06-04',None,None,None,None,'annual','src_aza_wildlife_behavior','https://www.aza.org/jobs?job=51629','Training, handling, care, and public-program wildlife role.'),
('Animal behavior research assistant / technician','Animal Behavioral Research Assistant','Brookfield Zoo Chicago','Brookfield, IL','2026-06-04',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?locale=en','Observed AZA research title.'),
('Animal communication researcher','Post Doctoral Associate, Elephant Communication','San Diego Zoo Wildlife Alliance','Escondido, CA','2026-05-25','Doctorate/postdoctorate',None,87264,98172,'annual','src_aza_elephantcomm','https://www.aza.org/jobs?job=51494','Three-year postdoctoral research position.'),
('Conservation geneticist / wildlife genomicist','Conservation Genetics Post Doctoral Associate','San Diego Zoo Wildlife Alliance','Escondido, CA',None,'Doctorate/postdoctorate',None,87264,98172,'annual','src_aza_genetics','https://www.aza.org/jobs?job=51965','Two-year conservation genetics postdoctoral position.'),
('Zoo registrar / animal records & permits specialist','Registrar','Lee Richardson Zoo','Garden City, KS',None,'College degree preferred','3+ years related experience preferred',None,None,'annual','src_aza_registrar','https://www.aza.org/Jobs?job=52409','Records, permits, transfers, ZIMS, behavior/enrichment/training/diet databases.'),
('Zoo / aquarium animal trainer','(Sr.) Trainer','John G. Shedd Aquarium','Chicago, IL',None,None,'Level depends on experience',26,35,'hourly','src_aza_senior_trainer','https://www.aza.org/JOBS?job=52529','Trainer/Senior Trainer pay band.'),
('Aquarist / aquarium animal-care specialist','Animal Care Specialist - Aquarium Team','Kansas City Zoo & Aquarium','Kansas City, MO',None,None,None,17.5,17.5,'hourly','src_aza_aquariumcare','https://www.aza.org/jobs?job=51307','SCUBA preferred; weekend/holiday work.'),
('Population biologist / zoo population management scientist','Manager, Wildlife Planning','Toronto Zoo','Scarborough, ON','2026-04-16',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=49490','Observed zoo wildlife-planning title.'),
('Zoo animal nutritionist / nutrition coordinator','Animal Nutrition Manager','Jacksonville Zoo & Botanical Gardens','Jacksonville, FL','2026-04-16',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=49490','Observed zoo nutrition-management title.'),
('Wildlife rehabilitator','Sea Turtle Rehabilitation Technician','NC Aquarium on Roanoke Island','Manteo, NC','2026-03-18',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=49122','Observed rehabilitation title.'),
('Wildlife technician / biological science technician','Conservation Field Technician','Brevard Zoo','Melbourne, FL','2026-03-17',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=49514','Observed conservation-field title.'),
('Naturalist / interpretive educator','Habitat Interpreter','Mystic Aquarium','Mystic, CT','2026-05-22',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=50913','Observed interpretation title.'),
('Zoo / aquarium educator','School & Teacher Programs Coordinator - Education','Aquarium of the Pacific','Long Beach, CA','2026-05-22',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=50913','Observed education-program title.'),
('Zoo research coordinator','Assistant Research Coordinator','Wildlife Conservation Society','New York, NY','2026-04-17',None,None,None,None,'annual','src_aza_jobs','https://www.aza.org/jobs?job=49073','Observed research coordination title.'),
# TWS
('Wildlife technician / biological science technician','Wildlife Diversity/Natural Heritage Zoology Technician','West Virginia Division of Natural Resources','Elkins, WV',None,'B.A./B.S.','0–1 year',15,17,'hourly','src_tws_diversitytech','https://careers.wildlife.org/job/wildlife-diversitynatural-heritage-zoology-technician-west-virginia/85441685/','Temporary biodiversity technician; 50–75% travel.'),
('Research / laboratory manager — behavioral or biological science','Quail Research Laboratory Manager','East Texas A&M University','Commerce, TX',None,'B.A./B.S.','1–2 years',50000,60000,'annual','src_tws_labmanager','https://careers.wildlife.org/jobs/function/Wildlife/','Current wildlife research lab manager posting.'),
('Conservation delivery / habitat program coordinator','GCJV Coastal Grassland Incentive Program and Habitat Delivery Coordinator','American Bird Conservancy','Lafayette, LA',None,'B.A./B.S.','3–5 years',74520,82800,'annual','src_tws_habitatdelivery','https://careers.wildlife.org/job/gulf-coast-joint-venture-gcjv-coastal-grassland-incentive-program-cgrip-and-habitat-delivery-coordinator/85122735/','Habitat conservation delivery leadership.'),
('Wildlife program manager','Regional Wildlife Program Manager - North Puget Sound Region 4','Washington Department of Fish & Wildlife','Stanwood, WA',None,'B.A./B.S.','5–7 years',123552,123552,'annual','src_tws_wildlife_manager','https://careers.wildlife.org/job/regional-wildlife-program-manager-north-puget-sound-region-4/85512902/','Regional wildlife program leadership.'),
('Conservation NGO scientist / coordinator','Conservation Impact Specialist','American Bird Conservancy','Remote, U.S.',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/','Featured current TWS posting.'),
('Wildlife program manager','State Administrative Manager - Applied Research Section Manager','Michigan Department of Natural Resources','Michigan',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/','Featured current TWS posting.'),
('Conservation delivery / habitat program coordinator','Rio Grande Joint Venture Conservation Delivery Specialist','American Bird Conservancy','Alpine, TX',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/','Featured current TWS posting.'),
('Habitat / wildlife management biologist','Assistant Regional Habitat Program Manager - Region 3','Washington Department of Fish & Wildlife','Ellensburg, WA',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/','Featured current TWS posting.'),
('Wildlife biologist','Butte Area Wildlife Biologist','Montana Fish, Wildlife & Parks','Butte, MT',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/jobs/?keywords=wildlife+technician','Current TWS search result.'),
('Wildlife diversity / nongame biologist','Nongame and Wetlands Habitat Biologist','Montana Fish, Wildlife & Parks','Helena, MT',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/jobs/?keywords=wildlife+technician','Current TWS search result.'),
('eDNA / molecular ecology technician','Environmental DNA Lab Technician','Great Basin Institute & U.S. Forest Service','Missoula, MT',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/jobs/?keywords=wildlife+technician','Current TWS search result.'),
('Wildlife technician / biological science technician','Avian Use Technician','Western EcoSystems Technology, Inc.','Lee County, AR',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/jobseeker/search/results/function/Field%20Technician/','Current field-tech listing.'),
('Wildlife technician / biological science technician','Chronic Wasting Disease Technician','Montana Fish, Wildlife & Parks','Montana',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/jobseeker/search/results/function/Field%20Technician/','Current disease-monitoring technician listing.'),
('Wildlife technician / biological science technician','Quail Research Technician','East Foundation','Hebbronville, TX',None,None,None,None,None,'annual','src_tws_jobs','https://careers.wildlife.org/jobs/?keywords=wildlife+technician','Current research technician listing.'),
# NWRA
('Wildlife rehabilitator','Wildlife Rehabilitation Technician','Ohio Wildlife Center','Powell, OH','2026-08-24','Bachelor’s','<1 year',18,18,'hourly','src_nwra_tech','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1097691&view=2','Full-time rehabilitation technician.'),
('Wildlife rehabilitation program manager','Rehabilitator','Tucson Wildlife Center','Tucson, AZ','2026-08-21','Intermediate/Advanced Wildlife Rehabilitator','<1 year',60000,60000,'annual','src_nwra_rehab','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1097520&view=2','Duties include oversight of wildlife areas, staff, records, rehab, and release.'),
('Wildlife rehabilitator','Wildlife Rehabilitation Specialist','Chintimini Wildlife Center','Corvallis, OR','2026-08-19','Bachelor’s','1–2 years',18,18,'hourly','src_nwra_specialist','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1097322&view=2','Full-time rehabilitation specialist.'),
('Wildlife rehabilitation program manager','Wildlife Care Manager','Lake Metroparks','Kirtland, OH','2026-08-14','Bachelor’s preferred','3–5 years',53040,91520,'annual','src_nwra_manager','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1096932&view=2','Operations, supervision, permits, budget, public education.'),
('Wildlife rehabilitator','Seasonal Avian Care Technician','Native Songbird Care & Conservation','Sebastopol, CA','2026-02-15','Intermediate/Advanced Wildlife Rehabilitator','1–2 years',20,22,'hourly','src_nwra_avian','https://www.nwrawildlife.org/networking/apply_now.aspx?id=1065489&view=2','Seasonal wildlife-care role.'),
# USAJOBS
('Wildlife technician / biological science technician','Biological Science Technician (Wildlife)','National Park Service','Point Reyes Station, CA',None,'Graduate education may substitute at GS-7','GS-6 equivalent experience or graduate education',63081,82007,'annual','src_usajobs_wildtech','https://www.usajobs.gov/job/882687500','Permanent career-seasonal GS-7.'),
('Wildlife refuge manager','Wildlife Refuge Manager','U.S. Fish and Wildlife Service','Winona, MN',None,None,'Progressive federal/professional experience',89508,116362,'annual','src_usajobs_refuge','https://www.usajobs.gov/job/883089800','GS-12 supervisory refuge manager.'),
('Wildlife refuge manager','Wildlife Refuge Manager','U.S. Fish and Wildlife Service','Ilwaco, WA',None,None,'Progressive federal/professional experience',119630,155521,'annual','src_usajobs_refuge2','https://www.usajobs.gov/job/883251400','GS-13 supervisory refuge manager.'),
('Natural-resource agency biologist','Fish and Wildlife Biologist','U.S. Fish and Wildlife Service','State College, PA',None,None,None,89508,116362,'annual','src_usajobs_fwbio','https://www.usajobs.gov/job/882387200','GS-12 0401 biological-sciences position.'),
('Natural-resource agency biologist','Senior Fish and Wildlife Biologist','U.S. Fish and Wildlife Service','Fort Worth, TX',None,None,None,97307,126502,'annual','src_usajobs_seniorbio','https://doi.usajobs.gov/job/882813600','GS-12 senior ecological-services position.'),
]

# Employee-directory / professional title observations from USGS; these are not job postings.
OBSERVED_TITLES=[
('Wildlife biologist','Research Wildlife Biologist','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal research title.'),
('Wildlife program manager','Supervisory Research Wildlife Biologist','U.S. Geological Survey - WERC',None,'employee_directory',TODAY,'src_usgs_werc','Supervisory research wildlife title.'),
('Research ecologist','Research Ecologist','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal research title.'),
('Research ecologist','Supervisory Research Ecologist','U.S. Geological Survey - WERC',None,'employee_directory',TODAY,'src_usgs_werc','Supervisory research ecology title.'),
('Research statistician — ecology/biology','Research Statistician','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal title.'),
('Research statistician — ecology/biology','Research Statistician (Biology)','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal biology-statistics title.'),
('Ecological data scientist','Biologist (Data Scientist)','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal title.'),
('Research / laboratory manager — behavioral or biological science','Biologist, Lab Manager','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal lab-management title.'),
('Conservation geneticist / wildlife genomicist','Supervisory Research Geneticist','U.S. Geological Survey - WERC',None,'employee_directory',TODAY,'src_usgs_werc','Current federal research-genetics title.'),
('Conservation geneticist / wildlife genomicist','Research Geneticist','U.S. Geological Survey - Forest & Rangeland Ecosystem Science Center',None,'employee_directory',TODAY,'src_usgs_werc','Current federal research-genetics title observed in USGS ecosystem science.'),
('GIS / wildlife spatial analyst','GIS Specialist','U.S. Geological Survey - Northern Prairie Wildlife Research Center',None,'employee_directory',TODAY,'src_usgs_npwrc','Current federal GIS title.'),
('Quantitative ecology research assistant','Wildlife Data Assistant','U.S. Geological Survey - Bird Banding Laboratory',None,'employee_directory',TODAY,'src_usgs_eesc','Current wildlife-data support title.'),
('Animal physiologist','Research Physiologist','U.S. Geological Survey - EESC',None,'employee_directory',TODAY,'src_usgs_eesc','Current federal research title.'),
]

COMPETENCIES=[
('comp_behavior_obs','Behavioral observation','Behavior & welfare','Systematic observation, ethograms, behavior coding, and interpretation.'),
('comp_learning','Learning & training','Behavior & welfare','Learning theory, conditioning, reinforcement, and humane training.'),
('comp_cognition','Animal cognition','Behavior & welfare','Perception, memory, decision making, and problem solving.'),
('comp_welfare','Welfare assessment','Behavior & welfare','Assessing physical/behavioral welfare and quality of life.'),
('comp_husbandry','Animal husbandry','Applied animal care','Feeding, sanitation, handling, recordkeeping, enclosure care, and daily management.'),
('comp_enrichment','Enrichment','Applied animal care','Designing and evaluating enrichment that supports species-appropriate behavior.'),
('comp_rehab','Wildlife rehabilitation','Applied animal care','Care, restraint, records, recovery, release criteria, and rehabilitation protocols.'),
('comp_release','Reintroduction & release','Applied conservation','Release planning, reintroduction, translocation, and post-release evaluation.'),
('comp_field','Wildlife field methods','Wildlife science','Survey design, capture/observation, monitoring, and field protocols.'),
('comp_speciesid','Species identification & natural history','Wildlife science','Taxonomy, field identification, life history, and natural history.'),
('comp_ecology','Ecology','Wildlife science','Organism-environment relationships, communities, habitats, and ecological processes.'),
('comp_population','Population biology','Wildlife science','Demography, abundance, survival, reproduction, population dynamics.'),
('comp_habitat','Habitat management & restoration','Applied conservation','Habitat assessment, restoration, management, and conservation implementation.'),
('comp_conservation','Conservation biology','Applied conservation','Species/population conservation, recovery, and biodiversity protection.'),
('comp_telemetry','Telemetry & movement','Methods','Radio/GPS/acoustic tracking and movement analysis.'),
('comp_gis','GIS & spatial analysis','Methods','Geographic information systems and spatial analysis.'),
('comp_stats','Statistics & data analysis','Methods','Statistical analysis, modeling, and quantitative inference.'),
('comp_research','Research design','Methods','Hypothesis development, study design, data collection, and scientific reasoning.'),
('comp_writing','Scientific writing & communication','Professional','Reports, papers, presentations, technical and public communication.'),
('comp_physiology','Animal physiology','Biological mechanisms','Organ systems, endocrine/stress physiology, and functional biology.'),
('comp_neuro','Neuroscience & neuroethology','Biological mechanisms','Neural mechanisms of behavior.'),
('comp_genetics','Genetics & genomics','Biological mechanisms','Genetics, population genetics, genomics, and molecular ecology.'),
('comp_regulatory','Permits, regulation & policy','Professional','Permitting, legal/regulatory frameworks, compliance, and agency procedures.'),
('comp_records','Animal records & databases','Professional','ZIMS/records systems, inventories, permits, transactions, and data stewardship.'),
('comp_nutrition','Animal nutrition','Applied animal care','Diet formulation, food systems, nutrition science, and feeding management.'),
('comp_public','Public education & stakeholder communication','Professional','Teaching, interpretation, outreach, client/stakeholder communication.'),
]

# New role competency importance.
NEW_COMP={
'Population biologist / zoo population management scientist':['comp_population','comp_genetics','comp_stats','comp_research','comp_writing','comp_conservation'],
'SSP coordinator / studbook keeper':['comp_population','comp_records','comp_conservation','comp_writing','comp_stats'],
'Zoo registrar / animal records & permits specialist':['comp_records','comp_regulatory','comp_writing','comp_husbandry'],
'Zoo animal nutritionist / nutrition coordinator':['comp_nutrition','comp_physiology','comp_stats','comp_husbandry','comp_research'],
'Zoo / aquarium animal trainer':['comp_learning','comp_behavior_obs','comp_husbandry','comp_welfare','comp_public'],
'Ambassador animal specialist / animal programs keeper':['comp_husbandry','comp_learning','comp_welfare','comp_public','comp_behavior_obs'],
'Canine behavior consultant':['comp_learning','comp_behavior_obs','comp_welfare','comp_public','comp_physiology'],
'Wildlife diversity / nongame biologist':['comp_field','comp_speciesid','comp_ecology','comp_stats','comp_gis','comp_conservation'],
'Species recovery biologist':['comp_population','comp_conservation','comp_release','comp_field','comp_gis','comp_regulatory'],
'Wildlife refuge manager':['comp_habitat','comp_conservation','comp_regulatory','comp_public','comp_ecology'],
'Conservation delivery / habitat program coordinator':['comp_habitat','comp_conservation','comp_gis','comp_public','comp_writing'],
'Wildlife program manager':['comp_conservation','comp_regulatory','comp_public','comp_writing','comp_ecology'],
'Conservation geneticist / wildlife genomicist':['comp_genetics','comp_stats','comp_population','comp_research','comp_conservation'],
'Research ecologist':['comp_ecology','comp_stats','comp_research','comp_gis','comp_writing'],
'Ecological data scientist':['comp_stats','comp_gis','comp_ecology','comp_research','comp_writing'],
'Research statistician — ecology/biology':['comp_stats','comp_research','comp_writing','comp_ecology'],
'eDNA / molecular ecology technician':['comp_genetics','comp_research','comp_stats','comp_ecology'],
'Remote sensing / geospatial ecologist':['comp_gis','comp_stats','comp_ecology','comp_research','comp_conservation'],
'Human dimensions / conservation social scientist':['comp_research','comp_stats','comp_public','comp_conservation','comp_writing'],
'Wildlife rehabilitation program manager':['comp_rehab','comp_husbandry','comp_regulatory','comp_public','comp_welfare'],
}

# Explicit progression graph. These relationships are curated and can be reviewed independently of the UI.
EDGES=[
('Zookeeper / animal-care specialist','Zoo behavioral-husbandry specialist','specialization','common','none','2–5 years','supported','src_aza_types','Keeper experience can progress into specialized behavioral-husbandry responsibilities.'),
('Zookeeper / animal-care specialist','Zoo / aquarium animal trainer','lateral','possible','none','1–3 years','supported','src_aza_jobs','Shared animal-care and training skill base.'),
('Zookeeper / animal-care specialist','Ambassador animal specialist / animal programs keeper','lateral','common','none','1–3 years','verified','src_aza_jobs','Current ambassador-animal titles demonstrate this specialization.'),
('Zookeeper / animal-care specialist','Animal collection / management specialist','natural_growth','common','none','5+ years','supported','src_aza_types','Lead/supervisory collection-management progression.'),
('Zookeeper / animal-care specialist','Zoo animal curator','management','common','none_or_grad','5–10+ years','verified','src_aza_types','AZA lists curators as collection-management leadership; current curator postings verify the role.'),
('Aquarist / aquarium animal-care specialist','Zoo / aquarium animal trainer','lateral','possible','none','1–3 years','verified','src_aza_jobs','Aquarium training roles share husbandry and behavior experience.'),
('Aquarist / aquarium animal-care specialist','Animal collection / management specialist','natural_growth','common','none','5+ years','supported','src_aza_types','Senior/head aquarist progression can lead to management.'),
('Behavioral husbandry specialist','Animal welfare / behavior coordinator','natural_growth','common','none','2–5 years','supported','src_aza_curator_behavior','Behavioral husbandry and welfare leadership strongly overlap.'),
('Behavioral husbandry specialist','Animal welfare scientist','research_progression','possible','M.S./Ph.D. commonly needed','variable','supported','src_abs_caab','Applied behavior/welfare expertise can progress into research-focused welfare science with graduate training.'),
('Zoo behavioral-husbandry specialist','Zoo animal curator','management','possible','none_or_grad','5+ years','verified','src_aza_curator_behavior','Curator of Behavioral Husbandry is a verified leadership pathway.'),
('Science-based animal trainer','Canine behavior consultant','specialization','possible','none','300+ behavior-consulting hours for CBCC-KA eligibility','verified','src_ccpdt_cbcc','Behavior consulting is a distinct advanced practice area.'),
('Shelter behavior specialist / coordinator','Canine behavior consultant','specialization','common','none','substantial behavior-case experience','supported','src_iaabc_shelter','Shelter behavior experience overlaps with behavior-consulting competencies.'),
('Conservation-breeding technician','Conservation-breeding scientist','research_progression','common','M.S./Ph.D. often useful','2–5 years','supported','src_aza_pmc','Technical breeding experience can progress toward research/science roles.'),
('Conservation-breeding technician','SSP coordinator / studbook keeper','professional_assignment','possible','none','professional zoo experience','verified','src_aza_program_roles','AZA program-leader roles are assigned to experienced zoo professionals.'),
('Population biologist / zoo population management scientist','Zoo conservation coordinator','lateral','possible','none','2–5 years','supported','src_aza_pmc','Population-management expertise connects to zoo conservation program work.'),
('SSP coordinator / studbook keeper','Population biologist / zoo population management scientist','research_progression','possible','M.S./Ph.D. may be needed','variable','supported','src_aza_pmc','Population planning and quantitative population science overlap but are not identical roles.'),
('Zoo registrar / animal records & permits specialist','Animal collection / management specialist','natural_growth','possible','none','3–5+ years','verified','src_aza_registrar','Records/transactions work can broaden into collection operations.'),
('Zoo animal nutritionist / nutrition coordinator','Animal collection / management specialist','lateral','possible','none','3–5+ years','supported','src_aza_jobs','Nutrition managers work closely with collection operations and animal-care leadership.'),
('Wildlife technician / biological science technician','Wildlife biologist','natural_growth','common','B.S. required for many professional roles','1–3+ years','verified','src_usajobs_wildtech','Technician experience is a common entry route into professional wildlife biology.'),
('Wildlife technician / biological science technician','Wildlife diversity / nongame biologist','natural_growth','common','B.S.; M.S. may help','1–3+ years','verified','src_tws_diversitytech','Current biodiversity technician work aligns with nongame/diversity biologist progression.'),
('Wildlife technician / biological science technician','eDNA / molecular ecology technician','lateral','possible','none','0–2 years','verified','src_tws_jobs','Current eDNA lab technician titles provide a molecular-monitoring lateral option.'),
('Wildlife technician / biological science technician','GIS / wildlife spatial analyst','specialization','possible','none','1–3 years + GIS skills','supported','src_tws_diversitytech','Field technicians with GIS/data skills can specialize spatially.'),
('Wildlife biologist','Species recovery biologist','specialization','common','M.S. often useful','2–5+ years','supported','src_usajobs_fwbio','Agency wildlife biology commonly includes threatened/endangered species recovery work.'),
('Wildlife biologist','Habitat / wildlife management biologist','lateral','common','none','2–5 years','supported','src_tws_jobs','Field and population biology can shift toward habitat-focused management.'),
('Wildlife biologist','Wildlife refuge manager','management','possible','specific 0485 coursework + experience','5+ years','verified','src_opm_0485','Refuge management is a distinct federal progression with specific coursework.'),
('Wildlife biologist','Wildlife program manager','management','common','none_or_grad','5–10+ years','verified','src_tws_wildlife_manager','Regional wildlife program manager is a verified leadership role.'),
('Wildlife biologist','Movement / spatial ecologist','specialization','possible','M.S. often useful','2–5 years','supported','src_usgs_npwrc','Spatial and movement specialties build on wildlife ecology plus quantitative methods.'),
('Wildlife biologist','Research ecologist','research_progression','possible','Ph.D. common for independent federal research','variable','verified','src_usgs_eesc','USGS research ecologist/wildlife biologist titles demonstrate research specialization.'),
('Wildlife rehabilitator','Wildlife rehabilitation / release coordinator','natural_growth','common','none','2–5 years','supported','src_nwra_jobs','Rehabilitation experience can expand into release/logistics coordination.'),
('Wildlife rehabilitator','Wildlife rehabilitation program manager','management','common','none','3–5+ years','verified','src_nwra_manager','Current wildlife care manager postings explicitly require progressive rehab/animal-care experience.'),
('Wildlife rehabilitation / release coordinator','Reintroduction / release field technician','lateral','possible','none','field monitoring skills helpful','supported','src_nwra_jobs','Release logistics can transition toward field-based reintroduction work.'),
('Reintroduction / release field technician','Post-release monitoring biologist','natural_growth','common','B.S.; M.S. may help','1–3 years','supported','src_tws_jobs','Field release experience leads naturally to monitoring/analysis roles.'),
('Post-release monitoring biologist','Species recovery biologist','natural_growth','possible','M.S. often useful','2–5 years','supported','src_usajobs_fwbio','Monitoring data feed directly into species-recovery decisions.'),
('Conservation delivery / habitat program coordinator','Natural-resource manager','natural_growth','common','none_or_grad','5+ years','verified','src_tws_habitatdelivery','Habitat delivery coordination develops program-management responsibilities.'),
('Habitat / wildlife management biologist','Conservation delivery / habitat program coordinator','lateral','common','none','2–5 years','verified','src_tws_habitatdelivery','Habitat biology and delivery coordination are adjacent applied conservation roles.'),
('GIS / wildlife spatial analyst','Remote sensing / geospatial ecologist','specialization','common','M.S. useful for advanced ecology','2–5 years','verified','src_usgs_npwrc','GIS roles can deepen into geospatial/remote-sensing ecology.'),
('GIS / wildlife spatial analyst','Ecological data scientist','lateral','possible','none_or_grad','2–5 years','verified','src_usgs_eesc','Spatial analysts can broaden into ecological data science.'),
('Quantitative ecology research assistant','Research statistician — ecology/biology','research_progression','possible','M.S./Ph.D. commonly needed','variable','verified','src_usgs_eesc','USGS research-statistician titles demonstrate an advanced quantitative pathway.'),
('Quantitative ecology research assistant','Quantitative ecologist / biometrician','natural_growth','common','M.S. often useful','2–5 years','supported','src_usgs_eesc','Research-assistant quantitative work commonly precedes specialist ecology roles.'),
('Ecological data scientist','Quantitative ecologist / biometrician','specialization','possible','M.S. often useful','2–5 years','supported','src_usgs_eesc','Data-science skills can specialize into quantitative ecological inference.'),
('eDNA / molecular ecology technician','Conservation geneticist / wildlife genomicist','research_progression','common','M.S./Ph.D. commonly needed','2–5 years','verified','src_aza_genetics','Molecular technician experience is a natural foundation for conservation genetics research.'),
('Research ecologist','Research scientist / principal investigator','research_progression','common','Ph.D. typical','5+ years','verified','src_usgs_eesc','Independent research scientists commonly advance through research-specialist roles.'),
('Conservation geneticist / wildlife genomicist','Research scientist / principal investigator','research_progression','common','Ph.D. typical','5+ years','verified','src_aza_genetics','Independent genetics research commonly progresses to PI/scientist leadership.'),
('University / laboratory research assistant','Research / laboratory manager — behavioral or biological science','natural_growth','common','none_or_grad','2–5 years','verified','src_tws_labmanager','Current lab-manager postings show a B.S.-accessible management step after research experience.'),
('University / laboratory research assistant','M.S. in animal behavior / ethology','graduate_transition','common','M.S.','0–3 years','supported','src_abs_caab','Research experience strengthens preparation for research-based graduate study.'),
('Research / laboratory manager — behavioral or biological science','Research scientist / principal investigator','research_progression','possible','Ph.D. usually needed','variable','supported','src_usgs_eesc','Lab management can precede independent research after graduate training.'),
('Zoo / aquarium educator','Conservation outreach / program coordinator','natural_growth','common','none','2–5 years','supported','src_aza_types','Education roles can progress to program coordination and leadership.'),
('Naturalist / interpretive educator','Wildlife / environmental educator','natural_growth','common','none','1–3 years','supported','src_tws_jobs','Interpretive work provides a foundation for broader environmental education.'),
]

CREDENTIALS=[
('cred_tws_awb','Associate Wildlife Biologist®','The Wildlife Society','professional certification','Academic credential for wildlife professionals demonstrating qualifying coursework.','src_tws_cert'),
('cred_tws_cwb','Certified Wildlife Biologist®','The Wildlife Society','professional certification','Professional wildlife credential requiring qualifying education and professional experience; upgrade commonly follows five years of professional experience.','src_tws_cert'),
('cred_fws_rehab','Federal Migratory Bird Rehabilitation Permit','U.S. Fish and Wildlife Service','permit','Required to rehabilitate covered migratory birds; current federal requirements include age 18+, at least 100 hands-on hours over at least one year for each bird type, and state compliance.','src_fws_rehab'),
('cred_abs_acaab','Associate Certified Applied Animal Behaviorist (ACAAB)','Animal Behavior Society','professional certification','Requires a research-based master’s degree in a biological or behavioral science with animal-behavior emphasis plus experience and endorsement requirements.','src_abs_caab'),
('cred_abs_caab','Certified Applied Animal Behaviorist (CAAB)','Animal Behavior Society','professional certification','Advanced applied animal behavior certification generally requiring relevant doctoral-level preparation plus professional experience.','src_abs_caab'),
('cred_ccpdt_cbcc','CBCC-KA®','Certification Council for Professional Dog Trainers','professional certification','Advanced canine behavior-consultant credential; current eligibility includes 300 hours of behavior consulting within the previous three years plus attestation and exam requirements.','src_ccpdt_cbcc'),
('cred_iaabc_sba','Shelter Behavior Affiliate (SBA)','International Association of Animal Behavior Consultants','professional credential','Shelter-behavior credential with recommended shelter experience and knowledge of learning/behavior change.','src_iaabc_shelter'),
]

QUALIFICATIONS=[
('qual_0486','Wildlife biologist','U.S. Office of Personnel Management','0486','Federal Wildlife Biology Series 0486','Degree or equivalent biological-science preparation.','Nonresearch positions: at least 9 semester hours wildlife subjects, 12 zoology, and 9 botany/plant sciences. Research positions also require 15 hours across physical/mathematical/earth sciences.','Grade-specific experience/education applies beyond the basic requirement.','src_opm_0486'),
('qual_0485','Wildlife refuge manager','U.S. Office of Personnel Management','0485','Federal Wildlife Refuge Management Series 0485','Degree in zoology, wildlife management, or appropriate biology field, or equivalent combination.','At least 9 semester hours zoology; 6 wildlife courses; 3 botany; 3 conservation biology.','Progressive grade-specific experience applies for manager positions.','src_opm_0485'),
('qual_0410','Zoologist','U.S. Office of Personnel Management','0410','Federal Zoology Series 0410','Degree in zoology or related science.','At least 20 semester hours in zoology and related animal sciences for related-discipline degrees.','Grade-specific experience/graduate education applies.','src_opm_0410'),
('qual_0408','Research ecologist','U.S. Office of Personnel Management','0408','Federal Ecology Series 0408','Degree in biology or related field underlying ecological research.','At least 30 semester hours biological sciences, including 9 ecology and 12 physical/mathematical sciences.','Grade-specific experience/graduate education applies.','src_opm_0408'),
('qual_0440','Conservation geneticist / wildlife genomicist','U.S. Office of Personnel Management','0440','Federal Genetics Series 0440','Degree in genetics or a basic biological science.','At least 9 semester hours in genetics for related biological-science degrees.','Graduate training is common because specialized genetics preparation may be limited at undergraduate level.','src_opm_0440'),
]

# Career-credential mapping by canonical name.
CRED_MAP=[
('Wildlife biologist','cred_tws_awb','useful','Can document qualifying wildlife coursework at/after graduation.'),
('Wildlife biologist','cred_tws_cwb','useful_later','Professional credential after qualifying education and experience.'),
('Wildlife diversity / nongame biologist','cred_tws_awb','useful','Useful professional wildlife credential.'),
('Habitat / wildlife management biologist','cred_tws_awb','useful','Useful professional wildlife credential.'),
('Wildlife rehabilitator','cred_fws_rehab','required_for_covered_birds','Federal permit required for migratory-bird rehabilitation; state requirements also apply.'),
('Wildlife rehabilitation program manager','cred_fws_rehab','role_dependent','At least one qualified/permitted person must cover federally regulated rehabilitation activities.'),
('Animal behaviorist / applied animal behavior scientist','cred_abs_acaab','useful_or_role_defining','Relevant for advanced professional applied-animal-behavior practice.'),
('Animal behaviorist / applied animal behavior scientist','cred_abs_caab','useful_or_role_defining','Advanced certification for doctoral-level applied behavior professionals.'),
('Canine behavior consultant','cred_ccpdt_cbcc','useful','Independent certification for experienced canine behavior consultants.'),
('Shelter behavior specialist / coordinator','cred_iaabc_sba','useful','Shelter-specific behavior credential.'),
]

# --- Program competencies derived from current program text and known structure ---
PROG_COMP={
'ME-WE':{'comp_field':3,'comp_ecology':3,'comp_population':3,'comp_habitat':3,'comp_gis':3,'comp_stats':3,'comp_research':2.5,'comp_writing':2.5,'comp_behavior_obs':1.8,'comp_telemetry':3,'comp_conservation':3,'comp_speciesid':2.7},
'ME-ZOO':{'comp_behavior_obs':2.2,'comp_ecology':2.6,'comp_speciesid':2.5,'comp_physiology':2.7,'comp_neuro':2.2,'comp_genetics':2.5,'comp_research':2.8,'comp_stats':2.0,'comp_writing':2.0,'comp_conservation':2.0},
'UMA-BIO':{'comp_behavior_obs':2.4,'comp_cognition':1.8,'comp_ecology':2.4,'comp_physiology':2.7,'comp_neuro':2.3,'comp_genetics':2.8,'comp_stats':2.5,'comp_research':3,'comp_writing':2.3,'comp_conservation':2.0},
'UMA-WEC':{'comp_field':3,'comp_ecology':3,'comp_population':3,'comp_habitat':3,'comp_gis':3,'comp_stats':3,'comp_conservation':3,'comp_research':2.5,'comp_speciesid':2.7,'comp_writing':2.4},
'UMA-AS':{'comp_husbandry':3,'comp_welfare':2.7,'comp_physiology':3,'comp_nutrition':3,'comp_genetics':2.5,'comp_learning':2,'comp_behavior_obs':2,'comp_research':2.5,'comp_stats':2,'comp_writing':1.7},
'URI-W':{'comp_field':3,'comp_ecology':3,'comp_population':2.8,'comp_habitat':2.7,'comp_stats':2.7,'comp_behavior_obs':2,'comp_conservation':3,'comp_research':2.7,'comp_speciesid':2.8,'comp_writing':2.3},
'URI-WZ':{'comp_field':3,'comp_ecology':3,'comp_population':2.8,'comp_conservation':3,'comp_husbandry':2.5,'comp_welfare':3,'comp_learning':2.8,'comp_behavior_obs':2.7,'comp_research':2.7,'comp_public':2,'comp_stats':2.5},
'URI-AZ':{'comp_husbandry':3,'comp_welfare':3,'comp_learning':3,'comp_behavior_obs':2.7,'comp_physiology':3,'comp_nutrition':2.5,'comp_research':2.5,'comp_public':2,'comp_records':1.8,'comp_stats':2},
'UNE-AB':{'comp_behavior_obs':3,'comp_learning':3,'comp_cognition':3,'comp_welfare':3,'comp_husbandry':2.5,'comp_enrichment':3,'comp_research':2.8,'comp_stats':2.4,'comp_public':1.7,'comp_ecology':2},
'UNE-AN':{'comp_behavior_obs':3,'comp_learning':3,'comp_cognition':3,'comp_welfare':2.7,'comp_neuro':3,'comp_physiology':2.5,'comp_research':3,'comp_stats':2.4,'comp_husbandry':2.2,'comp_enrichment':2.5},
}

# Generic competency inference for existing careers based on name/details/work tags.
KEYWORD_COMP=[
('comp_behavior_obs',['behavior','cognition','learning','communication','etholog']),('comp_learning',['training','trainer','learning','behaviorist']),('comp_welfare',['welfare','husbandry','enrichment']),('comp_husbandry',['keeper','aquarist','caregiver','caretaker','animal care','husbandry','rehabilit']),('comp_rehab',['rehabilit']),('comp_release',['reintroduction','release','post-release']),('comp_field',['wildlife','field','habitat','ecolog','ornith','mammalog','herpet']),('comp_speciesid',['ornith','mammalog','herpet','zoolog','field ecologist']),('comp_ecology',['ecolog','wildlife','conservation','habitat']),('comp_population',['population','wildlife biologist','conservation biologist']),('comp_habitat',['habitat','restoration','natural-resource']),('comp_conservation',['conservation','wildlife','endangered','restoration']),('comp_telemetry',['movement','telemetry','post-release']),('comp_gis',['gis','spatial','movement']),('comp_stats',['quantitative','biometric','statistic','data','research']),('comp_research',['research','scientist','professor','ecologist','biologist']),('comp_writing',['writer','communicator','research','coordinator','biologist']),('comp_physiology',['physiolog','ecophysiology']),('comp_neuro',['neuro']),('comp_genetics',['genetic','evolution']),('comp_regulatory',['permitting','compliance','agency','manager']),('comp_public',['educator','naturalist','outreach','communicator','trainer','service-dog'])]


def main():
    if DB.exists(): DB.unlink()
    con=sqlite3.connect(DB)
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript(SCHEMA.read_text())
    con.execute('INSERT INTO ingest_batches VALUES (?,?,?,?,?,?)',('batch_20260908_market_expansion','legacy migration + 2026 market-validation expansion',TODAY,None,'running','Initial normalized research-database build.'))
    con.executemany('INSERT INTO domains VALUES (?,?,?)',DOMAINS)
    con.executemany('INSERT INTO role_families VALUES (?,?,?,?)',FAMILIES)
    # Metadata
    con.executemany('INSERT INTO metadata(key,value) VALUES (?,?)',[
        ('schema_version','1.0'),('dataset_version','2026-09-08.1'),('retrieved_date',TODAY),('canonical_source','SQLite'),('notes','Initial normalized migration plus first real-market validation expansion.')])
    # Programs
    program_ids={}
    for p in D['programs']:
        pid='prg_'+p['code'].lower().replace('-','_'); program_ids[p['code']]=pid
        con.execute('INSERT INTO programs(program_id,code,school,title,program_type,profile_json,last_verified) VALUES (?,?,?,?,?,?,?)',(pid,p['code'],p['school'],p['title'],p.get('type'),json.dumps(p,ensure_ascii=False),TODAY))
    # Existing careers
    career_ids={}
    seq=1
    for c in D['careers']:
        cid=f'cr_{seq:04d}';seq+=1;career_ids[c['name']]=cid
        fam=family_for(c['name'],c['category'])
        desc=c.get('roleFocus') or c.get('details',{}).get('Typical education / progression','')
        con.execute('''INSERT INTO career_roles(career_id,family_id,name,slug,role_kind,market_status,evidence_status,description,education_summary,direct_animal_contact,career_stage,last_verified,source_origin)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cid,fam,c['name'],slug(c['name']),role_kind(c),c.get('details',{}).get('Market status'),evidence_status(c),desc,c.get('educationBand'),c.get('directContact'),career_stage(c),TODAY,'legacy_researched_matrix'))
        for k,score in zip(DIM_KEYS,c.get('dims',[0]*10)): con.execute('INSERT INTO career_dimensions VALUES (?,?,?)',(cid,k,float(score)))
        for tag in c.get('workTags',[]): con.execute('INSERT INTO career_work_tags VALUES (?,?)',(cid,tag))
        for code,supp in c.get('support',{}).items(): con.execute('INSERT INTO career_program_support(career_id,program_id,support_code,source_origin) VALUES (?,?,?,?)',(cid,program_ids[code],supp,'legacy_researched_matrix'))
    # New careers
    for c in NEW_ROLES:
        cid=f'cr_{seq:04d}';seq+=1;career_ids[c['name']]=cid
        con.execute('''INSERT INTO career_roles(career_id,family_id,name,slug,role_kind,market_status,evidence_status,description,education_summary,direct_animal_contact,career_stage,last_verified,source_origin)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cid,c['family_id'],c['name'],slug(c['name']),c['role_kind'],c['market_status'],c['evidence_status'],c['description'],c['educationBand'],c['directContact'],c['career_stage'],TODAY,'2026_market_expansion'))
        for k,score in zip(DIM_KEYS,c['dims']): con.execute('INSERT INTO career_dimensions VALUES (?,?,?)',(cid,k,float(score)))
        for tag in c['workTags']: con.execute('INSERT INTO career_work_tags VALUES (?,?)',(cid,tag))
        for code,supp in c['support'].items(): con.execute('INSERT INTO career_program_support(career_id,program_id,support_code,source_origin) VALUES (?,?,?,?)',(cid,program_ids[code],supp,'2026_market_expansion'))
    # Search aliases are not direct market observations. They preserve useful query terms while observed_titles remains evidence-only.
    alias_i=0
    for c in list(D['careers'])+list(NEW_ROLES):
        cid=career_ids[c['name']]
        for key,atype in [('Searchable job titles','searchable_title'),('Alternate names / terms','alternate_term')]:
            val=(c.get('details') or {}).get(key)
            if not val: continue
            for a in [x.strip() for x in str(val).split(';') if x.strip()]:
                alias_i+=1
                con.execute('INSERT OR IGNORE INTO career_aliases(alias_id,career_id,alias,alias_type,source_id,verification_status) VALUES (?,?,?,?,?,?)',(f'alias_{alias_i:04d}',cid,a,atype,None,'curated_search_term'))
    # Sources
    con.executemany('INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)',SOURCES+SPECIFIC_SOURCES)
    # Competencies
    con.executemany('INSERT INTO competencies VALUES (?,?,?,?)',COMPETENCIES)
    # Program competencies
    for code,vals in PROG_COMP.items():
        for comp,strength in vals.items(): con.execute('INSERT INTO program_competencies VALUES (?,?,?,?)',(program_ids[code],comp,strength,'Curated from current program curriculum/profile research.'))
    # Career competencies existing inference
    for c in D['careers']:
        cid=career_ids[c['name']]; blob=(c['name']+' '+c.get('roleFocus','')+' '+' '.join(c.get('workTags',[]))+' '+json.dumps(c.get('details',{}))).lower()
        comps=[]
        for comp,keys in KEYWORD_COMP:
            if any(k in blob for k in keys): comps.append(comp)
        for comp in dict.fromkeys(comps): con.execute('INSERT OR IGNORE INTO career_competencies VALUES (?,?,?)',(cid,comp,'important'))
    for name,comps in NEW_COMP.items():
        for comp in comps: con.execute('INSERT OR IGNORE INTO career_competencies VALUES (?,?,?)',(career_ids[name],comp,'important'))
    # Postings + title observations + salary observations
    for i,p in enumerate(POSTINGS,1):
        name,title,emp,loc,pdate,ed,exp,smin,smax,sunit,src,url,notes=p
        if name not in career_ids:
            raise KeyError(f'Posting career missing: {name}')
        pid=f'post_{i:04d}';cid=career_ids[name]
        con.execute('''INSERT INTO job_postings(posting_id,career_id,title,employer,location,posted_date,retrieved_date,education_min,experience_min,salary_min,salary_max,salary_unit,source_id,url,active_status,notes)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(pid,cid,title,emp,loc,pdate,TODAY,ed,exp,smin,smax,sunit,src,url,'current_or_recent',notes))
        oid=f'obs_post_{i:04d}'
        con.execute('INSERT INTO observed_titles VALUES (?,?,?,?,?,?,?,?,?)',(oid,cid,title,emp,loc,'job_posting',pdate or TODAY,src,notes))
        if smin is not None:
            amin,amax=smin,smax
            if sunit=='hourly': amin=smin*2080;amax=(smax if smax is not None else smin)*2080
            con.execute('INSERT INTO salary_observations VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(f'sal_{i:04d}',cid,pid,'job_posting',loc,smin,smax,sunit,amin,amax,pdate or TODAY,notes))
    # Non-posting observed titles
    for i,o in enumerate(OBSERVED_TITLES,1):
        name,title,org,loc,otype,odate,src,notes=o
        con.execute('INSERT INTO observed_titles VALUES (?,?,?,?,?,?,?,?,?)',(f'obs_dir_{i:04d}',career_ids[name],title,org,loc,otype,odate,src,notes))
    # Credentials
    con.executemany('INSERT INTO credentials VALUES (?,?,?,?,?,?)',CREDENTIALS)
    for name,cred,rel,notes in CRED_MAP:
        con.execute('INSERT INTO career_credentials VALUES (?,?,?,?)',(career_ids[name],cred,rel,notes))
    # Qualifications
    for qid,name,org,series,qname,edu,course,exp,src in QUALIFICATIONS:
        con.execute('INSERT INTO qualification_profiles VALUES (?,?,?,?,?,?,?,?,?)',(qid,career_ids[name],org,series,qname,edu,course,exp,src))
    # Edges
    for i,e in enumerate(EDGES,1):
        frm,to,rel,typ,edu,exp,status,src,notes=e
        con.execute('INSERT INTO career_edges VALUES (?,?,?,?,?,?,?,?,?,?)',(f'edge_{i:04d}',career_ids[frm],career_ids[to],rel,typ,edu,exp,status,src,notes))
    # Evidence records from authoritative sources
    evid=[]
    def add(entity_name,claim_type,value,src,conf='high',status='verified',notes=None):
        evid.append((f'ev_{len(evid)+1:04d}','career',career_ids[entity_name],claim_type,value,src,conf,status,None,TODAY,notes))
    add('Wildlife biologist','qualification','Federal GS-0486 nonresearch positions require 9 semester hours wildlife subjects, 12 zoology, and 9 botany/plant sciences.','src_opm_0486')
    add('Wildlife refuge manager','qualification','Federal GS-0485 requires zoology/wildlife/biology preparation including 9 hours zoology, 6 wildlife, 3 botany, and 3 conservation biology.','src_opm_0485')
    add('Zoologist','qualification','Federal GS-0410 requires zoology or related science with at least 20 semester hours zoology/related animal sciences.','src_opm_0410')
    add('Research ecologist','qualification','Federal GS-0408 requires 30 biological-science hours including 9 ecology and 12 physical/mathematical sciences.','src_opm_0408')
    add('Conservation geneticist / wildlife genomicist','qualification','Federal GS-0440 genetics work requires genetics or related biological science with at least 9 semester hours genetics.','src_opm_0440')
    add('Wildlife rehabilitator','permit','Federal migratory-bird rehabilitation requires a permit, state compliance, and at least 100 hands-on hours over at least one year for each migratory-bird type.','src_fws_rehab')
    add('Animal behaviorist / applied animal behavior scientist','credential','ACAAB requires research-based master’s preparation in biological/behavioral science with animal-behavior emphasis; CAAB is a higher doctoral-level certification route.','src_abs_caab')
    add('Canine behavior consultant','credential','CBCC-KA eligibility includes at least 300 hours of canine behavior consulting within the previous three years plus attestation and examination requirements.','src_ccpdt_cbcc')
    add('Population biologist / zoo population management scientist','market_structure','AZA Population Management Center staff include Population Biologists, a Planning Coordinator, and research support who conduct demographic/genetic analyses for SSP programs.','src_aza_pmc')
    add('SSP coordinator / studbook keeper','professional_role','AZA formally defines SSP Coordinator and Studbook Keeper responsibilities and associated training/accountability requirements.','src_aza_program_roles')
    add('Zoo registrar / animal records & permits specialist','market_title','Current/recent AZA postings verify Registrar as a dedicated zoo role managing records, permits, transfers, ZIMS, and related databases.','src_aza_registrar')
    add('Zoo behavioral-husbandry specialist','market_title','Current/recent AZA postings include Curator of Behavioral Husbandry and Wildlife Care Specialist, Behavior.','src_aza_curator_behavior')
    add('Zoo / aquarium animal trainer','market_title','Current AZA postings include Trainer, Senior Trainer, Assistant Trainer, and species-specific training roles.','src_aza_senior_trainer')
    add('Wildlife rehabilitation program manager','market_title','Current NWRA postings include Wildlife Care Manager and rehabilitation roles with staff, permit, budget, and program oversight.','src_nwra_manager')
    add('Conservation delivery / habitat program coordinator','market_title','Current TWS postings include Habitat Delivery Coordinator and Conservation Delivery Specialist.','src_tws_habitatdelivery')
    add('Wildlife program manager','market_title','Current TWS postings include Regional Wildlife Program Manager and Applied Research Section Manager.','src_tws_wildlife_manager')
    add('Research statistician — ecology/biology','market_title','USGS ecological science centers employ Research Statistician and Research Statistician (Biology) titles.','src_usgs_eesc')
    add('Ecological data scientist','market_title','USGS ecological science centers include the title Biologist (Data Scientist).','src_usgs_eesc')
    add('Research ecologist','market_title','USGS ecological science centers employ Research Ecologist and Supervisory Research Ecologist roles.','src_usgs_eesc')
    con.executemany('INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?)',evid)
    # Upgrade evidence status for any career with current/recent posting observations.
    con.execute("""UPDATE career_roles SET evidence_status='verified_current_market'
                   WHERE career_id IN (SELECT DISTINCT career_id FROM job_postings)
                   AND role_kind!='education_path'""")
    # Automatically create a transparent research-review queue for known coverage gaps.
    review_i=0
    for cid,name,kind in con.execute('SELECT career_id,name,role_kind FROM career_roles WHERE active=1'):
        if kind=='education_path': continue
        obs=con.execute('SELECT COUNT(*) FROM observed_titles WHERE career_id=?',(cid,)).fetchone()[0]
        posts=con.execute('SELECT COUNT(*) FROM job_postings WHERE career_id=?',(cid,)).fetchone()[0]
        edges=con.execute('SELECT COUNT(*) FROM career_edges WHERE from_career_id=? OR to_career_id=?',(cid,cid)).fetchone()[0]
        if obs==0:
            review_i+=1;con.execute('INSERT INTO review_queue VALUES (?,?,?,?,?,?,?,?,?)',(f'review_{review_i:04d}','career',cid,'observed_title_coverage','high','open',TODAY,None,'Find authoritative employer/professional examples of actual titles.'))
        elif posts==0:
            review_i+=1;con.execute('INSERT INTO review_queue VALUES (?,?,?,?,?,?,?,?,?)',(f'review_{review_i:04d}','career',cid,'current_posting_coverage','medium','open',TODAY,None,'Add current/recent posting evidence when available.'))
        if edges==0 and kind not in ('scientific_specialty','later_career'):
            review_i+=1;con.execute('INSERT INTO review_queue VALUES (?,?,?,?,?,?,?,?,?)',(f'review_{review_i:04d}','career',cid,'progression_coverage','low','open',TODAY,None,'Research explicit natural-growth, lateral, or specialization transitions.'))
    con.execute('UPDATE ingest_batches SET completed_at=?,status=? WHERE batch_id=?',(TODAY,'complete','batch_20260908_market_expansion'))
    con.commit()
    con.close()
    print(f'Built {DB}')

if __name__=='__main__': main()
