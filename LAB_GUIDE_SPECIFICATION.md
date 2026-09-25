# LAB-21170 Lab Guide Specification

## Purpose and editorial boundary

This specification records the implemented LAB-21170 attendee guide and the evidence still needed to finish it. The guide follows one synthetic Order Desk scenario through Webex Contact Center Flow Designer, MCP Lab, Webex Developer Portal, Control Hub, and Webex AI Agent Studio. Keep the nine checkpoints, short on-screen actions, existing MkDocs Material styling, and the visual language in `docs/stylesheets/extra.css`: dark navy `#051C2C`, cyan `#00bdeb`, and accessible link blue `#2866d0` on light backgrounds or `#6ea3ff` in slate mode.

The source **Webex One - Flow Designer Lab.docx** is a broader delivery map, not a source of click-level truth. The published guide uses observed tenant labels and distinguishes configured flows, Studio Preview results, and completed phone calls. Do not turn an untested path into a claimed outcome. The source cover and timing table disagree on duration, so the guide does not promise a session length.

The source also sketches a Pebble/data-driven branching mission and a Flow V2 export/validate/diff and Flow MCP authoring mission. Those are future extensions, not steps in the current nine-checkpoint Order Desk lab. The requested additions here focus on the Flow Designer template, queue, REST, Function, subflow, debugging, analytics, and AI-agent journey.

## Attendee journey

| Checkpoint | Attendee action | Reference result and evidence boundary |
| --- | --- | --- |
| 1 | Redeem the lab assignment and open Control Hub, Flow Designer, AI Agent Studio, Developer Portal, and MCP Lab. | Use the assigned tenant details; keep credentials out of guide media. |
| 2, Part A | Create **Simple Inbound Call to Queue** as a separate practice flow, select `Queue-1`, validate, publish, and route `Entry Point-1`. | Practice version 1 received calls. Debug showed welcome, queue, wait treatment, and EndFlow; Analyze showed completed executions. |
| 2, Part B | Build `ServiceDesk` with a welcome, two-choice menu, and a human queue. Inspect **Comprehensive Call Flow** for post-queue behavior. | The attendee's menu digit `2` must go directly to `Queue-1`. The retained reference version 1 still used `GeneralSupportMessage` and disconnected; published version 4 corrected that link. Version 4 has no confirmed digit `2` phone trace yet. |
| 2, queue treatment | Create **Queue Treatment Subflow** from its own template, attach it after Queue Contact in the separate practice flow, and add an optional callback choice in the main flow. | The Comprehensive template is a reference. **Callback** and **Blind Transfer** are main-flow activities and are not available in the subflow palette. Practice version 3 now routes the three formerly open error outputs through a spoken fallback and disconnect, passed Validation with 0 errors, and was published as Latest. It still needs a phone test. |
| 3 | Compare a direct Order Desk HTTP request with a refactored `OrderLookup` subflow and a published Python Function that parses the response. | Function tests covered usable, missing, and malformed-shape status values. A refactored `ServiceDesk` call reached `OrderLookup`, returned `Shipped` for `ORD-10482`, and appeared in Debug/Analyze. The earlier direct HTTP version has no separate confirmed phone trace. |
| 4–5 | Inspect the Order Desk MCP catalog and read-only `lookup_order`; keep any approval-gated ticket write separate. | The five-tool catalog and lookup were inspected live. Do not enable ticket writes for the voice agent. |
| 6 | Register `LAB21170 Order Desk MCP` in Developer Portal, allow the app in the assigned Control Hub tenant, save the temporary `Authorization` custom header, and enable only `lookup_order`. | Each admin screen has a credential-safe guide image. All four ticket tools remain off. After the MCP Lab session was resumed, its temporary bearer changed; refreshing the saved header restored the Control Hub tool catalog. A fresh screenshot shows the lookup-only permission state. |
| 7–8 | Create `LAB-21170 Order Support` with **Start from scratch → Autonomous**, attach `lookup_order`, set order-support instructions and human-handover behavior, preview, and publish. | After the bearer refresh, MCP Lab and a fresh Studio Preview both returned `Shipped` and September 29, 2026 for `ORD-10482`. The sample delivery date differed from an earlier Preview, so attendee instructions should compare against the live Order Desk result rather than a fixed date. A separate general-support Preview offered a human and recorded **Agent handover** after acceptance. These are Studio results, not voice-queue proof. |
| 9 | Replace the starter IVR in `ServiceDesk` with **Virtual Agent V2** and connect handled, escalated, errored, and queue-failure outcomes. | `ServiceDesk` version 5 is published as **Latest**, with zero validation errors. Active `Entry Point-1` routes to `ServiceDesk` **Latest**. The caller confirmed a fresh 22:14 order call spoke **Shipped** and September 29; Flow Designer Debug and AI Agent Studio Voice Sessions showed the same Interaction ID. The Voice `lookup_order` succeeded in 0.2 seconds, Debug recorded `NewContact → AIAgent → ContactEnded` with all Success, and Analyze showed one execution and zero node errors in the call window. The caller ended that call after the response. An earlier 20:48 order call exercised **Handled → DisconnectContact** and had a successful same-time Voice lookup, though its spoken wording was not captured. A separate general-support call at 21:46 reached `AIAgent → EscalationMessage → HumanAgentQueue → PlayMusic → PleaseWait → PlayMusic → ContactEnded`, all successful in Debug. The caller heard queue music; Analyze showed one execution and zero node errors in that call window. A human agent answer was not verified. |

The 21:46 general-support Voice session also attempted an order lookup before handoff. That action failed with **MCP execution failure** while the old temporary bearer was saved in Control Hub. The MCP Lab bearer changed after session renewal; updating the Control Hub header restored the tool catalog and the later lookup tests. The guide's troubleshooting row describes recovery without exposing the bearer.

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

## Remaining live verification

The final order and human-queue phone paths are verified. The earlier queue-treatment and direct-REST paths still need their own caller traces before the requested end-to-end author QA is complete. The attendee guide does not claim those paths were verified by phone. Courtesy Callback is conditional on the lab queue's entitlement.

1. In a coordinated phone-test window, route the repaired practice flow version 3 on **Latest**. Call, stay through queue treatment, press `2` at `CallbackOrWait`, and confirm another wait cycle. Capture its Debug trace and Analyze window, then restore `ServiceDesk` **Latest**. Test callback digit `1` only if Courtesy Callback is enabled.
2. `ServiceDesk` versions 1 and 4 have no active version label. Control Hub's entry-point picker routes by label, so it cannot select either historical version directly. Do not edit an older version in the original `ServiceDesk` flow: Flow Designer can replace its current draft, and republishing would move **Latest** away from the final AI version. Prepare separately named QA copies from the specific published versions through a supported import path, validate and publish each copy, and check its topology before routing it in a coordinated test window. Availability of the required Flow API or export/import access in this tenant is not yet established.
3. On the direct-REST copy of version 1, refresh its temporary Order Desk credential if needed. Call, press `1`, and confirm in Debug that `GetOrder` returns the status for `ORD-10482`. Version 1's digit `2` still plays the old placeholder; do not use it as evidence for the corrected general-support branch.
4. On the corrected-menu copy of version 4, call and press `2`. Confirm the call enters `Queue-1` and wait treatment without `GeneralSupportMessage` or OrderLookup. Capture Debug and Analyze, then restore and verify `ServiceDesk` version 5 **Latest** on the entry point.
5. Capture fresh screenshots or a short GIF for each newly verified result, crop caller identifiers and credentials, and revise the corresponding captions. Controlled Queue Contact failure and unavailable-order tests require a safe fixture; do not manufacture them as successful live calls.

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

The repository was cloned and rendered locally before guide edits. Colleague PR [#1](https://github.com/WebexCC-SA/LAB-21170/pull/1) was analyzed and merged additively. Guide and media changes landed through PR [#2](https://github.com/WebexCC-SA/LAB-21170/pull/2), QA revision through PR [#3](https://github.com/WebexCC-SA/LAB-21170/pull/3), attendee-writing/media polish through PR [#4](https://github.com/WebexCC-SA/LAB-21170/pull/4), and the verified human-queue trace through PR [#5](https://github.com/WebexCC-SA/LAB-21170/pull/5). The confirmed order-call result and final admin screenshots are in PR [#6](https://github.com/WebexCC-SA/LAB-21170/pull/6). PR [#7](https://github.com/WebexCC-SA/LAB-21170/pull/7) corrected the historical version 1 menu-route description. The strict MkDocs build, local preview, image-reference check, credential scan, and desktop and phone-width review passed for the guide; the later PR #7 text correction also passed a strict build and Pages deploy.

Keep the local preview and annotation review available for feedback. The order and human-handoff voice calls have now been checked against Debug, Analyze, and the relevant Studio Voice session. The refreshed MCP connection succeeded in MCP Lab, Studio Preview, and the later phone call. Finish the remaining live checks above, match each caller outcome to versioned evidence, and keep a safe screenshot at each admin action. Publish later corrections through the feature branch and a separate PR.
