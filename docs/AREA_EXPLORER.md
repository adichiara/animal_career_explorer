# Area-based explorer

`site/areas.html` is an additive, content-first route for students who are still learning what animal-related fields and kinds of work exist.

## Experience

1. Browse 15 overlapping fields and work areas in a searchable index.
2. Open one dedicated page for a field.
3. Read a continuous, article-style guide with clearly differentiated sections for scope, variation, questions, responsibilities, preparation, working conditions, careers, college study, terminology, and sources.
4. Follow simple links to related field guides or the complete career and college research tools when useful.

The article pages contain no nested card navigation, saved-state controls, reaction interface, or automatic scrolling. A short table of contents provides optional jump links without hiding any content. Contextual photographs introduce the guides and link to their credited government source pages.

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
- `site/area-article.js`
- `site/areas/<area-id>.html`
- `site/content/areas/index.json`
- `site/content/areas/<area-id>.json`
- `site/content/areas/README.md`

The route does not store user state and does not alter the files or saved state used by `site/index.html` or `site/discover.html`.

To remove the area-based experiment, delete the field-guide files listed above. The original and preference-based explorers require no restoration.
