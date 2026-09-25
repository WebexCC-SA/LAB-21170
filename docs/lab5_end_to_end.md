# Checkpoint 9: Attach the agent and test end to end

In the reference screenshots, published `ServiceDesk` version 5 sends callers directly to `LAB-21170 Order Support`. It passed Validation with **0 errors**, and Control Hub routes the active **Entry Point-1** to `ServiceDesk` **Latest**. Your version number may differ. Verify the order lookup and human queue handoff by phone after publishing your flow.

Before starting, confirm that `lookup_order` succeeds in AI Agent Studio Preview and the agent shows **Published**. In Preview, ask for general support, accept the offer of a human agent, and check **Sessions** for **Agent handover**. This checks the agent action; the phone test below checks the voice queue. If the MCP action is missing, finish Checkpoint 6 first.

## Replace the starter caller path

1. Open `ServiceDesk` in Flow Designer and turn **Edit** on.
2. Disconnect `NewContact` from `WelcomeMessage`. Keep the queue and wait-treatment nodes for reuse. Delete the direct **HTTP Request** activity so its temporary Authorization header does not remain in the draft.
3. Find **Virtual Agent V2** under **Contact handling** and drag it onto the canvas.
4. Set **Activity label** to `AIAgent`.
5. Connect `NewContact` directly to `AIAgent`.
6. In the activity settings, set **Contact Center AI Config** to **Webex AI Agent (Autonomous)**.
7. For **Virtual agent**, select the published `LAB-21170 Order Support` agent. Reopen the activity to confirm both selections saved.
8. Add a **Disconnect Contact** activity labeled `DisconnectContact`, or reuse one already on your canvas.
9. Connect the `AIAgent` **Handled** outcome to `DisconnectContact`.
10. Add a **Play Message** activity and label it `EscalationMessage`. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `I'll connect you with a human agent.`

    <figure markdown>
      ![EscalationMessage settings with text to speech enabled, Cisco Cloud Text-to-Speech, and the human connection message](assets/lab-guide/live/cp9-escalation-message-settings.jpg)
      <figcaption>Set the escalation prompt before the queue handoff.</figcaption>
    </figure>

11. Reuse `QueueContact_4b7` if it remains on the canvas. Remove its old incoming links from menu digit `2` and `OrderStatusMessage`, rename it `HumanAgentQueue`, and set **Voice → Static queue → Queue-1**. Connect `AIAgent` **Escalated → EscalationMessage → HumanAgentQueue**. If the activity is missing, add **Queue Contact** with those settings. If `Queue-1` is unavailable, stop here and check the assigned queue before publishing.

    <figure markdown>
      ![HumanAgentQueue settings showing Voice, Static queue, and Queue-1 in the ServiceDesk draft](assets/lab-guide/live/cp9-human-agent-queue-1.jpg)
      <figcaption>Set `HumanAgentQueue` to **Voice → Static queue → Queue-1**. Connect **Failure** to `QueueErrorMessage`.</figcaption>
    </figure>

12. From `HumanAgentQueue`'s normal output, connect **Play Music** (`PlayMusic_pgj` in this flow), then the **Play Message** activity `PleaseWait`. Connect `PleaseWait` back to Play Music so treatment repeats while the caller waits for an agent.
13. Reuse `QueueErrorMessage` if it is already on the canvas; otherwise add a **Play Message** activity with that label. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `I can't connect you to a person right now. Please try again later.` Connect the Queue Contact **Failure** output to this message, then to `DisconnectContact`.

    <figure markdown>
      ![QueueErrorMessage settings with text to speech enabled, Cisco Cloud Text-to-Speech, and the queue failure message](assets/lab-guide/live/cp9-queue-error-message-settings.jpg)
      <figcaption>Set the Queue Contact **Failure** prompt.</figcaption>
    </figure>

14. Add another **Play Message** activity and label it `AgentErrorMessage`. Enable text to speech, select **Cisco Cloud Text-to-Speech**, and enter: `Order support is temporarily unavailable. Please try again later.`

    <figure markdown>
      ![AgentErrorMessage settings with text to speech enabled, Cisco Cloud Text-to-Speech, and the AI error message](assets/lab-guide/live/cp9-agent-error-message-settings.jpg)
      <figcaption>Set the AI agent **Errored** prompt.</figcaption>
    </figure>

15. Connect the `AIAgent` **Errored** outcome to `AgentErrorMessage`, then connect `AgentErrorMessage` to `DisconnectContact`.
16. Remove unused starter IVR and API nodes. Wait for **Autosave**, turn on **Validation**, and resolve any errors. Confirm the final canvas has only the connected AI route and **0 errors**.

<figure markdown>
  ![ServiceDesk draft Virtual Agent V2 activity configured with the autonomous Order Support agent](assets/lab-guide/live/cp9-ai-agent-configured-draft.jpg)
  <figcaption>Set **Contact Center AI Config** to **Webex AI Agent (Autonomous)** and **Virtual agent** to `LAB-21170 Order Support`.</figcaption>
</figure>

<figure markdown>
  ![Live ServiceDesk version 5 draft canvas showing Start Flow connected to the AI agent and its outcome branches](assets/lab-guide/live/cp9-ai-flow-draft-topology.jpg)
  <figcaption>Check the three AI outcomes, queue failure path, and `PlayMusic_pgj → PleaseWait → PlayMusic_pgj` loop.</figcaption>
</figure>

<figure markdown>
  ![Flow Designer validation panel on ServiceDesk version 5 draft reporting zero errors and Ready to publish](assets/lab-guide/live/cp9-ai-flow-zero-errors.jpg)
  <figcaption>Confirm **0 errors** and **Ready to publish**. The three recommendations do not block publication.</figcaption>
</figure>

<figure markdown>
  ![Reference topology for the final caller path with AI-agent handled, human-queue escalation, and error outcomes](assets/lab-guide/02-final-agent-flow.png)
  <figcaption>Use this branch diagram with the live canvas above. Loop `PleaseWait` back to Play Music.</figcaption>
</figure>

!!! info "Before you call"
    Confirm that your published flow is **Latest** and **Entry Point-1** routes to `ServiceDesk` **Latest**. Validation confirms the wiring; the two phone tests below confirm what callers experience.

## Publish and test the final caller path

1. Select **Publish Flow** after validation. In the dialog, **Latest** is applied automatically; optionally select **Test** and enter a comment such as `AI agent with human queue`. Select **Publish Flow**, then confirm the new version is **Latest** in version history.

    <figure markdown>
      ![Flow Designer Publish dialog with automatic Latest label, optional Test label, comment, and Publish Flow button](assets/lab-guide/live/cp9-ai-flow-publish-dialog.jpg)
      <figcaption>Check **Latest**, add an optional label and comment, then select **Publish Flow**.</figcaption>
    </figure>

2. In Control Hub, open the assigned inbound **Entry Point** from Checkpoint 2 and confirm that **Routing flow** is `ServiceDesk` and **Version label** is `Latest`. In Flow Designer version history, confirm that **Latest** is on your newly published version. If the entry point uses an older fixed label, update the routing assignment before calling.

    <figure markdown>
      ![Control Hub entry point routing settings showing ServiceDesk and Latest](assets/lab-guide/live/cp9-entry-point-servicedesk-latest.jpg)
      <figcaption>Set **Routing flow** to `ServiceDesk` and **Version label** to `Latest`.</figcaption>
    </figure>

3. Call the same inbound phone number used in Checkpoints 2 and 3.
4. Say: `I need an update on order ORD-10482.`
5. If the agent asks for the order number, provide `ORD-10482`.
6. Confirm that the agent retrieves the order data through the external action and explains the status and delivery information.
7. Make a second call and say: `I need general support.` When the agent offers a human handoff, say: `Yes, please connect me to a human agent.` Confirm that `EscalationMessage` plays and the call enters `Queue-1`. If a test agent is available, answer in Agent Desktop. Otherwise, listen for the wait treatment.
8. In **Debug**, inspect both Interaction IDs. Confirm the order call reached `AIAgent` and the general-support call followed `AIAgent → EscalationMessage → HumanAgentQueue`. If the caller waited, confirm the trace continued through `PlayMusic/PleaseWait`. Test Queue Contact **Failure** separately only if you can safely create a controlled failure.

<figure markdown>
  ![ServiceDesk version history showing version 5 published as Latest and version 4 retained in history](assets/lab-guide/live/cp9-ai-flow-v5-latest.jpg)
  <figcaption>Confirm version 5 is **Latest**, published September 24, 2026 at 19:48:14 tenant time. Version 4 remains in history.</figcaption>
</figure>

**Target caller path:**

```text
Caller → ServiceDesk → AIAgent
  ├─ Order request → lookup_order (MCP) → response → Handled → disconnect
  ├─ General support → offer human → caller accepts → Escalated
  │    → EscalationMessage → Queue-1 → PlayMusic ↔ PleaseWait → human agent
  │                           └─ Failure → QueueErrorMessage → disconnect
  └─ Errored → AgentErrorMessage → disconnect
```

!!! success "Confirm after publishing and calling"
    - The connected caller path is `NewContact → AIAgent`; the starter menu and REST branch are removed from published version 5.
    - A live caller does not hear the old Flow Designer `WelcomeMessage` or numbered `SupportMenu`; the AI agent's own welcome message may still play.
    - The agent uses `lookup_order` and speaks the returned order and delivery details.
    - A general-support request prompts an offer of a human agent. Accepting it sends the call to `Queue-1` and wait treatment; an available test agent can answer.
    - A controlled Queue Contact failure, if tested, reaches `QueueErrorMessage` and ends safely.
    - `AgentErrorMessage` provides a clear fallback if the AI agent errors.

!!! warning "Before marking this checkpoint complete"
    Complete both phone calls and inspect their paths in **Debug**. Confirm the order response and the human queue handoff on your published flow. Test Queue Contact **Failure** only with a controlled failure.

## Optional: inspect Contact Center through MCP

The Order Desk MCP is the **external order tool** your voice agent uses. The optional Cisco services below let an approved MCP client inspect Contact Center flows or operations. If your organization has beta access, use its approved client, regional server URL, authentication method, and enabled tools. Do not use the Order Desk bearer for either Cisco service.

### A. Contact Center MCP Server: Flow tools

The [Contact Center MCP Server](https://developer.webex.com/mcp/docs/contact-center-mcp-server) provides Flow Designer tools backed by the FlowV2 authoring contract. Follow the [beta setup guide](https://developer.webex.com/create/docs/contact-center-mcp-server-beta) for supported clients and authentication. Your administrator must allow **Contact Center MCP** under **Control Hub → Apps → Agentic Apps** and enable the tools you need.

For a read-only tour, use `wxcc-list-flows` and `wxcc-get-flow` to find a flow, `wxcc-view-config` to inspect configuration, and `wxcc-get-activity-definitions`, `wxcc-describe-activity`, and `wxcc-get-choices` to inspect activities. Compare the result with the Flow Designer canvas. If writes are enabled, make changes in an unpublished test draft, inspect the diff, and run `wxcc-validate-flow` before publishing or assigning the flow. Check the tool names against your enabled catalog.

### B. Contact Center Operation MCP Server: read-only tools

The [Contact Center Operation MCP Server beta](https://developer.webex.com/create/docs/contact-center-operation-mcp-server-beta) is a separate **read-only** service. It cannot create, update, publish, or delete a flow. Confirm access, the regional URL, and enabled tools before connecting.

Use `wxcc-operations-describe-org` and `wxcc-operations-describe-metrics` to inspect available fields, `wxcc-operations-list-flows` to find a flow, and `wxcc-operations-explain-queue-routing` to inspect queue configuration. If you have an approved test contact ID and the tool is enabled, `wxcc-operations-get-contact-timeline` can show arrival, IVR, queue, agent, and end events. If an artifact is delayed or missing, check the source timeline before drawing a conclusion.

Before sharing a screenshot, crop out tokens, caller numbers, transcripts, and customer details.

[Continue to troubleshooting and completion](troubleshooting.md){ .md-button .md-button--primary }
