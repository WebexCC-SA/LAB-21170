# Checkpoints 4-5: Connect and test the order lookup

<span id="checkpoint-4-inspect-the-external-mcp-in-mcp-lab"></span>
## Checkpoint 4: Connect and inspect Order Desk in MCP Lab

After testing the Order Desk REST request in Flow Designer, connect the Order Desk MCP to the MCP Lab AI agent. You will exercise only its order lookup in this lab.

Return to the **AI agent** workspace in [MCP Lab](https://mcp-lab.webexdevs.com/). The Order Desk is a lab-provided simulation of an external order system. You do not need to enter an MCP URL or bearer token here.

1. On the lab-provided **Order Desk** card, select **Connect MCP**.
2. On **Connect the Order Desk MCP**, confirm that **Order Desk** and **Session token** are shown. Select **Inspect MCP tools**. Do not use **Inspect orders** on the card; that opens the sample order viewer, not the MCP connection.
3. On **Inspect the tool catalog**, review the available tools. Leave the five default selections in place. Confirm that `lookup_order` says **Runs automatically**.
4. Select **Connect to AI agent**.
5. On **Ready to use**, confirm that Order Desk has five tools ready, then select **Return to AI agent**.
6. In **Connected MCPs**, confirm that **Order Desk** shows **Connected**, **5 tools**, and **Active MCP**.

The MCP Lab test agent has access to all five tools, but this exercise uses only `lookup_order`. Do not run the ticket tools. Later, in Control Hub, you will allow only `lookup_order` for the Webex voice agent.

??? example "Show me: connect Order Desk"
    ![Order Desk MCP connection sequence from Connect MCP to Connected MCPs](assets/lab-guide/05-order-desk-mcp-connection.gif)

    ![Live MCP Lab sequence from Inspect MCP tools to the discovered five-tool catalog](assets/lab-guide/gifs/cp4-mcp-discovery-live.gif)

<figure markdown>
  ![Live Order Desk MCP catalog with five available tools](assets/lab-guide/live/cp4-mcp-tool-catalog-live.jpg)
  <figcaption markdown="span">Leave the default tool selections in place. You will test only <code>lookup_order</code>.</figcaption>
</figure>

!!! success "Confirm before continuing"
    - **Connected MCPs** shows **Order Desk** with five tools connected.
    - `lookup_order` is labeled **Runs automatically**.

<span id="checkpoint-5-exercise-automatic-reads-and-approval-gated-writes"></span>
## Checkpoint 5: Test the order lookup in MCP Lab

With Order Desk connected to the MCP Lab AI agent, test the same lookup you will add to the Webex voice agent.

### Run the required order read

1. Enter: `Use lookup_order for ORD-10482. Tell me only the order number, status, and estimated delivery date. Do not include customer or item details.`
2. Wait for the tool activity to finish.
3. In **Tool activity**, confirm that the agent called `lookup_order` automatically.
4. Confirm that the response includes the order number, current status, and estimated delivery date. The values may differ from the example screenshot.

<figure markdown>
  ![Live lookup_order response for ORD-10482 with order status and estimated delivery date alongside completed tool activity](assets/lab-guide/live/cp4-mcp-order-lookup-live.jpg)
  <figcaption markdown="span">Check the current result for your session; the sample status and date may change.</figcaption>
</figure>

!!! success "Continue when your lookup succeeds"
    Check **Tool activity** for an automatic `lookup_order` call and read the current status and delivery date for `ORD-10482`. In Checkpoint 6, allow only this lookup for the Webex voice agent.

[Continue to Checkpoints 6-8](lab4_mcp_agent_studio.md){ .md-button .md-button--primary }
