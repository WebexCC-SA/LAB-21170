# Bonus: inspect and edit a draft through Contact Center MCP

After completing Checkpoint 9, use the MCP Lab AI agent to inspect the `ServiceDesk` flow you built. Order Desk MCP reads a simulated business system; **Webex Contact Center MCP** reads and edits actual Contact Center flows. Start with flow inspection, then optionally make one small edit to a separate unpublished copy. Keep your completed `ServiceDesk` and its inbound routing unchanged.

Allow about **10–15 minutes** for inspection, plus **10–15 minutes** for the optional draft edit. Use the administrator account assigned to your sandbox.

## Enable Contact Center MCP in Control Hub

1. Open [Control Hub](https://admin.webex.com/). Sign in with the **Sandbox email** and **Sandbox password** from MCP Lab's **Test tenant** panel. Confirm that Control Hub shows your assigned organization, not your personal or company organization.
2. In the main navigation, select **Apps → Agentic Apps**. Find and open **Webex Contact Center**. Do not select **WebexCC Operation** or your external **Order Desk** app.
3. On **General**, under **Access**, select **Allowed for all users** in this sandbox organization.
4. **Click Save at the bottom of the General tab before opening another tab.** If access was already allowed and there are no unsaved changes, continue without changing it.

    ![Control Hub General Access panel with Allowed for all users selected](assets/lab-guide/live/bonus-control-hub-general.jpg){ width="800" }

    *General → Access: select **Allowed for all users**, then save before opening Tools.*

5. Open **Tools**. In the **Allow tool** column, turn on **List Flows** (`wxcc-list-flows`) and **Get Flow** (`wxcc-get-flow`). These are the minimum tools for flow inspection. You may enable other tools you are comfortable using in your assigned sandbox; selecting a tool does not run it.
6. **Click Save at the bottom of the Tools tab before leaving it.** If both tools were already enabled and there are no unsaved changes, continue without changing them.

    ![Control Hub Tools table showing Allow tool enabled for List Flows and Get Flow](assets/lab-guide/live/bonus-control-hub-read-tools.jpg){ width="800" }

    *Check the **Allow tool** column for both read tools. Save any changes before leaving Tools.*

7. Reopen **General** and confirm **Allowed for all users** is still selected. Reopen **Tools** and confirm **Allow tool** is still on for **List Flows** and **Get Flow**.

The Webex-hosted server's authentication is already configured. Do not enter the Order Desk bearer token or add a custom Authorization header in **Authentication**. You will sign in with your sandbox Webex account when connecting MCP Lab below. See [Provisioning on Control Hub](https://developer.webex.com/mcp/docs/provisioning-on-control-hub) for the product reference.

!!! success "Confirm before connecting"
    The **Webex Contact Center** app shows **Allowed**, and **List Flows** and **Get Flow** remain enabled after reopening **Tools**. If the app is missing, a setting cannot be saved, or your account lacks administrator access, stop and ask the facilitator.

## Keep your completed flow open

Return to your completed `ServiceDesk` tab in Flow Designer. If you closed it, open **Control Hub → Contact Center → Customer Experience → Flows → Manage Flows** and open `ServiceDesk`. Keep the flow tab open to compare the MCP result with your canvas.

!!! info "This lab uses ProdUS1"
    The MCP Lab **Webex Contact Center** preset points to the ProdUS1 server. Use it only for the assigned ProdUS1 sandbox. For another region, ask the facilitator for the regional URL from the signed-in [Contact Center MCP Server page](https://developer.webex.com/mcp/docs/contact-center-mcp-server).

## Connect with your sandbox Webex account

1. Return to the **AI agent** workspace in [MCP Lab](https://mcp-lab.webexdevs.com/). Select **Add MCP**, then **Webex Contact Center** under **Preconfigured server**. Do not use **Connect MCP** on the Order Desk card; that connects the simulated order system.

    ![MCP Lab server choices showing the Webex Contact Center preconfigured server below Order Desk](assets/lab-guide/live/bonus-mcp-lab-contact-center-preset.jpg){ width="680" }

    *Choose the **Webex Contact Center** preconfigured server, not Order Desk.*

2. Under **Authentication method**, select **Built-in Webex integration**. The preset initially selects **WCIT token**, so change it explicitly. You do not need to copy a bearer token for this connection.
3. Select **Authorize with Webex**. Sign in with the **Sandbox email** and **Sandbox password** from MCP Lab's **Test tenant** panel—not your personal Webex account. If Webex is already signed in as another user, switch to your assigned sandbox account before authorizing.

    ![MCP Lab Connect Webex Contact Center form with Built-in Webex integration selected and Authorize with Webex button](assets/lab-guide/live/bonus-mcp-lab-webex-authentication.jpg){ width="680" }

    *Select **Built-in Webex integration**, then **Authorize with Webex** to sign in with your sandbox account.*

4. Review the Webex consent screen and select **Accept** for the sandbox integration. The built-in integration requests a fixed set of permissions, including configuration write access. MCP Lab separately controls which tools the agent can use and requires approval for write actions.
5. When MCP Lab returns to **Choose tools**, all discovered tools are initially selected. Keep `wxcc-list-flows` and `wxcc-get-flow` selected for the inspection steps below. Leave other tools selected if you are comfortable using them, or clear their checkboxes. Read tools say **Runs automatically**; write tools say **Approval required**. The enabled count depends on your selection—it does not need to be exactly two.
6. Select **Connect MCP**. On **Ready to use**, check that the tool count matches your selection, then select **Return to AI agent**. Confirm that **Connected MCPs** shows **Webex Contact Center** as **Connected**. To change your selection later, open that card, choose the tools, and **click Save tools before closing the dialog**.

## Find your ServiceDesk flow

1. Return to [Control Hub](https://admin.webex.com/) and confirm that you are still in your assigned sandbox organization. In the main navigation, select **Account**, then the **Info** tab.
2. Under **Organization profile**, find **Organization ID**. Click the **copy icon** to the right of the field to copy your organization's ID.

    ![Control Hub Account Info page showing Organization profile, the Organization ID field, and its copy icon](assets/lab-guide/live/bonus-control-hub-organization-id.jpg){ width="900" }

    *Account → Info → Organization profile: copy **your** Organization ID. The ID shown here belongs to the example sandbox; do not use it in your prompt.*

3. Return to MCP Lab. Replace `<your organization ID>` in the prompt below with the ID you copied from Control Hub. If you renamed the imported flow, replace `ServiceDesk` with that name too. Paste the completed prompt into MCP Lab:

```text
Use wxcc-list-flows to find flows named ServiceDesk in organization <your organization ID>. Show each matching flow's name and ID. Do not create, change, or publish anything.
```

4. Wait for the tool call to finish. In **Tool activity**, look for `wxcc-list-flows completed`. Check that the response reports a matching flow, not an error, and refers to the organization ID in your prompt.
{: value="4" }
5. Find your `ServiceDesk` in the response. If there is more than one match, compare the flow ID with the value after `/flow/` in your Flow Designer URL. Do not select another attendee's flow.
6. Copy the returned flow ID for the next prompt.

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

## Optional: edit a separate unpublished draft

This stretch changes an activity's **description**, not its spoken message or caller path. It demonstrates an approval-gated MCP write without changing the flow that receives calls.

### Enable the draft tools you want to use

1. In **Control Hub → Apps → Agentic Apps → Webex Contact Center → Tools**, enable **Allow tool** for `wxcc-patch-flow-draft` and `wxcc-validate-flow`. **Click Save at the bottom before leaving Tools.** Reopen the tab to confirm they remain enabled.
2. In MCP Lab, open the **Webex Contact Center** card. Keep `wxcc-list-flows` and `wxcc-get-flow` selected, and select the two tools above. **Click Save tools before closing the dialog.** You may also select other tools you are comfortable using; they are not required for this stretch.
3. Confirm that patch says **Approval required**, while validation says **Runs automatically**. You do not need `wxcc-save-flow-draft` for this small patch; it replaces the whole draft rather than updating just one node.

    ![MCP Lab tool management showing the selected patch tool, decoded description, and Approval required label](assets/lab-guide/live/bonus-mcp-lab-draft-tools.jpg){ width="800" }

    *The example has eight selected tools. Your count may differ. The patch tool remains approval-gated even when it is enabled.*

### Create a copy, not a replacement

Make the copy in Flow Designer, then use MCP for the edit. A full flow can exceed the lab agent's response limit when reconstructed through chat. Do not export the earlier REST version from Checkpoint 3; it contains your temporary bearer.

1. Return to the completed `ServiceDesk` Flow Designer tab from Checkpoint 9. Confirm the main flow contains `AIAgent` and `EscalationMessage`, with **no `GetOrder` activity**.
2. Open the menu beside the flow name and select **Export**. Save the downloaded JSON privately with its `.json` extension.
3. In **Control Hub → Contact Center → Customer Experience → Flows → Manage Flows**, select **Create Flows**. Choose **Flow → Import a flow → Next**, then select the JSON you just exported.
4. Change the proposed flow name to `ServiceDeskMCPBonus` before selecting **Create flow**. If that name already exists, choose another name and use it consistently below. Never replace the original `ServiceDesk`.
5. In the copy, confirm that the expected activities and connections are present and `HumanAgentQueue` still uses your assigned `Queue-1`. Do not publish the copy or assign an entry point to it. Keep its tab open.
6. Get the copy's ID with this prompt, replacing the organization placeholder:

```text
Use wxcc-list-flows to find ServiceDeskMCPBonus in organization <your organization ID>. Report its name and ID. Use wxcc-get-flow to read its draft and report its name, version, EscalationMessage description and main-flow edges. Do not change anything.
```

7. Confirm that the returned copy has a **different flow ID** from `ServiceDesk` and that the ID matches the value after `/flow/` in the copy's Flow Designer URL.
{: value="7" }

### Patch one activity description

Replace the placeholders with your organization ID and the **copy's** flow ID:

```text
Use wxcc-get-flow to read the draft of flow <your ServiceDeskMCPBonus flow ID> in organization <your organization ID>. Locate EscalationMessage. Show its current properties.description and propose changing only that field to "MCP bonus: explains the human-agent handoff before queueing the caller." Keep every other node property, variable, edge and event flow unchanged. Do not save yet. Stop if the activity is missing.
```

1. Review the proposed description. Confirm that the target is `ServiceDeskMCPBonus`, not your completed `ServiceDesk`, and that no audio prompt or connection is being changed.
2. Send:

```text
Apply only the proposed EscalationMessage properties.description change to ServiceDeskMCPBonus using wxcc-patch-flow-draft. Read the draft again first and use its current expected_version. Do not change the source flow, prompts, edges, routing or published versions. Request approval for the patch.
```

3. At **Approval required**, confirm the tool is `wxcc-patch-flow-draft`, then select **Approve tool**. The card identifies the tool; it is not a detailed JSON diff. Select **Cancel** if the tool or the agent's plan differs from the description-only patch. Wait for `wxcc-patch-flow-draft completed`; an approval alone is not proof of success. If the tool reports a version conflict, reread the draft and review the plan again; do not force an overwrite.
{: value="3" }
4. Verify with a separate read and validation:

```text
Use wxcc-get-flow to reread the draft of flow <your ServiceDeskMCPBonus flow ID> in organization <your organization ID>. Report EscalationMessage properties.description and the main-flow edges. Use wxcc-validate-flow to validate that saved draft and report any ERROR or WARNING results. Do not save, publish or change routing.
```

5. Refresh the **copy's** Flow Designer tab and select `EscalationMessage`. Confirm the **Activity description** matches the new text and that the caller path is unchanged. Review any validation findings before continuing; a successful save does not prove the flow is valid. Leave the copy unpublished for facilitator cleanup.
{: value="5" }

!!! success "Draft edit verified"
    The saved copy has a different ID, the description is visible in both the MCP read-back and Flow Designer, and validation returned its actual results. Your original `ServiceDesk` and its entry-point routing are unchanged. This exercise does not test a new phone-call experience.

## Finish the bonus

1. In **Connected MCPs**, select the **Webex Contact Center** card.
2. Under **Remove this MCP**, select **Remove connection**, then **Delete MCP**. This removes the connection and its saved credential from your MCP Lab session, not the Webex server or your Contact Center flow.
3. Confirm the Contact Center card is gone. Keep your Order Desk connection if it is still present; do not reset the whole session to remove one MCP.

!!! success "Bonus complete"
    Both flow-read tools succeeded in your assigned sandbox, and their results match your `ServiceDesk` draft. If you completed the optional edit, leave `ServiceDeskMCPBonus` unpublished and tell the facilitator it needs cleanup. Leave the original completed flow and its entry-point routing in place.

Other tools are available for exploration in your assigned sandbox. Approve only changes you understand; this exercise does not require queue, entry-point, subscription or published-flow changes. The separate Contact Center Operations MCP is outside this exercise. See the [official references](references.md#bonus-webex-contact-center-mcp-services) for later exploration.

[Continue to troubleshooting and completion](troubleshooting.md){ .md-button .md-button--primary }
