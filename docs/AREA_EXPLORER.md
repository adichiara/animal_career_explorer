# Article-based reference site

The public site is a content-first reference for students who are still learning what animal-related fields, undergraduate programs, and kinds of work exist.

## Experience

1. Choose **Field Guides**, **College Programs**, or **Job Examples** from the homepage.
2. Browse a searchable index within that section.
3. Open one continuous, article-style guide with clearly differentiated sections and source links.
4. Move among articles with simple previous, index, and next links.

The article pages contain no saved-state controls, reaction interface, or automatic scrolling. A short table of contents provides optional jump links without hiding any content. Each field guide has one distinct photograph selected to show a characteristic kind of work or method without defining the entire field by a single species or location. On portrait screens, the photograph is height-constrained as well as width-responsive so it cannot occupy most of the viewport. The locally stored, optimized image links to its credited source page.

The homepage and primary navigation expose only the three reference sections. The previous complete research interface is preserved at `site/legacy.html`, and the preference-based explorer is preserved at `site/discover.html`; neither is linked from the new site.

## Sources and data

- Area content is loaded at runtime from the editable JSON files in `site/content/areas/`.
- Area definitions and distinctions draw from the project's *Core Animal-Related Fields* source.
- College Program guides merge the 10 focused records in `site/data.js` with the 7 hand-editable broader options in `site/content/programs/additional-programs.json`.
- Job Example guides use `site/data.js`.
- Job examples are dated observations, not current vacancy claims or a measure of the whole labor market.
- External links come primarily from the source notes in *Animal Behavior, Wildlife, Animal Care & Conservation — Undergraduate Pathways and Career Exploration Guide*.
- The linked sources include professional organizations, O*NET/BLS occupation pages, qualification and permit guidance, field job boards, and official university programs.
- Photo assignments, accessible descriptions, credits, source links, and license labels are stored in `site/content/areas/photos.json`.
- The 15 photographs are stored locally as cropped 1200 × 675 WebP files in `site/images/areas/`. Full credits are recorded in `site/images/areas/CREDITS.md`.

## Current interface files

- `site/index.html`
- `site/areas.html`
- `site/areas.css`
- `site/areas.js`
- `site/area-article.js`
- `site/areas/<area-id>.html`
- `site/programs.html`
- `site/programs.js`
- `site/program.html`
- `site/program-article.js`
- `site/jobs.html`
- `site/jobs.js`
- `site/job.html`
- `site/job-article.js`
- `site/navigation.js`
- `site/content/areas/index.json`
- `site/content/areas/<area-id>.json`
- `site/content/areas/README.md`
- `site/content/areas/photos.json`
- `site/images/areas/`

The new reference pages do not store user state. The retained `legacy.html` and `discover.html` files keep their original code and browser-storage behavior for backward reference.
