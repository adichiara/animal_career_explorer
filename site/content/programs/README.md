# School and program library

The public **School & Program Library** combines two kinds of detailed program
records:

- the 10 database-generated program records in `site/data.js`
- hand-researched records in `additional-programs.json`

The file `school-library.json` selects which program codes appear in the public library and stores browsing tags and field mappings. Additional research notes may remain in the data file without being rendered.

## Field mappings

Program records can be mapped to these eight animal-related fields:

1. Animal Biology
2. Zoology
3. Wildlife Biology
4. Animal Behavior
5. Animal Welfare Science
6. Animal Science with a non-agricultural companion/managed-animal emphasis
7. Zoo & Aquarium Science / Managed Animal Care
8. Veterinary Technology

Other field guides provide additional context and can still appear within program descriptions.

## Editing a hand-researched program

1. Edit the program object in `additional-programs.json`.
2. Use only facts supported by the program's linked official sources.
3. Update `lastVerified` after checking those sources.
4. Keep the internal `code` stable once it is referenced elsewhere.
5. If the program should appear in the public library, add or update its entry
   in `school-library.json`.

Preparation strengths retain the existing internal 0–3 scale for backend analysis. Public program pages use that evidence only to summarize skills the undergraduate curriculum should build strongly; they do not display a score or infer missing skills.

## Editing the public library

Each `school-library.json` entry must reference a code that exists either in
`site/data.js` or `additional-programs.json`. Its `primaryFields` values
must come from the eight field identifiers listed above. Tags are for browsing and
should describe documented program features rather than inferred interests.

Run the content-validation workflow, or its equivalent local checks, after
changes.
