# Finish the lab

The guide shows `ServiceDesk` version 5 published as **Latest** and selected by the entry point. Complete the lab with live calls that confirm both the order response and the route to a human queue.

```text
Caller → Flow Designer entry → AI agent
                           ├─ order → Order Desk MCP → response → handled → end
                           ├─ general support → human agent queue → queue treatment
                           └─ errored → spoken error message → disconnect
```

## Make the final calls

1. Call your assigned number and ask for an update on `ORD-10482`. Confirm that the agent uses `lookup_order` and speaks the order status and delivery information.
2. Call again and ask for a person. Confirm that the caller hears the escalation message and enters `Queue-1` wait treatment. If a test agent is available, confirm that the agent can answer.
3. In Flow Designer **Debug**, open both Interaction IDs and check the **Handled** and **Escalated** paths. In AI Agent Studio **Sessions**, inspect the `lookup_order` result. If either call takes an unexpected path, use [Troubleshooting](troubleshooting.md) before marking the lab complete.

## What the guide verifies

- The `SimpleQueue` practice flow was called live; **Debug** and **Analyze** show the queue path.
- A live call through the refactored `ServiceDesk` order branch returned `Shipped` for synthetic order `ORD-10482` and entered queue treatment. The earlier direct REST version and callback practice path still need their own phone checks if you want to verify those variants.
- Order Desk `lookup_order` worked in MCP Lab. The [published AI agent](assets/lab-guide/live/cp8-ai-agent-published.jpg) returned the order result in Preview, and its [Sessions trace](assets/lab-guide/live/cp8-session-lookup-order-success.jpg) recorded success. A Studio **Agent handover** badge shows a test-session request, not voice queue delivery.
- The final `ServiceDesk` version 5 [passed Validation with 0 errors](assets/lab-guide/live/cp9-ai-flow-zero-errors.jpg) and was published as **Latest**. A real [phone call followed its Handled path](assets/lab-guide/live/cp9-v5-handled-call-debug-path.jpg); a same-time [Voice session ran `lookup_order` successfully](lab5_end_to_end.md#compare-your-order-call), and Analyze counted one execution with zero node errors. Confirm the spoken response and test the human queue with a separate call.

## Beyond the lab

MCP Lab, Order Desk, the assigned organization, and its credentials are temporary training resources. For production use, plan managed credential storage and rotation, app and tool ownership, schema and allowlist review, timeout and retry behavior, monitoring, approval for write actions, data-handling rules, and tested error and escalation paths. Do not reuse the lab token, URLs, or sandbox configuration. See the [official product references](references.md).

Use this [online guide](overview.md) for the current lab. Historical Word and PDF snapshots are kept in the repository under `archive/2026-09-23-pre-update-walkthrough/`; they predate the queue-treatment, Function, subflow, and MCP steps.
