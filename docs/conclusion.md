# Lab complete

You built and called three versions of the `ServiceDesk` flow:

1. A welcome message and two-option starter IVR.
2. A temporary order-support branch that calls the Order Desk REST API directly.
3. A final caller path that bypasses the menu and hands the conversation directly to the AI agent.

You also inspected the external Order Desk MCP, confirmed the boundary between automatic reads and approval-gated writes, registered and enabled the server, customized the Track Package autonomous template for order support, and published an agent that uses `lookup_order`.

```text
Caller → Flow Designer entry → AI agent → Order Desk MCP → order response
```

## Lab environment and production use

MCP Lab, Order Desk, the assigned organization, and the supplied credentials are temporary training resources. They demonstrate the integration pattern; they are not a production deployment.

Before adapting this pattern for production, establish:

- managed credential storage and rotation;
- clear ownership of every registered app and tool;
- schema and allowlist review;
- timeout, retry, and operational-monitoring behavior;
- auditable approval for write actions;
- data-handling rules; and
- tested error and escalation paths.

Never reuse the lab bearer token, lab URLs, or sandbox configuration in a production environment. Continue with the [official product references](references.md) when you adapt the pattern.

## Take the guide with you

- [Download the Word walkthrough](assets/downloads/LAB-21170-flow-lab-walkthrough.docx)
- [Download the PDF walkthrough](assets/downloads/LAB-21170-flow-lab-walkthrough.pdf)

!!! success
    You are finished when the live phone call reaches the AI agent directly and returns the order and delivery details for `ORD-10482`.
