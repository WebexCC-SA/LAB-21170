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
2. Call again and say `I need general support`. Accept the offer to connect with a person. Listen for the escalation message and `Queue-1` wait treatment. If a test agent is available, confirm that the agent can answer.
3. In Flow Designer **Debug**, open both Interaction IDs. Confirm the order call reached `AIAgent` and the general-support call followed **Escalated** into `Queue-1`. In AI Agent Studio **Sessions**, inspect the `lookup_order` result. If either call takes an unexpected path, use [Troubleshooting](troubleshooting.md) before marking the lab complete.

## Check your results

- In the practice flow, check the [queue call in Debug](assets/lab-guide/live/cp2-debug-trace.png) and [completed calls in Analyze](assets/lab-guide/live/cp2-analyze-overview.png).
- For the REST and refactored versions, confirm the order call speaks the current status for `ORD-10482` and digit `2` reaches `Queue-1`. Open each call in **Debug**.
- In the final flow, confirm the order call reaches `AIAgent` and [Voice Sessions](lab5_end_to_end.md#compare-your-order-call) shows a successful `lookup_order` action.
- On a separate general-support call, accept the human handoff and confirm **Debug** shows `EscalationMessage → HumanAgentQueue → PlayMusic`.

## Beyond the lab

MCP Lab, Order Desk, the assigned organization, and its credentials are temporary training resources. For production use, decide who owns the app and tools, store and rotate credentials, review schemas and allowed data, set timeouts, retries, and monitoring, require approval for writes, and test error and escalation paths. Do not reuse the lab token, URLs, or sandbox configuration. See the [official product references](references.md).
