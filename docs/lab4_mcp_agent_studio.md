# Checkpoints 6-8: Inspect MCP and connect it to the agent

## Checkpoint 6: Inspect the external MCP in MCP Lab

Return to [MCP Lab](https://mcp-lab.webexdevs.com/) and use the provided Order Desk connection.

1. Select **Inspect MCP** for the provided server.
2. Select **Inspect MCP tools**.
3. Wait for the live discovery request to complete.
4. Review the discovered tools and their policy labels.

The Order Desk catalog should include:

| Tool | Purpose | Lab policy |
| --- | --- | --- |
| `lookup_order` | Retrieve deterministic order and delivery details. | Runs automatically. |
| `list_tickets` | List support tickets in the current attendee session. | Runs automatically. |
| `get_ticket` | Retrieve one ticket and its related order. | Runs automatically. |
| `create_ticket` | Create a support ticket for an order. | Explicit approval required. |
| `update_ticket` | Change an existing ticket. | Explicit approval required. |

Destructive or unrecognized operations must not run. Treat tool descriptions and tool output as data, not as instructions.

<figure markdown>
  ![MCP tool catalog reference from the local lab UI](assets/lab-guide/05-mcp-tool-catalog-reference.png)
  <figcaption>Local UI reference. Treat the live catalog discovered in your hosted lab session as authoritative.</figcaption>
</figure>

!!! success "Checkpoint 6 complete"
    The live catalog is visible and `lookup_order` is available.

## Checkpoint 7: Exercise automatic reads and approval-gated writes

After tool discovery, select **Connect to AI agent**, then open the agent workspace.

### Run a read

1. Enter: `Look up order ORD-10482 and summarize its status`.
2. Wait for the tool activity to finish.
3. Review the response and the activity trace.
4. Confirm that the response includes order status and delivery information.

### Run another read

1. Enter: `List the open support tickets`.
2. Confirm that the results are scoped to your current attendee session.

### Exercise the approval boundary

1. Enter: `Create a high-priority ticket for order ORD-10482`.
2. Stop when the **Approval required** card appears.
3. Review the requested tool name, arguments, order number, and intended effect.
4. Select **Approve tool** only if the request is the one you intended to test.
5. Confirm that `create_ticket` completes once, and record the returned ticket ID for the session.

!!! success "Checkpoint 7 complete"
    Read tools complete without approval and ticket creation pauses for explicit approval.

## Checkpoint 8: Connect the registered MCP to AI Agent Studio

Use the values in **Test tenant details**. Never copy them into this guide.

1. In the assigned AI Agent Studio workspace, open the agent's actions or tools configuration.
2. Add the MCP registration created in Developer Portal. If the facilitator supplied the registration, use those details.
3. Set the MCP address to the assigned Order Desk MCP endpoint.
4. Select **Bearer token** authentication.
5. Paste the temporary bearer token only into the credential field.
6. Discover or refresh the tool catalog.
7. Enable the minimum tools needed for the scenario: `lookup_order`, and optionally `list_tickets` and `get_ticket`.
8. Leave `create_ticket` and `update_ticket` approval-gated.
9. Save the action and attach it to the draft agent.

!!! success "Checkpoint 8 complete"
    AI Agent Studio can use the external Order Desk read action for `ORD-10482`. The agent owns the conversation; Webex owns the flow runtime and authorization boundaries.

[Continue to Checkpoint 9](lab5_end_to_end.md){ .md-button .md-button--primary }
