# LAB-21170 Lab Guide Specification

## Purpose and editorial boundary

This specification maps the source **Webex One - Flow Designer Lab.docx** and the requested additions onto the existing LAB-21170 attendee guide. The published guide remains a progressive Webex Contact Center Flow Designer and Webex AI Agent lab using the synthetic Order Desk service. Preserve the existing learning steps, the checkpoint numbering, the Order Desk scenario, and the current visual language. Extend the Flow Designer section with template, queue treatment, debugging, analytics, subflow, and Function exercises. Record only live-verified tenant behavior as runnable steps.

The Word source is a broader seven-mission, four-hour delivery map. Its reusable contracts are the one-flow progression, known-good checkpoints, explicit success/error/escalation paths, data-driven HTTP work, Python Function, AI Agent, and gated Flow API/MCP finale. The current site has nine checkpoints and a concrete Order Desk sandbox. Treat this revision as an expansion of that site, not a replacement with the source's generic customer-context scenario. The source cover also says 90 minutes while its timing table assumes four hours; confirm session timing before adding any attendee time estimate.

## Scope and source mapping

| Source or request | Attendee-guide placement | Required outcome |
| --- | --- | --- |
| Existing overview and scenario | `docs/overview.md` | Keep the Order Desk story. Show the complete practice route through the human queue and queue treatment, and the final AI-agent route with handled and escalated outcomes. |
| Product journey and bookmarks | Overview and `docs/lab1_getting_started.md` | Give working, labeled links for Control Hub, Flow Designer, Developer Portal, AI Agent Studio, and MCP Lab. Repeat the two requested quick links in Checkpoint 1. Verify the tenant's actual AI Agent Studio destination before hard-coding a deep link. |
| Word source Mission 1; requested template warm-up | Checkpoint 2, Part A | Start from **Simple Flow to Queue**, inspect the canvas, map its Queue Contact activity to the assigned queue, validate, publish, route the assigned inbound number, call, then inspect debugging and aggregate analytics. |
| Existing scratch-built `ServiceDesk` tutorial | Checkpoint 2, Part B | Retain the existing welcome/menu build and channel/call test. Make its relationship to the template warm-up explicit so the attendee does not accidentally overwrite the working template flow or route the wrong version. |
| Requested comprehensive wait treatment | Checkpoint 2, continuation of Part B | Inspect **Comprehensive Call Flow**, reproduce the appropriate post-queue wait/callback pattern in a subflow, connect and loop it with valid queue semantics, publish, call-test, inspect debug and analytics. Confirm the actual cross-flow copy/paste and subflow behavior in the tenant before writing exact click steps. |
| Word source Missions 2–4; existing REST test | Checkpoint 3 | Keep the current `ORD-10482` HTTP comparison branch. Add debug/analytics, refactor the HTTP lookup into a subflow, use a tested Function to parse/normalize the response, then validate both success and failure paths by live calls. |
| Word source Missions 5–6; existing AI Agent/MCP checkpoints | Checkpoints 4–9 | Preserve the existing Order Desk inspection, registration, agent creation, preview, and final call sequence. Update references and final queue handoff so earlier additions lead to the same completed journey. |
| Word source Mission 7; requested MCP bonus | A clearly labeled bonus after the required call path | Explore the Webex Contact Center MCP flow tools and the separate Operations MCP service only when endpoint, entitlement, auth, tool catalog, and permitted actions are verified in the lab tenant. Read/search before any bounded change; inspect diff and validation; publish through a human checkpoint. Do not describe the unreleased visual-canvas MCP Client activity as available. |

## Learner journey and target topology

The guide should distinguish two practice assets if the template warm-up and scratch-built `ServiceDesk` cannot safely share one flow. Name them clearly and state which flow the inbound channel points to at each test. Preserve every existing exercise, then place the new steps where the learner has the prerequisites to complete them.

```text
Practice: caller → welcome message → menu → Order Desk REST test
                                             → human agent queue → queue treatment

Final:    caller → Webex AI Agent → external Order Desk system → response
                                     ├─ Handled → end
                                     ├─ Escalated → human agent queue → queue treatment
                                     └─ Errored → honest fallback → human agent queue or safe exit
```

Use the same node names and edge labels in prose, diagrams, screenshots, and tested flow versions. A dotted edge in the overview diagram can denote the optional or later-added queue/treatment route, but the caption must say exactly what the dotted edge means. The final diagram should show the actual connected final flow, including **Handled**, **Escalated**, and **Errored**. The existing guide currently ends escalation after a message. Replace that behavior only after the assigned queue, agent availability, and live handoff are proven.

## Checkpoint 1 and overview edits

1. Extend **What you will build** and the solution-evolution diagram with the queue and queue-treatment path above. Keep the distinction between temporary REST comparison and final agent-led lookup.
2. Add a URL column to the product journey table. Use `https://admin.webex.com/` for Control Hub and `https://developer.webex.com/` for Developer Portal. For Flow Designer, distinguish the public developer entry from the lab's direct `https://flow-control.produs1.ciscoccservice.com/` route. Link AI Agent Studio to a verified stable entry or instruct users to open it from Control Hub if the URL depends on tenant or session.
3. Update the sequence after the REST response: inspect Flow Debugging; inspect Flow Analytics; refactor HTTP into a subflow; parse/normalize its response in a Function; then continue with MCP and agent setup. Add the requested two MCP services as a bonus after the required journey.
4. In Checkpoint 1, repeat a compact **Useful links and bookmarks** table including `https://admin.webex.com/` and `https://flow-control.produs1.ciscoccservice.com/`. Keep the MCP Lab link and explain that the assigned tenant details are authoritative for lab-specific values.

## Checkpoint 2: Flow Designer foundations

### Part A — template flow, live call, debug, analytics

**Objective:** publish a working first call from the **Simple Flow to Queue** template and learn where Flow Designer shows a single call's execution versus aggregate call behavior.

1. Open the assigned sandbox in Control Hub, then Flow Designer. Record the assigned entry point, number, queue, and an available test agent. Show the navigation to templates and the **Simple Flow to Queue** choice.
2. Create an attendee-unique flow from the template. Orient the learner to the canvas, activity panel, activity settings, Global Flow Properties, validation, publish/version controls, and debug/analytics entry points. Identify the template's start event, prompt, **Queue Contact**, treatment, success path, and error links from the actual tenant UI.
3. Point **Queue Contact** at the assigned queue. Configure or retain safe wait treatment and connect all required activity outcomes. Validate until no blocking errors remain. Publish a labeled version.
4. Associate the flow with the sandbox's existing entry point/channel and assigned phone number. State the exact object seen in the tenant; do not assume every pod needs a newly created channel. Confirm the routed version.
5. Call the number. Verify the message and queue experience and, when the test agent is available, answer the call. Capture the published canvas and a credential-free call outcome.
6. Open **Flow Debugging** for that call and point out the interaction identifier, ordered activity path, branch/outcome, and any errors without showing personal or secret values.
7. Make two or three more calls with distinct observable outcomes when feasible. Open **Flow Analytics**, identify its time filter and aggregation, and explain expected ingestion delay rather than treating a missing immediate aggregate as a flow failure.

**Pass:** a published template-based flow receives a call, reaches the assigned queue or validated treatment, its individual interaction is visible in Debugging, and the repeated calls appear in Analytics after the tenant's observed delay. Save a known-good checkpoint before continuing.

### Part B — retain the existing starter IVR, then extend queue treatment

Retain the current blank-canvas `ServiceDesk` instructions: `NewContact`, `WelcomeMessage`, `SupportMenu`, digit `2` to `GeneralSupportMessage`, digit `1` to the Checkpoint 3 HTTP branch, publication, routing, and live tests. Introduce this as a second learning pass after the template call and state explicitly when the inbound number is switched to `ServiceDesk`. Reuse the existing channel only where the tenant supports that update; otherwise use the verified channel/entry-point method.

Then open the **Comprehensive Call Flow** template as a reference. Identify the actual post-queue wait treatment, callback offer, loop condition, exit, and failure edges. Copy the supported activities into a subflow if the tenant permits cross-flow copy/paste; otherwise recreate the same verified pattern in the subflow. Wire the subflow into the practice flow at the correct queue treatment point. Verify that looping continues only while the contact is queued and cannot create an infinite caller journey after an agent answers or the call ends. Validate and publish a new version, call again, inspect its executed path in Debugging, and confirm repeated calls in Analytics. Capture the actual topology, subflow inputs/outputs, loop edge, callback choice, and call result.

**Pass:** the original IVR remains understandable and callable, queue treatment and callback behavior follow the tenant-supported template pattern, all exits and errors are connected, and live calls prove the path. Keep the previous published version as recovery.

## Checkpoint 3: HTTP, subflow, Function, and evidence

Preserve the existing Order Desk REST test: `SupportMenu` digit `1` reaches `GetOrder`, the HTTP response is used in `OrderStatusMessage`, and digit `2` still works. Keep the synthetic order number and tenant-supplied endpoint values. Add a queue route after the REST result only if it is part of the tested practice path; show its optionality and exit behavior explicitly.

1. Build and publish the initial HTTP branch. Test success by phone and inspect **HTTP Request** configuration, redacted request headers, status code, body shape, parsed variable, and output path in **Flow Debugging**. Make repeat calls and inspect **Flow Analytics**.
2. Refactor the HTTP lookup into a named subflow with explicit inputs and outputs. The parent flow should pass an order number and receive a stable result contract. Preserve timeout, non-2xx, missing-order, malformed-JSON, and other error paths where test fixtures exist. Do not show a raw response body or token in public media when it contains sensitive values.
3. Create a Function using the runtime verified in the tenant. Its job in this lab is to parse/normalize the HTTP response into a small, typed contract such as status, delivery summary, success flag, and safe fallback message. Test the exact code with valid, empty/missing-field, malformed, and error inputs; publish a version; invoke it from the subflow; map outputs explicitly to the parent. The Word source suggests Python 3.13, but confirm the actual runtime and Function activity UI before specifying click labels or code.
4. Validate and publish each meaningful checkpoint. Test the refactored happy path and at least one error/fallback call; inspect Debugging to prove the parent → subflow → Function → parent sequence and inspect Analytics after repeated calls. Confirm the spoken response uses parsed values and does not invent an order state.

**Pass:** the same phone number reaches a published flow; the Order Desk response travels through HTTP, subflow, and Function; success and failure paths are visible and safe; Debugging and Analytics evidence matches the calls; prior menu behavior still works.

## Later checkpoints and final call

Keep the current MCP Lab tool inspection, approval-gated write demonstration, Developer Portal Agentic App registration, Control Hub tool enablement, Track Package agent customization, `lookup_order` action, preview, and publish steps. The voice agent should retain read-only access for the final call; the approval-gated write remains a separate MCP Lab exercise. The final Flow Designer caller path should go straight to **Virtual Agent V2**. **Handled** ends cleanly, **Escalated** reaches the verified human queue and treatment, and **Errored** reaches a clear fallback with a safe queue or exit path. Test at least one handled call, one explicit human request, and one controlled error or documented fixture. Answer an escalated call in Agent Desktop when enabled, and verify only intended context is shared.

## Bonus: Webex Contact Center MCP services

Separate the Webex Contact Center Flow MCP service from the Operations MCP service. Before authoring runnable bonus steps, verify each service's current endpoint, access method, entitlement/region, live tool manifest, read/write policy, and whether the attendee identity can use it. Start with bounded discovery, search, and read examples against the assigned lab flow and operational objects. If a change is allowed, require a small draft proposal, exact diff, validation, and a separate human publish action. Label Early Access accurately. A service unavailable in the event tenant may be shown only as an instructor demonstration or clearly marked reference, never as a completed attendee exercise.

## Evidence and media contract

| Step class | Evidence to capture | Format and quality gate |
| --- | --- | --- |
| Static location or expected state | Template picker, queue setting, saved canvas, version, channel route, debug result, analytics view, Function tests, final topology | Full-resolution screenshot with clear focus, useful crop, readable labels, descriptive alt text, and a caption tied to the step. |
| “Show me how” interaction | Template creation, routing, queue/subflow wiring, callback loop, HTTP setup, Function attachment, Debugging and Analytics navigation, final agent wiring | Short GIF showing a complete action sequence and resulting state. Keep cursor pacing readable and avoid flashing or excessive repetition. Use a static fallback frame where motion cannot convey the information. |
| Live outcome | Test calls, debug trace, analytics after repeated calls, Function test outputs, agent preview, handoff | Screenshot or GIF captured from the real sandbox, with the precise version and expected outcome in the caption. |

Capture media as each live step is completed, then compare every image against the written instruction. Never use a mockup or borrowed screenshot as proof of a live tenant result. Crop or redact phone numbers, attendee identity, tokens, passwords, authorization headers, and customer fields when they are not required for the learner's decision. The public guide, Git history, generated site, downloadable walkthrough, screenshots, GIF frames, and alt text must be free of reusable secrets. Existing assets can remain when accurate; replace stale assets and broken placeholders, including empty `gif-capture` markers, with verified media.

## Design and implementation constraints

- Preserve MkDocs Material, existing navigation patterns, figure/caption style, admonitions, and the established colors in `docs/stylesheets/extra.css`: dark navy `#051C2C`, cyan `#00bdeb`, and link blue `#3a7fff`. New diagrams should use this palette and remain legible in both light and dark modes.
- Keep the lab's progressive checkpoint language and short numbered steps. Each section needs an objective, prerequisite state, exact action, observable result, and recovery guidance. Do not remove existing instructions merely to shorten the page.
- Give the attendee one clear flow/version/routing state at a time. Name any template warm-up flow separately from `ServiceDesk` unless live testing proves a safe single-flow progression.
- Ensure all visible activity outputs, especially queue, HTTP, Function, and Virtual Agent outcomes, have explicit safe paths. The guide should teach the difference between a single interaction's Debugging trace and aggregate Analytics.
- Use public product documentation and live tenant behavior for click-level truth. The source DOCX's internal Jira lifecycle table is an authoring input and must not become public attendee copy or an unverified availability claim.

## Review and completion gates

1. Clone and render the unchanged repository first; retain a baseline screenshot and confirm local navigation and styles. Make all changes on `arubhatt-flow-guide`, never on the default branch.
2. Perform each new flow activity in the sandbox before writing it as a runnable step. Record exact UI labels, supported topology, version names, call outcomes, and known-good recovery points. If cross-flow copy, callback, queue loop, Function parsing, or MCP access differs from the request, describe the observed behavior and adjust the guide to an equivalent tested exercise.
3. Review the complete guide page by page, including overview, bookmarks, Checkpoints 1–9, bonus, troubleshooting, navigation, media, and downloadable assets. Every step must have evidence appropriate to its complexity; every “Show me how” panel must have a real GIF.
4. Build the local site and inspect it in a browser at desktop and narrow widths, in light and dark modes. Verify links, diagram semantics, image/GIF loading, alt text, no overflow, and that the full caller journey reads in the right order.
5. Audit the repository and generated site for credentials before any remote update. Commit and push only `arubhatt-flow-guide` when the guide and media pass. Keep the local preview running and open an annotation-capable review view for attendee feedback. Merge to the default branch only after the owner reviews the branch.

**Definition of done:** the remote feature branch contains a complete, evidence-backed guide; the same revision renders locally for review; the live lab has proved the required queue, HTTP, subflow, Function, debug/analytics, agent, and handoff paths; every procedural GIF and screenshot matches the final instructions; and the public site on the default branch remains untouched until review.
