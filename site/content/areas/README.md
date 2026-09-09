# Editing the Area Explorer

The Area Explorer loads its content directly from the JSON files in this folder. A change committed to one of these files will appear on the site after the GitHub Pages workflow finishes.

## Most common edit

1. Open the file named for the area, such as `wildlife-rehabilitation.json`.
2. Click the pencil icon in GitHub.
3. Edit the wording inside the quotation marks.
4. Select **Commit changes**.
5. Wait for the Pages workflow to finish, then reload `areas.html`.

Each area file controls its overview, focus topics, questions, responsibilities, knowledge and skills, variations, settings, realities, related careers, college-program connections, adjacent areas, and references.

## Focus topics

Focus topics have a title and the description shown when the topic is expanded:

```json
{
  "title": "Emergency stabilization and supportive care",
  "description": "The first priority is to identify immediate threats to life..."
}
```

To provide hand-written examples instead of the automatically connected question, responsibility, and skill, add an `examples` list:

```json
{
  "title": "Emergency stabilization and supportive care",
  "description": "The first priority is to identify immediate threats to life...",
  "examples": [
    {
      "label": "Intake example",
      "text": "A window-strike bird may need a quiet, dark holding space..."
    }
  ],
  "source": "National Wildlife Rehabilitators Association"
}
```

`source` can be the exact title or URL of any item in that area's `references` list. If it is omitted, the site selects a related reference from the list.

## Adding custom detail elsewhere

Questions, responsibilities, knowledge and skills, settings, and practical realities are normally simple strings. The site creates their expanded connections from the other content in the area. A string can be replaced with an object whenever a custom explanation or examples are preferable:

```json
{
  "title": "Safe handling, restraint, and enclosure management",
  "description": "Handling methods are selected for the species, condition, and procedure...",
  "examples": [
    {
      "label": "Equipment example",
      "text": "Transport carriers, towels, nets, gloves, and barriers serve different purposes."
    }
  ]
}
```

## Other files

- `groups.json` controls the five broad group headings, descriptions, and colors.
- `index.json` controls which area files are loaded and their order.
- To add an area, create its JSON file and add the filename to the `areas` list in `index.json`.

## JSON rules

- Use double quotation marks around text and field names.
- Keep a comma between list items and fields, but not after the final item.
- Use `\"` when quotation marks need to appear inside text.
- Leave identifiers such as `id`, `group`, `programCodes`, and `related` unchanged unless their connections are also being updated.

If a file has invalid JSON or omits a required field, the Area Explorer displays a content-loading message with the file or field that needs attention rather than showing a partially broken page.
