"""Build a script-independent comparison from the current program library."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

def read(path):
    return json.loads((SITE / path).read_text())

def school_name(program):
    return {
        'University of Maine': 'University of Maine (Orono)',
        'University of Maine at Augusta': 'University of Maine at Augusta (Bangor Campus)',
        'SUNY Canton': 'SUNY Canton (Canton Campus)',
        'SUNY Delhi': 'SUNY Delhi (Delhi Campus)',
        'UMass Amherst': 'University of Massachusetts Amherst',
    }.get(program['school'], program['school'])

# Summaries of the experience descriptions in the source records, not new claims.
# Absence of a documented requirement must never become a "No" or a "Yes".
EXPERIENCE = {
    'ME-ZOO': 'Choice-dependent. Field courses, research and internships are options; direct animal contact depends on choices outside the core.',
    'ME-WE': 'Structured wildlife fieldwork: field ecology, an intensive field survey and a telemetry-based capstone. Required hands-on animal care is not established.',
    'UMA-BIO': 'Choice-dependent. Animal experience must be assembled through research, internships or placements; it is not automatic.',
    'UMA-WEC': 'Structured wildlife preparation. The record establishes field-oriented coursework, but not a required animal-handling or care placement.',
    'UMA-VT': 'Built-in clinical practice: advanced clinical coursework, community clinic practica and senior internships after the move to Newton.',
    'UNE-AB': 'Observation, methods, research and internship work are built around the major. Sustained hands-on husbandry needs deliberate planning.',
    'URI-AZ': 'The combined pathway includes zoo-based management coursework and an internship-linked certificate practicum. Confirm the placement’s direct animal duties.',
    'URI-W': 'Research apprenticeship or internship pathways and advanced experiential options. Required direct animal handling is not established.',
    'URI-WZ': 'The added certificate includes zoo-based management coursework and an internship-linked practicum. Confirm direct animal duties and combined scheduling.',
    'CAN-ABEC': 'Credit-bearing internships and zoo/aquarium internship options. A required direct animal-care placement is not established in the record.',
    'UNH-ZOO': 'Field and laboratory research opportunities. Required husbandry or animal-care experience is not established.',
    'DELVAL-ZOO': 'Animal work starts in the first year. Required Experience360 experience includes internships; confirm each placement’s animal-care duties.',
    'UMA-BGR-VT': 'Hands-on clinical and laboratory training in Bangor is documented. Confirm required animal-contact hours and the A.S./B.S. sequence.',
    'CANTON-VT': 'The A.A.S. foundation includes hands-on labs, kennel-duty rotations and two clinical preceptorships; the B.S. builds on it.',
    'DELHI-VT': 'Live-animal labs begin in the first semester of the A.A.S.; clinical teaching and professional experience support the B.S. continuation.',
}

def build():
    text = (SITE / 'data.js').read_text()
    data = json.loads(text.split('=', 1)[1].strip().removesuffix(';'))
    details = {p['code']: p for p in data['programs'] + read('content/programs/additional-programs.json')}
    library = read('content/programs/school-library.json')
    manifest = read('content/areas/index.json')
    fields = {a['id']: a for a in [read('content/areas/' + name) for name in manifest['areas']]}
    programs = [{**details[item['code']], **item} for item in library['programs']]
    new_england = {'University of Maine', 'University of Maine at Augusta', 'UMass Amherst', 'University of Massachusetts Amherst', 'University of New England', 'University of Rhode Island', 'University of New Hampshire'}
    programs.sort(key=lambda p: (p['school'] not in new_england, school_name(p), p['title']))
    assert {p['code'] for p in programs} == set(EXPERIENCE), 'Update experience summaries when library membership changes'
    rows = []
    for p in programs:
        code = p['code']
        field_links = ''.join(f'<li><a href="areas/{escape(fid)}.html">{escape(fields[fid]["title"])}</a></li>' for fid in p['primaryFields'])
        strengths = [c['name'] for c in p.get('competencies', []) if float(c['strength']) >= 2.4]
        skills = '<ul>' + ''.join(f'<li>{escape(name)}</li>' for name in strengths) + '</ul>' if strengths else 'Not documented.'
        sources = []
        for i, url in enumerate(p.get('sources', []), 1):
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            sources.append(f'<a href="{escape(url, quote=True)}">Official source {i}</a>')
        rows.append(f'''<tr id="{code}">
          <th scope="row"><small>{escape(school_name(p))}</small><a href="program.html?code={code}">{escape(p['title'])}</a></th>
          <td><ul>{field_links}</ul></td>
          <td><p>{escape(EXPERIENCE[code])}</p><a href="program.html?code={code}#experience">Read experience details →</a></td>
          <td>{skills}</td>
          <td><p>{escape(p['lookFirst'])}</p></td>
          <td>{'<br>'.join(sources)}<small>Record verified: {escape(p.get('lastVerified') or 'Date not recorded')}</small></td>
        </tr>''')
    template = (SITE / 'programs.html').read_text()
    template = template.replace('<a class="active" href="programs.html">', '<a href="programs.html">').replace('<a href="compare.html">Compare Programs</a>', '<a class="active" aria-current="page" href="compare.html">Compare Programs</a>')
    template = template.replace('<title>School &amp; Program Library | Animal Education Pathways</title>', '<title>Compare Programs | Animal Education Pathways</title>')
    template = template.replace('Browse researched undergraduate animal-related programs by school, field, and program emphasis.', 'Compare animal-related college programs, animal experience, documented skills, and questions to check.')
    content = f'''<main id="main" tabindex="-1" class="comparison-page">
      <header class="index-hero"><p class="eyebrow">School &amp; Program Library</p><h1>Compare Programs</h1><p>Compare all {len(programs)} pathways, grouped by New England first and then other schools, alphabetically within each region.</p><p><a href="programs.html">Browse the program guides →</a></p></header>
      <div class="comparison-key" id="comparisonHelp"><p><strong>Animal experience varies.</strong> Field research, observation, clinical practice and direct animal care are different kinds of experience. A hands-on tag alone does not establish a requirement. Where the record does not establish required animal contact, the table says so.</p><p><strong>Skills listed</strong> are the stronger preparation areas described in each program guide. They summarize the existing curriculum review; they are not standardized ratings, guarantees, or rankings. Electives, concentrations, minors and certificates can determine what a student actually studies.</p><p>On a narrow screen, scroll the table horizontally. Open a program for its full rationale and tradeoffs, or a field for career context.</p></div>
      <div class="comparison-scroll" role="region" aria-labelledby="comparisonCaption" aria-describedby="comparisonHelp" tabindex="0">
        <table class="comparison-table"><caption id="comparisonCaption">Program pathways and documented preparation</caption>
          <thead><tr><th scope="col">School and pathway</th><th scope="col">Connected fields</th><th scope="col">Animal work in the program</th><th scope="col">Skills emphasized in the guide</th><th scope="col">What to check first</th><th scope="col">Sources and record date</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </main>'''
    template = template.replace('<main id="app" tabindex="-1"></main>', content).replace('href="#app"', 'href="#main"')
    template = template.replace('<script src="data.js"></script><script src="programs.js"></script>', '<script src="navigation.js"></script>')
    (SITE / 'compare.html').write_text(template)
    print(f'Wrote comparison for {len(programs)} programs')

if __name__ == '__main__':
    build()
