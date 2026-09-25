# Finish the lab

Finish with two live calls: one for order status, and one for human support. Check each call in **Debug**. The screenshots show `ServiceDesk` version 5 as **Latest**; your version number may differ.

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

## Compare with the reference captures

- Compare your first practice call with the queue path shown in [**Debug**](assets/lab-guide/live/cp2-debug-trace.png) and [**Analyze**](assets/lab-guide/live/cp2-analyze-overview.png). For the direct REST version and the callback path, use separate calls and check their traces.
- Compare your refactored `ServiceDesk` order call with the reference trace: `OrderLookup` returned `Shipped` for synthetic order `ORD-10482`, then the flow played the status message and entered queue treatment.
- In MCP Lab, `lookup_order` returned the order details. The [published AI agent](assets/lab-guide/live/cp8-ai-agent-published.jpg) returned them in Preview, and [Sessions](assets/lab-guide/live/cp8-session-lookup-order-success.jpg) recorded a successful lookup. A Studio **Agent handover** badge confirms the Preview request; check voice queue delivery with a phone call.
- The final `ServiceDesk` flow [passed Validation with 0 errors](assets/lab-guide/live/cp9-ai-flow-zero-errors.jpg). A [phone call followed its Handled path](assets/lab-guide/live/cp9-v5-handled-call-debug-path.jpg), and a same-time [Voice session ran `lookup_order` successfully](lab5_end_to_end.md#compare-your-order-call). Confirm what your caller heard, then test the human queue with a separate call.

## Beyond the lab

MCP Lab, Order Desk, the assigned organization, and its credentials are temporary training resources. For production use, decide who owns the app and tools, store and rotate credentials, review schemas and allowed data, set timeouts, retries, and monitoring, require approval for writes, and test error and escalation paths. Do not reuse the lab token, URLs, or sandbox configuration. See the [official product references](references.md).
