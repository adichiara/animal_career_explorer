"""Build a script-independent comparison from the current program library.

Design rule: every cell must be scannable down its column. Anything that needs a
paragraph lives on the program page, which each row links to. Nothing here may
assert more than the source record establishes -- in particular, the absence of
a documented requirement is reported as "Not established", never as "No".
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

# Three states only, so the column can be read vertically. These restate the
# experience summaries previously held in this file; the full prose now lives on
# each program page. "Not established" means the record does not establish a
# required animal-contact component -- it does not mean the program lacks one.
BUILT_IN = 'built-in'
CHOICE = 'choice'
UNSTATED = 'unstated'

CONTACT_LABEL = {
    BUILT_IN: 'Built into the program',
    CHOICE: 'Depends on choices',
    UNSTATED: 'Not established in the record',
}

CONTACT = {
    'ME-WE': UNSTATED,
    'ME-ZOO': CHOICE,
    'UMA-BGR-VT': BUILT_IN,
    'UMA-BIO': CHOICE,
    'UMA-WEC': UNSTATED,
    'UMA-VT': BUILT_IN,
    'UNE-AB': CHOICE,
    'UNH-ZOO': UNSTATED,
    'URI-AZ': CHOICE,
    'URI-W': UNSTATED,
    'URI-WZ': CHOICE,
    'CAN-ABEC': UNSTATED,
    'DELVAL-ZOO': BUILT_IN,
    'CANTON-VT': BUILT_IN,
    'DELHI-VT': BUILT_IN,
}

# Competency records vary in how many entries they carry (5 to 12), so listing
# individual skill names made record completeness look like program strength.
# Rolling up to categories compresses that to 2-5 comparable chips per row.
STRONG = 2.4

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

    codes = {p['code'] for p in programs}
    for name, table in (('CONTACT', CONTACT), ('DEGREE', DEGREE)):
        missing, extra = codes - set(table), set(table) - codes
        assert not missing and not extra, f'{name} is out of step with the library: missing {missing}, extra {extra}'

    rows = []
    for p in programs:
        code = p['code']
        field_chips = ''.join(
            f'<a class="cmp-chip cmp-chip-field" href="areas/{escape(fid)}.html">{escape(fields[fid]["title"])}</a>'
            for fid in p['primaryFields'])
        categories = sorted({c['category'] for c in p.get('competencies', []) if float(c['strength']) >= STRONG})
        emphasis = ''.join(f'<span class="cmp-chip">{escape(c)}</span>' for c in categories) \
            or '<span class="cmp-none">Not documented</span>'
        state = CONTACT[code]
        rows.append(f'''<tr id="{code}">
          <th scope="row" data-label="School and pathway"><small>{escape(school_name(p))}</small><a href="program.html?code={code}">{escape(p['title'])}</a></th>
          <td data-label="Degree">{escape(DEGREE[code])}</td>
          <td data-label="Fields"><div class="cmp-chips">{field_chips}</div></td>
          <td data-label="Required animal contact"><span class="cmp-state cmp-state-{state}">{escape(CONTACT_LABEL[state])}</span> <a class="cmp-more" href="program.html?code={code}#experience">Details&nbsp;→</a></td>
          <td data-label="Documented emphasis"><div class="cmp-chips">{emphasis}</div></td>
          <td data-label="Verified">{escape(p.get('lastVerified') or 'Not recorded')}</td>
        </tr>''')

    template = (SITE / 'programs.html').read_text()
    template = template.replace('<a class="active" href="programs.html">', '<a href="programs.html">') \
        .replace('<a href="compare.html">Compare Programs</a>', '<a class="active" aria-current="page" href="compare.html">Compare Programs</a>')
    template = template.replace('<title>School &amp; Program Library | Animal Education Pathways</title>',
                                '<title>Compare Programs | Animal Education Pathways</title>')
    template = template.replace('Browse researched undergraduate animal-related programs by school, field, and program emphasis.',
                                'Compare animal-related college programs side by side: degree shape, connected fields, required animal contact, and documented emphasis.')

    content = f'''<main id="main" tabindex="-1" class="comparison-page">
      <header class="index-hero"><p class="eyebrow">School &amp; Program Library</p><h1>Compare Programs</h1><p>All {len(programs)} pathways side by side, New England first, then other schools. Open any program for its full rationale, tradeoffs, and sources.</p><p><a href="programs.html">Browse the program guides →</a></p></header>
      <details class="comparison-key" id="comparisonHelp">
        <summary>How to read this table</summary>
        <p><strong>Required animal contact</strong> has three values. <em>Built into the program</em> means the record documents required hands-on animal work. <em>Depends on choices</em> means it is available but set by electives, internships, or placements. <em>Not established in the record</em> means the official sources reviewed do not establish a required animal-contact component — it does not mean the program has none. Field research, observation, clinical practice, and direct animal care are different kinds of experience; check the program page for which applies.</p>
        <p><strong>Documented emphasis</strong> groups the stronger preparation areas described in each program guide. These summarize the existing curriculum review. They are not standardized ratings, guarantees, or rankings, and the number of areas shown partly reflects how much detail each record carries. Electives, concentrations, minors, and certificates determine much of what a student actually studies.</p>
        <p>Sources and verification notes for each program are on its own page.</p>
      </details>
      <div class="comparison-scroll" role="region" aria-labelledby="comparisonCaption" aria-describedby="comparisonHelp" tabindex="0">
        <table class="comparison-table"><caption id="comparisonCaption">Program pathways and documented preparation</caption>
          <thead><tr><th scope="col">School and pathway</th><th scope="col">Degree</th><th scope="col">Fields</th><th scope="col">Required animal contact</th><th scope="col">Documented emphasis</th><th scope="col">Verified</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </main>'''

    template = template.replace('<main id="app" tabindex="-1"></main>', content).replace('href="#app"', 'href="#main"')
    template = template.replace('<script src="data.js"></script><script src="programs.js"></script>',
                                '<script src="navigation.js"></script>')
    (SITE / 'compare.html').write_text(template)
    print(f'Wrote comparison for {len(programs)} programs')

if __name__ == '__main__':
    build()
