# Bonus: inspect your flow through Contact Center MCP

After completing Checkpoint 9, use the MCP Lab AI agent to inspect the `ServiceDesk` flow you built. Order Desk MCP reads a simulated business system; **Webex Contact Center MCP** reads your actual Contact Center flow. This exercise lists and reads flows only. It does not change the agent, flow, or inbound routing.

Allow about **10–15 minutes**. Use the administrator account assigned to your sandbox.

## Enable Contact Center MCP in Control Hub

1. Open [Control Hub](https://admin.webex.com/). Sign in with the **Sandbox email** and **Sandbox password** from MCP Lab's **Test tenant** panel. Confirm that Control Hub shows your assigned organization, not your personal or company organization.
2. In the main navigation, select **Apps → Agentic Apps**. Find and open **Webex Contact Center**. Do not select **WebexCC Operation** or your external **Order Desk** app.
3. On **General**, under **Access**, select **Allowed for all users** in this sandbox organization.
4. **Click Save at the bottom of the General tab before opening another tab.** If access was already allowed and there are no unsaved changes, continue without changing it.
5. Open **Tools**. In the **Allow tool** column, turn on **List Flows** (`wxcc-list-flows`) and **Get Flow** (`wxcc-get-flow`). Other tools may remain enabled; you will select only these two in MCP Lab.
6. **Click Save at the bottom of the Tools tab before leaving it.** If both tools were already enabled and there are no unsaved changes, continue without changing them.
7. Reopen **General** and confirm **Allowed for all users** is still selected. Reopen **Tools** and confirm **Allow tool** is still on for **List Flows** and **Get Flow**.

The Webex-hosted server's authentication is already configured. Do not enter the Order Desk bearer token or add a custom Authorization header in **Authentication**. You will sign in with your sandbox Webex account when connecting MCP Lab below. See [Provisioning on Control Hub](https://developer.webex.com/mcp/docs/provisioning-on-control-hub) for the product reference.

!!! success "Confirm before connecting"
    The **Webex Contact Center** app shows **Allowed**, and **List Flows** and **Get Flow** remain enabled after reopening **Tools**. If the app is missing, a setting cannot be saved, or your account lacks administrator access, stop and ask the facilitator.

## Identify your flow and organization

1. Return to your completed `ServiceDesk` tab in Flow Designer. If you closed it, open **Control Hub → Contact Center → Customer Experience → Flows → Manage Flows** and open `ServiceDesk`.
2. Copy the **organization ID** from the Flow Designer address: it is the value after `orgId=`. Copy only that ID, not the entire URL. You can also find it in **Control Hub → Account → Info → Organization profile → Organization ID**. Keep the flow tab open to compare the MCP result with your canvas.

!!! info "This lab uses ProdUS1"
    The MCP Lab **Webex Contact Center** preset points to the ProdUS1 server. Use it only for the assigned ProdUS1 sandbox. For another region, ask the facilitator for the regional URL from the signed-in [Contact Center MCP Server page](https://developer.webex.com/mcp/docs/contact-center-mcp-server).

## Connect with your sandbox Webex account

1. Return to the **AI agent** workspace in [MCP Lab](https://mcp-lab.webexdevs.com/). Select **Add MCP**, then **Webex Contact Center** under **Preconfigured server**. Do not use **Connect MCP** on the Order Desk card; that connects the simulated order system.
2. Under **Authentication method**, select **Built-in Webex integration**. The preset initially selects **WCIT token**, so change it explicitly. You do not need to copy a bearer token for this connection.
3. Select **Authorize with Webex**. Sign in with the **Sandbox email** and **Sandbox password** from MCP Lab's **Test tenant** panel—not your personal Webex account. If Webex is already signed in as another user, switch to your assigned sandbox account before authorizing.
4. Review the Webex consent screen and select **Accept** for the sandbox integration. The built-in integration requests a fixed set of permissions, including configuration write access; selecting read tools below limits this exercise to flow inspection.
5. When MCP Lab returns to **Choose tools**, all discovered tools are initially selected. Clear every selection except `wxcc-list-flows` and `wxcc-get-flow`. Confirm that **2 enabled** is shown and both tools say **Runs automatically**.
6. Select **Connect MCP**. On **Ready to use**, confirm **Webex Contact Center — 2 tools ready**, then select **Return to AI agent**. Confirm that **Connected MCPs** shows **Webex Contact Center** as **Connected** with the two selected tools.

## Find your ServiceDesk flow

Replace `<your organization ID>` in the prompt below with the ID you copied from Flow Designer. If you renamed the imported flow, replace `ServiceDesk` with that name too. Paste the completed prompt into MCP Lab:

```text
Use wxcc-list-flows to find flows named ServiceDesk in organization <your organization ID>. Show each matching flow's name and ID. Do not create, change, or publish anything.
```

1. Wait for the tool call to finish. In **Tool activity**, look for `wxcc-list-flows completed`. Check that the response reports a matching flow, not an error, and refers to the organization ID in your prompt.
2. Find your `ServiceDesk` in the response. If there is more than one match, compare the flow ID with the value after `/flow/` in your Flow Designer URL. Do not select another attendee's flow.
3. Copy the returned flow ID for the next prompt.

!!! warning "Stop if access fails"
    A connected badge or a discovered catalog is not a successful flow read. If the call returns an authorization error, an empty result for a flow you can see in Flow Designer, or data from another organization, stop and show the facilitator the tool name and error. Do not switch to the Order Desk bearer token or try a different organization ID.

## Read and compare the completed flow

Replace both placeholders, then send:

```text
Use wxcc-get-flow to read the draft of flow <your ServiceDesk flow ID> in organization <your organization ID>. Return only the main-flow connections as source -> output condition -> destination. Then state whether those connections form a closed waiting-loop cycle; a Queue Contact activity alone is not a loop. Do not infer connections or describe runtime behavior beyond the returned edges. Do not create, change, validate, or publish anything.
```

1. In **Tool activity**, look for `wxcc-get-flow completed`. Confirm that the response contains flow connections rather than an error and that your prompt used the same organization and flow ID.
2. Compare the returned connections with your Flow Designer canvas:
    - the caller starts with `NewPhoneContact → AIAgent`, without the starter menu;
    - **Handled** ends the order-support conversation;
    - **Escalated** follows `EscalationMessage → HumanAgentQueue`;
    - the queue's **Waiting** path alternates music and the existing wait message;
    - the queue's **Failure** path reaches the existing End Flow activity; and
    - **Errored** follows `AgentErrorMessage → DisconnectContact`.
3. If a connection is missing or the summary disagrees with the canvas, ask the facilitator to review the returned connections. Do not let the agent invent a path or repair the flow. A successful tool call confirms access; it does not guarantee an accurate AI explanation.

## Finish the bonus

1. In **Connected MCPs**, select the **Webex Contact Center** card.
2. Under **Remove this MCP**, select **Remove connection**, then **Delete MCP**. This removes the connection and its saved credential from your MCP Lab session, not the Webex server or your Contact Center flow.
3. Confirm the Contact Center card is gone. Keep your Order Desk connection if it is still present; do not reset the whole session to remove one MCP.

!!! success "Bonus complete"
    Both flow-read tools succeeded in your assigned sandbox, and their results match your `ServiceDesk` draft. No flows, queues, or entry points were created or changed. Leave the completed flow and its entry-point routing in place for the facilitator's cleanup.

This bonus stops here. Flow authoring and the separate Contact Center Operations MCP are outside this exercise. See the [official references](references.md#bonus-webex-contact-center-mcp-services) for later exploration.

[Continue to troubleshooting and completion](troubleshooting.md){ .md-button .md-button--primary }
