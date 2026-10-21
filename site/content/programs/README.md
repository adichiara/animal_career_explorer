# School and program library

The public **School & Program Library** combines two kinds of detailed program
records:

- the 10 database-generated program records in `site/data.js`
- hand-researched records in `additional-programs.json`

The file `school-library.json` is the presentation and recommendation layer. It
selects which program codes appear in the current browseable library and stores
the interest tags, school-fit fields, a short **why explore** note, and **look
first** guidance for each one.

## Current school-fit rule

A program belongs in the current library only when there is evidence for at
least one of these eight fields:

1. Animal Biology
2. Zoology
3. Wildlife Biology
4. Animal Behavior
5. Animal Welfare Science
6. Animal Science with a non-agricultural companion/managed-animal emphasis
7. Zoo & Aquarium Science / Managed Animal Care
8. Veterinary Technology

Other field guides remain useful context. Marine Biology, Ecology, Conservation
Biology, Animal Cognition, Wildlife Health, Wildlife Rehabilitation, and
Anthrozoology do **not** independently qualify a school for the current library.

The library is a browseable research set, not a ranking.

## Editing a hand-researched program

1. Edit the program object in `additional-programs.json`.
2. Use only facts supported by the program's linked official sources.
3. Update `lastVerified` after checking those sources.
4. Keep the internal `code` stable once it is referenced elsewhere.
5. If the program should appear in the current library, add or update its entry
   in `school-library.json`.

Preparation strengths retain the existing internal 0–3 scale. Program pages
convert them to whole-number 0–10 preparation indicators; these describe areas
within one program and are not school rankings.

## Editing the current library

Each `school-library.json` entry must reference a code that exists either in
`site/data.js` or `additional-programs.json`. Its `primaryFields` values
must come from the eight current school-fit fields. Tags are for browsing and
should describe documented program features rather than inferred interests.

Run the content-validation workflow, or its equivalent local checks, after
changes.
