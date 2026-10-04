# Lab Guide for WebexOne Lab LAB-21170

Web guide link: https://webexcc-sa.github.io/LAB-21170/

## ServiceDesk starter flow

The attendee download is [`docs/assets/lab-guide/ServiceDesk-starter.json`](docs/assets/lab-guide/ServiceDesk-starter.json). It includes the IVR, direct Order Desk HTTP lookup, response mapping, and queue treatment, but no working bearer token. Flow Designer binds `Queue-1` by name on import; attendees confirm that binding before publishing.

To regenerate the download from the sanitized source export:

```bash
.venv/bin/python scripts/build_starter_flow.py scripts/starter_flow_source.json docs/assets/lab-guide/ServiceDesk-starter.json
```

The builder generates new activity and link IDs. After regeneration, import the new JSON into a sandbox and recheck Flow Designer validation before distributing it. Do not add live credentials to either JSON file.


## Standalone Contact Center MCP bonus starter

All bonus attendees import [`ServiceDeskMCPBonus-starter.json`](docs/assets/lab-guide/ServiceDeskMCPBonus-starter.json): `NewPhoneContact` (Start Flow) → `EscalationMessage` (Play Message) → `EndFlow` (End Flow), with both normal and error message outputs connected to the end. It uses Cisco Cloud Text-to-Speech and default event entry nodes, without custom event paths. There are no credentials, queue bindings, AI agents, HTTP requests, or entry-point assignments. Keep it unpublished. The tested MCP patch changes the spoken message, supplies serialization-safe defaults, and preserves the main End Flow type; it does not change connections.

Regenerate it from the same sanitized export:

```bash
.venv/bin/python scripts/build_bonus_starter.py scripts/starter_flow_source.json docs/assets/lab-guide/ServiceDeskMCPBonus-starter.json
.venv/bin/python -m unittest discover -s tests -v
```

Recheck the exact download's import, approved MCP patch, saved message and native Flow Designer validation in an assigned sandbox after regeneration. MCP validation alone is not sufficient. The bonus guide uses this small practice draft even for attendees who completed the main lab; do not patch copies of their completed flows with this workaround.

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
