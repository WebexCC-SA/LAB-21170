# Checkpoints 4-5: Connect Order Desk and test the lookup

<span id="checkpoint-4-inspect-the-external-mcp-in-mcp-lab"></span>
## Checkpoint 4: Connect and inspect Order Desk in MCP Lab

The REST branch is published; its runtime response still needs the phone and Debug test in Checkpoint 3. Now inspect the same external system through MCP and see the tool contract an AI agent can use.

Return to the **AI agent** workspace in [MCP Lab](https://mcp-lab.webexdevs.com/). The Order Desk is a lab-provided simulation of an external order system. You do not need to enter an MCP URL or bearer token here.

1. On the lab-provided **Order Desk** card, select **Connect MCP**.
2. On **Connect the Order Desk MCP**, confirm that **Order Desk** and **Session token** are shown. Select **Inspect MCP tools**. Do not use **Inspect orders** on the card; that opens the sample order viewer, not the MCP connection.
3. On **Inspect the tool catalog**, review the five checked tools. The three read tools say **Runs automatically**; the two ticket-writing tools say **Approval required**.
4. Leave all five tools checked and select **Connect to AI agent**.
5. On **Ready to use**, confirm **Order Desk — 5 tools ready**, then select **Return to AI agent**.
6. In **Connected MCPs**, confirm that **Order Desk** shows **Connected**, **5 tools**, and **Active MCP**.

These five tools are connected only to the MCP Lab test agent. In Checkpoint 6, you will enable only `lookup_order` for the Webex voice agent.

??? example "Show me: connect and inspect Order Desk"
    ![Order Desk MCP connection sequence from Connect MCP to Connected MCPs](assets/lab-guide/05-order-desk-mcp-connection.gif)

    Follow the connection path through **Ready to use** and back to **Connected MCPs**. This recording shows the entire sequence.

    ![Live MCP Lab sequence from Inspect MCP tools to the discovered five-tool catalog](assets/lab-guide/gifs/cp4-mcp-discovery-live.gif)

    This closer view shows the live tool discovery. The server card displays a **Session token** label, not the token value.

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
  ![Live Order Desk MCP catalog with three automatic reads and two approval-required writes](assets/lab-guide/live/cp4-mcp-tool-catalog-live.jpg)
  <figcaption>Live MCP Lab catalog. All five tools were discovered in this session; the two ticket writes require approval.</figcaption>
</figure>

!!! success "Confirm before continuing"
    - **Connected MCPs** shows **Order Desk** with five tools.
    - `lookup_order`, `list_tickets`, and `get_ticket` are labeled as automatic read tools.
    - `create_ticket` and `update_ticket` are labeled as approval-required write tools.

<span id="checkpoint-5-exercise-automatic-reads-and-approval-gated-writes"></span>
## Checkpoint 5: Test the order lookup in MCP Lab

With Order Desk connected to the MCP Lab's AI agent, test the same order lookup that you will add to the Webex voice agent. Ticket tools are outside the required caller journey; the separate approval exercise below is optional.

### Run the required order read

1. Enter: `Use the connected Order Desk lookup_order tool for ORD-10482. Return only order number, status, and estimated delivery date. Omit customer name, email, address, tracking number, and item details.`
2. Wait for the tool activity to finish.
3. In **Tool activity**, confirm that the agent called `lookup_order` automatically.
4. Confirm that the response includes order status and delivery information for `ORD-10482`.

<figure markdown>
  ![Live lookup_order response for ORD-10482 with Shipped status and estimated delivery date, alongside completed tool activity](assets/lab-guide/live/cp4-mcp-order-lookup-live.jpg)
  <figcaption>Live read: `lookup_order` completed and returned `Shipped` with estimated delivery on September 28, 2026. The prompt kept customer details out of the displayed result.</figcaption>
</figure>

!!! success "Checkpoint complete"
    `lookup_order` ran automatically and returned order status and delivery data for `ORD-10482`. Continue to Checkpoint 6 when this is verified. The Webex voice agent will use only `lookup_order`.

### Optional MCP Lab bonus: inspect the approval boundary

This exercise stays in MCP Lab. It demonstrates how this lab gates a ticket write, but ticket tools are not enabled for the final Webex voice agent.

#### Read the session's tickets

1. Enter: `Use list_tickets for this attendee session. Show only ticket ID, related order number, status, and priority for open tickets. Omit customer information and descriptions.`
2. Confirm that the results are scoped to your current attendee session.

<figure markdown>
  ![Live list_tickets response showing only synthetic ticket IDs, related orders, status, and priority, with completed tool activity](assets/lab-guide/live/cp4-mcp-ticket-list-live.jpg)
  <figcaption>Live read: `list_tickets` completed for the attendee session. The captured response omits customer fields.</figcaption>
</figure>

#### Approve one synthetic ticket write

1. Enter: `Create one high-priority support ticket for synthetic order ORD-10482. Subject: LAB-21170 MCP approval verification. Description: Synthetic lab exercise to verify approval-gated create_ticket. Return only ticket ID, order number, status, and priority; omit customer information.`
2. Stop when the **Approval required** card appears.
3. Review the requested tool name and the prompt you sent. In the current lab UI the card identifies `create_ticket` but does not display the arguments, despite its explanatory text. If the request is ambiguous, cancel and write a more specific prompt.
4. Select **Approve tool** only if the request is the one you intended to test.
5. Read back the session's tickets and record the new ticket ID. If the assistant reports an error after approval, check `list_tickets` **before** retrying; a write may already have happened.

??? example "Show me: read, approve, and verify"
    ![Live MCP Lab sequence showing lookup_order, list_tickets, create_ticket approval, an assistant response error, and read-back of the created ticket](assets/lab-guide/gifs/cp5-mcp-read-and-approval-live.gif)

    This sequence uses actual lab screenshots. After approval, the assistant returned an invalid-response error. A separate `list_tickets` call found the new ticket, so the error did not mean the write failed.

<figure markdown>
  ![Live create_ticket approval card and pending tool activity](assets/lab-guide/live/cp4-mcp-ticket-approval-live.jpg)
  <figcaption>The approval gate paused the write before the tool ran. The prompt above the card specified one high-priority synthetic ticket for `ORD-10482`.</figcaption>
</figure>

!!! note "What happened in this live run"
    The test approval was selected once. The immediate assistant message said **“The lab service returned an invalid assistant response.”** A fresh `list_tickets` read found ticket `TKT-7D2AA52EB24243429CA6` for `ORD-10482`, **Open**, **High**, with the requested lab subject. The UI did not show `create_ticket` as a completed activity, so use the read-back as the evidence of the write. Do not submit the same create request again just because the assistant message fails.

    ![Live read-back confirms the created synthetic ticket after the assistant response error](assets/lab-guide/live/cp4-mcp-ticket-verified-live.jpg)

!!! success "Optional bonus confirmation"
    - The ticket list is scoped to your attendee session.
    - `create_ticket` pauses for approval. After approval, verify the resulting ticket with `list_tickets` and record its ID before any retry.

[Continue to Checkpoints 6-8](lab4_mcp_agent_studio.md){ .md-button .md-button--primary }
