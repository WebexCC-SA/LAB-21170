# Lab Guide for WebexOne Lab LAB-21170

Web guide link: https://webexcc-sa.github.io/LAB-21170/

## ServiceDesk starter flow

The attendee download is [`docs/assets/lab-guide/ServiceDesk-starter.json`](docs/assets/lab-guide/ServiceDesk-starter.json). It includes the IVR, direct Order Desk HTTP lookup, response mapping, and queue treatment, but no working bearer token. Flow Designer binds `Queue-1` by name on import; attendees confirm that binding before publishing.

To regenerate the download from the sanitized source export:

```bash
.venv/bin/python scripts/build_starter_flow.py scripts/starter_flow_source.json docs/assets/lab-guide/ServiceDesk-starter.json
```

The builder generates new activity and link IDs. After regeneration, import the new JSON into a sandbox and recheck Flow Designer validation before distributing it. Do not add live credentials to either JSON file.


## DOCX to Markdown script

Use `scripts/docx_to_markdown.py` to convert a DOCX lab guide into markdown files.

### What it does

- Reads one `.docx` input file
- Extracts all embedded images into `docs/assets/` (or a custom assets directory)
- Splits each Heading 1/Heading 2 that starts with `Lab` into its own markdown file in `docs/`
- Writes all non-lab content to `docs/non-lab.md`

### Usage

```bash
python scripts/docx_to_markdown.py path/to/guide.docx
```

Optional arguments:

- `--docs-dir` (default: `docs`)
- `--assets-dir` (default: `<docs-dir>/assets`)
