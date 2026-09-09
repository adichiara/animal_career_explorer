# Progressive career explorer

## Purpose

`site/discover.html` is an additive, lower-pressure entry point for students who are early in career exploration. It reduces the number of decisions shown at once while preserving access to the full research in the original explorer.

The existing `site/index.html`, `site/app.js`, and `site/styles.css` are unchanged.

## Experience sequence

1. Choose a comfortable starting point.
2. Explore broad kinds of work rather than unfamiliar job titles.
3. React to a small sample of real careers.
4. Look for patterns across a shortlist before considering college programs.

Detailed evidence, observed titles, pay, qualifications, and progression remain available in expandable sections and through the original full explorer.

## Files

- `site/discover.html` — separate entry point
- `site/discover.css` — isolated presentation styles
- `site/discover.js` — career-world mapping, reactions, shortlist, and program connections
- `site/data.js` — shared source data; not duplicated or modified

## State and rollback

The new experience stores choices under the separate browser key `animalExplorerDiscoveryV1`. It does not overwrite the original explorer's saved state.

To remove the experimental experience, delete the three `site/discover.*` files. The original explorer requires no restoration.
