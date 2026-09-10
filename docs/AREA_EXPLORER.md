# Area-based explorer

`site/areas.html` is an additive, content-first route for students who are still learning what animal-related fields and kinds of work exist.

## Experience

1. Browse 15 overlapping fields and work areas in a searchable selection workspace.
2. Open one area at a time and move among five focused views: Overview, Questions & Work, Knowledge, Careers & Study, and Sources.
3. Select any entry to update an adjacent detail panel with its explanation, examples, connections, and related source without expanding the page.
4. Optionally use compact thumbs-up or thumbs-down controls inside the detail panel when something stands out.
5. Review related careers, undergraduate paths, adjacent areas, and the full source collection.
6. Return to saved areas and quick marks. The experience does not calculate a fit score, rank careers, or eliminate an area.

The **How the work varies** choices in the Overview carry the main explanation of role and setting differences. Other views prioritize substantive field information instead of repeating qualifications on every item. Quick marks remain optional reminders rather than a scoring system.

## Sources and data

- Area content is loaded at runtime from the editable JSON files in `site/content/areas/`.
- Area definitions and distinctions draw from the project's *Core Animal-Related Fields* source.
- Career examples and college-path information use `site/data.js`.
- External links come primarily from the source notes in *Animal Behavior, Wildlife, Animal Care & Conservation — Undergraduate Pathways and Career Exploration Guide*.
- The linked sources include professional organizations, O*NET/BLS occupation pages, qualification and permit guidance, field job boards, and official university programs.

## Files and isolation

- `site/areas.html`
- `site/areas.css`
- `site/areas.js`
- `site/content/areas/index.json`
- `site/content/areas/<area-id>.json`
- `site/content/areas/README.md`

The route stores reactions under `animalExplorerAreasV1`. It does not alter the saved state or files used by `site/index.html` or `site/discover.html`.

To remove the area-based experiment, delete these three `site/areas.*` files. The original and preference-based explorers require no restoration.
