# Checkpoints 4-5: Connect Order Desk and test the lookup

<span id="checkpoint-4-inspect-the-external-mcp-in-mcp-lab"></span>
## Checkpoint 4: Connect and inspect Order Desk in MCP Lab

After configuring the Order Desk HTTP Request in Flow Designer, inspect the MCP tools you will use with the AI agent.

Return to the **AI agent** workspace in [MCP Lab](https://mcp-lab.webexdevs.com/). The Order Desk is a lab-provided simulation of an external order system. You do not need to enter an MCP URL or bearer token here.

1. On the lab-provided **Order Desk** card, select **Connect MCP**.
2. On **Connect the Order Desk MCP**, confirm that **Order Desk** and **Session token** are shown. Select **Inspect MCP tools**. Do not use **Inspect orders** on the card; that opens the sample order viewer, not the MCP connection.
3. On **Inspect the tool catalog**, review the five checked tools. The three read tools say **Runs automatically**; the two ticket-writing tools say **Approval required**.
4. Leave all five tools checked and select **Connect to AI agent**.
5. On **Ready to use**, confirm **Order Desk — 5 tools ready**, then select **Return to AI agent**.
6. In **Connected MCPs**, confirm that **Order Desk** shows **Connected**, **5 tools**, and **Active MCP**.

All five tools here belong to the MCP Lab test agent. In Checkpoint 6, you will allow only `lookup_order` for the Webex voice agent.

??? example "Show me: connect and inspect Order Desk"
    ![Order Desk MCP connection sequence from Connect MCP to Connected MCPs](assets/lab-guide/05-order-desk-mcp-connection.gif)

    Follow the connection through **Ready to use** and back to **Connected MCPs**.

    ![Live MCP Lab sequence from Inspect MCP tools to the discovered five-tool catalog](assets/lab-guide/gifs/cp4-mcp-discovery-live.gif)

    Inspect the five-tool catalog. The server card shows a **Session token** label without its value.

The Order Desk catalog should include:

| Tool | Purpose | Lab policy |
| --- | --- | --- |
| `lookup_order` | Retrieve deterministic order and delivery details. | Runs automatically. |
| `list_tickets` | List support tickets in the current attendee session. | Runs automatically. |
| `get_ticket` | Retrieve one ticket and its related order. | Runs automatically. |
| `create_ticket` | Create a support ticket for an order. | Explicit approval required. |
| `update_ticket` | Change an existing ticket. | Explicit approval required. |

<figure markdown>
  ![Live Order Desk MCP catalog with three automatic reads and two approval-required writes](assets/lab-guide/live/cp4-mcp-tool-catalog-live.jpg)
  <figcaption markdown="span">The catalog shows five tools. Both ticket writes require approval.</figcaption>
</figure>

!!! success "Confirm before continuing"
    - **Connected MCPs** shows **Order Desk** with five tools.
    - `lookup_order`, `list_tickets`, and `get_ticket` are labeled as automatic read tools.
    - `create_ticket` and `update_ticket` are labeled as approval-required write tools.

<span id="checkpoint-5-exercise-automatic-reads-and-approval-gated-writes"></span>
## Checkpoint 5: Test the order lookup in MCP Lab

With Order Desk connected to the MCP Lab AI agent, test the lookup you will add to the Webex voice agent. You can skip the ticket exercise below.

### Run the required order read

1. Enter: `Use the connected Order Desk lookup_order tool for ORD-10482. Return only order number, status, and estimated delivery date. Omit customer name, email, address, tracking number, and item details.`
2. Wait for the tool activity to finish.
3. In **Tool activity**, confirm that the agent called `lookup_order` automatically.
4. Confirm that the response includes order status and delivery information for `ORD-10482`.

<figure markdown>
  ![Live lookup_order response for ORD-10482 with Shipped status and estimated delivery date, alongside completed tool activity](assets/lab-guide/live/cp4-mcp-order-lookup-live.jpg)
  <figcaption markdown="span">`lookup_order` returned `Shipped` and an estimated delivery of September 28, 2026, without displaying customer details.</figcaption>
</figure>

!!! success "Continue when your lookup succeeds"
    Check **Tool activity** for an automatic `lookup_order` call and confirm the status and delivery data for `ORD-10482`. The screenshot above shows `Shipped` with an estimated delivery of September 28, 2026. In Checkpoint 6, allow only this lookup for the Webex voice agent.

### Optional: create a test ticket in MCP Lab

Create the test ticket only in MCP Lab. The Webex voice agent uses `lookup_order` only.

#### Read the session's tickets

1. Enter: `Use list_tickets for this attendee session. Show only ticket ID, related order number, status, and priority for open tickets. Omit customer information and descriptions.`
2. Confirm that the results are scoped to your current attendee session.

<figure markdown>
  ![Live list_tickets response showing only synthetic ticket IDs, related orders, status, and priority, with completed tool activity](assets/lab-guide/live/cp4-mcp-ticket-list-live.jpg)
  <figcaption markdown="span">`list_tickets` returned this session's ticket fields without customer details.</figcaption>
</figure>

#### Approve one synthetic ticket write

1. Enter: `Create one high-priority support ticket for synthetic order ORD-10482. Subject: LAB-21170 MCP approval verification. Description: Synthetic lab exercise to verify approval-gated create_ticket. Return only ticket ID, order number, status, and priority; omit customer information.`
2. Stop when the **Approval required** card appears.
3. Review the requested tool name and the prompt you sent. In the current lab UI the card identifies `create_ticket` but does not display the arguments, despite its explanatory text. If the request is ambiguous, cancel and write a more specific prompt.
4. Select **Approve tool** only if the request is the one you intended to test.
5. Read back the session's tickets and record the new ticket ID. If the assistant reports an error after approval, check `list_tickets` **before** retrying; a write may already have happened.

??? example "Show me: read, approve, and verify"
    ![Live MCP Lab sequence showing lookup_order, list_tickets, create_ticket approval, an assistant response error, and read-back of the created ticket](assets/lab-guide/gifs/cp5-mcp-read-and-approval-live.gif)

    After approval, the assistant returned an invalid-response error. A separate `list_tickets` call found the new ticket. Check the list before retrying a write.

<figure markdown>
  ![Live create_ticket approval card and pending tool activity](assets/lab-guide/live/cp4-mcp-ticket-approval-live.jpg)
  <figcaption markdown="span">Approval pauses `create_ticket`. Check that your prompt requests one high-priority synthetic ticket for `ORD-10482`.</figcaption>
</figure>

!!! note "If the assistant reports an error after approval"
    In the example, the assistant reported **“The lab service returned an invalid assistant response”** after approval, but a fresh `list_tickets` read found the new `ORD-10482` ticket as **Open** and **High**. The UI did not show `create_ticket` as completed. Use the ticket read-back to verify the write, and do not repeat the create request because of the assistant message alone.

    ![Live read-back confirms the created synthetic ticket after the assistant response error](assets/lab-guide/live/cp4-mcp-ticket-verified-live.jpg)

!!! success "Optional bonus confirmation"
    - The ticket list is scoped to your attendee session.
    - `create_ticket` pauses for approval. After approval, verify the resulting ticket with `list_tickets` and record its ID before any retry.

[Continue to Checkpoints 6-8](lab4_mcp_agent_studio.md){ .md-button .md-button--primary }
