"""Build a script-independent comparison from the current program library.

Each program compares concrete experience, study and planning decisions.
Requirements must be distinguished from elective opportunities. Detailed source
URLs and review dates are retained in comparison-notes.json; dates are not
rendered in the comparison cards.
"""
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

# Credential shape, short enough to scan. Derived from the program title only.
DEGREE = {
    'ME-WE': 'B.S.',
    'ME-ZOO': 'B.S.',
    'UMA-BGR-VT': 'A.S. or B.S.',
    'UMA-BIO': 'B.S.',
    'UMA-WEC': 'B.S. (concentration)',
    'UMA-VT': 'B.S.',
    'UNE-AB': 'B.S.',
    'UNH-ZOO': 'B.S.',
    'URI-AZ': 'B.S. + certificate',
    'URI-W': 'B.S.',
    'URI-WZ': 'B.S. + certificate',
    'CAN-ABEC': 'B.S. + minor',
    'DELVAL-ZOO': 'B.S.',
    'CANTON-VT': 'B.S. (on A.A.S. core)',
    'DELHI-VT': 'A.A.S. → B.S.',
}

def theme_for(field):
    if field.startswith('veterinary-'):
        return 'veterinary'
    if field in ('animal-behavior', 'animal-cognition', 'anthrozoology'):
        return 'behavior'
    if field in ('animal-welfare', 'animal-science', 'zoo-aquarium-science'):
        return 'care'
    if field.startswith(('wildlife-', 'conservation-', 'ecology', 'marine-', 'environmental-')):
        return 'wildlife'
    return 'biology'

# Concrete comparison summaries and primary sources are kept separately from
# program requirements. Review these whenever the linked curriculum changes.
def build():
    text = (SITE / 'data.js').read_text()
    data = json.loads(text.split('=', 1)[1].strip().removesuffix(';'))
    details = {p['code']: p for p in data['programs'] + read('content/programs/additional-programs.json')}
    library = read('content/programs/school-library.json')
    manifest = read('content/areas/index.json')
    fields = {a['id']: a for a in [read('content/areas/' + name) for name in manifest['areas']]}
    programs = [{**details[item['code']], **item} for item in library['programs']]
    new_england = {'University of Maine', 'University of Maine at Augusta', 'UMass Amherst',
                   'University of Massachusetts Amherst', 'University of New England',
                   'University of Rhode Island', 'University of New Hampshire'}
    programs.sort(key=lambda p: (p['school'] not in new_england, school_name(p), p['title']))

    notes = read('content/programs/comparison-notes.json')
    codes = {p['code'] for p in programs}
    for name, table in (('comparison notes', notes), ('DEGREE', DEGREE)):
        missing, extra = codes - set(table), set(table) - codes
        assert not missing and not extra, f'{name} is out of step with the library: missing {missing}, extra {extra}'

    rows = []
    for p in programs:
        code = p['code']
        field_chips = ''.join(
            f'<a class="cmp-chip cmp-chip-field" href="areas/{escape(fid)}.html">{escape(fields[fid]["title"])}</a>'
            for fid in p['primaryFields'])
        theme = theme_for(p['primaryFields'][0])
        note = notes[code]
        for key in ('focus', 'experience', 'study', 'consider', 'sources', 'reviewedOn'):
            assert note.get(key), (code, key)
        studies = ''.join(f'<li>{escape(item)}</li>' for item in note['study'])
        considerations = ''.join(f'<li>{escape(item)}</li>' for item in note['consider'])
        sources = ' · '.join(f'<a href="{escape(url, quote=True)}">Official source{f" {index}" if len(note["sources"]) > 1 else ""}</a>' for index, url in enumerate(note['sources'], 1))
        rows.append(f'''<tr id="{code}" role="row" class="theme-{theme}">
          <th scope="row" role="rowheader" data-label="School and pathway"><small>{escape(school_name(p))}</small><a href="program.html?code={code}">{escape(p['title'])}</a><span class="cmp-degree">{escape(DEGREE[code])}</span></th>
          <td role="cell" data-label="Program focus"><p>{escape(note['focus'])}</p><div class="cmp-chips">{field_chips}</div></td>
          <td role="cell" data-label="Animal experience"><p>{escape(note['experience'])}</p><a class="cmp-more" href="program.html?code={code}#experience">Experience details →</a></td>
          <td role="cell" data-label="Study examples"><ul class="cmp-list">{studies}</ul></td>
          <td role="cell" data-label="Planning considerations"><ul class="cmp-list">{considerations}</ul><p class="cmp-sources">{sources}</p><a class="cmp-more" href="program.html?code={code}">Full program guide →</a></td>
        </tr>''')

    template = (SITE / 'programs.html').read_text()
    template = template.replace('<a class="active" href="programs.html">', '<a href="programs.html">') \
        .replace('<a href="compare.html">Compare Programs</a>', '<a class="active" aria-current="page" href="compare.html">Compare Programs</a>')
    template = template.replace('<title>School &amp; Program Library | Animal Education Pathways</title>',
                                '<title>Compare Programs | Animal Education Pathways</title>')
    template = template.replace('Browse researched undergraduate animal-related programs by school, field, and program emphasis.',
                                'Compare animal-related college programs side by side: program focus, actual animal experience, coursework, and planning considerations.')

    content = f'''<main id="main" tabindex="-1" class="comparison-page">
      <header class="index-hero"><p class="eyebrow">School &amp; Program Library</p><h1>Compare Programs</h1><p>All {len(programs)} pathways side by side, New England first, then other schools. Open any program for its full rationale, tradeoffs, and sources.</p><p><a href="programs.html">Browse the program guides →</a></p></header>
      <details class="comparison-key" id="comparisonHelp">
        <summary>How to read this table</summary>
        <p><strong>Animal experience</strong> names the actual fieldwork, clinical practice, research or internship structure. Observation, animal handling and day-to-day husbandry provide different kinds of preparation.</p>
        <p><strong>Study examples</strong> show specific courses or subject areas. Requirements and electives are identified where established; these are examples, not a complete curriculum.</p>
        <p><strong>Planning considerations</strong> highlight differences that can affect the choice: species studied, campus moves, elective planning, and how a minor, certificate or associate-to-bachelor sequence fits together. Sources are linked in each card.</p>
      </details>
      <div class="comparison-scroll" role="region" aria-labelledby="comparisonCaption" aria-describedby="comparisonHelp">
        <table class="comparison-table" role="table"><caption id="comparisonCaption">Program pathways and documented preparation</caption>
          <thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">School and pathway</th><th scope="col" role="columnheader">Program focus</th><th scope="col" role="columnheader">Animal experience</th><th scope="col" role="columnheader">Study examples</th><th scope="col" role="columnheader">Planning considerations</th></tr></thead>
          <tbody role="rowgroup">{''.join(rows)}</tbody>
        </table>
      </div>
    </main>'''

    template = template.replace('<main id="app" tabindex="-1"></main>', content).replace('href="#app"', 'href="#main"')
    template = template.replace('  <script src="animal-details.js"></script>\n', '')
    template = template.replace('<script src="data.js"></script><script src="programs.js"></script>',
                                '<script src="navigation.js"></script>')
    (SITE / 'compare.html').write_text(template)
    print(f'Wrote comparison for {len(programs)} programs')

if __name__ == '__main__':
    build()
