"""Check public navigation, comparison coverage, and accessibility landmarks."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
RETIRED = {'jobs.html', 'jobs.js', 'job.html', 'job-article.js', 'legacy.html', 'discover.html'}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.main = []
        self.skip = []
        self.rows = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
            if 'skip-link' in a.get('class', '').split():
                self.skip.append(a['href'])
        if tag == 'main':
            self.main.append(a)
        if tag == 'tr' and a.get('id'):
            self.rows.append(a['id'])

for name in RETIRED:
    assert not (SITE / name).exists(), name
pages = {p: Page(p.read_text()) for p in SITE.rglob('*.html') if 'resources' not in p.parts}
for path, page in pages.items():
    text = path.read_text()
    if 'site-header' in text:
        assert len(page.main) == 1 and page.main[0].get('tabindex') == '-1', path
        assert page.skip == ['#' + page.main[0]['id']], path
    for href in page.links:
        u = urlsplit(href)
        if u.scheme or u.netloc:
            continue
        target = (path.parent / unquote(u.path)).resolve() if u.path else path
        assert target.name not in RETIRED, (path, href)
        assert target.exists(), (path, href)
        if u.fragment and not u.query and target in pages:
            assert unquote(u.fragment) in pages[target].ids, (path, href)
for name in ['area-article.js', 'areas.js', 'programs.js', 'program-article.js', 'navigation.js']:
    text = (SITE / name).read_text()
    assert not re.search(r'(?:jobs?|legacy|discover)\.html', text), name
comparison = pages[SITE / 'compare.html']
library = json.loads((SITE / 'content/programs/school-library.json').read_text())
assert sorted(comparison.rows) == sorted(item['code'] for item in library['programs'])
assert len(comparison.rows) == len(set(comparison.rows))
for field in {field for p in library['programs'] for field in p['primaryFields']}:
    assert (SITE / 'areas' / (field + '.html')).exists(), field
schools = json.loads((SITE / 'content/programs/schools.json').read_text())
assert set(schools['programSchools']) == {p['code'] for p in library['programs']}
topics = {'type', 'size', 'campus', 'housing', 'studentLife', 'recreation'}
for code, school_id in schools['programSchools'].items():
    school = schools['schools'][school_id]
    assert set(school['facts']) == topics, school_id
    # Retain the single-photo field for browsers with the previous script cached.
    assert school['photo'] == school['photos'][0], school_id
    facts = {**school['facts'], **schools['programOverrides'].get(code, {}).get('facts', {})}
    for topic, fact in facts.items():
        assert fact['text'] and fact['sources'], (code, topic)
        for key in fact['sources']:
            source = school['sources'][key]
            assert source['url'].startswith('https://') and source['retrievedOn'], (code, key)
    override = schools['programOverrides'].get(code, {})
    campuses = override.get('campuses', school['campuses'])
    photos = override.get('photos', school['photos'])
    assert campuses and len(photos) == len(campuses), code
    for photo in photos:
        for key in ['url', 'alt', 'caption', 'credit', 'source', 'retrievedOn']:
            assert photo.get(key), (code, key)
        assert photo['source'].startswith('https://'), code
        photo_url = photo['url']
        if not photo_url.startswith('https://'):
            assert photo_url.startswith('images/schools/') and (SITE / photo_url).is_file(), code
            assert photo['originalUrl'].startswith('https://'), code

print(f'Public navigation and landmarks pass; comparison covers {len(comparison.rows)} programs.')

# A changed program renderer must have a new browser-cache identity.
import hashlib
version = hashlib.sha256((SITE / "program-article.js").read_bytes()).hexdigest()[:12]
assert f'src="program-article.js?v={version}"' in (SITE / "program.html").read_text()
