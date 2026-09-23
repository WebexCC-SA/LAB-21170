# Lab complete

You built and called three versions of the `ServiceDesk` flow:

1. A welcome message and two-option starter IVR.
2. A temporary order-support branch that calls the Order Desk REST API directly.
3. A final caller path that bypasses the menu and hands the conversation directly to the AI agent.

You also inspected the external Order Desk MCP, confirmed the boundary between automatic reads and approval-gated writes, registered and enabled the server, customized the Track Package autonomous template for order support, and published an agent that uses `lookup_order`.

```text
Caller → Flow Designer entry → AI agent → Order Desk MCP → order response
```

## Take the guide with you

- [Download the Word walkthrough](assets/downloads/LAB-21170-flow-lab-walkthrough.docx)
- [Download the PDF walkthrough](assets/downloads/LAB-21170-flow-lab-walkthrough.pdf)

!!! success
    You are finished when the live phone call reaches the AI agent directly and returns the order and delivery details for `ORD-10482`.
