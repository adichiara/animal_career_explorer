# Animal Pathways — content update

Generated 2026-09-15. The prose rewrite, the disambiguation work, and the
code-reference sweep, consolidated.

## What to install

```
content/areas/     15 field guides + index.json   -> site/content/areas/
areas_build.py     the generator                  -> scripts/ (or repo root)
patches/           two diffs                      -> apply with git apply
```

`content/areas/` is the deliverable. Copy it over `site/content/areas/`.

## What changed in the guides

**Openings rewritten (13 of 15).** Institutional history — founding dates, journal
launch years, society names — is out of every `bigPicture`. Eleven of fifteen used to
spend their second or third sentence on it. Every displaced fact still lives in
`variations` or `references`; nothing verified was lost. Ecology and Wildlife Ecology
& Management were already in this voice and are untouched.

**"Rather than" went from 49 uses to 2.** It had become a verbal tic that made every
guide sound like the same narrator. The two survivors are deliberate: in Zoo &
Aquarium Science ("animals in human care rather than captive animals") and Wildlife
Health ("a source of human infection rather than on wildlife health as an end in
itself"), the contrast is the content.

**`realities` reshaped in all 15.** Warnings intact — none softened, none removed.
What changed is sentence shape, and that sourced encouraging facts now get a visible
slot instead of sitting buried in `variations`: NAI certification reachable before
graduation, wildlife rehabilitation credentials not requiring a degree, applied
behavior having no single required major, welfare coordinator roles not requiring a
doctorate.

**New: `senses` block on Animal Science.** Three different things go by that name —
the occupation (about 3,100 people nationally, median near $68,930, mostly
graduate-level livestock research), the degree (contents set by the concentration),
and the everyday phrase (science about animals generally). The third says plainly
that if that is the sense the reader means, this guide is one option among many
rather than the place to start.

**New: Animal Science <-> Animal Behavior `distinction`**, mirrored onto both guides
in the pattern already used for Ecology and Wildlife. It cites the University of New
England's own program page, which answers the question directly: animal science and
animal behavior are not the same.

## areas_build.py

Single source of truth. Edit the `area()` calls, then:

    python3 areas_build.py site/content/areas

Exits non-zero if anything fails validation, so it can be wired into a commit hook.

**The build assembles content. It does not rewrite prose.** That is a deliberate
change from the earlier version, which expanded acronyms by string substitution and
then carried a `CLEANUP` list to repair the damage it had caused. Two bugs came out
of that stage — an expansion carrying a leading "the" produced "The the National
Association for Interpretation (NAI)", and a blanket repair rule for `"a the "`
matched inside `"idea the audience"` and deleted a real word. Both produced valid
JSON with resolving pointers, so validation reported nothing. Only diffing the
output against the previous build surfaced them.

Both stages are gone. What replaced them is a check:

```python
for acr, full in ACRONYMS.items():
    if re.search(rf"\b{acr}\b", prose) and full not in prose:
        problems.append(f"{a['id']}: '{acr}' used but '{full}' never appears")
```

Same guarantee — every acronym is spelled out once per guide — but the build names
the guide and stops, and you fix the sentence in the source, where a human controls
the articles and the capitalisation. Nothing can be silently mangled in a file you
were not editing, because nothing is edited.

The build also fails if a program code appears in prose. Codes are back-end
identifiers only.

Both checks are verified to fire: injecting a bare `AVMA` into the Zoology guide, or
`UMA-AS` into Animal Science, fails the build with a message naming the guide.

Two steps still run after assembly, and both only add structure, never alter text:
reference keys expand into full reference objects, and `programCodes` expand into a
`programs[]` array carrying school and full program title.

## patches/

**`export_site_data.patch`** — removes program codes from career prose at the
pipeline, so the fix survives a rebuild. Drops five `details` keys (269 instances)
that restated `careers[].support` as bare code lists, plus the career-level `notes`
field (73 instances) holding unsourced school-coupled asides such as "Particularly
natural at UNE/UMass Biology". `support` is the source of truth and `job-article.js`
already renders it with full program titles and school names. Eleven genuine
`details` keys are retained and contain no school or code references.

Note the scope: `notes` is dropped entirely, not only where it names a school.

**`area-article.patch`** — one line. The program heading fell back to the code when a
title was missing; it now falls back to the school name.

## Known open items

- **"Actually" (22 uses) and "the field" (19).** Lower-grade than the tic just
  cleared, and often doing real work. Each wants reading in context, not a sweep.
- **`short` lines** still mix three grammatical shapes across 14 to 24 words. They
  render together on the index page, where the inconsistency shows.
- **`legacy.html` and `discover.html`** are live, crawlable, and unlinked. They carry
  old branding, render program codes prominently, and hardcode "the ten college
  paths" when there are now seventeen. After the export patch, the code lists they
  render will be empty. Worth retiring.
- **Salary data.** The largest outstanding item: 93 roles carrying about 13 recycled
  SOC wage bands, several mapped to occupations that do not describe them. The BLS
  research is done; the rebuild is not.
