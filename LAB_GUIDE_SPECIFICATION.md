# LAB-21170 Lab Guide Specification

## Purpose and editorial boundary

This specification records the implemented LAB-21170 attendee guide and the evidence still needed to finish it. The guide follows one synthetic Order Desk scenario through Webex Contact Center Flow Designer, MCP Lab, Webex Developer Portal, Control Hub, and Webex AI Agent Studio. Keep the nine checkpoints, short on-screen actions, existing MkDocs Material styling, and the visual language in `docs/stylesheets/extra.css`: dark navy `#051C2C`, cyan `#00bdeb`, and link blue `#3a7fff`.

The source **Webex One - Flow Designer Lab.docx** is a broader delivery map, not a source of click-level truth. The published guide uses observed tenant labels and distinguishes configured flows, Studio Preview results, and completed phone calls. Do not turn an untested path into a claimed outcome. The source cover and timing table disagree on duration, so the guide does not promise a session length.

## Attendee journey

| Checkpoint | Attendee action | Reference result and evidence boundary |
| --- | --- | --- |
| 1 | Redeem the lab assignment and open Control Hub, Flow Designer, AI Agent Studio, Developer Portal, and MCP Lab. | Use the assigned tenant details; keep credentials out of guide media. |
| 2, Part A | Create **Simple Inbound Call to Queue** as a separate practice flow, select `Queue-1`, validate, publish, and route `Entry Point-1`. | Practice version 1 received calls. Debug showed welcome, queue, wait treatment, and EndFlow; Analyze showed completed executions. |
| 2, Part B | Build `ServiceDesk` with a welcome, two-choice menu, and a human queue. Inspect **Comprehensive Call Flow** for post-queue behavior. | In the menu practice path, digit `2` goes directly to `Queue-1`. It must never play the old general-support placeholder and disconnect. |
| 2, queue treatment | Create **Queue Treatment Subflow** from its own template, attach it after Queue Contact in the separate practice flow, and add an optional callback choice in the main flow. | The Comprehensive template is a reference. **Callback** and **Blind Transfer** are main-flow activities and are not available in the subflow palette. The published practice version 2 configuration has no completed caller test and has open error outputs to repair before routing. |
| 3 | Compare a direct Order Desk HTTP request with a refactored `OrderLookup` subflow and a published Python Function that parses the response. | Function tests covered usable, missing, and malformed-shape status values. A refactored `ServiceDesk` call reached `OrderLookup`, returned `Shipped` for `ORD-10482`, and appeared in Debug/Analyze. The earlier direct HTTP version has no separate confirmed phone trace. |
| 4–5 | Inspect the Order Desk MCP catalog and read-only `lookup_order`; keep any approval-gated ticket write separate. | The five-tool catalog and lookup were inspected live. Do not enable ticket writes for the voice agent. |
| 6 | Register `LAB21170 Order Desk MCP` in Developer Portal, allow the app in the assigned Control Hub tenant, save the temporary `Authorization` custom header, and enable only `lookup_order`. | Each admin screen has a credential-safe guide image. All four ticket tools remain off. |
| 7–8 | Create `LAB-21170 Order Support` with **Start from scratch → Autonomous**, attach `lookup_order`, set order-support instructions and human-handover behavior, preview, and publish. | Studio Preview returned order details for `ORD-10482`; its session trace recorded a successful MCP action. A separate general-support Preview offered a human and recorded **Agent handover** after acceptance. These are Studio results, not voice-queue proof. |
| 9 | Replace the starter IVR in `ServiceDesk` with **Virtual Agent V2** and connect handled, escalated, errored, and queue-failure outcomes. | `ServiceDesk` version 5 is published as **Latest**, with zero validation errors. Active `Entry Point-1` routes to `ServiceDesk` **Latest**. Fresh version 5 phone, Debug, and Analyze evidence is still required. |

## Flow topology and versions

```text
Practice menu: caller → welcome → SupportMenu
  ├─ 1 → direct REST, then OrderLookup subflow and Function in later versions
  │       → status or honest fallback → Queue-1 → wait treatment
  └─ 2 → Queue-1 → wait treatment

Final version 5: caller → AIAgent (Virtual Agent V2)
  ├─ Handled → DisconnectContact
  ├─ Escalated → EscalationMessage → HumanAgentQueue (Queue-1)
  │               → PlayMusic ↔ PleaseWait
  │               └─ queue Failure → QueueErrorMessage → DisconnectContact
  └─ Errored → AgentErrorMessage → DisconnectContact
```

The final version starts `NewContact → AIAgent`. The numbered menu and direct REST activity are absent from that published caller path. Earlier versions remain in Flow Designer version history for practice and recovery. The order lookup is an external MCP action attached to the AI agent; the Function and HTTP subflow belong to the earlier comparison exercise.

## Remaining live checks

1. Place a fresh version 5 order call. Ask about `ORD-10482`; confirm the spoken status and delivery information. In Debug, match the completed call to version 5 and verify the `AIAgent` path. Check the same version and time window in Analyze after ingestion.
2. Place a separate version 5 call asking for general support. Accept the offer of a human agent. Confirm that no numbered menu or general-support placeholder plays, then listen for the escalation message and queue treatment. If an assigned test agent is available, answer the call. Verify `AIAgent → EscalationMessage → HumanAgentQueue` in Debug and check Analyze. Do not infer phone delivery from Studio Preview.
3. If the practice version 2 callback exercise will be presented as fully tested, first connect its Menu, Callback, and confirmation-message error outputs, republish, route it with the assigned tenant owner's coordination, and call-test both wait and callback branches. Keep its present publication screenshot labeled as configuration evidence until then.
4. If the direct REST exercise will be presented as a verified phone result, route its historical published version in a controlled test and capture its own Debug trace. The guide currently distinguishes this from the proven refactored lookup call.
5. Capture fresh screenshots or a short GIF for any newly verified result, crop caller identifiers and credentials, and revise the corresponding captions. Controlled Queue Contact failure and unavailable-order tests require a safe fixture; do not manufacture them as successful live calls.

## Evidence and media contract

| Evidence | What the guide may say |
| --- | --- |
| Saved settings, zero-error Validation, and published version | Configuration and publication succeeded. They do not establish caller experience. |
| Studio Preview plus Sessions action trace | The agent used `lookup_order` or the system **Agent handover** action in chat Preview. They do not establish a phone queue handoff. |
| Completed phone call plus Debug interaction | The stated path executed for that call and flow version. Exclude the caller number, interaction identifier, and sensitive payloads from public media. |
| Analyze after completed calls | Aggregate counts for the selected flow version and time window; ingestion can lag. A callback-registered call may be excluded from completed-call totals. |

Use real tenant screenshots and GIFs with readable crops, precise alt text, and captions that identify the action or outcome. A screenshot sequence can show setup steps; label it as setup rather than a completed call. Do not include temporary bearer values, event tokens, passwords, reusable headers, caller numbers, private transcripts, or customer details in source, generated site, screenshots, GIF frames, or downloads. Archive outdated Word and PDF walkthroughs rather than offering them as the current guide.

## Optional Contact Center MCP material

The external Order Desk MCP serves the AI agent. The Webex Contact Center Flow MCP and Operations MCP are separate Cisco services. The guide presents their documented read-only discovery as an optional reference because neither service was used in this lab tenant. Availability, endpoint, authentication, entitlement, enabled catalog, and permitted action must be verified before turning a tool name into an attendee exercise. Do not describe an unreleased visual-canvas MCP Client activity as available or imply that the read-only Operations service edits flows.

## Delivery state and completion checks

The repository was cloned and rendered locally before guide edits. Colleague PR [#1](https://github.com/WebexCC-SA/LAB-21170/pull/1) was analyzed and merged additively. The guide and media checkpoint was pushed as PR [#2](https://github.com/WebexCC-SA/LAB-21170/pull/2) and merged to `main`; the feature branch was synchronized with that merge. The user authorized these merges and asked for continued work on the feature branch, with another PR **later** after the remaining work is complete. Do not reinstate an owner-review or do-not-merge gate for PR #2.

For the next revision, keep the local preview running for feedback, review every checkpoint in the rendered site, run strict MkDocs build and link/media checks, inspect desktop and narrow layouts, and audit both source and generated site for secrets. Push the finished revision to the feature branch for the later PR. The guide is complete when every asserted caller outcome has matching versioned evidence, each admin action has a safe screenshot, and the final voice order and human-handoff calls have been checked in Debug and Analyze.
