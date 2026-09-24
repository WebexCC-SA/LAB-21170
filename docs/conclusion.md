# Finish the lab

The lab is complete when an assigned phone call reaches the published autonomous agent, its **MCP** `lookup_order` action returns the order and delivery details for `ORD-10482`, and an escalation reaches the human queue. Inspect the call in Flow Designer Debug and confirm the intended outcomes before marking the final path complete.

```text
Caller → Flow Designer entry → AI agent → Order Desk MCP → order response
                           └─ escalation → human agent queue
```

## What the captured walkthrough verifies

| Checkpoint | Captured evidence |
| --- | --- |
| Practice queue flow, version 1 | `SimpleQueue` was published and exercised by phone; Debug and Analytics screenshots show those calls. |
| Reusable queue treatment, version 2 | The Queue Treatment subflow and a practice parent flow with a callback-or-wait menu were published. The parent flow passed Validation with 0 errors. No phone call through version 2 was captured; three optional error outputs remained unconnected. |
| Direct Order Desk branch | `ServiceDesk` version 1 was published with the direct HTTP request. Its phone response has not been captured. |
| Reusable lookup | The parser Function passed sample tests and was published; the guarded `OrderLookup` subflow was published as version 1. |
| Refactored caller path | `ServiceDesk` version 2 passed validation, was published with `Test` and `Latest`, and was assigned to Entry Point-1. Its phone response has not been captured. |
| AI and MCP path | An autonomous agent draft and MCP registration form were prepared. The Order Desk Agentic App was not submitted or enabled in the captured tenant, and Studio had no available MCP action. Final agent Preview, publication, and phone call remain to be completed. |

Use the [completion checklist](troubleshooting.md) as checks to perform, not as a record that every check already passed. Screenshots identify which steps were exercised live and which still need runtime verification.

## Lab environment and production use

MCP Lab, Order Desk, the assigned organization, and the supplied credentials are temporary training resources. They demonstrate the integration pattern; they are not a production deployment.

Before adapting this pattern for production, establish managed credential storage and rotation, app and tool ownership, schema and allowlist review, timeout and retry behavior, operational monitoring, auditable approval for write actions, data-handling rules, and tested error and escalation paths. Do not reuse the lab bearer token, lab URLs, or sandbox configuration. Continue with the [official product references](references.md).

## Current guide

This online guide contains the updated queue-treatment, Function, subflow, and MCP checkpoints. Earlier Word and PDF walkthroughs remain archived in the repository and do not include these updates.
