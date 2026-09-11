# Area-based explorer

`site/areas.html` is an additive, content-first route for students who are still learning what animal-related fields and kinds of work exist.

## Experience

1. Browse 15 overlapping fields and work areas in a searchable selection workspace.
2. Choose the field and current section from persistent menus designed for a mobile screen.
3. Move through short, distinct sections for focus, variation, questions, responsibilities, knowledge, settings, realities, careers, college study, glossary terms, and sources.
4. Choose one item at a time from a menu to read its full explanation, examples, connections, and related source without expanding the page or triggering automatic scrolling.
5. View Careers and College Study separately, while retaining links to the complete research tools.
6. Optionally save areas or use compact thumbs-up and thumbs-down controls when something stands out.

The Overview uses grouped menus and a contextual photograph to orient the reader before the detailed sections. Each subsequent screen has its own label, color, and symbol. Quick marks remain optional reminders rather than a scoring system.

## Sources and data

- Area content is loaded at runtime from the editable JSON files in `site/content/areas/`.
- Area definitions and distinctions draw from the project's *Core Animal-Related Fields* source.
- Career examples and college-path information use `site/data.js`.
- External links come primarily from the source notes in *Animal Behavior, Wildlife, Animal Care & Conservation — Undergraduate Pathways and Career Exploration Guide*.
- The linked sources include professional organizations, O*NET/BLS occupation pages, qualification and permit guidance, field job boards, and official university programs.
- Contextual photographs are credited and linked to the U.S. Fish & Wildlife Service or NOAA Fisheries source page.

## Files and isolation

- `site/areas.html`
- `site/areas.css`
- `site/areas.js`
- `site/content/areas/index.json`
- `site/content/areas/<area-id>.json`
- `site/content/areas/README.md`

The route stores reactions under `animalExplorerAreasV1`. It does not alter the saved state or files used by `site/index.html` or `site/discover.html`.

To remove the area-based experiment, delete these three `site/areas.*` files. The original and preference-based explorers require no restoration.
