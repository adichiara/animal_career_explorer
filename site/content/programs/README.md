# Additional college programs

`additional-programs.json` contains researched college options that were worth
preserving but were not part of the original focused comparison.

The College Programs index loads this file after the 10 database-generated
program records in `site/data.js`. Each object must have a unique internal
`code`, but the code is used only in page URLs and is not shown as page content.

To edit an additional program:

1. Change its text in `additional-programs.json`.
2. Keep the JSON valid: double quotes, commas between items, and no comments.
3. Keep `collection` set to `additional` so it appears in the broader-options
   section rather than the focused shortlist.
4. Update `lastVerified` after checking the linked official sources.
5. Preview through a local web server; browser security prevents `fetch()` from
   loading JSON when an HTML file is opened directly from disk.

Preparation strengths use the same internal 0–3 scale as the generated data.
The site converts them to whole-number 0–10 scores for display.

These records are intentionally separate from the generated database export so
normal database rebuilds do not overwrite hand-edited summaries.
